# Podsumowanie Projektu - Walkative RAG System

## 🎯 Cel Projektu

System RAG (Retrieval-Augmented Generation) dla bazy danych Walkative, który umożliwia:
- Wyszukiwanie semantyczne w bazie danych PostgreSQL z pgvector
- Generowanie odpowiedzi używając Google Gemini API
- Interfejs czatu do interakcji z bazą wiedzy

## 📁 Struktura Projektu (Monorepo)

```
walkative-rag/
├── backend/                    # Backend FastAPI (Python)
│   ├── app.py                 # Główna aplikacja FastAPI z endpointami
│   ├── rag.py                 # Logika RAG (wyszukiwanie + generowanie odpowiedzi)
│   ├── models.py              # Modele Pydantic dla API
│   ├── database.py            # Połączenie z PostgreSQL
│   └── __init__.py
│
├── frontend/                   # Frontend React + TypeScript (Vite)
│   ├── components/            # Komponenty React
│   │   ├── ChatInterface.tsx # Główny interfejs czatu
│   │   ├── Message.tsx        # Komponent wiadomości
│   │   ├── SourceCard.tsx     # Karta źródła
│   │   └── icons/             # Ikony SVG
│   ├── services/
│   │   └── ragService.ts      # Serwis do komunikacji z backendem
│   ├── App.tsx                # Główny komponent
│   ├── index.tsx              # Entry point
│   ├── types.ts               # Definicje TypeScript
│   ├── package.json           # Zależności Node.js
│   └── vite.config.ts         # Konfiguracja Vite
│
├── .env                        # Zmienne środowiskowe (NIE COMMITOWAĆ)
├── .env.example               # Przykładowa konfiguracja
├── requirements.txt            # Zależności Python
├── add_embedding_columns.py   # Skrypt: dodawanie kolumn embedding
├── generate_embeddings.py     # Skrypt: generowanie embeddingów
├── check_embedding_progress.py # Skrypt: monitorowanie postępu
└── test_setup.py              # Skrypt: testowanie konfiguracji
```

## 🔧 Technologie

### Backend
- **FastAPI** - framework webowy
- **PostgreSQL** z **pgvector** - baza danych z wektorami
- **Google Gemini API** - embeddingi (text-embedding-004) i generowanie (gemini-2.5-flash)
- **Python 3.14**

### Frontend
- **React 19** + **TypeScript**
- **Vite** - build tool
- **Tailwind CSS** (via CDN)

## 🔑 Konfiguracja

### Zmienne środowiskowe (`.env`)

```bash
# Google Gemini API Key
GOOGLE_API_KEY=your_gemini_api_key_here

# PostgreSQL Database Connection
DATABASE_URL=postgresql://Lechu1@localhost:5432/walkative_local
```

### Frontend (`.env.local`)

```bash
# URL backendu RAG
VITE_RAG_API_URL=http://127.0.0.1:8000/api/query
# Dla AI Studio użyj tunelu Cloudflare:
# VITE_RAG_API_URL=https://xxxxx.trycloudflare.com/api/query
```

## 🚀 Uruchomienie

### Backend

```bash
# 1. Aktywuj środowisko wirtualne
source venv/bin/activate

# 2. Uruchom serwer
uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000
```

Backend dostępny: `http://127.0.0.1:8000`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend dostępny: `http://localhost:3000`

### Tunel HTTPS (dla AI Studio)

```bash
cloudflared tunnel --url http://127.0.0.1:8000
```

## 📡 API Endpoints

### Główne endpointy

- `POST /api/query` - **Główny endpoint dla frontendu** (zgodny z AI Studio)
  - Request: `{"query": "pytanie użytkownika"}`
  - Response: `{"answer": "...", "sources": [...]}`

- `POST /chat` - Alternatywny endpoint RAG
- `POST /search` - Wyszukiwanie semantyczne
- `GET /docs` - Dokumentacja Swagger
- `GET /health` - Health check

## 🗄️ Baza Danych

### Struktura
- **Schema:** `main`
- **Rozszerzenie:** `pgvector` (wersja 0.8.1)
- **Wymiar wektora:** 768 (text-embedding-004)

### Kolumny embedding
- Automatyczne wykrywanie kolumn tekstowych
- Format: `{original_column}_embedding` typu `vector(768)`
- **76 kolumn** z embeddingami w różnych tabelach
- **14,990 rekordów** zembedowanych (100%)

### Główne tabele z embeddingami
- `articles_article` - artykuły (content, description w wielu językach)
- `products_product` - produkty (descriptions, SEO)
- `products_producthighlight` - wyróżnienia produktów
- `points_point` - punkty na mapie (descriptions)
- `mailing_mailing` - maile (body)
- `notes_note` - notatki (content)
- I wiele innych...

## 🔍 Jak Działa System

### 1. Wyszukiwanie Semantyczne (`backend/rag.py`)

```python
search_similar_content(query: str, limit: int = 5)
```

Proces:
1. Generuje embedding dla zapytania użytkownika (text-embedding-004, RETRIEVAL_QUERY)
2. Przeszukuje wszystkie kolumny z embeddingami w bazie
3. Używa cosine similarity (`<=>` operator w pgvector)
4. Zwraca top-k najbardziej podobnych fragmentów

### 2. Generowanie Odpowiedzi (`backend/rag.py`)

```python
generate_rag_response(query: str, context_results: List[SearchResult])
```

