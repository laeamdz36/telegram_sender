"""Module to lad the config file for the application."""
import configparser
from pathlib import Path
import json


def load_config():
    """Load the configuration from the specified file path."""

    # Archivo estatico de configuración
    file_path = "./config.ini"
    config_path = Path(__file__).parent.joinpath(file_path)

    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def load_json(file_name):
    """Load json conf databases file and return """

    path_file = Path(__file__).parent.resolve().joinpath(file_name)
    json_data = None
    try:
        with open(path_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        json_data = data
    except FileNotFoundError:
        print(f"File not found {path_file}")
    except json.JSONDecodeError as e:
        print(f"Failed to decode json file: {e}")

    return json_data
