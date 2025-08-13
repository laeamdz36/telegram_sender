"""Aplication to send notifications to telegram."""
import asyncio
import datetime as dt
from telegram import Bot
from app.load_config import load_config
from app.logger import logger
from app.dates_infos import get_message


BOT_TOKEN = ""


async def send_msg(msg="Empty message"):
    """Send a message to the Telegram bot, executed by the scheduler."""

    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id="1571717715", text=msg, parse_mode="HTML")


def date_infos():
    """Compute date information."""
    date_str = load_config()["General"]["initial_date"]
    # Convert string "2024-01-14 11:19:00" to datetime object (example)
    date_obj = dt.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    return date_obj


if __name__ == "__main__":
    logger.info("Starting the Telegram bot message sender.")
    logger.debug("Preparing to send a message.")
    # compute info for date from config file
    date_msg = get_message()
    asyncio.run(send_msg(date_msg))
