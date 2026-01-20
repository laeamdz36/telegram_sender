"""Definition of logger for the application."""
import logging
import sys


def init_logger2():
    """Configure and return the logger instance"""

    logger = logging.getLogger("app_telebot")

    # Avoid adding multiple handlers if already configured
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        logger.propagate = True  # avoid duplicated logs

        # Stream handler
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # hide logs from httpx and httpcore
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    return logger


def init_logger():
    """Init logger with uvicorn"""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    logger = logging.getLogger("app_telebot")
    logger.setLevel(logging.INFO)

    return logger


logger = init_logger()
