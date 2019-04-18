"""Fixture and objects for the Switcher integration tests."""

from asyncio import (AbstractEventLoop, get_event_loop,
                     StreamReader, StreamWriter)
from binascii import unhexlify
from typing import Any, Generator, List, Tuple

from asynctest import patch, Mock
from pytest import fixture

from aioswitcher.consts import ENCODING_CODEC, WEEKDAY_TUP
from aioswitcher.schedules import SwitcherV2Schedule

from .common import (create_random_time, get_later_time_for_minute_delta,
                     get_weekday_for_day_delta)


DUMMY_CONTROL_HEX_RESPONSE = 'fef0360002320102d0b2824e340002000000d0b2824e0000a8e4b65c00000000000000000000f0fe0100060000000000000000500000'
DUMMY_CREATE_SCHEDULE_HEX_RESPONSE = 'fef06100023201022948834e3400020000002948834e0000521eb75c00000000000000000000f0fe03003100030001fc01e871a35cf87fa35cce0e000001010201e06aa35cf078a35cce0e0000020100019862b75ca069b75c00000000fe8c0000'
DUMMY_DELETE_SCHEDULE_HEX_RESPONSE = 'fef05100023201024576834e3400020000004576834e00003d20b75c00000000000000000000f0fe08002100020001fc01e871a35cf87fa35cce0e000001010201e06aa35cf078a35cce0e0000ba9c0000'
DUMMY_DISABLE_ENABLE_SCHEDULE_HEX_RESPONSE = 'fef06100023201026e76834e3400020000006e76834e00001620b75c00000000000000000000f0fe07003100030001fc01e871a35cf87fa35cce0e000001010201e06aa35cf078a35cce0e0000020000019862b75ca069b75c0000000031870000'
DUMMY_GET_SCHEDULES_HEX_RESPONSE = 'fef0510002320102f050834e340002000000f050834e00008906b75c00000000000000000000f0fe06002100020001fc01e871a35cf87fa35cce0e000001010201e06aa35cf078a35cce0e000012150000'
DUMMY_LOGIN_HEX_RESPONSE = 'fef02c000232a100f050834e3400020e00000000000000008806b75c00000000000000000000f0fe5fbf0000'
DUMMY_SET_AUTO_OFF_HEX_RESPONSE = 'fef03400023201022c4e834e3400020000002c4e834e00005418b75c00000000000000000000f0fe0400040028230000fcf30000'
DUMMY_STATE_HEX_RESPONSE = 'fef06b0002320103f050834e340002000000f050834e00008906b75c00000000000000000000f0fe537769746368657220426f696c65723200000000000000000000000000000000031c0000000000000000b71b65000000000000000000000000181500000102e8620000'
DUMMY_UPDATE_NAME_HEX_RESPONSE = 'fef02c0002320202e341834e340002000000e341834e00009b17b75c00000000000000000000f0feea880000'


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


@fixture(name='tcp_connection')
def mock_tcp_connection() \
        -> Generator[Tuple[StreamReader, StreamWriter], Any, None]:
    """Fixture for mocking asyncio.open_connection"""
    with patch ('aioswitcher.api.open_connection') as conn:
        reader = Mock(StreamReader)
        writer = Mock(StreamWriter)
        conn.return_value = (reader, writer)
        yield reader, writer


@fixture(name='api_stage_success_login')
def mock_api_stage_success_login() -> Generator[None, None, str]:
    """Fixture for mocking a success login response from the api."""
    return unhexlify(DUMMY_LOGIN_HEX_RESPONSE.encode(ENCODING_CODEC))


@fixture(name='api_stage_failed_login')
def mock_api_stage_fail_login() -> Generator[None, None, str]:
    """Fixture for mocking a failed login response from the api."""
    return DUMMY_LOGIN_HEX_RESPONSE


@fixture(name='api_stage_success_get_state')
def mock_api_stage_success_get_state() -> Generator[None, None, List[str]]:
    """Fixture for mocking a success get state response from the api."""
    return [
        unhexlify(DUMMY_LOGIN_HEX_RESPONSE.encode(ENCODING_CODEC)),
        unhexlify(DUMMY_STATE_HEX_RESPONSE.encode(ENCODING_CODEC))
        ]


