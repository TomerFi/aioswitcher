"""Test cases for the aioswitcher.schedules module."""

from asyncio import AbstractEventLoop, wait
from binascii import unhexlify

from pytest import fail, mark, raises

from aioswitcher.consts import (
    ALL_DAYS, ENCODING_CODEC, FRIDAY, MONDAY, SATURDAY,
    SCHEDULE_DUE_ANOTHER_DAY_FORMAT, SCHEDULE_DUE_TODAY_FORMAT,
    SCHEDULE_DUE_TOMMOROW_FORMAT, SUNDAY, THURSDAY, TUESDAY, WEDNESDAY)
from aioswitcher.schedules import (
    calc_next_run_for_schedule, SwitcherV2Schedule)

from .asserters import assert_lists_equal


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

@mark.asyncio
async def test_set_get_SwitcherV2Schedule(event_loop: AbstractEventLoop) -> None:
    """Test setters of SwitcherV2Schedule object."""
    schedule = SwitcherV2Schedule(
        event_loop, 0,
        [unhexlify('3031303130323031653036616133356366303738613335636365306530303030')])

    await wait([schedule.init_future])

    assert schedule.enabled
    assert schedule.schedule_data.decode(
        ENCODING_CODEC) == '01010201e06aa35cf078a35c'


    with raises(TypeError) as exc_info_enable:
        schedule.enabled = "not_bool"

    assert exc_info_enable.type is TypeError

    with raises(TypeError) as exc_info_data:
        schedule.schedule_data = 0

    assert exc_info_data.type is TypeError

    schedule.enabled = False
    assert not schedule.as_dict().get('_enabled')

    schedule.schedule_data = "Test String"
    assert "Test String" == schedule.as_dict().get('_schedule_data')


@mark.asyncio
async def test_select_recur_SwitcherV2Schedule(event_loop: AbstractEventLoop) -> None:
    """Test selective recurring SwitcherV2Schedule object."""
    schedule = SwitcherV2Schedule(
        event_loop, 0,
        [unhexlify('3031303130323031653036616133356366303738613335636365306530303030')])

    await wait([schedule.init_future])
    
    assert schedule.schedule_id == '1'
    
    assert schedule.enabled
    assert schedule.recurring
    await assert_lists_equal(schedule.days, [MONDAY])
    assert schedule.start_time == '17:00'
    assert schedule.end_time == '18:00'
    assert schedule.duration == '1:00:00'
    assert schedule.schedule_data.decode(
        ENCODING_CODEC) == '01010201e06aa35cf078a35c'


    with raises(TypeError) as exc_info_enable:
        schedule.enabled = "not_bool"

    assert exc_info_enable.type is TypeError

    with raises(TypeError) as exc_info_data:
        schedule.schedule_data = 0

    assert exc_info_data.type is TypeError


@mark.asyncio
async def test_full_recur_SwitcherV2Schedule(event_loop: AbstractEventLoop) -> None:
    """Test full recurring SwitcherV2Schedule object."""
    schedule = SwitcherV2Schedule(
        event_loop, 0,
        [unhexlify('3031303166653031653036616133356366303738613335636365306530303030')])

    await wait([schedule.init_future])
    
    assert schedule.schedule_id == '1'
    assert schedule.enabled
    assert schedule.recurring
    #print(schedule.days)
    await assert_lists_equal(schedule.days, [FRIDAY, MONDAY, SATURDAY, SUNDAY,
                                             THURSDAY, TUESDAY, WEDNESDAY])
    assert schedule.start_time == '17:00'
    assert schedule.end_time == '18:00'
    assert schedule.duration == '1:00:00'
    assert schedule.schedule_data.decode(
        ENCODING_CODEC) == '0101fe01e06aa35cf078a35c'


@mark.asyncio
async def test_non_recur_SwitcherV2Schedule(event_loop: AbstractEventLoop) -> None:
    """Test non-recurring SwitcherV2Schedule object."""
    schedule = SwitcherV2Schedule(
        event_loop, 0,
        [unhexlify('3031303130303031653036616133356366303738613335636365306530303030')])

    await wait([schedule.init_future])
    
    assert schedule.schedule_id == '1'
    assert schedule.enabled
    assert schedule.recurring
    await assert_lists_equal(schedule.days, [])
    assert schedule.start_time == '17:00'
    assert schedule.end_time == '18:00'
    assert schedule.duration == '1:00:00'
    assert schedule.schedule_data.decode(
        ENCODING_CODEC) == '01010001e06aa35cf078a35c'
