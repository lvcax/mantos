from datetime import datetime
from enum import Enum
from uuid import UUID

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class JerseyVersion(str, Enum):
    home = 'home'
    away = 'away'
    third = 'third'
    fourth = 'fourth'
    special = 'special'


class JerseyType(str, Enum):
    player = 'player'
    goalkeeper = 'goalkeeper'
    training = 'training'


class Club(Base):
    __tablename__ = 'clubs'

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    country: Mapped[str] = mapped_column(String(20))

    jerseys: Mapped[list['Jersey']] = relationship(
        back_populates='club', cascade='all, delete-orphan'
    )

    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(onupdate=func.now())


class Jersey(Base):
    __tablename__ = 'jerseys'

    id: Mapped[UUID] = mapped_column(primary_key=True)
    model_name: Mapped[str] = mapped_column(
        String(50)
    )
    model_year: Mapped[str] = mapped_column(String(4))
    version: Mapped[JerseyVersion]
    type: Mapped[JerseyType]
    supplier: Mapped[str] = mapped_column(String(20))
    club_id: Mapped[UUID] = mapped_column(ForeignKey('clubs.id'))

    club: Mapped[Club] = relationship(back_populates='clubs')

    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(onupdate=func.now())
