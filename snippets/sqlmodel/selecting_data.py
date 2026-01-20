"""Selecting data from database"""

from sqlmodel import Field, Session, SQLModel, create_engine, select
from dev_test import Hero


def read_data():
    """Read data from database test"""

    engine = create_engine("sqlite:///database.db")

    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Boy")
        hero = session.exec(statement).first()
        print(hero)


if __name__ == "__main__":
    read_data()
