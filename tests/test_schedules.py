"""Test cases for the aioswitcher.schedules module."""

from asyncio import AbstractEventLoop, wait
from binascii import unhexlify

from pytest import fail, mark, raises

from aioswitcher.consts import (
    ENCODING_CODEC, HANDLED_EXCEPTIONS,
    SCHEDULE_DUE_ANOTHER_DAY_FORMAT, SCHEDULE_DUE_TODAY_FORMAT,
    SCHEDULE_DUE_TOMMOROW_FORMAT)
from aioswitcher.schedules import (
    calc_next_run_for_schedule, SwitcherV2Schedule)

from .asserters import assert_lists_equal
from .consts import (
    DUMMY_SELECTIVE_RECCURING_PROFILE, DUMMY_FULL_RECCURING_PROFILE,
    DUMMY_NON_RECCURING_PROFILE)


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

    except HANDLED_EXCEPTIONS as exc:
        fail(exc)


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

    except HANDLED_EXCEPTIONS as exc:
        fail(exc)


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

    except HANDLED_EXCEPTIONS as exc:
        fail(exc)


@mark.asyncio
async def test_setters_and_getters_schedule(
        event_loop: AbstractEventLoop) -> None:
    """Test setters of SwitcherV2Schedule object."""
    schedule = SwitcherV2Schedule(
        event_loop, 0,
        [unhexlify(DUMMY_SELECTIVE_RECCURING_PROFILE['schedule_data'])])

    await wait([schedule.init_future])

    assert schedule.enabled
    assert schedule.schedule_data.decode(ENCODING_CODEC) == \
        DUMMY_SELECTIVE_RECCURING_PROFILE['schedule_data_decoded']

    with raises(TypeError) as exc_info_enable:
        schedule.enabled = "not_bool"

    assert exc_info_enable.type is TypeError

    with raises(TypeError) as exc_info_data:
        schedule.schedule_data = 0

    assert exc_info_data.type is TypeError

    schedule.enabled = False
    assert not schedule.as_dict().get('_enabled')

    schedule.schedule_data = "Test String"
    assert schedule.as_dict().get('_schedule_data') == "Test String"


@mark.asyncio
async def test_selective_recurring_schedule(
        event_loop: AbstractEventLoop) -> None:
    """Test selective recurring SwitcherV2Schedule object."""
    schedule = SwitcherV2Schedule(
        event_loop, 0,
        [unhexlify(DUMMY_SELECTIVE_RECCURING_PROFILE['schedule_data'])])

    await wait([schedule.init_future])

    assert schedule.schedule_id == \
        DUMMY_SELECTIVE_RECCURING_PROFILE['schedule_id']
    assert schedule.enabled
    assert schedule.recurring

    await assert_lists_equal(
        schedule.days, DUMMY_SELECTIVE_RECCURING_PROFILE['days_list'])

    assert schedule.start_time == \
        DUMMY_SELECTIVE_RECCURING_PROFILE['start_time']
    assert schedule.end_time == \
        DUMMY_SELECTIVE_RECCURING_PROFILE['end_time']
    assert schedule.duration == \
        DUMMY_SELECTIVE_RECCURING_PROFILE['duration']
    assert schedule.schedule_data.decode(ENCODING_CODEC) == \
        DUMMY_SELECTIVE_RECCURING_PROFILE['schedule_data_decoded']


@mark.asyncio
async def test_full_recurring_schedule(
        event_loop: AbstractEventLoop) -> None:
    """Test full recurring SwitcherV2Schedule object."""
    schedule = SwitcherV2Schedule(
        event_loop, 0,
        [unhexlify(DUMMY_FULL_RECCURING_PROFILE['schedule_data'])])

    await wait([schedule.init_future])

    assert schedule.schedule_id == DUMMY_FULL_RECCURING_PROFILE['schedule_id']
    assert schedule.enabled
    assert schedule.recurring

    await assert_lists_equal(
        schedule.days, DUMMY_FULL_RECCURING_PROFILE['days_list'])

    assert schedule.start_time == DUMMY_FULL_RECCURING_PROFILE['start_time']
    assert schedule.end_time == DUMMY_FULL_RECCURING_PROFILE['end_time']
    assert schedule.duration == DUMMY_FULL_RECCURING_PROFILE['duration']
    assert schedule.schedule_data.decode(ENCODING_CODEC) == \
        DUMMY_FULL_RECCURING_PROFILE['schedule_data_decoded']


@mark.asyncio
async def test_non_recurring_schedule(
        event_loop: AbstractEventLoop) -> None:
    """Test non-recurring SwitcherV2Schedule object."""
    schedule = SwitcherV2Schedule(
        event_loop, 0,
        [unhexlify(DUMMY_NON_RECCURING_PROFILE['schedule_data'])])

    await wait([schedule.init_future])

    assert schedule.schedule_id == DUMMY_NON_RECCURING_PROFILE['schedule_id']
    assert schedule.enabled  # TODO this should return False, fix dummy packet!
    assert schedule.recurring

    await assert_lists_equal(
        schedule.days, DUMMY_NON_RECCURING_PROFILE['days_list'])

    assert schedule.start_time == DUMMY_NON_RECCURING_PROFILE['start_time']
    assert schedule.end_time == DUMMY_NON_RECCURING_PROFILE['end_time']
    assert schedule.duration == DUMMY_NON_RECCURING_PROFILE['duration']
    assert schedule.schedule_data.decode(ENCODING_CODEC) ==  \
        DUMMY_NON_RECCURING_PROFILE['schedule_data_decoded']