Proces:
1. Buduje kontekst z wyników wyszukiwania
2. Tworzy prompt dla Gemini (gemini-2.5-flash)
3. Generuje odpowiedź na podstawie kontekstu
4. Zwraca odpowiedź z źródłami

### 3. Frontend (`frontend/services/ragService.ts`)

```typescript
queryRagApi(query: string): Promise<RagApiResponse>
```

Proces:
1. Wysyła POST request do `/api/query`
2. Wyświetla odpowiedź w interfejsie czatu
3. Pokazuje źródła (sources) obok odpowiedzi

## 🔐 CORS Configuration

Backend skonfigurowany dla:
- Lokalnego developmentu (localhost:3000, 5173, 8080)
- Google Cloud origins (`.usercontent.goog` via regex)
- `allow_credentials: True`

## 📊 Status Embeddingów

- **Zembedowane:** 14,990 rekordów (100%)
- **Kolumny:** 76 kolumn z embeddingami
- **Status:** ✅ Wszystkie rekordy przetworzone

Sprawdź postęp:
```bash
python check_embedding_progress.py
```

## 🛠️ Skrypty Pomocnicze

### `add_embedding_columns.py`
- Automatycznie wykrywa kolumny tekstowe
- Dodaje kolumny `{column}_embedding` typu `vector(768)`

### `generate_embeddings.py`
- Generuje embeddingi dla wszystkich rekordów bez embeddingów
- Przetwarza po 1000 rekordów na raz (limit w SQL)
- Można bezpiecznie przerwać i wznowić

### `check_embedding_progress.py`
- Pokazuje statystyki embeddingów
- Lista kolumn z pozostałymi rekordami
- Podsumowanie postępu

### `test_setup.py`
- Testuje połączenie z bazą
- Sprawdza pgvector
- Weryfikuje konfigurację API

## 🌐 Integracja z AI Studio

### Konfiguracja
- Frontend działa w Google Cloud (AI Studio)
- Backend lokalny (lub na serwerze)
- Komunikacja przez tunel Cloudflare (HTTPS)

### URL Tunelu
- Generowany przez: `cloudflared tunnel --url http://127.0.0.1:8000`
- Format: `https://xxxxx.trycloudflare.com`
- Ustaw w `frontend/.env.local`: `VITE_RAG_API_URL=https://xxxxx.trycloudflare.com/api/query`

## 📝 Ważne Uwagi

### Jakość odpowiedzi
- **Aktualny problem:** Jakość odpowiedzi jest niska
- **Możliwe przyczyny:**
  - Zbyt mało kontekstu w promptach
  - Nieodpowiednie dopasowanie wyników wyszukiwania
  - Model może wymagać lepszego prompt engineering
  - Może potrzeba więcej wyników (limit=5)

### Rozwiązania do rozważenia
1. Zwiększyć limit wyników wyszukiwania (np. 10-15 zamiast 5)
2. Ulepszyć prompt w `generate_rag_response()`
3. Filtrowanie wyników po minimalnym podobieństwie
4. Lepsze formatowanie kontekstu dla modelu
5. Użycie bardziej zaawansowanego modelu (np. gemini-pro zamiast gemini-2.5-flash)

## 🔄 Git Workflow

### Repozytorium
- **GitHub:** https://github.com/piotrlechowski-arch/walkative-RAG-website-chat
- **Struktura:** Monorepo (backend + frontend)
- **Branch:** `main`

### Ostatnie commity
- `6da1cb7` - Clean up: Remove duplicate frontend files
- `1dbed49` - Merge: Integrate backend with existing frontend repository
- `52be054` - Add quick start guide

## 🐛 Znane Problemy / Do Poprawy

1. **Jakość odpowiedzi RAG** - wymaga ulepszenia
2. **URL w sources** - obecnie zawsze `"#"` - można dodać logikę generowania URL
3. **Brak testów** - można dodać testy jednostkowe
4. **Brak walidacji** - można dodać więcej walidacji w API

## 📚 Dokumentacja

- `README.md` - Główna dokumentacja
- `QUICKSTART.md` - Szybki start
- `frontend/README.md` - Dokumentacja frontendu
- `SETUP_GITHUB.md` - Instrukcje GitHub

## 🎯 Następne Kroki

1. **Poprawa jakości odpowiedzi RAG**
   - Zwiększyć limit wyników
   - Ulepszyć prompt
   - Dodać filtrowanie po podobieństwie

2. **Dodanie funkcjonalności**
   - Generowanie URL dla sources
   - Lepsze formatowanie odpowiedzi
   - Cache dla często zadawanych pytań

3. **Optymalizacja**
   - Indeksy w bazie danych
   - Optymalizacja zapytań SQL
   - Rate limiting w API

4. **Testy**
   - Testy jednostkowe
   - Testy integracyjne
   - Testy E2E

## 🔗 Linki

- **GitHub:** https://github.com/piotrlechowski-arch/walkative-RAG-website-chat
- **AI Studio:** https://ai.studio/apps/drive/1lLQ4OX04Vi6ZhJUC_p8dyGe_aXJs_8Qc
- **Backend API Docs:** http://127.0.0.1:8000/docs (gdy backend działa)

## 👤 Kontakt / Właściciel

- **Użytkownik:** Piotr Lechowski
- **Firma:** Walkative
- **Strony:** freewalkingtour.com, walkative.eu

---

**Ostatnia aktualizacja:** 2025-11-15
**Status:** ✅ Działający system, wymaga poprawy jakości odpowiedzi

