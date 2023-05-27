from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import Session
from sqlalchemy.sql import Insert, Update

from models import Schedule
from schemas import ClassInfo, ClassUpdate


def get_schedules_by_student(student_id: int, db: Session) -> list[Schedule]:
    return list(db.scalars(select(Schedule).where(Schedule.student == student_id)))

def add_schedule_stmt(**values) -> Insert[Schedule]:
    return insert(Schedule).values(values)

def to_seconds(weekday: int, hours: int, minutes: int) -> int:
    return weekday * 24 * 60 * 60 + hours * 60 * 60 + minutes * 60

def add_schedule(data: ClassInfo, student: int, db: Session) -> None:
    start_hours, start_minutes = map(int, data.start.split(':'))
    end_hours, end_minutes = map(int, data.end.split(':'))

    insert_values = {
        'start': to_seconds(data.weekday, start_hours, start_minutes),
        'end': to_seconds(data.weekday, end_hours, end_minutes),
        'student_id': student,
        'subject_id': data.subject_id,
        'room_id': data.room_id
    }

    db.execute(add_schedule_stmt(**insert_values))
    db.commit()

def update_schedule_stmt(schedule_id: int, **values) -> Update[Schedule]:
    return update(Schedule).where(Schedule.id == schedule_id).values(values)

def update_schedule(data: ClassUpdate, db: Session) -> None:
    start_hours, start_minutes = map(int, data.data.start.split(':'))
    end_hours, end_minutes = map(int, data.data.end.split(':'))

    update_values = {
        'start': to_seconds(data.data.weekday, start_hours, start_minutes),
        'end': to_seconds(data.data.weekday, end_hours, end_minutes),
        'subject_id': data.data.subject_id,
        'room_id': data.data.room_id
    }

    db.execute(update_schedule_stmt(data.schedule_id, **update_values))
    db.commit()

def delete_schedule(schedule_id: int, db: Session) -> None:
    stmt = delete(Schedule).where(Schedule.id == schedule_id)
    db.execute(stmt)
    db.commit()
