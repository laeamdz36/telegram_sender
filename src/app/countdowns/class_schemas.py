"""Definition for class for sql model schemas"""

from datetime import date
from typing import Optional
from sqlmodel import Field, SQLModel


class Person(SQLModel, table=True):
    """Schema for person definition"""
    id: int | None = Field(default=None, primary_key=True)
    name: str
    second_name: str
    last_name: str
    birth_date: date


class PersonBase(SQLModel):
    """Schema for person definition"""
    name: str
    second_name: str
    last_name: str
    birth_date: date


class Personv2(PersonBase, table=True):
    """DB table, heritance from Base and add table"""
    id: Optional[int] = Field(default=None, primary_key=True)


class PersonCreate(PersonBase):
    """Schema for inputs"""
    pass
