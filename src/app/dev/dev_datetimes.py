"""Develompent of datetime handling"""
import datetime as dt


async def get_system_time() -> str:
    """Return the current system datetime using py datetime module"""

    # get the current time
    dt_current = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"current_time": dt_current}
