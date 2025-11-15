#!/usr/bin/env python3
"""
Skrypt do automatycznego wykrywania kolumn tekstowych i dodawania kolumn embedding.
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONN_STRING = os.getenv("DATABASE_URL", "postgresql://Lechu1@localhost:5432/walkative_local")

def get_text_columns(conn):
    """Wykrywa wszystkie kolumny typu text do embedowania."""
    cur = conn.cursor()
    
    query = """
    SELECT table_schema, table_name, column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = 'main'
      AND data_type = 'text'
      AND (
        column_name LIKE '%content%' 
        OR column_name LIKE '%description%' 
        OR column_name LIKE '%body%'
        OR column_name LIKE '%text%'
      )
    ORDER BY table_name, column_name;
    """
    
    cur.execute(query)
    return cur.fetchall()

def column_exists(conn, schema, table, column):
    """Sprawdza czy kolumna już istnieje."""
    cur = conn.cursor()
    query = """
    SELECT column_name 
    FROM information_schema.columns
    WHERE table_schema = %s 
      AND table_name = %s 
      AND column_name = %s;
    """
    cur.execute(query, (schema, table, column))
    return cur.fetchone() is not None

def add_embedding_column(conn, schema, table, column):
    """Dodaje kolumnę embedding dla danej kolumny tekstowej."""
    embedding_column = f"{column}_embedding"
    
    if column_exists(conn, schema, table, embedding_column):
        print(f"  ✓ Kolumna {schema}.{table}.{embedding_column} już istnieje")
        return False
    
    cur = conn.cursor()
    alter_query = f'ALTER TABLE "{schema}"."{table}" ADD COLUMN "{embedding_column}" vector(768);'
    
    try:
        cur.execute(alter_query)
        conn.commit()
        print(f"  ✓ Dodano kolumnę {schema}.{table}.{embedding_column}")
        return True
    except Exception as e:
        conn.rollback()
        print(f"  ✗ Błąd przy dodawaniu {schema}.{table}.{embedding_column}: {e}")
        return False

def main():
    print("Łączenie z bazą danych...")
    conn = psycopg2.connect(DB_CONN_STRING)
    
    try:
        print("\nWykrywanie kolumn tekstowych...")
        columns = get_text_columns(conn)
        
        if not columns:
            print("Nie znaleziono kolumn do przetworzenia.")
            return
        
        print(f"Znaleziono {len(columns)} kolumn do przetworzenia.\n")
        
        added_count = 0
        skipped_count = 0
        
        for schema, table, column, data_type in columns:
            print(f"Przetwarzanie: {schema}.{table}.{column}")
            if add_embedding_column(conn, schema, table, column):
                added_count += 1
            else:
                skipped_count += 1
        
        print(f"\n✓ Zakończono: dodano {added_count} kolumn, pominięto {skipped_count} kolumn")
        
    finally:
        conn.close()

if __name__ == "__main__":
    main()

