from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from mantos.database import get_session
from mantos.models import Club
from mantos.schemas import ClubList, ClubPublic, ClubSchema
from mantos.utils import search_country

router = APIRouter(prefix='/clubs', tags=['clubs'])

Session = Annotated[Session, Depends(get_session)]


@router.post('/', status_code=201, response_model=ClubPublic)
def create_club(club: ClubSchema, session: Session):
    db_club = session.scalar(select(Club).where(Club.name == club.name))

    if db_club:
        raise HTTPException(status_code=400, detail='club already exists')

    if not search_country(club.country):
        raise HTTPException(status_code=400, detail='invalid country name')

    db_club = Club(name=club.name, country=club.country)

    session.add(db_club)
    session.commit()
    session.refresh(db_club)

    return db_club


@router.get('/', status_code=200, response_model=ClubList)
def list_clubs(
    session: Session,
    name: str = Query(None),
    country: str = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
):
    query = select(Club)

    if name:
        query = query.filter(Club.name.contains(name))

    if country:
        if not search_country(country):
            raise HTTPException(status_code=400, detail='invalid country name')
        query = query.filter(Club.country.contains(country))

    clubs = session.scalars(query.offset(offset).limit(limit)).all()

    return {'clubs': clubs}
