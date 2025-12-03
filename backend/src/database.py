from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv
import os

load_dotenv()

# Constitution requires Neon Serverless Postgres
# Fallback to DATABASE_URL for local development with SQLite
DATABASE_URL = os.getenv("NEON_DATABASE_URL") or os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "No database URL found! Please set NEON_DATABASE_URL for production "
        "or DATABASE_URL for local development in your .env file."
    )

# Neon requires specific connection pool settings for serverless
engine_kwargs = {"echo": False}

if "neon.tech" in DATABASE_URL or "postgresql://" in DATABASE_URL:
    # Neon Serverless Postgres configuration
    engine_kwargs.update({
        "poolclass": NullPool,  # Serverless doesn't need connection pooling
        "connect_args": {
            "connect_timeout": 10,
            "options": "-c timezone=utc"
        }
    })
else:
    # SQLite or other databases
    if DATABASE_URL.startswith("sqlite"):
        engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
