#!/usr/bin/env python3
"""
Skrypt do generowania embeddingów dla wszystkich kolumn tekstowych w bazie danych.
Używa Google Gemini API (text-embedding-004) do generowania wektorów.
"""

import os
import psycopg2
import google.generativeai as genai
from dotenv import load_dotenv
import time

load_dotenv()

# Konfiguracja
DB_CONN_STRING = os.getenv("DATABASE_URL", "postgresql://Lechu1@localhost:5432/walkative_local")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = "text-embedding-004"

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY nie jest ustawiony w pliku .env")

genai.configure(api_key=GOOGLE_API_KEY)

def get_columns_to_process(conn):
    """Pobiera listę wszystkich kolumn z embeddingami do przetworzenia."""
    cur = conn.cursor()
    
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

def get_rows_without_embeddings(conn, schema, table, original_column, embedding_column):
    """Pobiera rekordy bez embeddingów."""
    cur = conn.cursor()
    
    # Pobierz kolumnę ID (zakładamy że pierwsza kolumna to id)
    id_query = f"""
    SELECT column_name 
    FROM information_schema.columns
    WHERE table_schema = %s 
      AND table_name = %s 
      AND column_name = 'id'
    LIMIT 1;
    """
    cur.execute(id_query, (schema, table))
    id_result = cur.fetchone()
    
    if not id_result:
        # Spróbuj uuid
        id_query = f"""
        SELECT column_name 
        FROM information_schema.columns
        WHERE table_schema = %s 
          AND table_name = %s 
          AND (column_name = 'uuid' OR column_name LIKE '%_id')
        ORDER BY ordinal_position
        LIMIT 1;
        """
        cur.execute(id_query, (schema, table))
        id_result = cur.fetchone()
    
    if not id_result:
        return []
    
    id_column = id_result[0]
    
    # Pobierz rekordy bez embeddingów
    select_query = f'''
    SELECT "{id_column}", "{original_column}"
    FROM "{schema}"."{table}"
    WHERE "{original_column}" IS NOT NULL 
      AND "{original_column}" != ''
      AND "{embedding_column}" IS NULL
    LIMIT 1000;
    '''
    
    cur.execute(select_query)
    return cur.fetchall(), id_column

def generate_embedding(content):
    """Generuje embedding dla danego tekstu."""
    try:
        result = genai.embed_content(
            model=MODEL_NAME,
            content=content,
            task_type="RETRIEVAL_DOCUMENT"
        )
        return result['embedding']
    except Exception as e:
        print(f"    ✗ Błąd generowania embeddingu: {e}")
        return None

def update_embedding(conn, schema, table, id_column, record_id, embedding_column, embedding):
    """Aktualizuje embedding w bazie danych."""
    cur = conn.cursor()
    update_query = f'''
    UPDATE "{schema}"."{table}"
    SET "{embedding_column}" = %s
    WHERE "{id_column}" = %s;
    '''
    cur.execute(update_query, (embedding, record_id))
    conn.commit()

def process_column(conn, schema, table, original_column, embedding_column):
    """Przetwarza wszystkie rekordy dla danej kolumny."""
    print(f"\nPrzetwarzanie: {schema}.{table}.{original_column}")
    
    rows, id_column = get_rows_without_embeddings(conn, schema, table, original_column, embedding_column)
    
    if not rows:
        print(f"  ✓ Brak rekordów do przetworzenia")
        return 0, 0
    
    print(f"  Znaleziono {len(rows)} rekordów do przetworzenia")
    
    processed = 0
    errors = 0
    
    for record_id, content in rows:
        if not content or not content.strip():
            continue
        
        # Ograniczenie długości tekstu (max ~8000 tokenów dla embedding)
        if len(content) > 20000:
            content = content[:20000]
        
        embedding = generate_embedding(content)
        
        if embedding:
            try:
                update_embedding(conn, schema, table, id_column, record_id, embedding_column, embedding)
                processed += 1
                if processed % 10 == 0:
                    print(f"  Przetworzono {processed}/{len(rows)} rekordów...")
            except Exception as e:
                print(f"    ✗ Błąd zapisu dla ID {record_id}: {e}")
                errors += 1
        else:
            errors += 1
        
        # Małe opóźnienie, żeby nie przeciążać API
        time.sleep(0.1)
    
    print(f"  ✓ Zakończono: {processed} przetworzonych, {errors} błędów")
    return processed, errors

def main():
    print("Łączenie z bazą danych...")
    conn = psycopg2.connect(DB_CONN_STRING)
    
    try:
        print("Wykrywanie kolumn do przetworzenia...")
        columns = get_columns_to_process(conn)
        
        if not columns:
            print("Nie znaleziono kolumn z embeddingami.")
            return
        
        print(f"Znaleziono {len(columns)} kolumn do przetworzenia.\n")
        
        total_processed = 0
        total_errors = 0
        
        for schema, table, embedding_column, original_column in columns:
            processed, errors = process_column(conn, schema, table, original_column, embedding_column)
            total_processed += processed
            total_errors += errors
        
        print(f"\n{'='*60}")
        print(f"✓ Zakończono przetwarzanie wszystkich kolumn")
        print(f"  Przetworzono: {total_processed} rekordów")
        print(f"  Błędy: {total_errors}")
        print(f"{'='*60}")
        
    finally:
        conn.close()
        print("\nPołączenie z bazą danych zostało zamknięte.")

if __name__ == "__main__":
    main()

