# Walkative RAG System

<div align="center">
<img width="1200" height="475" alt="GHBanner" src="https://github.com/user-attachments/assets/0aa67016-6eaf-458a-adb2-6e31a0763ed6" />
</div>

System RAG (Retrieval-Augmented Generation) dla bazy danych walkative_local z użyciem Google Gemini API i pgvector.

**View your app in AI Studio:** https://ai.studio/apps/drive/1lLQ4OX04Vi6ZhJUC_p8dyGe_aXJs_8Qc

## Struktura projektu

```
walkative-rag/
├── backend/              # Backend FastAPI
│   ├── __init__.py
│   ├── app.py           # Główna aplikacja FastAPI
│   ├── database.py      # Połączenie z bazą danych
│   ├── rag.py           # Logika RAG (wyszukiwanie + generowanie odpowiedzi)
│   └── models.py        # Modele Pydantic
├── frontend/            # Frontend React + TypeScript
│   ├── components/      # Komponenty React
│   ├── services/        # Serwisy API
│   └── ...
├── .env                 # Zmienne środowiskowe (utwórz na podstawie .env.example)
├── .env.example         # Przykładowa konfiguracja
├── requirements.txt     # Zależności Python
├── add_embedding_columns.py  # Skrypt do dodawania kolumn embedding
├── generate_embeddings.py    # Skrypt do generowania embeddingów
└── check_embedding_progress.py  # Skrypt do monitorowania postępu
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

1. **Przejdź do folderu frontend:**
```bash
cd frontend
```

2. **Zainstaluj zależności:**
```bash
npm install
```

3. **Skonfiguruj zmienne środowiskowe:**
```bash
cp .env.example .env.local
# Edytuj .env.local i ustaw VITE_RAG_API_URL
```

4. **Uruchom frontend:**
```bash
npm run dev
```

Frontend będzie dostępny pod adresem: `http://localhost:3000`

Szczegółowe instrukcje w [frontend/README.md](frontend/README.md)

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

Zobacz [frontend/README.md](frontend/README.md) dla szczegółowych instrukcji.

Szybki start:
```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

### Tunel HTTPS (dla developmentu z AI Studio)

Jeśli frontend działa w Google Cloud, użyj cloudflared do utworzenia tunelu HTTPS:

```bash
cloudflared tunnel --url http://127.0.0.1:8000
```

Użyj wygenerowanego URL w konfiguracji frontendu (`frontend/.env.local`).

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
- ✅ Frontend React + TypeScript z interfejsem czatu

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
- `frontend/` - Kod React/TypeScript

### Szybki start

Zobacz [QUICKSTART.md](QUICKSTART.md) dla szybkiego przewodnika uruchomienia.
