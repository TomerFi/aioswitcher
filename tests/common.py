"""Common tools for use with the Switcher integration test cases."""

from datetime import datetime, timedelta
from random import randint


def get_weekday_for_day_delta(day_delta: int = 1) -> int:
    """Use to get the weekday of the next day delta from today (1=tommorow)."""
    return (datetime.today() + timedelta(days=day_delta)).weekday()


def create_random_time(hour_delta: int = 1) -> str:
    """Use to create a random HH:MM time."""
    min_hour = (datetime.now() + timedelta(hours=hour_delta)).hour
    return '{}:{}'.format(
        '00{}'.format(str(randint(min_hour, 23)))[-2:],  # nosec
        '00{}'.format(str(randint(0, 59)))[-2:])  # nosec


def get_later_time_for_minute_delta(minute_delta: int = 30) -> str:
    """Use to get HH:MM time calculating minutes delta from now."""
    delta_time = datetime.now() + timedelta(minutes=minute_delta)
    return '{}:{}'.format(
        '00{}'.format(delta_time.hour)[-2:],
        '00{}'.format(delta_time.minute)[-2:])
