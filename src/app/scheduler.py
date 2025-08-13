"""Module to control the schedules for tasks"""
from apscheduler.schedulers.background import BackgroundScheduler
import datetime as dt
from app.logger import logger


def test_task():
    """Test task to verify scheduler functionality"""
    logger.info(f"Test task executed at {dt.datetime.now()}")


def assign_tasks(scheduler):
    """Asignation of task cron type"""

    scheduler.add_job(test_task, 'cron',
                      day_of_week='mon-fri', hour=9, minute=30)
    scheduler.add_job(test_task, 'cron',
                      day_of_week='*', hour=4, minute=00)


def start_scheduler():
    """Start the background scheduler"""

    scheduler = BackgroundScheduler()
    logger.info("Starting the scheduler...")
    try:
        scheduler.start()
        logger.info("Scheduler started successfully.")
    except Exception as e:
        logger.error(f"Failed to start the scheduler: {e}")
    return scheduler
