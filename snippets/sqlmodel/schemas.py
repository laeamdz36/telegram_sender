"""Definition of sechemas for database"""

from datetime import date
from sqlmodel import SQLModel, Field


class Person(SQLModel, table=True):
    """Schema for person definition"""
    id: int | None = Field(default=None, primary_key=True)
    name: str
    second_name: str
    last_name: str
    birth_date: date
