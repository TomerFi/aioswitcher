"""Test cases for the aioswitcher schedules helper functions."""

from asyncio import AbstractEventLoop

from pytest import fail, mark

from aioswitcher.consts import (
    SCHEDULE_DUE_ANOTHER_DAY_FORMAT, SCHEDULE_DUE_TODAY_FORMAT,
    SCHEDULE_DUE_TOMMOROW_FORMAT)
from aioswitcher.schedules import (
    calc_next_run_for_schedule, SwitcherV2Schedule)


@mark.asyncio
async def test_recurring_schedule_next_runtime_tommorow(
        event_loop: AbstractEventLoop,
        recurring_tommorow_schedule: SwitcherV2Schedule) -> None:
    """Test the calc_next_run_for_schedule tool."""
    try:
        result = await calc_next_run_for_schedule(
            event_loop, recurring_tommorow_schedule)
        assert SCHEDULE_DUE_TOMMOROW_FORMAT.format(
            recurring_tommorow_schedule.start_time) == result

    except (ValueError, IndexError, RuntimeError) as exc:
        fail("failed to calculate next run time for recurring schedule, {}"
             .format(exc))


@mark.asyncio
async def test_recurring_schedule_next_runtime_another_day(
        event_loop: AbstractEventLoop,
        recurring_another_day_schedule: SwitcherV2Schedule) -> None:
    """Test the calc_next_run_for_schedule tool."""
    try:
        result = await calc_next_run_for_schedule(
            event_loop, recurring_another_day_schedule)
        assert SCHEDULE_DUE_ANOTHER_DAY_FORMAT.format(
            recurring_another_day_schedule.days[0],
            recurring_another_day_schedule.start_time) == result

    except (ValueError, IndexError, RuntimeError) as exc:
        fail("failed to calculate next run time for recurring schedule, {}"
             .format(exc))


@mark.asyncio
async def test_non_recurring_schedule_next_runtime_calc(
        event_loop: AbstractEventLoop,
        non_recurring_in_30_minutes_schedule: SwitcherV2Schedule) -> None:
    """Test the calc_next_run_for_schedule tool."""
    try:
        result = await calc_next_run_for_schedule(
            event_loop, non_recurring_in_30_minutes_schedule)

        assert SCHEDULE_DUE_TODAY_FORMAT.format(
            non_recurring_in_30_minutes_schedule.start_time) == result

    except (ValueError, IndexError, RuntimeError) as exc:
        fail("failed to calculate next run time for non recurring schedule, {}"
             .format(exc))
