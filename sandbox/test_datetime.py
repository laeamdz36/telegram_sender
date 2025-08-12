"""Construction of datetime messaege for telegram bot."""
import datetime as dt
from app.load_config import load_config
import app.dates_infos as dts


def date_infos():
    """Compute date information."""
    date_str = load_config()["General"]["initial_date"]
    # Convert string "2024-01-14 11:19:00" to datetime object (example)
    date_obj = dt.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    return date_obj


if __name__ == "__main__":
    print(f"Initial date: {dts.date_infos().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Elapsed days: {dts.get_elapsed_days() + 1:,}")
    print(f"Elapsed hours: {dts.get_elapsed_hours():,.2f}")
