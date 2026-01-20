"""Definition for class for sql model schemas"""

from datetime import date
from typing import Optional
from sqlmodel import Field, SQLModel


class Person(SQLModel, table=True):
    """Schema for person definition to Database"""
    id: int | None = Field(default=None, primary_key=True)
    name: str
    second_name: str | None = Field(default=None)
    last_name: str
    birth_date: date
    relationship: str


class PersonBase(SQLModel):
    """Schema for data validation from clients over endpoints"""
    name: str
    second_name: str
    last_name: str
    birth_date: date
    relationship: str


class Personv2(PersonBase, table=True):
    """Schema for person definition to Database"""
    id: Optional[int] = Field(default=None, primary_key=True)


class PersonCreate(PersonBase):
    """Schema for inputs"""
    pass
