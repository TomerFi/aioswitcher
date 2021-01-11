"""Fixture and objects for the Switcher integration tests."""

# fmt: off
from asyncio import (AbstractEventLoop, StreamReader, StreamWriter,
                     get_event_loop)
from binascii import unhexlify
from typing import Any, Generator, List, Tuple, Union

from pytest import fixture

from aioswitcher.consts import ENCODING_CODEC, WEEKDAY_TUP
from aioswitcher.schedules import SwitcherV2Schedule
from tests.async_mock import AsyncMock, Mock, patch

from .common import (create_random_time, get_later_time_for_minute_delta,
                     get_weekday_for_day_delta)
from .consts import (DUMMY_CONTROL_RESPONSE, DUMMY_CREATE_SCHEDULE_RESPONSE,
                     DUMMY_DELETE_SCHEDULE_RESPONSE,
                     DUMMY_DISABLE_ENABLE_SCHEDULE_RESPONSE,
                     DUMMY_GET_SCHEDULES_RESPONSE, DUMMY_GET_STATE_RESPONSE,
                     DUMMY_LOGIN_RESPONSE, DUMMY_SET_AUTO_OFF_RESPONSE,
                     DUMMY_UPDATE_NAME_RESPONSE)

# fmt: on


@fixture(name="recurring_tommorow_schedule")
def mock_recurring_tommorow_schedule() -> Generator[
    SwitcherV2Schedule, Any, None
]:
    """Fixture from recurring schedule."""
    schedule_patch = patch(
        "aioswitcher.schedules.SwitcherV2Schedule",
        recurring=True,
        start_time=create_random_time(),
        days=[WEEKDAY_TUP[get_weekday_for_day_delta()]],
    )

    schedule = schedule_patch.start()
    yield schedule
    schedule_patch.stop()


@fixture(name="recurring_another_day_schedule")
def mock_recurring_another_day_schedule() -> Generator[
    SwitcherV2Schedule, Any, None
]:
    """Fixture from recurring schedule."""
    schedule_patch = patch(
        "aioswitcher.schedules.SwitcherV2Schedule",
        recurring=True,
        start_time=create_random_time(),
        days=[WEEKDAY_TUP[get_weekday_for_day_delta(3)]],
    )

    schedule = schedule_patch.start()
    yield schedule
    schedule_patch.stop()


@fixture(name="non_recurring_in_30_minutes_schedule")
def mock_non_recurring_in_30_minutes_schedule() -> Generator[
    SwitcherV2Schedule, Any, None
]:
    """Fixture from recurring schedule."""
    schedule_patch = patch(
        "aioswitcher.schedules.SwitcherV2Schedule",
        recurring=False,
        start_time=get_later_time_for_minute_delta(),
    )

    schedule = schedule_patch.start()
    yield schedule
    schedule_patch.stop()


@fixture(name="event_loop", scope="session")
def mock_event_loop() -> Generator[AbstractEventLoop, Any, None]:
    """Fixture from creating a asyncio event loop."""
    loop = get_event_loop()
    yield loop
    loop.close()


@fixture(name="tcp_connection")
def mock_tcp_connection() -> Generator[AsyncMock, Any, None]:
    """Fixture for mocking asyncio.open_connection."""
    with patch("aioswitcher.api.open_connection") as conn:
        reader = Mock(StreamReader)
        writer = Mock(StreamWriter)
        conn.return_value = (reader, writer)
        yield reader


@fixture(name="api_stage_success_login")
def mock_api_stage_success_login() -> bytes:
    """Fixture for mocking a success login response from the api."""
    return unhexlify(DUMMY_LOGIN_RESPONSE.encode(ENCODING_CODEC))


@fixture(name="api_stage_failed_login")
def mock_api_stage_fail_login() -> str:
    """Fixture for mocking a failed login response from the api."""
    return DUMMY_LOGIN_RESPONSE


@fixture(name="api_stage_success_get_state")
def mock_api_stage_success_get_state() -> List[bytes]:
    """Fixture for mocking a success get state response from the api."""
    return create_standard_packets_list()


@fixture(name="api_stage_fail_get_state")
def mock_api_stage_fail_get_state() -> Tuple[bytes, str]:
    """Fixture for mocking a failed get state response from the api."""
    return (
        unhexlify(DUMMY_LOGIN_RESPONSE.encode(ENCODING_CODEC)),
        DUMMY_GET_STATE_RESPONSE,
    )


@fixture(name="api_stage_success_control")
def mock_api_stage_success_control() -> List[bytes]:
    """Fixture for mocking a success control response from the api."""
    return create_standard_packets_list(DUMMY_CONTROL_RESPONSE)


@fixture(name="api_stage_success_update_name")
def mock_api_stage_success_update_name() -> List[bytes]:
    """Fixture for mocking a success update_name response from the api."""
    return create_standard_packets_list(DUMMY_UPDATE_NAME_RESPONSE)


@fixture(name="api_stage_success_set_auto_off")
def mock_api_stage_success_set_auto_off() -> List[bytes]:
    """Fixture for mocking a success set_auto_off response from the api."""
    return create_standard_packets_list(DUMMY_SET_AUTO_OFF_RESPONSE)


@fixture(name="api_stage_success_get_schedules")
def mock_api_stage_success_get_schedules() -> List[bytes]:
    """Fixture for mocking a success get_schedules response from the api."""
    return create_standard_packets_list(DUMMY_GET_SCHEDULES_RESPONSE)


@fixture(name="api_stage_success_create_schedule")
def mock_api_stage_success_create_schedule() -> List[bytes]:
    """Fixture for mocking a success create_schedule response from the api."""
    return create_standard_packets_list(DUMMY_CREATE_SCHEDULE_RESPONSE)


@fixture(name="api_stage_success_delete_schedule")
def mock_api_stage_success_delete_schedule() -> List[bytes]:
    """Fixture for mocking a success delete_schedule response from the api."""
    return create_standard_packets_list(DUMMY_DELETE_SCHEDULE_RESPONSE)


@fixture(name="api_stage_success_en_disable_schedule")
def mock_api_stage_success_en_disable_schedule() -> List[bytes]:
    """Fixture for mocking a success enable_disable response from the api."""
    return create_standard_packets_list(DUMMY_DISABLE_ENABLE_SCHEDULE_RESPONSE)


def create_standard_packets_list(
    additional_packet: Union[None, str] = None
) -> List[bytes]:
    """Create a bytes list from the standard packets."""
    packets_list = [
        unhexlify(DUMMY_LOGIN_RESPONSE.encode(ENCODING_CODEC)),
        unhexlify(DUMMY_GET_STATE_RESPONSE.encode(ENCODING_CODEC)),
    ]
    if additional_packet:
        packets_list.append(
            unhexlify(additional_packet.encode(ENCODING_CODEC))
        )
    return packets_list
