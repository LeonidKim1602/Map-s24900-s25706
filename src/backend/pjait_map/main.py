from typing import Annotated

from fastapi import Cookie, Depends, FastAPI, Response
from sqlalchemy.orm import Session

import crud
from dependencies import get_db, issue_token, authenticate_user
from schemas import User, ClassInfo, ScheduleInfo


app = FastAPI()


@app.post('/login')
async def login_post(data: User, db: Session = Depends(get_db)) -> Response:
    if not data.login.startswith('s'):
        return Response(status_code=404)

    try:
        number = int(data.login[1:])
    except ValueError:
        return Response(status_code=404)

    student = crud.get_student(number, db)

    if student is None or data.password != student.password:
        return Response(status_code=404)

    response = Response()

    token = issue_token(student.number)
    response.set_cookie(key='session', value=token, max_age=600, expires=600)

    return response

@app.post('/schedule')
async def add_schedule(info: ClassInfo, auth_cookie: Annotated[str | None, Cookie()] = None, db: Session = Depends(get_db)) -> Response:
    if auth_cookie is None:
        return Response(status_code=401)

    student_id = authenticate_user(auth_cookie)

    if student_id is None:
        return Response(status_code=401)

    crud.add_schedule(info, student_id, db)

    return Response(status_code=201)

@app.put('/schedule')
async def update_schedule(data: ScheduleInfo, auth_cookie: Annotated[str | None, Cookie()] = None, db: Session = Depends(get_db)) -> Response:
    if auth_cookie is None:
        return Response(status_code=401)

    student_id = authenticate_user(auth_cookie)

    if student_id is None:
        return Response(status_code=401)

    student = crud.get_student(student_id, db)

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

    student_id = authenticate_user(auth_cookie)

    if student_id is None:
        return Response(status_code=401)

    student = crud.get_student(student_id, db)

    if student is None:
        return Response(status_code=401)

    schedule = crud.get_schedule(schedule_id, db)

    if schedule not in student.schedules:
        return Response(status_code=403)

    crud.delete_schedule(schedule_id, db)
    return Response(status_code=200)