@fixture(name='api_stage_fail_get_state')
def mock_api_stage_fail_get_state() -> Generator[None, None, List[str]]:
    """Fixture for mocking a failed get state response from the api."""
    return [
        unhexlify(DUMMY_LOGIN_HEX_RESPONSE.encode(ENCODING_CODEC)),
        DUMMY_STATE_HEX_RESPONSE
        ]


@fixture(name='api_stage_success_control')
def mock_api_stage_success_control() -> Generator[None, None, List[str]]:
    """Fixture for mocking a success control response from the api."""
    return [
        unhexlify(DUMMY_LOGIN_HEX_RESPONSE.encode(ENCODING_CODEC)),
        unhexlify(DUMMY_STATE_HEX_RESPONSE.encode(ENCODING_CODEC)),
        unhexlify(DUMMY_CONTROL_HEX_RESPONSE.encode(ENCODING_CODEC))
        ]


@fixture(name='api_stage_success_update_name')
def mock_api_stage_success_update_name() -> Generator[None, None, List[str]]:
    """Fixture for mocking a success update_name response from the api."""
    return [
        unhexlify(DUMMY_LOGIN_HEX_RESPONSE.encode(ENCODING_CODEC)),
        unhexlify(DUMMY_STATE_HEX_RESPONSE.encode(ENCODING_CODEC)),
        unhexlify(DUMMY_UPDATE_NAME_HEX_RESPONSE.encode(ENCODING_CODEC))
        ]


@fixture(name='api_stage_success_set_auto_off')
def mock_api_stage_success_set_auto_off() -> Generator[None, None, List[str]]:
    """Fixture for mocking a success set_auto_off response from the api."""
    return [
        unhexlify(DUMMY_LOGIN_HEX_RESPONSE.encode(ENCODING_CODEC)),
        unhexlify(DUMMY_STATE_HEX_RESPONSE.encode(ENCODING_CODEC)),
        unhexlify(DUMMY_SET_AUTO_OFF_HEX_RESPONSE.encode(ENCODING_CODEC))
        ]


@fixture(name='api_stage_success_get_schedules')
def mock_api_stage_success_get_schedules() -> Generator[None, None, List[str]]:
    """Fixture for mocking a success get_schedules response from the api."""
    return [
        unhexlify(DUMMY_LOGIN_HEX_RESPONSE.encode(ENCODING_CODEC)),
        unhexlify(DUMMY_STATE_HEX_RESPONSE.encode(ENCODING_CODEC)),
        unhexlify(DUMMY_GET_SCHEDULES_HEX_RESPONSE.encode(ENCODING_CODEC))
        ]


@fixture(name='api_stage_success_create_schedule')
def mock_api_stage_success_create_schedule() \
        -> Generator[None, None, List[str]]:
    """Fixture for mocking a success create_schedule response from the api."""
    return [
        unhexlify(DUMMY_LOGIN_HEX_RESPONSE.encode(ENCODING_CODEC)),
        unhexlify(DUMMY_STATE_HEX_RESPONSE.encode(ENCODING_CODEC)),
        unhexlify(DUMMY_CREATE_SCHEDULE_HEX_RESPONSE.encode(ENCODING_CODEC))
        ]


@fixture(name='api_stage_success_delete_schedule')
def mock_api_stage_success_delete_schedule() \
        -> Generator[None, None, List[str]]:
    """Fixture for mocking a success delete_schedule response from the api."""
    return [
        unhexlify(DUMMY_LOGIN_HEX_RESPONSE.encode(ENCODING_CODEC)),
        unhexlify(DUMMY_STATE_HEX_RESPONSE.encode(ENCODING_CODEC)),
        unhexlify(DUMMY_DELETE_SCHEDULE_HEX_RESPONSE.encode(ENCODING_CODEC))
        ]


@fixture(name='api_stage_success_en_disable_schedule')
def mock_api_stage_success_en_disable_schedule() \
        -> Generator[None, None, List[str]]:
    """Fixture for mocking a success en_disable response from the api."""
    return [
        unhexlify(DUMMY_LOGIN_HEX_RESPONSE.encode(ENCODING_CODEC)),
        unhexlify(DUMMY_STATE_HEX_RESPONSE.encode(ENCODING_CODEC)),
        unhexlify(DUMMY_DISABLE_ENABLE_SCHEDULE_HEX_RESPONSE.encode(
            ENCODING_CODEC))
        ]
