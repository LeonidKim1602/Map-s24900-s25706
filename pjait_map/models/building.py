from sqlalchemy.orm import Mapped, relationship, mapped_column

from .registry import mapper_registry


@mapper_registry.mapped_as_dataclass
class Building:
    __tablename__ = 'Building'

    id: Mapped[int] = mapped_column('BuildingId', primary_key=True)
    name: Mapped[str] = mapped_column('Name')
    
    floors: Mapped[list['Floor']] = relationship(
        back_populates='', default_factory=lambda: []
    )
