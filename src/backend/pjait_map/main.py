from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from pydantic import BaseModel

import crud
from dependencies import get_db
from models import Student

app = FastAPI()


class StudentSchema(BaseModel):
    number: int
    password: str
    name: str
    surname: str

def schema_from_model(model: Student) -> StudentSchema:
    return StudentSchema(
        number=model.number,
        password=model.password,
        name=model.name,
        surname=model.surname
    )

@app.get('/student/{number}')
async def read_students(number: int, db: Session = Depends(get_db)) -> StudentSchema | None:
    model = crud.get_student_by_number(number, db)
    return schema_from_model(model) if model is not None else None
