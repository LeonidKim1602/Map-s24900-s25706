from fastapi import APIRouter, Depends, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

import crud
from dependencies import DatabaseManager, get_weekday, get_time
from pjait_map_common.schemas import Schedule, NewSchedule, ScheduleChange


router = APIRouter(prefix="/schedule", dependencies=[Depends(DatabaseManager.get_db)])


@router.get("/student/{student_id}")
async def get_schedule(
    student_id: int, db: Session = Depends(DatabaseManager.get_db)
) -> Response:
    student = crud.get_student(student_id, db)

    if student is None:
        return Response(status_code=404)

    schedules = [
        jsonable_encoder(
            Schedule(
                subject_id=s.subject_id,
                room_id=s.room_id,
                weekday=get_weekday(s.start),
                start=get_time(s.start),
                end=get_time(s.end),
            )
        )
        for s in student.schedules
    ]

    return JSONResponse(content=schedules)


@router.post("/")
async def add_schedule(
    data: NewSchedule, db: Session = Depends(DatabaseManager.get_db)
) -> Response:
    crud.add_schedule(data, db)
    return Response(status_code=201)


@router.put("/")
async def update_schedule(
    data: ScheduleChange, db: Session = Depends(DatabaseManager.get_db)
) -> Response:
    crud.update_schedule(data, db)
    return Response(status_code=201)


@router.delete("/{studend_id}/{schedule_id}")
async def delete_schedule(
    student_id: int, schedule_id: int, db: Session = Depends(DatabaseManager.get_db)
) -> Response:
    student = crud.get_student(student_id, db)

    if student is None:
        return Response(status_code=404)

    schedule = crud.get_schedule(schedule_id, db)

    if schedule not in student.schedules:
        return Response(status_code=404)

    crud.delete_schedule(schedule_id, db)
    return Response(status_code=200)
