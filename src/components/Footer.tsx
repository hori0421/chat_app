import React from 'react';
import { ChatInput } from './ChatInput';

interface FooterProps {
  onSendMessage: (message: string) => void;
  isLoading: boolean;
}

const Footer: React.FC<FooterProps> = ({ onSendMessage, isLoading }) => {
  return (
    <footer className="bg-white border-t border-gray-200 p-4">
      <div className="container mx-auto">
        <ChatInput onSendMessage={onSendMessage} isLoading={isLoading} />
      </div>
    </footer>
  );
};

export default Footer; 