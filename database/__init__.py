import os
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from config import database_url

db_dir = Path(__file__).parent.parent / "db"
os.makedirs(db_dir, exist_ok=True)

Base = declarative_base()

engine = create_async_engine(
    database_url,
    echo=True,
    connect_args={
        "check_same_thread": False
    }
)

SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)
