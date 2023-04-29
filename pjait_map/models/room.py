from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .registry import mapper_registry


@mapper_registry.mapped_as_dataclass
class Room:
    __tablename__ = 'Room'

    id: Mapped[int] = mapped_column('RoomId', primary_key=True)
    name: Mapped[str] = mapped_column('RoomName')

    floor_id: Mapped[int] = mapped_column(ForeignKey('Floor.FloorId'))
    floor: Mapped['Floor'] = relationship(back_populates='Floor')

    schedules: Mapped[list['Schedule']] = relationship(
        back_populates='Schedule', default_factory=lambda: []
    )
