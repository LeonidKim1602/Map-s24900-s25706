from typing import Iterable

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

DB_URL = 'sqlite:///test.db'

engine = create_engine(DB_URL, connect_args={'check_same_thread': False})
connection = engine.connect()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Iterable[Session]:
    with SessionLocal() as db:
        yield db
