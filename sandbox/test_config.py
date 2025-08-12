"""Module to load configuration settings from an INI file."""

from app.load_config import load_config

if __name__ == "__main__":
    config = load_config()
    print(config.sections())
