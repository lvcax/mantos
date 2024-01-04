from uuid import UUID

from pydantic import BaseModel


class Message(BaseModel):
    detail: str


class ClubSchema(BaseModel):
    name: str
    country: str


class ClubPublic(BaseModel):
    id: UUID
    name: str
    country: str


class ClubList(BaseModel):
    clubs: list[ClubPublic]
