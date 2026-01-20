"""Testing SQL Model"""

from sqlmodel import Field, Session, SQLModel, create_engine

# Databases
test = "sqlite:///database.db"
birthdays = "sqlite:///birthdays.db"


class Hero(SQLModel, table=True):
    """Simple class to write in db"""
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int


hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson", age=50)
hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador", age=60)
hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

engine = create_engine("sqlite:///database.db")

SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    session.add(hero_1)
    session.add(hero_2)
    session.add(hero_3)
    session.commit()
