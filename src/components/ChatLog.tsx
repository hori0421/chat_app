import React from 'react';
import { MessageBubble } from './MessageBubble';
import LoadingSpinner from './LoadingSpinner';

interface ChatLogProps {
  messages: { role: string; content: string }[];
  loading: boolean;
}

const ChatLog: React.FC<ChatLogProps> = ({ messages, loading }) => {
  return (
    <div className="space-y-4">
      {messages.map((msg, index) => (
        <MessageBubble key={index} role={msg.role} content={msg.content} />
      ))}
      {loading && <LoadingSpinner />}
    </div>
  );
};

export default ChatLog; 