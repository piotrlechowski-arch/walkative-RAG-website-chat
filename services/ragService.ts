import type { RagApiResponse } from '../types';

// Adres URL Twojego backendu. Zmieniono na publiczny adres tunelu Cloudflare,
// aby umożliwić komunikację z serwerem.
const RAG_API_URL = 'https://hearings-heavily-editing-recipes.trycloudflare.com/api/query';

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
  console.log(`Sending query to RAG backend: "${query}" at ${RAG_API_URL}`);

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
        detail: 'Nie udało się odczytać szczegółów błędu z odpowiedzi serwera.' 
      }));
      throw new Error(`Błąd serwera: ${response.status} ${response.statusText}. Szczegóły: ${errorData.detail || 'Brak dodatkowych informacji.'}`);
    }

    const data: RagApiResponse = await response.json();
    return data;
  } catch (error) {
    console.error("Błąd podczas komunikacji z API RAG:", error);
    
    // Specjalna obsługa błędu 'Failed to fetch', który jest bardzo częsty w developmencie
    if (error instanceof TypeError && error.message === 'Failed to fetch') {
      throw new Error('Nie udało się nawiązać połączenia z serwerem backendu. Upewnij się, że serwer jest uruchomiony i dostępny pod adresem: ' + RAG_API_URL);
    }

    // Rzucamy błąd dalej, aby komponent UI mógł go obsłużyć
    if (error instanceof Error) {
        throw error; // Rzuć oryginalny błąd, jeśli już jest instancją Error
    }

    // W przeciwnym razie, utwórz nowy obiekt błędu
    throw new Error('Wystąpił nieoczekiwany problem z połączeniem. Sprawdź konsolę, aby uzyskać więcej informacji.');
  }
};