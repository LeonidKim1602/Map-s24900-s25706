from sqlalchemy.orm import Session

from models import Student
from schemas import CreateUser


def get_student(number: int, db: Session) -> Student | None:
    return db.get(Student, number)

def add_student(schema: CreateUser, db: Session) -> Student:
    number = int(schema.login[1:])
    student = Student(
        number=number,
        password=schema.password,
        name=schema.name,
        surname=schema.surname
    )

    db.add(student)
    db.commit()
    db.refresh(student)

    return student
