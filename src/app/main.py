"""Aplication to send notifications to telegram."""
import asyncio
import datetime as dt
from typing import List
from pathlib import Path
from functools import lru_cache
from fastapi import FastAPI, BackgroundTasks, Depends
from fastapi import Request
from sqlmodel import Session, select
from contextlib import asynccontextmanager
from telegram import Bot
from pydantic_settings import BaseSettings, SettingsConfigDict
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pydantic import BaseModel, ValidationError, Field
from app.weather import request_file
from app.dates_infos import get_message
from app.phrase_otd.phrase_main import requester, format_data
from app.countdowns import rest_control as ctd
from app.countdowns.class_schemas import Person, Personv2, PersonCreate, PersonBase
from app.logger import logger
from app.countdowns.checkers import compute_next_date

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE_PATH = BASE_DIR / ".env"
logger.info("Starting APP")
# logger.addHandler(logging.StreamHandler())
# log_uv_err = logging.getLogger("uvicorn.error")

logger.info("APP instantiation DONE!")

scheduler = AsyncIOScheduler()


class Settings(BaseSettings):
    """Settings to load env file"""
    token: str | None = Field(default=None)
    chatid_local: str | None = Field(default=None)
    chatid_projectIzta: str | None = Field(default=None)
    chatid_grafanaNotify: str | None = Field(default=None)
    chatid_devChannel: str | None = Field(default=None)
    storm_key: str | None = Field(default=None)

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        extra='allow'
    )


class SensorReport(BaseModel):
    """Define the innser structure of the message"""

    message: str  # relevant data to nitify drom ignition
    Room: str  # data for sensor in room
    LivingRoom: str  # data for sensor in living room


class InMessage(BaseModel):
    """Simple message validation"""

    text: str


class CurrentTimeResponse(BaseModel):
    """Schema for the current system time response"""
    status: str
    current_time: str


@lru_cache()
def get_settings():
    """Init settings"""
    try:
        settings = Settings()
    except ValidationError as e:
        print(f"Key error on env file - {e}")
        settings = None
    return settings


async def pub_dev_logger():
    """Developmernt test scheduler"""

    logger.info("***** Live string schduler *****")


async def execute_date_computes():
    """Execute date monitoring for upcoming dates"""

    compute_next_date()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle the start and stop of scheduler of APScheduler"""

    # Initializing scheduler
    logger.info("Printing form starting")
    # log_uv_err.info("Starting app lifespan")
    # log_uv_err.info("Adding job to APSchedule - %s", "pub_logger_dev")
    logger.info("Adding Scheduler job to APSchedule")
    scheduler.add_job(execute_date_computes, "interval", seconds=5)
    # scheduler.add_job(pub_logger_dev, "interval", seconds=5)

    # init databases
    logger.info("Starting database")
    ctd.mod_init()

    scheduler.start()
    # Code up to yield is executed while server is running
    yield
    # Code after yield is executed when server is closed
    logger.info("Stopping APScheduler...")
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)


@app.get("/db")
def register_form(request: Request):
    """Dev"""
    return "Hello"


def get_db_session():
    """Get the session to the database"""
    engine = ctd.get_engine()
    with Session(engine) as session:
        yield session


@app.post("/dev_db/person", response_model=Person)
def insert_person(person_data: PersonCreate, session: Session = Depends(get_db_session)):
    """Insert person in the database"""

    pserson_db = Personv2.model_validate(person_data)
    session.add(pserson_db)
    session.commit()
    session.refresh(pserson_db)
    return pserson_db


@app.get("/dev_db/persons", response_model=List[Person])
def read_persons(session: Session = Depends(get_db_session)):
    """Get all persons in the database"""
    persons = session.exec(select(Personv2)).all()
    return persons


async def send_message(text):
    """Send message with telegram bot"""

    settings = get_settings()
    if settings.token:
        bot = Bot(token=settings.token)
        async with bot:
            await bot.send_message(chat_id=settings.chatid_local, text=text, parse_mode="HTML")


async def send_tel_izta(msg):
    """Send message to telegram group"""

    settings = get_settings()
    if settings.token:
        bot = Bot(token=settings.token)
        async with bot:
            await bot.send_message(chat_id=settings.chatid_projectIzta, text=msg, parse_mode="HTML")


async def send_grafana_msg(msg: str = None):
    """Send a message to garfana channel"""

    settings = get_settings()
    if settings.token:
        bot = Bot(token=settings.token)
        chat_id = settings.chatid_grafanaNotify
        async with bot:
            await bot.send_message(chat_id=chat_id, text="TEST", parse_mode="HTML")


async def send_dev_channel(msg):
    """Send data to Dev Channel"""

    settings = get_settings()
    if settings.token:
        bot = Bot(token=settings.token)
        chat_id = settings.chatid_devChannel
        async with bot:
            await bot.send_message(chat_id=chat_id, text=msg, parse_mode="HTML")


async def weather_exec():
    """Call async funciton and return response"""

    result = await request_file()
    return result


@app.post("/send_message/")
async def send_msg(msg: SensorReport):
    """Send telegram for weather sensor data for home"""
    # insert datetime
    today = dt.datetime.now().strftime("%Y-%d-%m %H:%M:%S")
    text = msg.message + " " + today
    text += f"\nRoom: {msg.Room}"
    text += f"\nLiving Room: {msg.LivingRoom}"
    task_weather = asyncio.create_task(weather_exec())
    weather_forecast = await task_weather
    if weather_forecast:
        text += f"\n{weather_forecast}"
    text += f"\n{get_message()}"
    task = asyncio.create_task(send_message(text))
    await task


@app.post("/send_izta/")
async def notify_izta(msg: InMessage, background_task: BackgroundTasks):
    """Test chatid_local for telegram group"""

    task = asyncio.create_task(requester())
    phrase = await task
    if phrase is not None:
        phrase = format_data(phrase)
        msg = get_message()
        msg = f"{msg}\n" + phrase
    background_task.add_task(send_tel_izta, msg)
    return {"status": "ok"}


@app.post("/pub_chanel1/")
async def pub_channel1(msg: InMessage, background_task: BackgroundTasks):
    """Pub on chanel ID dev """

    settings = get_settings()
    chatid = settings.chatid_grafanaNotify
    background_task.add_task(send_grafana_msg)
    return {"status": "ok", "chatid": chatid}


@app.post("/pub_devChannel/")
async def pub_dev_channel(msg: InMessage, background_task: BackgroundTasks):
    """Pub on chanel ID dev """

    task = asyncio.create_task(requester())
    phrase = await task
    phrase = format_data(phrase)
    msg = get_message()
    msg = f"{msg}\n" + phrase
    background_task.add_task(send_dev_channel, msg)
    return {"status": "ok"}


@app.get("/utils/get_currentDatetimeSys", response_model=CurrentTimeResponse)
async def get_system_datetime():
    """Return the current dattiem in the system"""

    current_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"status": "ok", "current_time": current_time}


if __name__ == "__main__":
    print(ENV_FILE_PATH)
    try:
        settings = get_settings()
        print(settings.token)
        print(settings.chatid_local)
        print(settings.chatid_projectIzta)
    except ValidationError:
        print("Settings validation error")
