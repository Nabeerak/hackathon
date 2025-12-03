#!/usr/bin/env python
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

try:
    DATABASE_URL = os.getenv("NEON_DATABASE_URL")
    print(f"[INFO] Database URL: {DATABASE_URL[:50]}...")

    engine = create_engine(DATABASE_URL)
    print("[OK] Engine created successfully")

    # Test connection
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version()"))
        version = result.scalar()
        print(f"[OK] PostgreSQL version: {version}")

    # Check if tables exist
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """))
        tables = [row[0] for row in result]
        print(f"[OK] Tables: {tables}")

except Exception as e:
    print(f"[ERROR] {type(e).__name__}: {e}")
