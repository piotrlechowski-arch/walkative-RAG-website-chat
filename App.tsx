
import React from 'react';
import ChatInterface from './components/ChatInterface';
import { InfoIcon } from './components/icons/InfoIcon';

const App: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 flex flex-col">
      <header className="bg-gray-800/50 backdrop-blur-sm border-b border-gray-700 p-4 shadow-lg sticky top-0 z-10">
        <h1 className="text-xl md:text-2xl font-bold text-center text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-cyan-400">
          Czat RAG z Treścią Twojej Strony
        </h1>
      </header>
      
      <main className="flex-grow flex flex-col items-center justify-center p-4">
          <div className="bg-gray-800 border border-gray-700 rounded-lg p-4 mb-6 max-w-4xl w-full flex items-start space-x-3 text-sm text-gray-300">
              <div className="flex-shrink-0 pt-1">
                <InfoIcon className="w-5 h-5 text-cyan-400" />
              </div>
              <div>
                  <h2 className="font-semibold text-gray-100 mb-1">Jak to działa?</h2>
                  <p>
                    Ten interfejs jest połączony z Twoim backendem RAG (Retrieval-Augmented Generation). Gdy zadajesz pytanie, jest ono wysyłane do serwera, który:
                  </p>
                  <ol className="list-decimal list-inside mt-2 space-y-1 text-gray-400">
                      <li>Przekształca Twoje pytanie w wektor (embedding).</li>
                      <li>Używa rozszerzenia <code className="bg-gray-700 text-cyan-400 px-1 py-0.5 rounded text-xs">pgvector</code> w bazie PostgreSQL do znalezienia w Twojej witrynie najbardziej trafnych fragmentów treści.</li>
                      <li>Przesyła te fragmenty wraz z Twoim pytaniem do modelu Gemini, aby wygenerować precyzyjną odpowiedź.</li>
                      <li>Zwraca odpowiedź wraz z użytymi źródłami.</li>
                  </ol>
              </div>
          </div>

          <div className="w-full max-w-4xl flex-grow h-[calc(100vh-250px)]">
            <ChatInterface />
          </div>
      </main>
    </div>
  );
};

export default App;
