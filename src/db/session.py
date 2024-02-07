from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(url=SQLALCHEMY_DATABASE_URL, echo=True)
session_pool = sessionmaker(bind=engine, autocommit=False)


def get_db() -> Generator:
    try:
        db = session_pool()
        yield db
    finally:
        db.close()
