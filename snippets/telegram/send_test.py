"""SImple testing text message"""

import datetime as dt
import asyncio
from telegram import Bot
from dotenv import load_dotenv
import os

# read env file


def load_env_file():
    """Load the .env file"""

    load_dotenv()


async def send_message(the_message: str):
    """Send a simple message to telegram"""

    token = os.environ["token"]
    bot = Bot(token=token)
    await bot.send_message(chat_id="1571717715", text=the_message, parse_mode="HTML")


async def main():
    """Main async loop"""
    await send_message(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == "__main__":
    load_env_file()
    asyncio.run(main())
