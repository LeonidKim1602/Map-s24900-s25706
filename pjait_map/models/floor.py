from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.sql.schema import ForeignKey

from .registry import mapper_registry


@mapper_registry.mapped_as_dataclass
class Floor:
    __tablename__ = 'Floor'

    id: Mapped[int] = mapped_column('FloorId', primary_key=True)
    floor: Mapped[int] = mapped_column('Floor')

    building_id: Mapped[int] = mapped_column(ForeignKey('Building.BuildingId'))
    building: Mapped['Building'] = relationship(back_populates='Building')

    rooms: Mapped[list['Room']] = relationship(
        back_populates='Room', default_factory=lambda: []
    )
