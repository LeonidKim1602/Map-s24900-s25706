from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Room


def get_rooms(db: Session) -> list[Room]:
    return list(db.scalars(select(Room)))
