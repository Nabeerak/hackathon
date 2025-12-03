from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("NEON_DATABASE_URL")
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    # Drop tables in correct order due to foreign keys
    conn.execute(text("DROP TABLE IF EXISTS messages CASCADE"))
    conn.execute(text("DROP TABLE IF EXISTS conversations CASCADE"))
    conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))
    conn.execute(text("DROP TABLE IF EXISTS alembic_version CASCADE"))
    conn.commit()
    print("All tables dropped successfully")
