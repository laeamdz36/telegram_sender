""" Module to define function to monitoring database data
    in order to calculate upcoming dates.
"""
import datetime as dt
from sqlmodel import Session, select
from app.logger import logger
from app.countdowns.class_schemas import Personv2
import app.countdowns.rest_control as db


def compute_next_date():
    """Get the next date to current date"""

    today = dt.datetime.today().date().strftime("%Y-%m-%d")
    logger.info(f"The date: {today}")
    # read the database
    engine = db.get_engine()
    with Session(engine) as session:
        persons = session.exec(select(Personv2)).all()

    logger.info(persons)
