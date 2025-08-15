"""Aplication to send notifications to telegram."""
import asyncio
import datetime as dt
from telegram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
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


async def main():
    """Main execution function to initialize scheduler and send msg."""
    logger.info("Starting async main funciton")
    # initialize async scheduler
    logger.debug("Initialization of async scheduler")
    async_sch = AsyncIOScheduler()
    logger.debug("Adding jobs")
    logger.info("Added JOB 'send_msg'")
    async_sch.add_job(send_msg, "cron", second="*/10", id="send_msg")
    async_sch.start()

    try:
        logger.info("Starting main cycle")
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError as e:
        logger.error("Error in cycle: %s", e, exc_info=True)

        # execute the main event loop
if __name__ == "__main__":
    logger.info("Starting Telegram bot message sender.".center(50, "*"))
    # compute info for date from config file
    date_msg = get_message()
    try:
        asyncio.run(main())
    except (RuntimeError, asyncio.CancelledError) as e:
        logger.error("Error in main execution: %s", e, exc_info=True)
