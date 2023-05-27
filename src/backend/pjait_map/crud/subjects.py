from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Subject


def get_subjects(db: Session) -> list[Subject]:
    return list(db.scalars(select(Subject)))
