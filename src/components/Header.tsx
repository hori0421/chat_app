import React from 'react';
import { MessageCircle, PlusCircle } from 'lucide-react';

interface HeaderProps {
  onNewChat: () => void;
}

const Header: React.FC<HeaderProps> = ({ onNewChat }) => {
  return (
    <header className="bg-blue-600 text-white p-4 shadow-md">
      <div className="container mx-auto flex items-center justify-between">
        <div className="flex items-center">
          <MessageCircle className="mr-2" />
          <h1 className="text-2xl font-bold">AI Chat Assistant</h1>
        </div>
        <button
          onClick={onNewChat}
          className="flex items-center bg-white text-blue-600 px-4 py-2 rounded-lg hover:bg-blue-100 transition-colors duration-200"
        >
          <PlusCircle className="mr-2" />
          New Chat
        </button>
      </div>
    </header>
  );
};

export default Header; 