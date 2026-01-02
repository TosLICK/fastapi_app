from typing import Any, Generator, Annotated
from fastapi import Depends
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.repository.sightseeings_repository import SightseeingRepository
from src.configuration.config import ConfigData, ConfigReader

config_data: ConfigData | None = None

def get_configuration() -> ConfigData:  # Singleton pattern for global configuration
    global config_data
    if config_data is None:
        config_reader = ConfigReader()
        config_data = config_reader.read()
    return config_data

engine: Engine | None = None

def get_engine(config: Annotated[ConfigData, Depends(get_configuration)]) -> Engine:  # Singleton pattern for global engine
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
