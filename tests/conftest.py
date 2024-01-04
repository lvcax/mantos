import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from mantos.app import app
from mantos.database import get_session
from mantos.models import Base, Club
from mantos.settings import Settings


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(Settings().DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    with Session() as session:
        yield session
        session.rollback()

    Base.metadata.drop_all(engine)


@pytest.fixture
def club(session):
    club: Club = Club(name='Milan', country='Italy')

    session.add(club)
    session.commit()
    session.refresh(club)

    return club
