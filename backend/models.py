"""Modele Pydantic dla API."""

from pydantic import BaseModel
from typing import List, Optional

class SearchRequest(BaseModel):
    """Request do wyszukiwania semantycznego."""
    query: str
    limit: Optional[int] = 5

class SearchResult(BaseModel):
    """Pojedynczy wynik wyszukiwania."""
    text: str
    table: str
    column: str
    record_id: str
    similarity: float

class SearchResponse(BaseModel):
    """Odpowiedź z wynikami wyszukiwania."""
    results: List[SearchResult]
    query: str

class ChatRequest(BaseModel):
    """Request do czatu RAG."""
    query: str
    limit: Optional[int] = 5

class QueryRequest(BaseModel):
    """Request dla endpointu /api/query (kompatybilny z AI Studio)."""
    query: str

class ChatResponse(BaseModel):
    """Odpowiedź z czatu RAG."""
    answer: str
    context: List[SearchResult]
    query: str

class Source(BaseModel):
    """Źródło informacji dla odpowiedzi RAG."""
    id: str
    title: str
    url: str
    snippet: str

class QueryResponse(BaseModel):
    """Odpowiedź dla endpointu /api/query (kompatybilna z AI Studio)."""
    answer: str
    sources: List[Source]

