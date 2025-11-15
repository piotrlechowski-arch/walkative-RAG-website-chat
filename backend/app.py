"""Główna aplikacja FastAPI dla systemu RAG."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import SearchRequest, SearchResponse, ChatRequest, ChatResponse, QueryRequest, QueryResponse, Source
from .rag import search_similar_content, generate_rag_response

app = FastAPI(
    title="Walkative RAG API",
    description="API do wyszukiwania semantycznego i RAG dla bazy walkative_local",
    version="1.0.0"
)

# Zezwól na żądania z Twojego frontendu (działającego na innym porcie)
# Lista dozwolonych źródeł - dodaj origin swojego frontendu jeśli nie ma go na liście
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8080",
    "https://aistudio.google.com",
    "https://generativelanguage.googleapis.com",
]

# Dodaj origin z Google Cloud Functions/App Engine (usercontent.goog)
# Używamy allow_origin_regex dla dynamicznych origins z Google
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.usercontent\.goog$",  # Dla wszystkich Google Cloud origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Endpoint główny - informacje o API."""
    return {
        "message": "Walkative RAG API",
        "version": "1.0.0",
        "endpoints": {
            "/search": "Wyszukiwanie semantyczne",
            "/chat": "Czat z RAG",
            "/docs": "Dokumentacja API (Swagger)"
        }
    }

@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """
    Wyszukiwanie semantyczne - zwraca podobne fragmenty z bazy danych.
    
    Args:
        request: Obiekt z zapytaniem i limitem wyników
    
    Returns:
        Lista najbardziej podobnych fragmentów z metadanymi
    """
    try:
        results = search_similar_content(request.query, request.limit)
        return SearchResponse(
            query=request.query,
            results=results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Czat z RAG - wyszukuje podobne fragmenty i generuje odpowiedź.
    
    Args:
        request: Obiekt z pytaniem użytkownika
    
    Returns:
        Odpowiedź wygenerowana przez model z kontekstem
    """
    try:
        # Wyszukaj podobne fragmenty
        context_results = search_similar_content(request.query, request.limit)
        
        # Generuj odpowiedź używając kontekstu
        answer = generate_rag_response(request.query, context_results)
        
        return ChatResponse(
            query=request.query,
            answer=answer,
            context=context_results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.post("/api/query", response_model=QueryResponse)
async def query_rag_endpoint(request: QueryRequest):
    """
    Endpoint RAG zgodny z AI Studio - obsługuje zapytania z frontendu.
    
    Args:
        request: Obiekt z zapytaniem użytkownika
    
    Returns:
        Odpowiedź z wygenerowaną odpowiedzią i źródłami
    """
    try:
        # Wyszukaj podobne fragmenty
        context_results = search_similar_content(request.query, limit=5)
        
        if not context_results:
            return QueryResponse(
                answer="Nie znalazłem żadnych informacji na ten temat w mojej bazie wiedzy.",
                sources=[]
            )
        
        # Generuj odpowiedź używając kontekstu
        answer = generate_rag_response(request.query, context_results)
        
        # Przygotuj źródła w formacie zgodnym z AI Studio
        sources = []
        for result in context_results:
            sources.append(Source(
                id=result.record_id,
                title=f"{result.table}.{result.column}",
                url="#",  # Możemy później dodać logikę do generowania URL
                snippet=result.text[:200] + "..." if len(result.text) > 200 else result.text
            ))
        
        return QueryResponse(
            answer=answer,
            sources=sources
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

