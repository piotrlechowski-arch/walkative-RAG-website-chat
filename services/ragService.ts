
import type { RagApiResponse } from '../types';

// Adres URL Twojego backendu. Używamy ścieżki względnej, zakładając,
// że serwer deweloperski ma skonfigurowane proxy lub backend serwuje pliki frontendu.
// W razie potrzeby zmień na pełny adres, np. 'http://localhost:8000/api/query'.
const RAG_API_URL = '/api/query';

/**
 * Wysyła zapytanie do prawdziwego backendu RAG.
 *
 * Ta funkcja zastępuje poprzednią, mockową implementację.
 *
 * @param query - Pytanie użytkownika.
 * @returns Obietnica, która rozwiązuje się do obiektu RagApiResponse.
 * @throws Błąd, jeśli komunikacja z serwerem się nie powiedzie.
 */
export const queryRagApi = async (query: string): Promise<RagApiResponse> => {
  console.log(`Sending query to RAG backend: "${query}"`);

  try {
    const response = await fetch(RAG_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      // Backend powinien oczekiwać obiektu JSON z kluczem 'query'
      body: JSON.stringify({ query }),
    });

    if (!response.ok) {
      // Próba odczytania bardziej szczegółowego błędu z odpowiedzi JSON od serwera
      const errorData = await response.json().catch(() => ({ 
        message: 'Nie udało się odczytać szczegółów błędu z odpowiedzi serwera.' 
      }));
      throw new Error(`Błąd serwera: ${response.status} ${response.statusText}. ${errorData.detail || ''}`);
    }

    const data: RagApiResponse = await response.json();
    return data;
  } catch (error) {
    console.error("Błąd podczas komunikacji z API RAG:", error);
    // Rzucamy błąd dalej, aby komponent UI mógł go obsłużyć
    // i wyświetlić odpowiednią wiadomość użytkownikowi.
    throw new Error('Nie udało się połączyć z serwerem RAG. Sprawdź konsolę, aby uzyskać więcej informacji.');
  }
};
