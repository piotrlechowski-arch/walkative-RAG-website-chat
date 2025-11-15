# Walkative RAG System

System RAG (Retrieval-Augmented Generation) dla bazy danych walkative_local z użyciem Google Gemini API i pgvector.

## Struktura projektu

```
walkative-rag/
├── backend/              # Backend FastAPI
│   ├── __init__.py
│   ├── app.py           # Główna aplikacja FastAPI
│   ├── database.py      # Połączenie z bazą danych
│   ├── rag.py           # Logika RAG (wyszukiwanie + generowanie odpowiedzi)
│   └── models.py        # Modele Pydantic
├── frontend/            # Frontend (do dodania)
├── .env                 # Zmienne środowiskowe (utwórz na podstawie .env.example)
├── .env.example         # Przykładowa konfiguracja
├── requirements.txt     # Zależności Python
├── add_embedding_columns.py  # Skrypt do dodawania kolumn embedding
├── generate_embeddings.py    # Skrypt do generowania embeddingów
├── check_embedding_progress.py  # Skrypt do monitorowania postępu
└── README.md            # Ten plik
```

## Instalacja

### Backend

1. **Utwórz środowisko wirtualne:**
```bash
python3 -m venv venv
source venv/bin/activate
```

2. **Zainstaluj zależności:**
```bash
pip install -r requirements.txt
```

3. **Skonfiguruj zmienne środowiskowe:**
```bash
cp .env.example .env
# Edytuj .env i dodaj swój GOOGLE_API_KEY
```

### Frontend

(Instrukcje do dodania po skonfigurowaniu frontendu)

## Konfiguracja bazy danych

1. **Zainstaluj pgvector** (jeśli jeszcze nie):
```bash
brew install pgvector
```

2. **Aktywuj rozszerzenie w bazie:**
```bash
psql walkative_local -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

3. **Dodaj kolumny embedding** (jeśli jeszcze nie):
```bash
python add_embedding_columns.py
```

## Generowanie embeddingów

Uruchom skrypt do generowania embeddingów dla wszystkich kolumn tekstowych:

```bash
python generate_embeddings.py
```

Sprawdź postęp:
```bash
python check_embedding_progress.py
```

## Uruchomienie

### Backend

```bash
source venv/bin/activate
uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000
```

Backend będzie dostępny pod adresem: `http://localhost:8000`

### Frontend

(Instrukcje do dodania)

### Tunel HTTPS (dla developmentu z AI Studio)

Jeśli frontend działa w Google Cloud, użyj cloudflared do utworzenia tunelu HTTPS:

```bash
cloudflared tunnel --url http://127.0.0.1:8000
```

Użyj wygenerowanego URL w konfiguracji frontendu.

## Endpointy API

- `GET /` - Informacje o API
- `GET /docs` - Dokumentacja Swagger
- `GET /health` - Health check
- `POST /search` - Wyszukiwanie semantyczne
- `POST /chat` - Czat z RAG
- `POST /api/query` - Endpoint zgodny z AI Studio

## Funkcjonalności

- ✅ Automatyczne wykrywanie kolumn tekstowych do embedowania
- ✅ Generowanie embeddingów dla wszystkich wersji językowych (pl, en, de, es)
- ✅ Wyszukiwanie semantyczne z cosine similarity
- ✅ RAG z użyciem Google Gemini (gemini-2.5-flash)
- ✅ REST API z FastAPI
- ✅ Automatyczna dokumentacja API (Swagger)
- ✅ CORS skonfigurowany dla Google Cloud origins

## Uwagi techniczne

- **Wymiar wektora:** 768 (text-embedding-004)
- **Task type:** `RETRIEVAL_DOCUMENT` dla dokumentów, `RETRIEVAL_QUERY` dla zapytań
- **Model czatu:** gemini-2.5-flash
- **Obsługa języków:** Automatyczna dla wszystkich wersji językowych w bazie

## Rozwiązywanie problemów

**Błąd: "GOOGLE_API_KEY nie jest ustawiony"**
- Upewnij się, że plik `.env` istnieje i zawiera `GOOGLE_API_KEY`

**Błąd: "ModuleNotFoundError"**
- Aktywuj środowisko wirtualne: `source venv/bin/activate`
- Zainstaluj zależności: `pip install -r requirements.txt`

**Błąd połączenia z bazą danych**
- Sprawdź czy PostgreSQL jest uruchomiony: `brew services list | grep postgresql`
- Sprawdź czy baza `walkative_local` istnieje
- Zweryfikuj `DATABASE_URL` w pliku `.env`

**Błąd CORS / Private Network Access**
- Użyj cloudflared do utworzenia tunelu HTTPS
- Upewnij się, że origin frontendu jest dodany do `allow_origins` w `backend/app.py`

## Development

### Struktura monorepo

Projekt używa struktury monorepo z osobnymi folderami dla backendu i frontendu:
- `backend/` - Kod Python/FastAPI
- `frontend/` - Kod frontendu (do dodania)

### Git workflow

1. Utwórz nowe repozytorium na GitHub
2. Dodaj remote:
```bash
git remote add origin https://github.com/TwojaNazwa/walkative-rag.git
```
3. Dodaj pliki i commit:
```bash
git add .
git commit -m "Initial commit: Backend RAG system"
git push -u origin main
```
