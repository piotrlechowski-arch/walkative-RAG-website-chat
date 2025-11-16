
import React from 'react';
import type { ChatMessage } from '../types';
import SourceCard from './SourceCard';
import { BotIcon } from './icons/BotIcon';
import { UserIcon } from './icons/UserIcon';
import { ErrorIcon } from './icons/ErrorIcon';

interface MessageProps {
  message: ChatMessage;
}

const Message: React.FC<MessageProps> = ({ message }) => {
  const isUser = message.role === 'user';
  const isError = message.isError;

  return (
    <div className={`flex items-start gap-3 ${isUser ? 'justify-end' : 'justify-start'}`}>
      {!isUser && (
        <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${isError ? 'bg-red-500' : 'bg-gradient-to-br from-purple-500 to-cyan-400'}`}>
            {isError ? <ErrorIcon className="w-5 h-5 text-white" /> : <BotIcon className="w-5 h-5 text-white" />}
        </div>
      )}
      
      <div className={`max-w-xl ${isUser ? 'order-last' : ''}`}>
        <div className={`px-4 py-3 rounded-2xl ${isUser ? 'bg-purple-600 text-white rounded-br-none' : isError ? 'bg-red-900/50 border border-red-700/50 text-red-200 rounded-bl-none' : 'bg-gray-700 text-gray-200 rounded-bl-none'}`}>
          <p className="whitespace-pre-wrap">{message.content}</p>
        </div>
        
        {message.sources && message.sources.length > 0 && (
          <div className="mt-3">
            <h4 className="text-xs font-semibold text-gray-400 mb-2">Źródła:</h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
              {message.sources.map((source) => (
                <SourceCard key={source.id} source={source} />
              ))}
            </div>
          </div>
        )}
      </div>

       {isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-600 flex items-center justify-center">
            <UserIcon className="w-5 h-5 text-gray-300" />
        </div>
      )}
    </div>
  );
};

export default Message;