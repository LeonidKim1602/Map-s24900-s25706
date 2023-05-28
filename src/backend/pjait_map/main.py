from typing import Annotated

from fastapi import Cookie, Depends, FastAPI, Response
from fastapi.responses import Response
from sqlalchemy.orm import Session
from pydantic import BaseModel

import crud
from dependencies import get_db
from models import Student
from schemas import LoginData, ClassInfo, ClassUpdate


app = FastAPI()

cookie_storage: dict[str, int] = {}


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

@app.post('/login')
async def login_post(data: LoginData, db: Session = Depends(get_db)) -> Response:
    if not data.login.startswith('s'):
        return Response(status_code=404)

    number = int(data.login[1:])
    student = crud.get_student_by_number(number, db)

    if student is None or data.password != student.password:
        return Response(status_code=404)

    response = Response()
    response.set_cookie(key='user', value=student.name) # Find a way to make session
    cookie_storage[student.name] = student.number
    return response

@app.post('/schedule')
async def add_schedule(info: ClassInfo, auth_cookie: Annotated[str | None, Cookie()] = None, db: Session = Depends(get_db)) -> Response:
    if auth_cookie is None:
        return Response(status_code=401)

    student_id = cookie_storage[auth_cookie]
    crud.add_schedule(info, student_id, db)
    return Response(status_code=201)

@app.put('/schedule')
async def update_schedule(data: ClassUpdate, auth_cookie: Annotated[str | None, Cookie()] = None, db: Session = Depends(get_db)) -> Response:
    if auth_cookie is None:
        return Response(status_code=401)

    student_id = cookie_storage[auth_cookie]
    student = crud.get_student_by_number(student_id, db)

    if student is None:
        return Response(status_code=401)

    schedule = crud.get_schedule(data.schedule_id, db)

    if schedule not in student.schedules:
        return Response(status_code=403)

    crud.update_schedule(data, db)
    return Response(status_code=201)

@app.delete('/schedule/{schedule_id}')
async def delete_schedule(schedule_id: int, auth_cookie: Annotated[str | None, Cookie()] = None, db: Session = Depends(get_db)) -> Response:
    if auth_cookie is None:
        return Response(status_code=401)

    student_id = cookie_storage[auth_cookie]
    student = crud.get_student_by_number(student_id, db)

    if student is None:
        return Response(status_code=401)

    schedule = crud.get_schedule(schedule_id, db)

    if schedule not in student.schedules:
        return Response(status_code=403)

    crud.delete_schedule(schedule_id, db)
    return Response(status_code=200)
