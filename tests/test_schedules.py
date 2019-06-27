"""Test cases for the aioswitcher.schedules module."""

# fmt: off
from asyncio import AbstractEventLoop, wait
from binascii import unhexlify

from pytest import fail, mark, raises

from aioswitcher.consts import (HANDLED_EXCEPTIONS,
                                SCHEDULE_DUE_ANOTHER_DAY_FORMAT,
                                SCHEDULE_DUE_TODAY_FORMAT,
                                SCHEDULE_DUE_TOMMOROW_FORMAT)
from aioswitcher.schedules import (SwitcherV2Schedule,
                                   calc_next_run_for_schedule)

from .asserters import assert_lists_equal
from .consts import (DUMMY_FULL_RECCURING_DAYS_LIST,
                     DUMMY_FULL_RECCURING_DURATION,
                     DUMMY_FULL_RECCURING_END_TIME,
                     DUMMY_FULL_RECCURING_SCHEDULE_DATA,
                     DUMMY_FULL_RECCURING_SCHEDULE_DATA_BYTES,
                     DUMMY_FULL_RECCURING_SCHEDULE_ID,
                     DUMMY_FULL_RECCURING_START_TIME,
                     DUMMY_NON_RECCURING_DAYS_LIST,
                     DUMMY_NON_RECCURING_DURATION,
                     DUMMY_NON_RECCURING_END_TIME,
                     DUMMY_NON_RECCURING_SCHEDULE_DATA,
                     DUMMY_NON_RECCURING_SCHEDULE_DATA_BYTES,
                     DUMMY_NON_RECCURING_SCHEDULE_ID,
                     DUMMY_NON_RECCURING_START_TIME,
                     DUMMY_SELECTIVE_RECCURING_DAYS_LIST,
                     DUMMY_SELECTIVE_RECCURING_DURATION,
                     DUMMY_SELECTIVE_RECCURING_END_TIME,
                     DUMMY_SELECTIVE_RECCURING_SCHEDULE_DATA,
                     DUMMY_SELECTIVE_RECCURING_SCHEDULE_DATA_BYTES,
                     DUMMY_SELECTIVE_RECCURING_SCHEDULE_ID,
                     DUMMY_SELECTIVE_RECCURING_START_TIME)

# fmt: on


@mark.asyncio
async def test_recurring_schedule_next_runtime_tommorow(
    event_loop: AbstractEventLoop,
    recurring_tommorow_schedule: SwitcherV2Schedule,
) -> None:
    """Test the calc_next_run_for_schedule tool."""
    try:
        result = await calc_next_run_for_schedule(
            event_loop, recurring_tommorow_schedule
        )
        assert (
            SCHEDULE_DUE_TOMMOROW_FORMAT.format(
                recurring_tommorow_schedule.start_time
            )
            == result
        )

    except HANDLED_EXCEPTIONS as exc:
        fail(exc)


@mark.asyncio
async def test_recurring_schedule_next_runtime_another_day(
    event_loop: AbstractEventLoop,
    recurring_another_day_schedule: SwitcherV2Schedule,
) -> None:
    """Test the calc_next_run_for_schedule tool."""
    try:
        result = await calc_next_run_for_schedule(
            event_loop, recurring_another_day_schedule
        )
        assert (
            SCHEDULE_DUE_ANOTHER_DAY_FORMAT.format(
                recurring_another_day_schedule.days[0],
                recurring_another_day_schedule.start_time,
            )
            == result
        )

    except HANDLED_EXCEPTIONS as exc:
        fail(exc)


@mark.asyncio
async def test_non_recurring_schedule_next_runtime_calc(
    event_loop: AbstractEventLoop,
    non_recurring_in_30_minutes_schedule: SwitcherV2Schedule,
) -> None:
    """Test the calc_next_run_for_schedule tool."""
    try:
        result = await calc_next_run_for_schedule(
            event_loop, non_recurring_in_30_minutes_schedule
        )

        assert (
            SCHEDULE_DUE_TODAY_FORMAT.format(
                non_recurring_in_30_minutes_schedule.start_time
            )
            == result
        )

    except HANDLED_EXCEPTIONS as exc:
        fail(exc)


