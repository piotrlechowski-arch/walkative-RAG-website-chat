# Quick Start Guide

Szybki przewodnik uruchomienia całego projektu.

## Wymagania

- Python 3.14+
- Node.js 18+
- PostgreSQL z pgvector
- Google Gemini API Key

## Krok 1: Backend

```bash
# 1. Utwórz środowisko wirtualne
python3 -m venv venv
source venv/bin/activate

# 2. Zainstaluj zależności
pip install -r requirements.txt

# 3. Skonfiguruj .env
cp .env.example .env
# Edytuj .env i dodaj GOOGLE_API_KEY

# 4. Uruchom backend
uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000
```

Backend będzie dostępny: `http://127.0.0.1:8000`

## Krok 2: Frontend

W nowym terminalu:

```bash
# 1. Przejdź do folderu frontend
cd frontend

# 2. Zainstaluj zależności
npm install

# 3. Skonfiguruj .env.local
cp .env.example .env.local
# Domyślnie używa http://127.0.0.1:8000/api/query

# 4. Uruchom frontend
npm run dev
```

Frontend będzie dostępny: `http://localhost:3000`

## Krok 3: (Opcjonalnie) Tunel dla AI Studio

Jeśli chcesz używać z AI Studio (Google Cloud):

```bash
# W osobnym terminalu
cloudflared tunnel --url http://127.0.0.1:8000
```

Skopiuj wygenerowany URL i ustaw w `frontend/.env.local`:
```
VITE_RAG_API_URL=https://xxxxx.trycloudflare.com/api/query
```

## Weryfikacja

1. Backend: `curl http://127.0.0.1:8000/health`
2. Frontend: Otwórz `http://localhost:3000` w przeglądarce
3. Przetestuj czat - zadaj pytanie o wycieczki

## Troubleshooting

**Backend nie startuje:**
- Sprawdź czy PostgreSQL działa
- Sprawdź czy `.env` ma poprawny `GOOGLE_API_KEY`

**Frontend nie łączy się z backendem:**
- Sprawdź czy backend działa na porcie 8000
- Sprawdź `VITE_RAG_API_URL` w `.env.local`
- Sprawdź CORS w konsoli przeglądarki (F12)

**Błąd CORS:**
- Upewnij się, że backend ma poprawnie skonfigurowany CORS
- Dla AI Studio użyj tunelu Cloudflare

