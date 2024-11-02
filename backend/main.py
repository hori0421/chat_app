import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, APIRouter, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import firebase_admin
from firebase_admin import credentials, firestore, auth
from openai import OpenAI
from fastapi.responses import StreamingResponse
import requests
import json
import aiohttp

load_dotenv()
# ANSI escape codes for colors
class CustomFormatter(logging.Formatter):
    # 色の定義
    colors = {
        "DEBUG": "\x1b[38;5;245m",  # 薄灰色
        "INFO": "\x1b[32m",         # 緑色
        "WARNING": "\x1b[33m",      # 黄色
        "ERROR": "\x1b[31m",        # 赤色
        "CRITICAL": "\x1b[35m",     # マゼンタ
    }
    cyan = "\x1b[36m"  # 水色
    grey = "\x1b[38;5;245m"  # 灰色
    reset = "\x1b[0m"  # リセット

    # フォーマットの定義
    def format(self, record):
        levelname = record.levelname
        message = record.getMessage()
        asctime = self.formatTime(record, self.datefmt)
        filename = record.filename
        lineno = record.lineno

        # ログレベルに色を適用
        levelname_colored = f"{self.colors.get(levelname, self.reset)}{levelname}{self.reset}"
        # 時刻に水色を適用
        asctime_colored = f"{self.cyan}{asctime}{self.reset}"
        # ファイル名と行番号に灰色を適用
        fileinfo_colored = f"{self.grey}({filename}:{lineno}){self.reset}"
        
        # インデントを制御
        indent = " " * (9 - len(levelname))

        return f"{levelname_colored}:{indent} {asctime_colored} - {message}    {fileinfo_colored}"

# ロガーの設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.propagate = False

# ハンドラの設定
handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter())
logger.addHandler(handler)

# テストログ
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")

BASE_URL = "http://34.106.181.57/v1"
API_KEY = os.getenv("DIFY_API_KEY")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Firebase Admin SDKの初期化を修正
try:
    # 環境変数のパスから認証情報を読み込む
    cred = credentials.Certificate('firebase-credentials.json')
    firebase_admin.initialize_app(cred)
    logger.info("Successfully initialized Firebase with credentials")
except Exception as e:
    logger.error(f"Firebase initialization error: {e}")
    raise

db = firestore.client()
    
class UserData(BaseModel):
    user_id: str
    session_id: Optional[str] = None
    user_prompt: Optional[str] = None

class SessionData(BaseModel):
    user_id: str
    session_id: str

class UserPrompt(SessionData):
    user_prompt: str

def register_new_message_doc(user_id:str, session_id:str, data: dict, conversation_id:str = None):
    logger.info(f"Register new message doc for user ID: {user_id}, Session ID: {session_id}")
    if db.collection(user_id).document(session_id).get().get('conversation_id') is None and conversation_id is not None:
        db.collection(user_id).document(session_id).update({'conversation_id': conversation_id})
    docs = db.collection(user_id).document(session_id).collection('history').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1).get()
    if not docs:
        latest_id = 0
    else:
        latest_id = int(docs[0].id)
    insert_doc_ref = db.collection(user_id).document(session_id).collection('history').document(f"{(latest_id + 1):04d}")
    insert_doc_ref.set(data)
    
def get_conversation_id(user_id:str,session_id:str):
    logger.info("get conversation_id")
    return db.collection(user_id).document(session_id).get().get('conversation_id')
    

