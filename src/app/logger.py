"""Definition of logger for the application."""
import logging
import sys


def init_logger():
    """Configure and return the logger instance"""

    # get configure logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    # hide logs from telegram bot and httpx
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    return logging.getLogger("main_app")


logger = init_logger()
