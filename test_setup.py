#!/usr/bin/env python3
"""Prosty skrypt testowy do weryfikacji konfiguracji."""

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_CONN_STRING = os.getenv("DATABASE_URL", "postgresql://Lechu1@localhost:5432/walkative_local")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

print("Test konfiguracji systemu RAG\n")
print("=" * 60)

# Test 1: Połączenie z bazą
print("1. Test połączenia z bazą danych...")
try:
    conn = psycopg2.connect(DB_CONN_STRING)
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()[0]
    print(f"   ✓ Połączono z PostgreSQL: {version[:50]}...")
    conn.close()
except Exception as e:
    print(f"   ✗ Błąd: {e}")
    exit(1)

# Test 2: Sprawdzenie pgvector
print("\n2. Test rozszerzenia pgvector...")
try:
    conn = psycopg2.connect(DB_CONN_STRING)
    cur = conn.cursor()
    cur.execute("SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';")
    result = cur.fetchone()
    if result:
        print(f"   ✓ pgvector zainstalowany: wersja {result[1]}")
    else:
        print("   ✗ pgvector nie jest zainstalowany")
        exit(1)
    conn.close()
except Exception as e:
    print(f"   ✗ Błąd: {e}")
    exit(1)

# Test 3: Sprawdzenie kolumn embedding
print("\n3. Test kolumn embedding...")
try:
    conn = psycopg2.connect(DB_CONN_STRING)
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) 
        FROM information_schema.columns
        WHERE table_schema = 'main'
          AND column_name LIKE '%_embedding'
          AND data_type = 'USER-DEFINED';
    """)
    count = cur.fetchone()[0]
    print(f"   ✓ Znaleziono {count} kolumn z embeddingami")
    conn.close()
except Exception as e:
    print(f"   ✗ Błąd: {e}")
    exit(1)

# Test 4: Sprawdzenie Google API Key
print("\n4. Test konfiguracji Google API...")
if GOOGLE_API_KEY and GOOGLE_API_KEY != "your_google_api_key_here":
    print(f"   ✓ GOOGLE_API_KEY jest ustawiony (długość: {len(GOOGLE_API_KEY)})")
else:
    print("   ⚠ GOOGLE_API_KEY nie jest ustawiony - ustaw go w pliku .env")

print("\n" + "=" * 60)
print("✓ Wszystkie testy podstawowe zakończone pomyślnie!")
print("\nNastępne kroki:")
print("1. Ustaw GOOGLE_API_KEY w pliku .env")
print("2. Uruchom: python generate_embeddings.py (aby wygenerować embeddingi)")
print("3. Uruchom: uvicorn backend.app:app --reload (aby uruchomić backend)")