@app.post("/insert_user_prompt")
async def insert_user_prompt(data: UserData):
    logger.info(f"User ID: {data.user_id}, Session ID: {data.session_id}, User Prompt: {data.user_prompt}")
    try:
        user_data = {
            "role": "user",
            "content": data.user_prompt,
            "timestamp": firestore.SERVER_TIMESTAMP
        }
        register_new_message_doc(data.user_id, data.session_id, user_data)
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/get_completion")
async def get_completion(data: UserData):
    logger.info(f"Session ID: {data.session_id}")
    try:
        messages = await create_message(data.user_id, data.session_id)
        if not messages:
            logger.info("No messages found")
        conversation_id = get_conversation_id(data.user_id, data.session_id)
        payload = {
            "query": messages[-1]["content"],
            "inputs": {},
            "response_mode": "streaming",
            "user": "default_user",
            "conversation_id": conversation_id
        }
        logger.info(f"Payload: {payload}")
        url = f"{BASE_URL}/chat-messages"
        logger.info(f"API_KEY: {API_KEY}")
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status == 200:
                    logger.info(f"Response status: {response.status}")
                    full_response = ""
                    response_conversation_id = ""
                    async for line in response.content:
                        line = line.decode('utf-8')
                        if line:
                            logger.debug(f"Received line: {line[:20]}...{line[-20:]}")
                            try:
                                response_data = json.loads(line.replace("data: ", ""))
                                logger.debug(f"Response data: \n{json.dumps(response_data, indent=4)}")
                                if 'answer' in response_data:
                                    full_response += response_data['answer']
                                if 'conversation_id' in response_data:
                                    response_conversation_id = response_data['conversation_id']
                            except json.JSONDecodeError as jde:
                                logger.warning(f"JSON decode error: {jde}")
                                continue
                    if full_response:
                        logger.info(f"Full response: {full_response}")
                        assistant_data = {
                            "role": "assistant",
                            "content": full_response,
                            "timestamp": firestore.SERVER_TIMESTAMP
                        }
                        register_new_message_doc(data.user_id,data.session_id, assistant_data, response_conversation_id)
                        return {"response": full_response}
                else:
                    logger.error(f"Failed to fetch data: {response.status}")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/history_latest")
async def get_history_latest(data: UserData):
    try:
        docs = db.collection(data.user_id).order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1).get()
        if not docs:
            logger.info("No documents found")
            # 新しいセッションを作成
            new_doc_ref = db.collection(data.user_id).document('chat_0001')
            new_doc_ref.set({'title': "new chat", 'timestamp': firestore.SERVER_TIMESTAMP, 'conversation_id': None})
            new_doc_ref.collection('history').document('init').set({})
            new_doc_ref.collection('history').document('init').delete()
            new_session_id = "chat_0001"
            logger.info(f"New chat initialized with session ID: {new_session_id}")
            return await get_history_latest(data)
        else:   
            latest_doc = docs[0]
            subcollection_docs = latest_doc.reference.collection('history').order_by('timestamp').stream()
            history = [doc.to_dict() for doc in subcollection_docs]
            return {"history": history, "session_id": latest_doc.id}
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/history")
async def get_history(data: UserData):
    try:
        logger.info(f"Getting history for user ID: {data.user_id}, Session ID: {data.session_id}")
        docs = db.collection(data.user_id).document(data.session_id).collection('history').order_by('timestamp').stream()
        history = [doc.to_dict() for doc in docs]
        return {"history": history}
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/new_chat")
async def new_chat(data: UserData):
    try:
        latest_session_id = db.collection(data.user_id).order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1).get()
        latest_number = int(latest_session_id[0].id.split('_')[1])
        new_session_id = f"chat_{latest_number + 1:04d}"
        db.collection(data.user_id).document(new_session_id).set({'title': "new chat", 'timestamp': firestore.SERVER_TIMESTAMP, 'conversation_id': None})
        init_doc_ref = db.collection(data.user_id).document(new_session_id).collection('history').document('init')
        init_doc_ref.set({})
        init_doc_ref.delete()
        logger.info(f"New session created with ID: {new_session_id}")
        return {"session_id": new_session_id}
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def create_message(user_id:str, session_id:str):
    logger.info(f"Creating message for session ID: {session_id}")
    try:
        docs = db.collection(user_id).document(session_id).collection('history').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(50).stream()
        history = [doc.to_dict() for doc in docs]
        history.reverse()
        messages = [{"role": entry["role"], "content": entry["content"]} for entry in history]
        return messages
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/login")
async def login_with_google(token: str = Body(...)):
    try:
        # Firebase Admin SDKを使用してIDトークンを検証
        logger.debug(f"Token: {token}")
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        
        # ユーザ情報を取得
        user = auth.get_user(uid)
        
        return {"uid": uid, "email": user.email, "name": user.display_name}
    except auth.InvalidIdTokenError:
        logger.error("Invalid ID token")
        raise HTTPException(status_code=401, detail="Invalid ID token")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


router = APIRouter()

app.include_router(router)

if __name__ == "__main__":
    try:
        import uvicorn
        port = int(os.getenv("PORT", "8080"))
        logger.info(f"Starting server on port {port}")
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=port,
            reload=False,
            workers=1,
            access_log=True,
            log_level="info"
        )
    except Exception as e:
        logger.critical(f"Failed to start server: {str(e)}", exc_info=True)
        raise