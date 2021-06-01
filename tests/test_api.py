"""Test cases for the aioswitcher.api module."""

# fmt: off
from asyncio import AbstractEventLoop, wait
from datetime import timedelta
from typing import List, Tuple

from pytest import mark, raises

from aioswitcher.api import SwitcherV2Api
from aioswitcher.api.messages import ResponseMessageType
from aioswitcher.consts import COMMAND_ON, STATE_OFF
from aioswitcher.errors import DecodingError
from tests.async_mock import AsyncMock

from .asserters import assert_api_messege_base_type, assert_lists_equal
from .consts import DUMMY_DEVICE_ID, DUMMY_IP_ADDRESS

# fmt: on


@mark.asyncio
async def test_api_login_success(
    event_loop: AbstractEventLoop,
    tcp_connection: AsyncMock,
    api_stage_success_login: bytes,
) -> None:
    """Test the SwitcherV2Api successful login."""
    async with SwitcherV2Api(
        event_loop,
        DUMMY_IP_ADDRESS,
        DUMMY_DEVICE_ID,
    ) as swapi:
        reader = tcp_connection
        reader.read.return_value = api_stage_success_login
        response = await swapi.login()

        assert response
        assert response.session_id == "f050834e"

        await assert_api_messege_base_type(response, ResponseMessageType.LOGIN)


@mark.asyncio
async def test_api_login_fail(
    event_loop: AbstractEventLoop,
    tcp_connection: AsyncMock,
    api_stage_failed_login: bytes,
) -> None:
    """Test the SwitcherV2Api failed login."""
    async with SwitcherV2Api(
        event_loop,
        DUMMY_IP_ADDRESS,
        DUMMY_DEVICE_ID,
    ) as swapi:
        reader = tcp_connection
        reader.read.return_value = api_stage_failed_login

        with raises(DecodingError) as exc_info:
            await swapi.login()

        assert exc_info.type is DecodingError


@mark.asyncio
async def test_api_get_state_success(
    event_loop: AbstractEventLoop,
    tcp_connection: AsyncMock,
    api_stage_success_get_state: List[bytes],
) -> None:
    """Test the SwitcherV2Api successful get_state."""
    async with SwitcherV2Api(
        event_loop,
        DUMMY_IP_ADDRESS,
        DUMMY_DEVICE_ID,
    ) as swapi:
        reader = tcp_connection
        reader.read.side_effect = api_stage_success_get_state
        response = await swapi.get_state()

        assert response

        await wait([response.init_future])

        assert response.state == STATE_OFF
        assert response.time_left == "00:00:00"
        assert response.time_on == "00:00:00"
        assert response.auto_off == "01:30:00"
        assert response.power == 0
        assert response.current == 0.0

        await assert_api_messege_base_type(response, ResponseMessageType.STATE)


@mark.asyncio
async def test_api_get_state_fail(
    event_loop: AbstractEventLoop,
    tcp_connection: AsyncMock,
    api_stage_fail_get_state: Tuple[bytes, str],
) -> None:
    """Test the SwitcherV2Api failed get_state."""
    async with SwitcherV2Api(
        event_loop,
        DUMMY_IP_ADDRESS,
        DUMMY_DEVICE_ID,
    ) as swapi:
        reader = tcp_connection
        reader.read.side_effect = api_stage_fail_get_state
        response = await swapi.get_state()

        assert response

        await wait([response.init_future])

        assert response.init_future.exception()


@mark.asyncio
async def test_api_control_success(
    event_loop: AbstractEventLoop,
    tcp_connection: AsyncMock,
    api_stage_success_control: List[bytes],
) -> None:
    """Test the SwitcherV2Api successful control."""
    async with SwitcherV2Api(
        event_loop,
        DUMMY_IP_ADDRESS,
        DUMMY_DEVICE_ID,
    ) as swapi:
        reader = tcp_connection
        reader.read.side_effect = api_stage_success_control
        response = await swapi.control_device(COMMAND_ON)

        await assert_api_messege_base_type(
            response, ResponseMessageType.CONTROL
        )


