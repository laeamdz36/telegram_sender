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
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pydantic import BaseModel, ValidationError, Field
from app.load_config import load_config
import logging
from app.dev.dev_datetimes import get_system_time
from app.weather import request_file
from app.dates_infos import get_message
from app.phrase_otd.phrase_main import requester, format_data
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


async def get_weather():
    """Get the SMN api data"""

    # api for data forecast data by day and to 3 days
    url_1 = "https://smn.conagua.gob.mx/tools/GUI/webservices/index.php?method=1"
    # api for data forecast by hour and by 48 hours
    url_3 = "https://smn.conagua.gob.mx/tools/GUI/webservices/index.php?method=3"

    storm_endpoint = "https://api.stormglass.io/v2"


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


@app.get("/weather/get_file/")
async def serve_weather_data():
    """Function to handle request and processing weather data"""

    # execute the function to request the file


if __name__ == "__main__":
    print(ENV_FILE_PATH)
    try:
        settings = get_settings()
        print(settings.token)
        print(settings.chatid_local)
        print(settings.chatid_projectIzta)
    except ValidationError:
        print("Settings validation error")
