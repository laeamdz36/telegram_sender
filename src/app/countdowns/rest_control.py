"""Module to handle resquests to database"""

from pathlib import Path
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
import app.countdowns.funcs as dbs
from app.countdowns.class_schemas import Personv2
from app.logger import logger


def _db_url():
    """Return tha url to the database"""

    # get db_name
    db = dbs.get_databases()[0]
    # get the db path
    db_path = Path(__file__).resolve()
    logger.info("Path resolved: %s", db_path)
    for path in db_path.parents:
        if "app" in path.name:
            logger.info("app in path.name: %s", path)
            db_path = path.joinpath("data").joinpath(db)
            break
    logger.info("Database in: %s", db_path)
    db_url = f"sqlite+aiosqlite:///{db_path}"
    return db_url


# Create the global engine for the database
# engine = create_engine(_db_url(), echo=False, connect_args={
#     "check_same_thread": False})
engine = create_async_engine(_db_url(), echo=False)


async def create_db():
    """Create database"""

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


@asynccontextmanager
async def get_session(commit: bool = True):
    """Get the session to the current working database"""

    async with AsyncSession(engine) as session:
        try:
            yield session
            if commit:
                await session.commit()
        except Exception:
            await session.rollback()
            raise


async def get_session_dep(commit: bool = True) -> AsyncGenerator[AsyncSession, None]:
    """Return AsyncSession for FastApi dependency"""

    async with AsyncSession(engine) as session:
        try:
            yield session
            if commit:
                await session.commit()
        except Exception:
            await session.rollback()
            raise


async def insert_person(person: Personv2):
    """Insert a person record to the database"""

    async with get_session() as session:
        session.add(person)
        await session.flush()
        await session.refresh(person)
        return person


async def get_all_persons() -> list[Personv2]:
    """Get all persons from database"""

    async with get_session(commit=False) as session:
        result = await session.exec(select(Personv2))
        return result.all()
