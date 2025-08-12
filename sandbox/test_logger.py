"""Test script for the logger module.
This script initializes the logger and logs messages at various levels."""

from app.logger import init_logger

if __name__ == "__main__":
    # Test of the logger module
    logger = init_logger()
    logger.info("Logger initialized successfully.")
    logger.debug("This is a debug message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")
