from sqlalchemy import insert, select
from sqlalchemy.orm import Session
from sqlalchemy.sql import Insert

from models import Student
from schemas import SignupData


def get_student_by_number(number: int, db: Session) -> Student | None:
    return db.scalar(select(Student).where(Student.number == number))

def add_student_stmt(**kwarg) -> Insert[Student]:
    return insert(Student).values(kwarg)

def add_student(data: SignupData, db: Session) -> None:
    insert_values = {
        'number': data.login.login,
        'password': data.login.password,
        'name': data.name,
        'surname': data.surname
    }

    db.execute(add_student_stmt(**insert_values))
    db.commit()
