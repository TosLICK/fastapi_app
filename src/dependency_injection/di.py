from typing import Any, Generator, Annotated
from fastapi import Depends
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.repository.sightseeings_repository import SightseeingRepository
from src.configuration.config import AppConfig

configuration: AppConfig | None = None

def get_configuration() -> AppConfig:  # Singleton pattern for global configuration
    global configuration
    if configuration is None:
        configuration = AppConfig()
    return configuration

engine: Engine | None = None

def get_engine(config: Annotated[AppConfig, Depends(get_configuration)]) -> Engine:  # Singleton pattern for global engine
    global engine
    if engine is None:
        engine = create_engine(config.connection_string, echo=True)
    return engine

session_factory: sessionmaker[Session] | None = None

def get_session_factory(engine: Annotated[Engine, Depends(get_engine)]) -> sessionmaker[Session]:  # Singleton pattern for global session factory
    global session_factory
    if session_factory is None:
        session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return session_factory

def get_db_session(session_factory: Annotated[sessionmaker[Session], Depends(get_session_factory)]) -> Generator[Session, Any, None]:  # Transient session
    db = session_factory()
    try:
        yield db
    finally:
        db.close()

def get_sightseeing_repository(db: Annotated[Session, Depends(get_db_session)]) -> SightseeingRepository:  # Transient repository
    return SightseeingRepository(db)
