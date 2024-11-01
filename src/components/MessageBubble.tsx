import React from 'react';
import { User, Bot } from 'lucide-react';

interface MessageBubbleProps {
  role: string;
  content: string;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ role, content }) => {
  const isUser = role === 'user';
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`flex items-start space-x-2 max-w-3/4 ${isUser ? 'flex-row-reverse' : ''}`}>
        <div className={`p-2 rounded-full ${isUser ? 'bg-blue-500' : 'bg-gray-300'}`}>
          {isUser ? <User className="w-6 h-6 text-white" /> : <Bot className="w-6 h-6 text-gray-600" />}
        </div>
        <div className={`p-3 rounded-lg ${isUser ? 'bg-blue-100 text-blue-800' : 'bg-white text-gray-800'} shadow`}>
          <p className="text-sm">{content}</p>
        </div>
      </div>
    </div>
  );
};