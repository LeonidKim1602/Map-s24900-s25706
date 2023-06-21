from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

import crud
from dependencies import DatabaseManager
from pjait_map_common.schemas import User, CreateUser


router = APIRouter(prefix="/student", dependencies=[Depends(DatabaseManager.get_db)])


@router.post("/")
async def get_student(
    user: User, db: Session = Depends(DatabaseManager.get_db)
) -> Response:
    student = crud.get_student(user.number, db)

    if student is None:
        return Response(status_code=404)

    if student.password != user.password:
        return Response(status_code=401)

    return Response(status_code=200)


@router.post("/new")
async def create_student(
    user: CreateUser, db: Session = Depends(DatabaseManager.get_db)
) -> Response:
    student = crud.get_student(user.number, db)
    if student is not None:
        return Response(status_code=403)

    crud.add_student(user, db)
    return Response(status_code=201)
