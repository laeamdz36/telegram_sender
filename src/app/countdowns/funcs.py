"""Module to the usage of countdowns"""
from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine
from app.countdowns.class_schemas import Person

DB_PATH = "/data"
DB_BIRTHDAYS = "birthdays.db"
DB_JSON_FILE = "databases.json"
DB_JSON_CONFIG = "databases"


def create_table(engine):
    """Creat table into the database"""

    SQLModel.metadata.create_all(engine)


def add_person(person: Person, engine):
    """Add person to database birthdays"""

    with Session(engine) as session:
        session.add(person)
        session.commit()


def get_databases() -> list[str]:
    """Return a list of databases"""

    data = ["databases.db"]
    return data
