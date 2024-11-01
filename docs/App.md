# プログラム概要
このプログラムは、AIチャットアシスタントを実装したReactアプリケーションです。ユーザーがメッセージを送信し、AIからの応答を受け取ることができるインターフェースを提供します。ユーザーは新しいチャットセッションを開始することも可能で、過去のメッセージ履歴を取得する機能も備えています。

## 主な機能
1. **メッセージの送信**: ユーザーが入力したメッセージをサーバーに送信し、その応答を受け取ります。
2. **チャット履歴の表示**: 過去のメッセージ履歴を表示し、新しいメッセージとともに更新されます。
3. **新しいチャットの開始**: ボタン一つで新しいチャットセッションを開始できます。
4. **ローディングスピナー**: メッセージ送信中やデータ取得中にローディングスピナーが表示され、処理中であることが視覚的に示されます。

## 使用方法
- アプリケーション起動後、画面上部に「New Chat」ボタンがあります。このボタンをクリックすると、新しいチャットセッションが開始されます。
- チャットウィンドウにメッセージを入力し、「送信」ボタン（ChatInputコンポーネント内）を押すことで、AIへのメッセージ送信が行われます。これによってAIからの応答も自動的に取得されて表示されます。
- 画面には過去の会話履歴がリスト形式で表示され、新たなメッセージはその下に追加されていきます。

## コード構成
- `App.tsx`: メインコンポーネントであり、アプリケーション全体の状態管理やUIレンダリングを担当します。主な状態として`session_id`（現在のチャットセッションID）、`messages`（会話履歴）、`loading`（ローディング状態）があります。
- `MessageBubble`: 各メッセージバブルコンポーネント。役割（ユーザーまたはAI）と内容を受け取り、それぞれ異なるスタイルで表示します。
- `ChatInput`: ユーザーからの入力用コンポーネント。ここでユーザーはテキストメッセージを入力し、送信することができます。
- `LoadingSpinner`: データ処理中に表示されるスピナーコンポーネントです。

## APIとの連携
このアプリケーションは以下のAPIエンドポイントと連携しています:
- `GET /history_latest`: 最新のチャット履歴とsession_idを取得します。
- `POST /history`: 指定されたsession_idに基づいて過去のチャット履歴を取得します。
- `POST /insert_user_prompt`: ユーザーから送られたプロンプト（メッセージ）を保存します。
- `POST /get_completion`: AIから応答内容を取得します。
- `POST /new_chat`: 新しいチャットセッションIDを生成します。

## 注意事項
このプログラムはローカル環境で動作するよう設計されていますので、APIサーバー（localhost:8000）が稼働している必要があります。また、エラーハンドリングも含まれており、通信エラーなどの場合にはコンソールへエラーメッセージが出力されます。
# 詳細
## 詳細なコード説明

### インポートセクション
- `import React, { useState, useEffect } from 'react';`
  - ReactとReact Hooks（useState, useEffect）をインポートします。
- `import axios from 'axios';`
  - HTTPリクエストを行うためのAxiosライブラリをインポートします。
- `import { MessageBubble } from './components/MessageBubble';`
  - メッセージ表示用のコンポーネントをインポートします。
- `import { ChatInput } from './components/ChatInput';`
  - ユーザー入力用のコンポーネントをインポートします。
- `import { MessageCircle, PlusCircle } from 'lucide-react';`
  - アイコンコンポーネントをインポートします。
- `import LoadingSpinner from './components/LoadingSpinner';`
  - ローディングスピナー用のコンポーネントをインポートします。

### インターフェース定義
- `interface Message {...}`
  - メッセージオブジェクトの型を定義し、役割（role）、内容（content）、タイムスタンプ（timestamp）を持つことが示されています。

### Appコンポーネント
- `const [session_id, setSesstionId] = useState("");`
  - 現在のチャットセッションIDを保持するための状態変数です。
- `const [messages, setMessages] = useState<Message[]>([]);`
  - チャットメッセージの履歴を保持するための状態変数です。初期値は空の配列です。
- `const [loading, setLoading] = useState(false);`
  - データ処理中かどうかを示すローディング状態を保持するための変数です。

### useEffectフック
- `useEffect(() => { fetchHistory("", true); }, []);`
  - コンポーネントがマウントされたときに最新のチャット履歴を取得するために`fetchHistory`関数を呼び出します。依存配列が空なので、初回のみ実行されます。

### fetchHistory関数
- `const fetchHistory = async (session_id:string, latest:boolean = false) => {...}`
  - 指定されたセッションIDまたは最新履歴に基づいてメッセージ履歴を取得する非同期関数です。成功時には`setSesstionId`と`setMessages`で状態更新します。エラー発生時にはコンソールにエラーメッセージが出力されます。

### handleSendMessage関数
- `const handleSendMessage = async (message: string) => {...}`
  - ユーザーから送信されたメッセージを処理し、AIからの応答も取得する非同期関数です。ローディング状態を管理し、メッセージ送信後に履歴更新とAI応答取得が行われます。エラー発生時にはローディング状態が解除され、エラーメッセージが出力されます。

### handleNewChat関数
- `const handleNewChat = async () => {...}`
  - 新しいチャットセッションを開始し、新しいセッションIDで履歴を取得する非同期関数です。新しいチャットボタンが押された際に呼ばれます。

### JSX部分
#### レンダリング構造
- `<div className="flex flex-col h-screen bg-gray-100">...</div>`
  - アプリケーション全体のレイアウト構造で、フレックスボックスで縦に並ぶデザインになっています。
#### ヘッダー部分
- `<header className="bg-blue-600 text-white p-4 shadow-md">...</header>`
  - アプリケーション名と新しいチャットボタンが配置されています。ボタンは`handleNewChat`関数にバインドされています。
#### メイン部分
- `<main className="flex-grow container mx-auto p-4 overflow-y-auto">...</main>`
  - チャットメッセージが表示される領域で、各メッセージは`MessageBubble`コンポーネントとしてレンダリングされます。また、ローディング中にはスピナーも表示されます。
#### フッター部分
- `<footer className="bg-white border-t border-gray-200 p-4">...</footer>`
  - ユーザーからのメッセージ入力用コンポーネントである`ChatInput`が配置されています。