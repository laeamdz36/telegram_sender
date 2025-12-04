"""Aplication to send notifications to telegram."""
import asyncio
import sys
import datetime as dt
from pathlib import Path
from functools import lru_cache
from fastapi import FastAPI, BackgroundTasks
from contextlib import asynccontextmanager
from telegram import Bot
import arrow
from pydantic_settings import BaseSettings, SettingsConfigDict
from app.weather import main_weather  # main async execution
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pydantic import BaseModel, ValidationError, Field
from app.load_config import load_config
import logging
from app.dates_infos import get_message
print(">>> EXECUTANDO app/main.py (PID)",
      __import__("os").getpid(), "stdout:", sys.stdout)
sys.stdout.flush()

logger = logging.getLogger("app_telebot")
logger.addHandler(logging.StreamHandler())
log_uv_err = logging.getLogger("uvicorn.error")

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
ENV_FILE_PATH = BASE_DIR / ".env"

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


@lru_cache()
def get_settings():
    """Init settings"""
    try:
        settings = Settings()
    except ValidationError as e:
        print(f"Key error on env file - {e}")
        settings = None
    return settings


async def pub_logger_dev():
    """Function async to development, publish in log current datetime"""

    dt_now = arrow.utcnow().to("local")
    log_uv_err.info("DATE: %s", dt_now.format())
    print("Log form print")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle the start and stop of scheduler of APScheduler"""

    print("Printing form starting")
    log_uv_err.info("Starting app lifespan")
    log_uv_err.info("Adding job to APSchedule - %s", "pub_logger_dev")
    scheduler.add_job(pub_logger_dev, "interval", seconds=5)

    scheduler.start()
    # Code up to yield is executed while server is running
    yield
    # Code after yield is executed when server is closed
    logger.info("Stopping APScheduler...")
    scheduler.shutdown()


async def get_weather_data():
    """Call SMN weather endpoints for forecast data"""

    # this task need to be ascheduled every 6 hours
    # execute the main async task in the weather module
    pass


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


async def dev_tel_izta(msg):
    """Development function to test message sent to izta group telegram"""

    settings = get_settings()
    if settings.token:
        bot = Bot(token=settings.token)
        async with bot:
            await bot.send_message(chat_id=settings.chatid_local, text=msg, parse_mode="HTML")


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


async def get_weather():
    """Get the SMN api data"""

    # api for data forecast data by day and to 3 days
    url_1 = "https://smn.conagua.gob.mx/tools/GUI/webservices/index.php?method=1"
    # api for data forecast by hour and by 48 hours
    url_3 = "https://smn.conagua.gob.mx/tools/GUI/webservices/index.php?method=3"

    storm_endpoint = "https://api.stormglass.io/v2"


@app.post("/send_message/")
async def send_msg(msg: SensorReport):
    """Send telegram for weather sensor data for home"""
    # insert datetime
    today = dt.datetime.now().strftime("%Y-%d-%m %H:%M:%S")
    text = msg.message + " " + today
    text += f"\nRoom: {msg.Room}"
    text += f"\nLiving Room: {msg.LivingRoom}"
    text += f"\n{get_message()}"
    task = asyncio.create_task(send_message(text))
    await task


@app.post("/send_izta/")
async def notify_izta(msg: InMessage, background_task: BackgroundTasks):
    """Test chatid_local for telegram group"""

    msg = get_message()
    background_task.add_task(send_tel_izta, msg)
    return {"status": "ok"}


@app.post("/test_izta_dev/")
async def dev_notify_izta(msg: InMessage):
    """Development function for send message to teelgram group"""
    msg = get_message()
    task = asyncio.create_task(dev_tel_izta(msg))
    await task


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

    msg = get_message()
    background_task.add_task(send_dev_channel, msg)
    return {"status": "ok"}


if __name__ == "__main__":
    print(ENV_FILE_PATH)
    try:
        settings = get_settings()
        print(settings.token)
        print(settings.chatid_local)
        print(settings.chatid_projectIzta)
    except ValidationError:
        print("Settings validation error")
