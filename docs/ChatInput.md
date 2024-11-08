# ChatInput コンポーネント ドキュメント

## 概要
`ChatInput` コンポーネントは、チャットアプリケーションにおいてユーザーがメッセージを入力し送信するためのインターフェースを提供します。このコンポーネントは、メッセージの入力フィールドと送信ボタンを含み、ユーザーが簡単にメッセージを送信できるように設計されています。

## 主な機能
- ユーザーがテキストメッセージを入力できるフィールド。
- メッセージが空でない場合のみ送信ボタンが有効になる。
- メッセージ送信中は入力フィールドと送信ボタンが無効化される。
- メッセージ送信後、入力フィールドはクリアされる。

## プロパティ
このコンポーネントは以下のプロパティを受け取ります:
- `onSendMessage`: (関数) メッセージを引数として受け取り、実際にメッセージを送信する処理を行うコールバック関数です。必須です。
- `isLoading`: (boolean) メッセージ送信中かどうかを示すフラグです。`true` の場合、入力フィールドとボタンは無効化されます。必須です。

## 使用方法
このコンポーネントは以下のように使用できます:
```jsx
<ChatInput onSendMessage={handleSendMessage} isLoading={isSending} />
```
ここで、`handleSendMessage` はメッセージを処理する関数であり、`isSending` は現在メッセージが送信中かどうかの状態管理用変数です。

### 例:
```jsx
import React, { useState } from 'react';
import { ChatInput } from './ChatInput';

const ChatApp = () => {
  const [isSending, setIsSending] = useState(false);
  
  const handleSendMessage = async (message) => {
    setIsSending(true);
    // メッセージ送信処理（API呼び出しなど）
    await sendMessageToServer(message);
    setIsSending(false);
  };
  
  return (
    <div>
      <ChatInput onSendMessage={handleSendMessage} isLoading={isSending} />
    </div>
  );
};
```

## スタイルクラスについて
このコンポーネントでは Tailwind CSS を使用してスタイリングされています。主なスタイルクラスには以下があります:
- `flex`, `items-center`, `space-x-2`: フォーム全体のレイアウト設定。
- `p-2`, `border`, `rounded-lg`: 入力フィールドやボタンの外観設定。
- `focus:outline-none`, `focus:ring-*`: フォーカス時のスタイル設定。
bg-gray-300 や bg-blue-500: ボタンの背景色設定。これらは状態によって変更されます。
inactive 状態ではカーソルが無効になります。 \\ \\ \\ \\
# 詳細
## コンポーネントの内部処理

### 1. インポート文
- `React` と `useState` をインポート: React の機能を利用するために必要です。
- `Send` アイコンを `lucide-react` からインポート: メッセージ送信ボタンに表示するアイコンとして使用されています。

### 2. インターフェース定義
- `ChatInputProps`: このインターフェースは、コンポーネントが受け取るプロパティの型を定義しています。`onSendMessage` はメッセージを送信するための関数、`isLoading` は送信中かどうかを示すブール値です。

### 3. コンポーネント本体
- `ChatInput`: 関数コンポーネントとして定義され、受け取ったプロパティに基づいて動作します。以下の処理が行われます:
  - **状態管理**: `useState` を使ってメッセージ入力用の状態 `message` を管理します。初期値は空文字列です。

### 4. メッセージ送信処理
- `handleSubmit`: フォーム送信時に呼び出される関数です。以下の流れで処理が行われます:
  - イベントのデフォルト動作をキャンセルします（ページリロードを防ぐ）。
  - メッセージが空でなく、かつ送信中でない場合にのみ、`onSendMessage` を呼び出し、現在のメッセージを引数として渡します。その後、入力フィールドをクリアします。

### 5. JSX レンダリング
- フォーム要素: `form` タグには `onSubmit` 属性があり、ユーザーが Enter キーでメッセージを送信できるようになっています。
- 入力フィールド: ユーザーがメッセージを入力するためのテキストボックスです。以下の特徴があります:
  - 値は `message` 状態にバインドされており、変更時に状態更新関数 (`setMessage`) が呼ばれます。
  - プレースホルダーとして "Type your message here..." が設定されています。
  - スタイルクラスにより外観が整えられています。送信中は無効化されます。
- ボタン要素: メッセージ送信ボタンであり、条件付きでスタイルや無効化設定が適用されます:
  - ボタンは送信中またはメッセージが空の場合には無効化され、異なる背景色（灰色）になります。
  - メッセージが入力されていれば青色になり、ホバー時に色が変わります。アイコンも表示されています。
