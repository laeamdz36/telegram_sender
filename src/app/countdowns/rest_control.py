"""Module to handle resquests to database"""

from pathlib import Path
from datetime import date
from sqlmodel import SQLModel, create_engine, Session
import app.countdowns.funcs as dbs
from app.countdowns.class_schemas import Person
from app.logger import logger


def _bd_url():
    """Return tha url to the database"""

    # get db_name
    db = dbs.get_databases()[0]
    # get the db path
    db_path = Path(__file__).resolve()
    logger.info(f"Path resolved: {db_path}")
    for path in db_path.parents:
        if "app" in path.name:
            logger.info(f"app in path.name: {path}")
            db_path = path.joinpath("data").joinpath(db)
            break
    logger.info(f"Database in: {db_path}")
    db_url = f"sqlite:///{db_path}"
    return db_url


def create_tables():
    """Create tables in the database"""

    # get the db url
    db_url = _bd_url()
    # create dummy data
    engine = create_engine(db_url)
    p1 = Person(name="Luis",
                second_name="Luis",
                last_name="Mendez",
                birth_date=date(2025, 7, 24))
    with Session(engine) as session:
        session.add(p1)
        session.commit()
        session.refresh(p1)


def get_engine():
    """Get the instance engine for the database"""

    db_url = _bd_url()
    engine = create_engine(db_url, echo=False, connect_args={
                           "check_same_thread": False})
    return engine


def mod_init():
    """Initialize all stubs for countdows"""

    db_url = _bd_url()
    # Init the database, create if not exists
    engine = create_engine(db_url, echo=False, connect_args={
                           "check_same_thread": False})
    SQLModel.metadata.create_all(engine)
