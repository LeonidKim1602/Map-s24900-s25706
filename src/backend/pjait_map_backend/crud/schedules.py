from sqlalchemy import delete
from sqlalchemy.orm import Session

from models import Schedule, Subject, Student, Room
from schemas import ClassInfo, ScheduleInfo


def to_seconds(weekday: int, hours: int, minutes: int) -> int:
    return weekday * 24 * 60 * 60 + hours * 60 * 60 + minutes * 60


def get_schedule(id: int, db: Session) -> Schedule | None:
    return db.get(Schedule, id)


def add_schedule(data: ClassInfo, student: int, db: Session) -> Schedule:
    start_hours, start_minutes = map(int, data.start.split(":"))
    end_hours, end_minutes = map(int, data.end.split(":"))

    start = to_seconds(data.weekday, start_hours, start_minutes)
    end = to_seconds(data.weekday, end_hours, end_minutes)

    schedule = Schedule(
        start=start,
        end=end,
        student_id=student,
        student=db.get(Student, student),
        subject_id=data.subject_id,
        subject=db.get(Subject, data.subject_id),
        room_id=data.room_id,
        room=db.get(Room, data.room_id),
    )

    db.add(schedule)
    db.commit()
    db.refresh(schedule)

    return schedule


def update_schedule(data: ScheduleInfo, db: Session) -> Schedule | None:
    start_hours, start_minutes = map(int, data.data.start.split(":"))
    end_hours, end_minutes = map(int, data.data.end.split(":"))

    start = to_seconds(data.data.weekday, start_hours, start_minutes)
    end = to_seconds(data.data.weekday, end_hours, end_minutes)

    schedule = db.get(Schedule, data.schedule_id)

    if schedule is None:
        return None

    schedule.start = start
    schedule.end = end
    schedule.subject_id = data.data.subject_id
    schedule.subject = db.get(Subject, data.data.subject_id)
    schedule.room_id = data.data.room_id
    schedule.room = db.get(Room, data.data.room_id)

    db.commit()

    return schedule


def delete_schedule(schedule_id: int, db: Session) -> None:
    stmt = delete(Schedule).where(Schedule.id == schedule_id)
    db.execute(stmt)
    db.commit()
