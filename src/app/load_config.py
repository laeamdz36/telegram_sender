"""Module to lad the config file for the application."""
import configparser
from pathlib import Path


def load_config():
    """Load the configuration from the specified file path."""

    # Archivo estatico de configuración
    file_path = "./config.ini"
    config_path = Path(__file__).parent.joinpath(file_path)

    config = configparser.ConfigParser()
    config.read(config_path)
    return config