@mark.asyncio
async def test_setters_and_getters_schedule(
    event_loop: AbstractEventLoop
) -> None:
    """Test setters of SwitcherV2Schedule object."""
    schedule = SwitcherV2Schedule(
        event_loop, 0, [unhexlify(DUMMY_SELECTIVE_RECCURING_SCHEDULE_DATA)]
    )

    await wait([schedule.init_future])

    assert schedule.enabled
    assert (
        schedule.schedule_data == DUMMY_SELECTIVE_RECCURING_SCHEDULE_DATA_BYTES
    )

    with raises(TypeError) as exc_info_enable:
        schedule.enabled = "not_bool"  # type: ignore

    assert exc_info_enable.type is TypeError

    with raises(TypeError) as exc_info_data:
        schedule.schedule_data = 0  # type: ignore

    assert exc_info_data.type is TypeError

    schedule.enabled = False
    assert not schedule.as_dict().get("_enabled")

    schedule.schedule_data = b"4855f34ca8c58d6f1453"
    assert schedule.as_dict().get("_schedule_data") == b"4855f34ca8c58d6f1453"


@mark.asyncio
async def test_selective_recurring_schedule(
    event_loop: AbstractEventLoop
) -> None:
    """Test selective recurring SwitcherV2Schedule object."""
    schedule = SwitcherV2Schedule(
        event_loop, 0, [unhexlify(DUMMY_SELECTIVE_RECCURING_SCHEDULE_DATA)]
    )

    await wait([schedule.init_future])

    assert schedule.schedule_id == DUMMY_SELECTIVE_RECCURING_SCHEDULE_ID
    assert schedule.enabled
    assert schedule.recurring

    await assert_lists_equal(
        schedule.days, DUMMY_SELECTIVE_RECCURING_DAYS_LIST
    )

    assert schedule.start_time == DUMMY_SELECTIVE_RECCURING_START_TIME
    assert schedule.end_time == DUMMY_SELECTIVE_RECCURING_END_TIME
    assert schedule.duration == DUMMY_SELECTIVE_RECCURING_DURATION
    assert (
        schedule.schedule_data == DUMMY_SELECTIVE_RECCURING_SCHEDULE_DATA_BYTES
    )


@mark.asyncio
async def test_full_recurring_schedule(event_loop: AbstractEventLoop) -> None:
    """Test full recurring SwitcherV2Schedule object."""
    schedule = SwitcherV2Schedule(
        event_loop, 0, [unhexlify(DUMMY_FULL_RECCURING_SCHEDULE_DATA)]
    )

    await wait([schedule.init_future])

    assert schedule.schedule_id == DUMMY_FULL_RECCURING_SCHEDULE_ID
    assert schedule.enabled
    assert schedule.recurring

    await assert_lists_equal(schedule.days, DUMMY_FULL_RECCURING_DAYS_LIST)

    assert schedule.start_time == DUMMY_FULL_RECCURING_START_TIME
    assert schedule.end_time == DUMMY_FULL_RECCURING_END_TIME
    assert schedule.duration == DUMMY_FULL_RECCURING_DURATION
    assert schedule.schedule_data == DUMMY_FULL_RECCURING_SCHEDULE_DATA_BYTES


@mark.asyncio
async def test_non_recurring_schedule(event_loop: AbstractEventLoop) -> None:
    """Test non-recurring SwitcherV2Schedule object."""
    schedule = SwitcherV2Schedule(
        event_loop, 0, [unhexlify(DUMMY_NON_RECCURING_SCHEDULE_DATA)]
    )

    await wait([schedule.init_future])

    assert schedule.schedule_id == DUMMY_NON_RECCURING_SCHEDULE_ID
    assert schedule.enabled  # TODO this should return False, fix dummy packet!
    assert schedule.recurring

    await assert_lists_equal(schedule.days, DUMMY_NON_RECCURING_DAYS_LIST)

    assert schedule.start_time == DUMMY_NON_RECCURING_START_TIME
    assert schedule.end_time == DUMMY_NON_RECCURING_END_TIME
    assert schedule.duration == DUMMY_NON_RECCURING_DURATION
    assert schedule.schedule_data == DUMMY_NON_RECCURING_SCHEDULE_DATA_BYTES
