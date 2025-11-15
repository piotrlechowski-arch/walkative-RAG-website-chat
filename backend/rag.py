"""Logika RAG - wyszukiwanie semantyczne i generowanie odpowiedzi."""

import google.generativeai as genai
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from typing import List, Dict
from .database import get_db_connection
from .models import SearchResult

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = "text-embedding-004"
CHAT_MODEL = "gemini-2.5-flash"

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

def generate_query_embedding(query: str) -> List[float]:
    """Generuje embedding dla zapytania użytkownika."""
    result = genai.embed_content(
        model=MODEL_NAME,
        content=query,
        task_type="RETRIEVAL_QUERY"
    )
    return result['embedding']

def get_all_embedding_columns(conn) -> List[Dict]:
    """Pobiera listę wszystkich kolumn z embeddingami."""
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    query = """
    SELECT 
        table_schema,
        table_name,
        column_name,
        REPLACE(column_name, '_embedding', '') as original_column
    FROM information_schema.columns
    WHERE table_schema = 'main'
      AND column_name LIKE '%_embedding'
      AND data_type = 'USER-DEFINED'
    ORDER BY table_name, column_name;
    """
    
    cur.execute(query)
    return cur.fetchall()

def get_id_column(conn, schema: str, table: str) -> str:
    """Znajduje kolumnę ID dla danej tabeli."""
    cur = conn.cursor()
    
    # Spróbuj 'id'
    query = """
    SELECT column_name 
    FROM information_schema.columns
    WHERE table_schema = %s 
      AND table_name = %s 
      AND column_name = 'id'
    LIMIT 1;
    """
    cur.execute(query, (schema, table))
    result = cur.fetchone()
    
    if result:
        return result[0]
    
    # Spróbuj 'uuid' lub pierwszą kolumnę z '_id'
    query = """
    SELECT column_name 
    FROM information_schema.columns
    WHERE table_schema = %s 
      AND table_name = %s 
      AND (column_name = 'uuid' OR column_name LIKE '%_id')
    ORDER BY ordinal_position
    LIMIT 1;
    """
    cur.execute(query, (schema, table))
    result = cur.fetchone()
    
    if result:
        return result[0]
    
    # Fallback - pierwsza kolumna
    query = """
    SELECT column_name 
    FROM information_schema.columns
    WHERE table_schema = %s 
      AND table_name = %s 
    ORDER BY ordinal_position
    LIMIT 1;
    """
    cur.execute(query, (schema, table))
    result = cur.fetchone()
    
    return result[0] if result else 'id'

def search_similar_content(query: str, limit: int = 5) -> List[SearchResult]:
    """
    Wyszukuje podobne treści w bazie danych używając cosine similarity.
    
    Args:
        query: Tekst zapytania użytkownika
        limit: Maksymalna liczba wyników
    
    Returns:
        Lista wyników z metadanymi
    """
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY nie jest ustawiony")
    
    # Generuj embedding dla zapytania
    query_embedding = generate_query_embedding(query)
    
    conn = get_db_connection()
    all_results = []
    
    try:
        columns = get_all_embedding_columns(conn)
        
        for col_info in columns:
            schema = col_info['table_schema']
            table = col_info['table_name']
            embedding_column = col_info['column_name']
            original_column = col_info['original_column']
            
            id_column = get_id_column(conn, schema, table)
            
            # Zapytanie SQL z cosine distance
            # Konwertuj embedding do formatu PostgreSQL array
            embedding_str = '[' + ','.join(map(str, query_embedding)) + ']'
            
            search_query = f'''
            SELECT 
                "{original_column}" as text,
                '{table}' as table_name,
                '{original_column}' as column_name,
                "{id_column}"::text as record_id,
                1 - ("{embedding_column}" <=> %s::vector) as similarity
            FROM "{schema}"."{table}"
            WHERE "{embedding_column}" IS NOT NULL
              AND "{original_column}" IS NOT NULL
              AND "{original_column}" != ''
            ORDER BY "{embedding_column}" <=> %s::vector
            LIMIT %s;
            '''
            
            cur = conn.cursor()
            cur.execute(search_query, (embedding_str, embedding_str, limit * 2))
            
            for row in cur.fetchall():
                all_results.append(SearchResult(
                    text=row[0],
                    table=row[1],
                    column=row[2],
                    record_id=row[3],
                    similarity=float(row[4])
                ))
        
        # Sortuj wszystkie wyniki po podobieństwie i zwróć top-k
        all_results.sort(key=lambda x: x.similarity, reverse=True)
        return all_results[:limit]
        
    finally:
        conn.close()

def generate_rag_response(query: str, context_results: List[SearchResult]) -> str:
    """
    Generuje odpowiedź używając RAG - łączy kontekst z bazy z modelem językowym.
    
    Args:
        query: Pytanie użytkownika
        context_results: Lista podobnych fragmentów z bazy
    
    Returns:
        Odpowiedź wygenerowana przez model
    """
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY nie jest ustawiony")
    
    # Buduj kontekst z wyników wyszukiwania
    context_parts = []
    for i, result in enumerate(context_results, 1):
        context_parts.append(
            f"[Źródło {i} - {result.table}.{result.column}]:\n{result.text[:500]}..."
        )
    
    context = "\n\n".join(context_parts)
    
    # Prompt dla modelu (zgodny z AI Studio)
    prompt = f"""Jesteś pomocnym asystentem, który odpowiada na pytania użytkowników na podstawie dostarczonych fragmentów treści z witryny internetowej. Twoja odpowiedź musi być oparta wyłącznie na informacjach zawartych w tych fragmentach. Podaj zwięzłą i precyzyjną odpowiedź. Jeśli odpowiedź nie znajduje się w dostarczonym kontekście, odpowiedz: "Przepraszam, ale nie mogę znaleźć odpowiedzi na to pytanie w mojej bazie wiedzy."

KONTEKST:

{context}

PYTANIE UŻYTKOWNIKA:

{query}

ODPOWIEDŹ:

"""
    
    try:
        model = genai.GenerativeModel(CHAT_MODEL)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Błąd podczas generowania odpowiedzi: {str(e)}"

