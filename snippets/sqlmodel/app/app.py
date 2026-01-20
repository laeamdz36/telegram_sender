"""Test application to working with fast api async DB"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from schemas import Person


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup logic"""

    # create databases

app = FastAPI(lifespan=lifespan)
