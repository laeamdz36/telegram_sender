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

    df["state"] = np.select(conditions, options, default="None")
    return df


def convert_to_this_year(df: pd.DataFrame):
    """Convert a date columnt year for current year"""

    today = pd.Timestamp.now().normalize()
    df["birth_date"] = pd.to_datetime(df["birth_date"])
    df["this_year"] = df['birth_date'].apply(
        lambda x: x.replace(year=today.year))
    df["days_to_go"] = (df["this_year"] - today).dt.days
    df["relationship"] = df["relationship"].astype(str)
    df["relationship"] = df['relationship'].apply(
        lambda x: x.lower())
    return df


def get_next_birthday(df: pd.DataFrame):
    """Extract from dataframe the more next birthday"""

    result = df.loc[df[df["days_to_go"] > 0]["days_to_go"].idxmin()]
    msg = "Next Birthday:\n"
    msg += f"Name: {result['name']} {result['last_name']}\n"
    msg += f"Days to go: {result['days_to_go']}\n"
    msg += f"Birthday: {result['birth_date']}"
    logger.info(msg)
    return msg


def get_next_birthday_family(df: pd.DataFrame):
    """Extract from dataframe the more next birthday"""

    result = df.loc[
        df[
            (df["days_to_go"] > 0) & (df["relationship"] == "family")]
        ["days_to_go"].idxmin()]
    msg = "Next Birthday:\n"
    msg += f"Name: {result['name']} {result['second_name']} {result['last_name']}\n"
    msg += f"Days to go: {result['days_to_go']}\n"
    msg += f"Birthday: {result['birth_date'].month_name()} / "
    msg += f"{result['birth_date'].day} - "
    msg += f"{result['birth_date'].day_name()}"
    logger.info(msg)
    return msg


def get_next_birthday_friends(df: pd.DataFrame):
    """Extract from dataframe the more next birthday"""

    result = df.loc[
        df[
            (df["days_to_go"] > 0) & (df["relationship"] == "friend")]
        ["days_to_go"].idxmin()]
    msg = "Next Birthday:\n"
    msg += f"Name: {result['name']} {result['second_name']} {result['last_name']}\n"
    msg += f"Days to go: {result['days_to_go']}\n"
    msg += f"Birthday: {result['birth_date'].month_name()} / "
    msg += f"{result['birth_date'].day} - "
    msg += f"{result['birth_date'].day_name()}"
    logger.info(msg)
    return msg


async def compute_next_date() -> Sequence[Personv2]:
    """Get the next date to current date"""

    # get data from persons as datafra,e
    df = await build_dataframe()
    if df is not None:
        # Accepted due to low rows records
        df = await asyncio.to_thread(convert_to_this_year, df)
        df = await asyncio.to_thread(date_categorize, df)
        logger.info(df)
        await asyncio.to_thread(get_next_birthday_family, df)
        await asyncio.to_thread(get_next_birthday_friends, df)
    else:
        logger.info("DATABASE EMPTY")


async def get_family_birthday():
    """Return a string with the next family birthday"""

    msg = None
    df = await build_dataframe()
    if df is not None:
        # Accepted due to low rows records
        df = await asyncio.to_thread(convert_to_this_year, df)
        df = await asyncio.to_thread(date_categorize, df)
        msg = await asyncio.to_thread(get_next_birthday_family, df)
    else:
        logger.info("DATABASE EMPTY")
    return msg


async def get_friend_birthday():
    """Return a string with the next family birthday"""

    msg = None
    df = await build_dataframe()
    if df is not None:
        # Accepted due to low rows records
        df = await asyncio.to_thread(convert_to_this_year, df)
        df = await asyncio.to_thread(date_categorize, df)
        msg = await asyncio.to_thread(get_next_birthday_friends, df)
    else:
        logger.info("DATABASE EMPTY")
    return msg
