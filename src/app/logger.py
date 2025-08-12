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
    # Silenciar los logs de la librería de telegram-bot
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    return logging.getLogger("main_app")


# Si quieres que el logger se configure una sola vez
# y se pueda acceder a él en toda la aplicación
logger = init_logger()
