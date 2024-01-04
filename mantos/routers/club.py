from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from mantos.database import get_session
from mantos.models import Club
from mantos.schemas import ClubPublic, ClubSchema

router = APIRouter(prefix='/clubs', tags=['clubs'])

Session = Annotated[Session, Depends(get_session)]


@router.post('/', status_code=201, response_model=ClubPublic)
def create_club(club: ClubSchema, session: Session):
    db_club = session.scalar(select(Club).where(Club.name == club.name))

    if db_club:
        raise HTTPException(status_code=400, detail='club already exists')

    db_club = Club(name=club.name, country=club.country)

    session.add(db_club)
    session.commit()
    session.refresh(db_club)

    return db_club
