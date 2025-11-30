"""Snippet for start server fast Api"""

import datetime as dt
from fastapi import FastAPI
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ValidationError
# from pydantic_settings import SettingsConfigDict
from functools import lru_cache
from telegram import Bot
import asyncio


app = FastAPI()


class Settings(BaseSettings):
    token: str
    chat_id: str
    model_config = SettingsConfigDict(
        # Aquí va la configuración, ej:
        env_file=".env",
        # Esto NO resuelve el error de abajo, pero es la forma correcta.
        extra='allow'
    )


class InMessage(BaseModel):
    """Define the innser structure of the message"""

    message: str
    sensor: str


@lru_cache()
def get_settings():
    """Init settings"""
    return Settings()


async def send_message(text):
    """Send message with telegram bot"""
    try:
        settings = get_settings()
    except ValidationError:
        print("Key error on env file")
        return None
    bot = Bot(token=settings.token)
    await bot.send_message(chat_id=settings.chat_id, text=text, parse_mode="HTML")


@app.post("/send_message/")
async def send_msg(msg: InMessage):
    """Receive the json"""
    # insert datetime
    today = dt.datetime.now().strftime("%Y-%d-%m %H:%M:%S")
    text = msg.message + " " + today
    text += f"\nSensor: {msg.sensor}"
    task = asyncio.create_task(send_message(text))
    await task


async def main():
    """Execute main event loop"""

    send1 = asyncio.create_task(send_message("TEST1"))
    await send1

if __name__ == "__main__":
    asyncio.run(main())
