"""Fixture and objects for the Switcher integration tests."""

from asyncio import AbstractEventLoop, get_event_loop
from typing import Any, Generator

from asynctest import patch
from pytest import fixture

from aioswitcher.consts import WEEKDAY_TUP
from aioswitcher.schedules import SwitcherV2Schedule

from .common import (create_random_time, get_later_time_for_minute_delta,
                     get_weekday_for_day_delta)


@fixture(name='recurring_tommorow_schedule')
def mock_recurring_tommorow_schedule() \
        -> Generator[SwitcherV2Schedule, Any, None]:
    """Fixture from recurring schedule."""
    schedule_patch = patch(
        'aioswitcher.schedules.SwitcherV2Schedule',
        recurring=True,
        start_time=create_random_time(),
        days=[WEEKDAY_TUP[get_weekday_for_day_delta()]])

    schedule = schedule_patch.start()
    yield schedule
    schedule_patch.stop()


@fixture(name='recurring_another_day_schedule')
def mock_recurring_another_day_schedule() \
        -> Generator[SwitcherV2Schedule, Any, None]:
    """Fixture from recurring schedule."""
    schedule_patch = patch(
        'aioswitcher.schedules.SwitcherV2Schedule',
        recurring=True,
        start_time=create_random_time(),
        days=[WEEKDAY_TUP[get_weekday_for_day_delta(3)]])

    schedule = schedule_patch.start()
    yield schedule
    schedule_patch.stop()


@fixture(name='non_recurring_in_30_minutes_schedule')
def mock_non_recurring_in_30_minutes_schedule() \
        -> Generator[SwitcherV2Schedule, Any, None]:
    """Fixture from recurring schedule."""
    schedule_patch = patch(
        'aioswitcher.schedules.SwitcherV2Schedule',
        recurring=False,
        start_time=get_later_time_for_minute_delta())

    schedule = schedule_patch.start()
    yield schedule
    schedule_patch.stop()


@fixture(name='event_loop', scope='session')
def mock_event_loop() -> Generator[AbstractEventLoop, Any, None]:
    """Fixture from creating a asyncio event loop."""
    loop = get_event_loop()
    yield loop
    loop.close()
