"""Testing wrote into database and read to dataframe"""

from datetime import date
from contextlib import contextmanager
import pandas as pd
from sqlmodel import Session, create_engine, SQLModel, select
from schemas import Person

DATABASE_NAME = "database_persons.db"


def get_url():
    """Create the url for this database"""

    url = f"sqlite:///{DATABASE_NAME}"
    return url


engine = create_engine(get_url(), connect_args={
    "check_same_thread": False})


@contextmanager
def get_session(commit: bool = True):
    """Get the session to the current working database"""

    session = Session(engine)
    try:
        yield session
        if commit:
            session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def create_db():
    """Create the database"""

    SQLModel.metadata.create_all(engine)


def insert_person(person: Person):
    """Insert a new person to database and use id inmediatelly"""

    with get_session() as session:
        session.add(person)
        session.flush()
        session.refresh(person)


def ins_person(person: Person):
    """Insert a new person to database and use id inmediatelly"""

    with get_session() as session:
        session.add(person)


def get_all_persons() -> pd.DataFrame:
    """Get all data from db"""

    result = None
    with get_session(commit=False) as session:
        result = session.exec(select(Person)).all()
        rows = [p.model_dump() for p in result]
        df = pd.DataFrame.from_records(rows)
    return df


if __name__ == "__main__":

    # create database
    create_db()
    # create records to insert to database
    person1 = Person(name="Luis",
                     second_name="Luis",
                     last_name="Mendez",
                     birth_date=date(1990, 7, 24))
    # insert to database
    ins_person(person1)
    print("Inserted person to db")
    df_persons = get_all_persons()
    print(df_persons)