@mark.asyncio
async def test_api_set_device_name_success(
    event_loop: AbstractEventLoop,
    tcp_connection: AsyncMock,
    api_stage_success_update_name: List[bytes],
) -> None:
    """Test the SwitcherV2Api successful set_device_name."""
    async with SwitcherV2Api(
        event_loop,
        DUMMY_IP_ADDRESS,
        DUMMY_DEVICE_ID,
    ) as swapi:
        reader = tcp_connection
        reader.read.side_effect = api_stage_success_update_name
        response = await swapi.set_device_name("irrelevant")

        await assert_api_messege_base_type(
            response, ResponseMessageType.UPDATE_NAME
        )


@mark.asyncio
async def test_api_set_auto_shutdown_success(
    event_loop: AbstractEventLoop,
    tcp_connection: AsyncMock,
    api_stage_success_set_auto_off: List[bytes],
) -> None:
    """Test the SwitcherV2Api successful set_auto_shutdown."""
    async with SwitcherV2Api(
        event_loop,
        DUMMY_IP_ADDRESS,
        DUMMY_DEVICE_ID,
    ) as swapi:
        reader = tcp_connection
        reader.read.side_effect = api_stage_success_set_auto_off
        response = await swapi.set_auto_shutdown(timedelta(hours=1))

        await assert_api_messege_base_type(
            response, ResponseMessageType.AUTO_OFF
        )


@mark.asyncio
async def test_api_get_schedules_success(
    event_loop: AbstractEventLoop,
    tcp_connection: AsyncMock,
    api_stage_success_get_schedules: List[bytes],
) -> None:
    """Test the SwitcherV2Api successful get_schedules."""
    async with SwitcherV2Api(
        event_loop,
        DUMMY_IP_ADDRESS,
        DUMMY_DEVICE_ID,
    ) as swapi:
        reader = tcp_connection
        reader.read.side_effect = api_stage_success_get_schedules
        response = await swapi.get_schedules()

        assert response
        assert response.found_schedules

        futures = []
        for schedule in response.get_schedules:
            futures.append(schedule.init_future)
        await wait(futures)

        schedule_data_list = []
        for fut in futures:
            schedule_data_list.append(fut.result().schedule_data)

        await assert_lists_equal(
            schedule_data_list,
            ["0001fc01e871a35cf87fa35c", "01010201e06aa35cf078a35c"],
        )

        await assert_api_messege_base_type(
            response, ResponseMessageType.GET_SCHEDULES
        )


@mark.asyncio
async def test_api_delete_schedule_success(
    event_loop: AbstractEventLoop,
    tcp_connection: AsyncMock,
    api_stage_success_delete_schedule: List[bytes],
) -> None:
    """Test the SwitcherV2Api successful delete_schedule."""
    async with SwitcherV2Api(
        event_loop,
        DUMMY_IP_ADDRESS,
        DUMMY_DEVICE_ID,
    ) as swapi:
        reader = tcp_connection
        reader.read.side_effect = api_stage_success_delete_schedule
        response = await swapi.delete_schedule("0")

        await assert_api_messege_base_type(
            response, ResponseMessageType.DELETE_SCHEDULE
        )


@mark.asyncio
async def test_api_create_schedule_success(
    event_loop: AbstractEventLoop,
    tcp_connection: AsyncMock,
    api_stage_success_create_schedule: List[bytes],
) -> None:
    """Test the SwitcherV2Api successful create_schedule."""
    async with SwitcherV2Api(
        event_loop,
        DUMMY_IP_ADDRESS,
        DUMMY_DEVICE_ID,
    ) as swapi:
        reader = tcp_connection
        reader.read.side_effect = api_stage_success_create_schedule
        response = await swapi.create_schedule("")

        await assert_api_messege_base_type(
            response, ResponseMessageType.CREATE_SCHEDULE
        )


@mark.asyncio
async def test_api_disable_enable_schedule_success(
    event_loop: AbstractEventLoop,
    tcp_connection: AsyncMock,
    api_stage_success_en_disable_schedule: List[bytes],
) -> None:
    """Test the SwitcherV2Api successful disable_enable_schedule."""
    async with SwitcherV2Api(
        event_loop,
        DUMMY_IP_ADDRESS,
        DUMMY_DEVICE_ID,
    ) as swapi:
        reader = tcp_connection
        reader.read.side_effect = api_stage_success_en_disable_schedule
        response = await swapi.disable_enable_schedule("")

        await assert_api_messege_base_type(
            response, ResponseMessageType.DISABLE_ENABLE_SCHEDULE
        )
