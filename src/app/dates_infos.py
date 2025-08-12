"""Module to obtain stastistics information from the initial date."""
import datetime as dt
from app.load_config import load_config


def date_infos():
    """Compute date information."""
    date_str = load_config()["General"]["initial_date"]
    # Convert string "2024-01-14 11:19:00" to datetime object (example)
    date_obj = dt.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    return date_obj


def get_elapsed_days():
    """Calculate the number of days elapsed since the initial date."""
    initial_date = date_infos()
    current_date = dt.datetime.now()
    elapsed_days = (current_date - initial_date).days
    return elapsed_days


def get_elapsed_hours():
    """Calculate the number of hours elapsed since the initial date."""
    initial_date = date_infos()
    current_date = dt.datetime.now()
    elapsed_hours = (current_date - initial_date).total_seconds() / 3600
    return elapsed_hours


def get_message():
    """Build a message with the initial date."""
    message = f"Dia **{get_elapsed_days():,}** comenzamos"
    return message
