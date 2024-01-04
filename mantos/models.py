import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, String, func, types, text
from sqlalchemy.dialects.postgresql import UUID
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

    id: Mapped[uuid.UUID] = mapped_column(
        types.Uuid,
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    name: Mapped[str] = mapped_column(String(60))
    country: Mapped[str] = mapped_column(String(60))
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(insert_default=func.now(), onupdate=func.now())
