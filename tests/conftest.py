import sys
from pathlib import Path
# Ensure project root is on sys.path so 'src' imports work when running pytest
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from typing import Generator
from fastapi.testclient import TestClient

from src.database.models import Base
from src.repository.sightseeings_repository import SightseeingRepository
from src.dependency_injection import di as di_module
from src.main import app as fastapi_app

# In-memory SQLite for tests
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def engine() -> Generator[Engine, None, None]:
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    Base.metadata.create_all(bind=engine)
    try:
        yield engine
    finally:
        engine.dispose()

@pytest.fixture()
def db_session(engine: Engine) -> Generator[Session, None, None]:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture()
def repo(db_session: Session) -> SightseeingRepository:
    return SightseeingRepository(db_session)

@pytest.fixture()
def client(repo: SightseeingRepository) -> Generator[TestClient, None, None]:
    # Override the DI function that provides SightseeingRepository
    original = di_module.get_sightseeing_repository
    fastapi_app.dependency_overrides[di_module.get_sightseeing_repository] = lambda: repo
    client = TestClient(fastapi_app)
    yield client
    fastapi_app.dependency_overrides.pop(di_module.get_sightseeing_repository, None)
    di_module.get_sightseeing_repository = original
