# MessageBubble コンポーネント ドキュメント

## 概要
`MessageBubble` は、チャットアプリケーションにおけるメッセージのバブルを表示するための React コンポーネントです。このコンポーネントは、ユーザーとボットのメッセージを視覚的に区別し、適切なスタイルで表示します。

## 目的
このコンポーネントは、チャットインターフェース内でメッセージを表示するために設計されています。ユーザーからのメッセージとボットからの応答を明確に区別し、それぞれ異なるデザインで表現します。

## プロパティ
### `MessageBubbleProps`
- `role` (string): メッセージの送信者の役割。値は 'user' または 'bot' のいずれかです。
- `content` (string): 表示するメッセージの内容。

## 使用方法
以下は、このコンポーネントを使用する例です:
```jsx
<MessageBubble role="user" content="こんにちは！" />
<MessageBubble role="bot" content="こんにちは！どんなご用件でしょうか？" />
```
このようにして、ユーザーとボットそれぞれのメッセージを表示できます。

## スタイルとレイアウト
- ユーザーからのメッセージは右側に配置され、青色の背景が適用されます。
- ボットからのメッセージは左側に配置され、灰色の背景が適用されます。
- 各メッセージにはアイコンが付与されており、ユーザーには白いユーザーアイコンが、ボットには灰色のボットアイコンが表示されます。
- メッセージバブルには影があり、視覚的な深みを加えています。

## 拡張性・変更点について
このコンポーネントはシンプルな構造になっているため、新しい機能やスタイルを追加することが容易です。例えば:
- 新しい役割（例: 管理者）を追加したり、その場合のスタイルを定義したりできます。
- アイコンや色合いなども簡単にカスタマイズ可能です。 

## 注意事項
- `role` プロパティには正しい値（'user' または 'bot'）を指定してください。それ以外の場合、意図した通りに表示されない可能性があります。
# 詳細
## コードの説明

### インポート部分
- `import React from 'react';`: React ライブラリをインポートし、コンポーネントを作成するために必要です。
- `import { User, Bot } from 'lucide-react';`: ユーザーとボットのアイコンを表示するために、Lucide アイコンライブラリから関連アイコンをインポートしています。

### インターフェース定義
- `interface MessageBubbleProps`: このインターフェースは、`MessageBubble` コンポーネントに渡されるプロパティの型を定義します。
  - `role: string;`: メッセージの送信者の役割（ユーザーまたはボット）を指定します。
  - `content: string;`: 表示するメッセージの内容を指定します。

### コンポーネント定義
- `export const MessageBubble: React.FC<MessageBubbleProps>`: `MessageBubble` コンポーネントを定義し、`MessageBubbleProps` 型を使用してプロパティを受け取ります。

### メッセージ送信者の判別
- `const isUser = role === 'user';`: プロパティとして渡された `role` が 'user' であるかどうかを判別し、ブール値として格納します。この情報はスタイルやレイアウトの条件分岐に使用されます。

### JSX の構造
- `<div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>`: メッセージバブル全体のラッパーで、ユーザーとボットで異なる配置（右寄せまたは左寄せ）を適用します。
  - `flex` クラスはフレックスボックスレイアウトを適用し、メッセージバブル内の要素を整列させます。

- `<div className={`flex items-start space-x-2 max-w-3/4 ${isUser ? 'flex-row-reverse' : ''}`}>`: メッセージ内容とアイコンを含むラッパーです。ユーザーの場合はアイコンとメッセージが逆方向に配置されます。

- `<div className={`p-2 rounded-full ${isUser ? 'bg-blue-500' : 'bg-gray-300'}`}>`: アイコンが表示される部分で、ユーザーの場合は青色、ボットの場合は灰色の背景が適用されます。これにより視覚的な区別が強調されます。
  - `rounded-full` クラスにより、円形のデザインになります。

- `{isUser ? <User className="w-6 h-6 text-white" /> : <Bot className="w-6 h-6 text-gray-600" />}`: ユーザーまたはボットに応じて異なるアイコンが表示されます。サイズや色も設定されています。

- `<div className={`p-3 rounded-lg ${isUser ? 'bg-blue-100 text-blue-800' : 'bg-white text-gray-800'} shadow`}>`: メッセージ内容が表示される部分で、背景色やテキストカラーもユーザーによって異なります。また、影効果が追加されており、立体感があります。 
  - `rounded-lg` クラスにより角が丸くなっています。

### メッセージ内容表示
- `<p className="text-sm">{content}</p>`: 実際のメッセージ内容が小さめのフォントサイズで表示されます。