from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, Response
from sqlalchemy.orm import Session

import crud
from dependencies import get_db, authenticate_user
from schemas import ClassInfo, ScheduleInfo


router = APIRouter(
    prefix='/schedule',
    dependencies=[Depends(get_db)]
)

@router.post('/')
async def add_schedule(info: ClassInfo, auth_cookie: Annotated[str | None, Cookie()] = None, db: Session = Depends(get_db)) -> Response:
    if auth_cookie is None:
        return Response(status_code=401)

    student_id = authenticate_user(auth_cookie)

    if student_id is None:
        return Response(status_code=401)

    crud.add_schedule(info, student_id, db)

    return Response(status_code=201)

@router.put('/')
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

@router.delete('/{schedule_id}')
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
