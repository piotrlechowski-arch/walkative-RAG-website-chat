import React, { useState, useRef, useEffect, useCallback } from 'react';
import type { ChatMessage } from '../types';
import { queryRagApi } from '../services/ragService';
import Message from './Message';
import { SendIcon } from './icons/SendIcon';

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);
  
  const addMessage = useCallback((message: Omit<ChatMessage, 'id'>) => {
    setMessages((prev) => [...prev, { ...message, id: Date.now().toString() }]);
  }, []);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessageContent = input;
    setInput('');
    addMessage({ role: 'user', content: userMessageContent });
    setIsLoading(true);

    try {
      const response = await queryRagApi(userMessageContent);
      addMessage({
        role: 'assistant',
        content: response.answer,
        sources: response.sources,
      });
    } catch (error) {
      console.error("Error querying RAG API:", error);
      const errorMessage = error instanceof Error 
        ? error.message 
        : 'Wystąpił nieznany błąd.';

      const detailedErrorMessage = `Przepraszam, wystąpił krytyczny błąd komunikacji.

**Komunikat błędu:**
${errorMessage}

---

To najprawdopodobniej problem z konfiguracją Twojego serwera backend, a nie błąd w aplikacji czatu. Oto najczęstsza przyczyna i rozwiązanie:

**Problem: Brak konfiguracji CORS w backendzie (np. FastAPI)**
Przeglądarka ze względów bezpieczeństwa blokuje zapytania do serwera, jeśli nie zezwoli on na połączenia z innych "źródeł" (origin).

**✅ Rozwiązanie (dla FastAPI w Pythonie):**

1.  Otwórz plik \`main.py\` swojego serwera.
2.  Upewnij się, że masz dodany poniższy kod:

    \`\`\`python
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware

    app = FastAPI()

    # Lista dozwolonych źródeł
    origins = [
        "*",  # Na czas dewelopmentu, zezwól na wszystko
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    \`\`\`

3.  Zapisz plik i **zrestartuj serwer** (\`uvicorn\`).

---
Jeśli to nie pomoże, sprawdź również:
- Czy serwer backendowy jest na pewno uruchomiony?
- Czy serwer nasłuchuje na adresie \`http://127.0.0.1:8000\`?
`;
      
      addMessage({
        role: 'assistant',
        content: detailedErrorMessage,
        isError: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-gray-800 border border-gray-700 rounded-lg shadow-2xl">
      <div className="flex-grow p-4 overflow-y-auto">
        <div className="flex flex-col space-y-4">
          {messages.map((msg) => (
            <Message key={msg.id} message={msg} />
          ))}
          {isLoading && (
            <div className="flex justify-start">
               <div className="bg-gray-700 rounded-lg p-3 max-w-lg animate-pulse">
                  <div className="w-16 h-4 bg-gray-600 rounded"></div>
               </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>
      <div className="p-4 border-t border-gray-700 bg-gray-800 rounded-b-lg">
        <form onSubmit={handleSendMessage} className="flex items-center space-x-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Zadaj pytanie o treść strony..."
            disabled={isLoading}
            className="flex-grow bg-gray-700 border border-gray-600 rounded-full py-2 px-4 text-gray-200 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 transition duration-200 disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="bg-purple-600 text-white rounded-full p-3 hover:bg-purple-700 disabled:bg-gray-600 disabled:cursor-not-allowed transition duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-purple-500"
          >
            <SendIcon className="w-5 h-5" />
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatInterface;