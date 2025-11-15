#!/usr/bin/env python3
"""
Skrypt do monitorowania postępu generowania embeddingów.
Pokazuje ile rekordów zostało zembedowanych i ile jeszcze pozostało.
"""

import psycopg2
import os
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv()

DB_CONN_STRING = os.getenv("DATABASE_URL", "postgresql://Lechu1@localhost:5432/walkative_local")

def get_embedding_stats():
    """Pobiera statystyki embeddingów dla wszystkich kolumn."""
    conn = psycopg2.connect(DB_CONN_STRING)
    cur = conn.cursor()
    
    # Pobierz wszystkie kolumny z embeddingami
    cur.execute("""
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
    """)
    
    columns = cur.fetchall()
    
    stats = []
    total_with = 0
    total_without = 0
    total_records = 0
    
    print("=" * 90)
    print("MONITOROWANIE POSTĘPU GENEROWANIA EMBEDDINGÓW")
    print("=" * 90)
    print()
    
    for schema, table, embedding_col, original_col in columns:
        # Sprawdź ile rekordów ma embeddingi
        query = f'''
        SELECT 
            COUNT(*) as total,
            COUNT("{embedding_col}") as with_embedding,
            COUNT(*) - COUNT("{embedding_col}") as without_embedding
        FROM "{schema}"."{table}"
        WHERE "{original_col}" IS NOT NULL 
          AND "{original_col}" != '';
        '''
        
        cur.execute(query)
        result = cur.fetchone()
        
        if result and result[0] > 0:
            total, with_emb, without_emb = result
            total_records += total
            total_with += with_emb
            total_without += without_emb
            
            percentage = (with_emb / total) * 100 if total > 0 else 0
            
            # Pokaż tylko kolumny z pozostałymi rekordami lub wszystkie jeśli mało kolumn
            if without_emb > 0 or len(columns) < 20:
                status = "✓" if without_emb == 0 else "⚠"
                print(f"{status} {schema}.{table}.{original_col}")
                print(f"   Zembedowane: {with_emb:,}/{total:,} ({percentage:.1f}%)")
                if without_emb > 0:
                    print(f"   Pozostało: {without_emb:,} rekordów")
                print()
            
            stats.append({
                'schema': schema,
                'table': table,
                'column': original_col,
                'total': total,
                'with_embedding': with_emb,
                'without_embedding': without_emb,
                'percentage': percentage
            })
    
    print("=" * 90)
    print("PODSUMOWANIE:")
    print("=" * 90)
    print(f"Łącznie rekordów do zembedowania: {total_records:,}")
    if total_records > 0:
        overall_percentage = (total_with / total_records) * 100
        print(f"✓ Zembedowane: {total_with:,} ({overall_percentage:.1f}%)")
        print(f"⚠ Pozostało: {total_without:,} ({100 - overall_percentage:.1f}%)")
        
        # Pokaż kolumny z największą liczbą pozostałych rekordów
        remaining_cols = [s for s in stats if s['without_embedding'] > 0]
        if remaining_cols:
            remaining_cols.sort(key=lambda x: x['without_embedding'], reverse=True)
            print()
            print("Top 5 kolumn z największą liczbą pozostałych rekordów:")
            for i, col in enumerate(remaining_cols[:5], 1):
                print(f"  {i}. {col['table']}.{col['column']}: {col['without_embedding']:,} rekordów")
    print("=" * 90)
    
    conn.close()
    return stats

if __name__ == "__main__":
    get_embedding_stats()

