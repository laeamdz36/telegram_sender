""" Module to define function to monitoring database data
    in order to calculate upcoming dates.
"""
import datetime as dt
import asyncio
from typing import Sequence
from sqlmodel import Session, select
from sqlmodel.ext.asyncio.session import AsyncSession
import pandas as pd
import numpy as np
from app.logger import logger
from app.countdowns.class_schemas import Personv2
import app.countdowns.rest_control as db


async def build_dataframe():
    """Return the dataframe with all data"""

    data = None
    df = None
    async with AsyncSession(db.engine) as session:
        result = await session.exec(select(Personv2))
        persons = result.all()
        if persons:
            data = [p.model_dump() for p in persons]
    if data:
        df = await asyncio.to_thread(pd.DataFrame, data)
    return df


def date_categorize(df: pd.DataFrame):
    """Label definition for dates"""

    conditions = [
        df["days_to_go"] < 0,
        df["days_to_go"] == 0,
        df["days_to_go"] > 0,
    ]

    options = ["Passed", "Today", "Upcoming"]

    df["state"] = np.select(conditions, options)


async def compute_next_date() -> Sequence[Personv2]:
    """Get the next date to current date"""

    # Get the current date
    # today = dt.datetime.today().date()
    today = pd.Timestamp.now().normalize()
    logger.info("The date: %s", today)
    # get data from persons as datafra,e
    df = await build_dataframe()
    if df is not None:
        df["birth_date"] = pd.to_datetime(df["birth_date"])
        df["this_year"] = df['birth_date'].apply(
            lambda x: x.replace(year=today.year))
        df["days_to_go"] = (df["this_year"] - today).dt.days
        logger.info(df)
    else:
        logger.info("DATABASE EMPTY")
