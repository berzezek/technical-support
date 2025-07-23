from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import config
from src.database.base import Base

engine = create_engine(config.get("DATABASE_URL"), echo=True, future=True)

SessionLocal = sessionmaker(bind=engine)

async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_all():
    with engine.begin() as conn:
        Base.metadata.create_all(bind=conn)
