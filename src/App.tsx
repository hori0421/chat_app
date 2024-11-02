import { useState, useEffect } from 'react';
import axios from 'axios';
import { getAuth, signInWithPopup, GoogleAuthProvider, onAuthStateChanged } from "firebase/auth";
import { initializeApp } from "firebase/app";
import Header from './components/Header';
import Footer from './components/Footer';
import ChatLog from './components/ChatLog';

// Firebaseの設定
const firebaseConfig = {
  apiKey: "AIzaSyCIIjX5X2gIax_klqwsu6mqDneOg-AovR8",
  authDomain: "tutorial-598c5.firebaseapp.com",
  projectId: "tutorial-598c5",
  storageBucket: "tutorial-598c5.appspot.com",
  messagingSenderId: "755922303290",
  appId: "1:755922303290:web:b398d808cbb31b49087803",
  measurementId: "G-FCW364SLXK"
};

// backendのURL
const backend_url = 'https://backend-755922303290.asia-northeast1.run.app/';

// Firebaseアプリの初期化
initializeApp(firebaseConfig);

interface Message {
  role: string;
  content: string;
  timestamp: any;
}

interface UserData {
  user_id: string;
  session_id: string;
}

function App() {
  const [userData, setUserData] = useState<UserData | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  const [auth, setAuth] = useState<ReturnType<typeof getAuth> | null>(null); // Firebase Auth インスタンスの取得

  useEffect(() => {
    setAuth(getAuth());
  }, []);
  
  useEffect(() => {
    if (auth) {
      onAuthStateChanged(auth, async (user) => {
        if (user) {
          console.log(user);
          setUserData({
            user_id: user.email || '',
            session_id: ''
          });
          console.log(user.email)
        }
      });
    }
  }, [auth]);

  useEffect(() => {
    if (auth) {
    } else {
      setAuth(getAuth());
    }

    if (userData && userData.session_id == '') {
      console.log(userData);
      fetchHistory(userData.user_id,);
    }else if(userData && userData.session_id != ''){
      fetchHistory(userData.user_id, userData.session_id);
    }
  }, [userData]);

  const fetchHistory = async (user_id: string, session_id: string | undefined = undefined) => {
    try {
      if (!session_id) {
        const response = await axios.post(backend_url + 'history_latest', { user_id: user_id });
        setUserData((prevUserData) => ({
          ...prevUserData,
          session_id: response.data.session_id,
          user_id: response.data.user_id || prevUserData?.user_id || ''
        }));
        setMessages(response.data.history);
      } else {
        const response = await axios.post(backend_url + 'history', { user_id: user_id, session_id: session_id });
        setMessages(response.data.history);
      }
    } catch (error) {
      console.error("Error fetching history:", error);
    }
  };

  const handleSendMessage = async (message: string) => {
    setLoading(true);
    try {
      if (!userData || !userData.user_id || !userData.session_id) {
        console.error("User data is incomplete.");
        setLoading(false);
        return;
      }

      await axios.post(backend_url + 'insert_user_prompt', { user_id: userData.user_id, session_id: userData.session_id, user_prompt: message }, { headers: { "Content-Type": "application/json" } });
      await fetchHistory(userData.user_id, userData.session_id);
      const response = await axios.post(backend_url + 'get_completion', { user_id: userData.user_id, session_id: userData.session_id }, { headers: { "Content-Type": "application/json" } });
      await fetchHistory(userData.user_id, userData.session_id);
      setLoading(false);
    } catch (error) {
      console.error("Error sending message:", error);
      setLoading(false);
    }
  };

  const authenticateUser = async () => {
    const provider = new GoogleAuthProvider();
    const auth = getAuth();
    try {
      const result = await signInWithPopup(auth, provider);
      setUserData({
        user_id: result.user.email || '',
        session_id: ''
      });
      return result.user; // ユーザー情報を返す
    } catch (error) {
      alert('正常にサインインできませんでした。');
      return null; // エラーが発生した場合はnullを返す
    }
  };

  const handleNewChat = async () => {
    if (userData) {
      // 新しいセッションを作成
      console.log(userData);
      const new_session_id = await axios.post(backend_url + 'new_chat', { user_id: userData.user_id });
      setUserData((prevUserData) => ({
          ...prevUserData,
          session_id: new_session_id.data.session_id,
          user_id: prevUserData?.user_id || ''
        }));
      fetchHistory(userData.user_id, new_session_id.data.session_id);
    } else {
      console.error("User authentication failed. Cannot start new chat.");
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      {userData && (
        <Header onNewChat={handleNewChat} />
      )}
      <main className="flex-grow container mx-auto p-4 overflow-y-auto">
        {userData ? (
          <ChatLog messages={messages} loading={loading} />
        ) : (
          <div className="flex items-center justify-center h-full">
            <button onClick={authenticateUser} className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors duration-200">
              ログイン
            </button>
          </div>
        )}
      </main>
        {userData && (
        <Footer onSendMessage={handleSendMessage} isLoading={loading} />
      )}
    </div>
  );
}

export default App;