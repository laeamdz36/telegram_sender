""" Module to define function to monitoring database data
    in order to calculate upcoming dates.
"""
import datetime as dt
from typing import Sequence
from sqlmodel import Session, select
import pandas as pd
from app.logger import logger
from app.countdowns.class_schemas import Personv2
import app.countdowns.rest_control as db


def compute_next_date() -> Sequence[Personv2]:
    """Get the next date to current date"""

    today = dt.datetime.today().date().strftime("%Y-%m-%d")
    logger.info("The date: %s", today)
    # read the database
    engine = db.get_engine()
    with Session(engine) as session:
        persons = session.exec(select(Personv2)).all()

    logger.info(persons)
    return persons


def create_df():
    """Create dataframe from sql results"""

    results = compute_next_date()
    df = pd.DataFrame(p.model_dump() for p in results)
    logger.info("The dataframe: %s", df)
