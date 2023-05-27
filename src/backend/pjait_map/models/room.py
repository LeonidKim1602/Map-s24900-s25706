from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .registry import mapper_registry


@mapper_registry.mapped_as_dataclass
class Room:
    __tablename__ = 'Room'

    id: Mapped[int] = mapped_column('RoomId', primary_key=True)
    name: Mapped[str] = mapped_column('RoomName')

    location_id: Mapped[int] = mapped_column(ForeignKey('Location.LocationId'))
    location: Mapped['Location'] = relationship(back_populates='Location')

    schedules: Mapped[list['Schedule']] = relationship(
        back_populates='Schedule', default_factory=lambda: []
    )

@mapper_registry.mapped_as_dataclass
class Location:
    __tablename__ = 'Location'

    id: Mapped[int] = mapped_column('LocationId', primary_key=True)
    x: Mapped[int] = mapped_column('X')
    y: Mapped[int] = mapped_column('Y')

    file_id: Mapped[int] = mapped_column(ForeignKey('File.FileId'))
    file: Mapped['File'] = relationship(back_populates='File')

    rooms: Mapped[list['Room']] = relationship(
        back_populates='Room', default_factory=lambda: []
    )

@mapper_registry.mapped_as_dataclass
class File:
    __tablename__ = 'File'

    id: Mapped[int] = mapped_column('FileId', primaty_key=True)
    name: Mapped[str] = mapped_column('Filename')

    locations: Mapped[list['Location']] = relationship(
        back_populates='Location', default_factory=lambda: []
    )
