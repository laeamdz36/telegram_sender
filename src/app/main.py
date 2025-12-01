"""Aplication to send notifications to telegram."""
import asyncio
import datetime as dt
from pathlib import Path
from functools import lru_cache
from fastapi import FastAPI
from telegram import Bot
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, ValidationError, Field
from app.load_config import load_config
from app.logger import logger
from app.dates_infos import get_message

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
ENV_FILE_PATH = BASE_DIR / ".env"


class Settings(BaseSettings):
    """Settings to load env file"""
    token: str | None = Field(default=None)
    chat_id: str | None = Field(default=None)
    storm_key: str | None = Field(default=None)
    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        extra='allow'
    )


class InMessage(BaseModel):
    """Define the innser structure of the message"""

    message: str
    Room: str
    LivingRoom: str


@lru_cache()
def get_settings():
    """Init settings"""
    return Settings()


async def send_message(text):
    """Send message with telegram bot"""
    try:
        settings = get_settings()
    except ValidationError as e:
        print(f"Key error on env file - {e}")
        return None
    bot = Bot(token=settings.token)
    await bot.send_message(chat_id=settings.chatid, text=text, parse_mode="HTML")


async def get_weather():
    """Get the SMN api data"""

    # api for data forecast data by day and to 3 days
    url_1 = "https://smn.conagua.gob.mx/tools/GUI/webservices/index.php?method=1"
    # api for data forecast by hour and by 48 hours
    url_3 = "https://smn.conagua.gob.mx/tools/GUI/webservices/index.php?method=3"

    storm_endpoint = "https://api.stormglass.io/v2"


@app.post("/send_message/")
async def send_msg(msg: InMessage):
    """Receive the json"""
    # insert datetime
    today = dt.datetime.now().strftime("%Y-%d-%m %H:%M:%S")
    text = msg.message + " " + today
    text += f"\nRoom: {msg.Room}"
    text += f"\nLiving Room: {msg.LivingRoom}"
    text += f"\n{get_message()}"
    task = asyncio.create_task(send_message(text))
    await task

if __name__ == "__main__":
    print(ENV_FILE_PATH)
    try:
        settings = get_settings()
        print(settings.token)
    except ValidationError:
        print("Settings validation error")
