from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.sql.schema import ForeignKey

from .registry import mapper_registry


@mapper_registry.mapped_as_dataclass
class Schedule:
    __tablename__ = 'Schedule'

    id: Mapped[int] = mapped_column('ScheduleId', primary_key=True)
    start: Mapped[int] = mapped_column('Start')
    end: Mapped[int] = mapped_column('End')

    student_id: Mapped[int] = mapped_column(ForeignKey('Student.StudentId'))
    student: Mapped['Student'] = relationship(back_populates='Student')

    subject_id: Mapped[int] = mapped_column(ForeignKey('Subject.SubjectId'))
    subject: Mapped['Subject'] = relationship(back_populates='Subject')

    room_id: Mapped[int] = mapped_column(ForeignKey('Room.RoomId'))
    room: Mapped['Room'] = relationship(back_populates='Room')
