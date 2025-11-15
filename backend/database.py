"""Połączenie z bazą danych PostgreSQL."""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://Lechu1@localhost:5432/walkative_local")

def get_db_connection():
    """Tworzy połączenie z bazą danych."""
    return psycopg2.connect(DATABASE_URL)

