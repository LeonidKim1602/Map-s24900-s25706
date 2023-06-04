from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from dependencies import DatabaseManager, issue_token
from schemas import User, CreateUser
import crud


router = APIRouter(prefix="/user", dependencies=[Depends(DatabaseManager.get_db)])


@router.post("/login")
async def login(data: User, db: Session = Depends(DatabaseManager.get_db)) -> Response:
    if not data.login.startswith("s"):
        return Response(status_code=400)

    try:
        number = int(data.login[1:])
    except ValueError:
        return Response(status_code=400)

    student = crud.get_student(number, db)

    if student is None or data.password != student.password:
        return Response(status_code=401)

    response = Response()

    token = issue_token(student.number)
    response.set_cookie(key="session", value=token, max_age=600, expires=600)

    return response


@router.post("/singup")
async def signup(
    data: CreateUser, db: Session = Depends(DatabaseManager.get_db)
) -> Response:
    if not data.login.startswith("s"):
        return Response(status_code=400)

    try:
        int(data.login[1:])
    except ValueError:
        return Response(status_code=400)

    student = crud.add_student(data, db)

    response = Response()

    token = issue_token(student.number)
    response.set_cookie(key="session", value=token, max_age=600, expires=600)

    return response
