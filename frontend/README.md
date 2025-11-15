# Frontend - Walkative RAG Chat

Frontend aplikacji RAG do czatu z bazą wiedzy Walkative.

## Technologie

- React 19
- TypeScript
- Vite
- Tailwind CSS (via CDN)

## Instalacja

```bash
cd frontend
npm install
```

## Konfiguracja

1. Skopiuj plik `.env.example` do `.env.local`:
```bash
cp .env.example .env.local
```

2. Edytuj `.env.local` i ustaw:
   - `VITE_RAG_API_URL` - URL backendu (domyślnie: `http://127.0.0.1:8000/api/query`)
   - `GEMINI_API_KEY` - (opcjonalne) Klucz API Gemini jeśli potrzebny

## Uruchomienie

### Development lokalny

```bash
npm run dev
```

Aplikacja będzie dostępna pod adresem: `http://localhost:3000`

### Z AI Studio (Google Cloud)

Jeśli frontend działa w Google Cloud, użyj tunelu Cloudflare dla backendu:

1. Uruchom tunel w terminalu (w folderze głównym projektu):
```bash
cloudflared tunnel --url http://127.0.0.1:8000
```

2. Skopiuj wygenerowany URL (np. `https://xxxxx.trycloudflare.com`)

3. Ustaw w `.env.local`:
```bash
VITE_RAG_API_URL=https://xxxxx.trycloudflare.com/api/query
```

## Build

```bash
npm run build
```

## Struktura

```
frontend/
├── components/          # Komponenty React
│   ├── ChatInterface.tsx
│   ├── Message.tsx
│   ├── SourceCard.tsx
│   └── icons/          # Ikony
├── services/           # Serwisy API
│   └── ragService.ts   # Serwis do komunikacji z backendem
├── types.ts            # Definicje typów TypeScript
├── App.tsx             # Główny komponent
└── index.tsx           # Entry point

```

## Integracja z backendem

Frontend komunikuje się z backendem przez endpoint `/api/query`:

```typescript
POST /api/query
Content-Type: application/json

{
  "query": "jakie wycieczki mamy w krakowie"
}
```

Odpowiedź:
```json
{
  "answer": "...",
  "sources": [
    {
      "id": "...",
      "title": "...",
      "url": "#",
      "snippet": "..."
    }
  ]
}
```
