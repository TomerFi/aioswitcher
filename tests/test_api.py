"""Test cases for the aioswitcher.api module."""

from asyncio import AbstractEventLoop, StreamReader, StreamWriter, wait
from datetime import timedelta
from typing import List, Tuple

from pytest import mark, raises

from aioswitcher.api import SwitcherV2Api
from aioswitcher.api.messages import ResponseMessageType
from aioswitcher.consts import COMMAND_ON, ENCODING_CODEC, STATE_OFF
from aioswitcher.errors import DecodingError

from .asserters import assert_api_messege_base_type, assert_lists_equal
from .consts import (DUMMY_DEVICE_ID, DUMMY_DEVICE_PASSWORD, DUMMY_IP_ADDRESS,
                      DUMMY_PHONE_ID)


@mark.asyncio
async def test_SwitcherV2Api_login_success(
        event_loop: AbstractEventLoop,
        tcp_connection: Tuple[StreamReader, StreamWriter],
        api_stage_success_login: str) -> None:
    """Test the SwitcherV2Api tcp connection."""
    async with SwitcherV2Api(
            event_loop, DUMMY_IP_ADDRESS, DUMMY_PHONE_ID,
            DUMMY_DEVICE_ID, DUMMY_DEVICE_PASSWORD) as swapi:
        reader, writer = tcp_connection
        reader.read.return_value = api_stage_success_login
        response = await swapi.login()

        assert 'f050834e' == response.session_id
        await assert_api_messege_base_type(response, ResponseMessageType.LOGIN)


@mark.asyncio
async def test_SwitcherV2Api_login_fail(
        event_loop: AbstractEventLoop,
        tcp_connection: Tuple[StreamReader, StreamWriter],
        api_stage_failed_login: str) -> None:
    """Test the SwitcherV2Api tcp connection."""
    async with SwitcherV2Api(
            event_loop, DUMMY_IP_ADDRESS, DUMMY_PHONE_ID,
            DUMMY_DEVICE_ID, DUMMY_DEVICE_PASSWORD) as swapi:
        reader, writer = tcp_connection
        reader.read.return_value = api_stage_failed_login

        with raises(DecodingError) as exc_info:
                await swapi.login()

        assert exc_info.type is DecodingError


@mark.asyncio
async def test_SwitcherV2Api_get_state_success(
        event_loop: AbstractEventLoop,
        tcp_connection: Tuple[StreamReader, StreamWriter],
        api_stage_success_get_state: List[str]) -> None:
    """Test the SwitcherV2Api tcp connection."""
    async with SwitcherV2Api(
            event_loop, DUMMY_IP_ADDRESS, DUMMY_PHONE_ID,
            DUMMY_DEVICE_ID, DUMMY_DEVICE_PASSWORD) as swapi:
        reader, writer = tcp_connection
        reader.read.side_effect = api_stage_success_get_state
        response = await swapi.get_state()

        await wait([response.init_future])

        assert STATE_OFF == response.state
        assert '00:00:00' == response.time_left
        assert '01:30:00' == response.auto_off
        assert 0 == response.power
        assert 0.0 == response.current
    
        await assert_api_messege_base_type(response, ResponseMessageType.STATE)


@mark.asyncio
async def test_SwitcherV2Api_get_state_fail(
        event_loop: AbstractEventLoop,
        tcp_connection: Tuple[StreamReader, StreamWriter],
        api_stage_fail_get_state: List[str]) -> None:
    """Test the SwitcherV2Api tcp connection."""
    async with SwitcherV2Api(
            event_loop, DUMMY_IP_ADDRESS, DUMMY_PHONE_ID,
            DUMMY_DEVICE_ID, DUMMY_DEVICE_PASSWORD) as swapi:
        reader, writer = tcp_connection
        reader.read.side_effect = api_stage_fail_get_state
        response = await swapi.get_state()

        await wait([response.init_future])

        assert response._init_future.exception()


@mark.asyncio
async def test_SwitcherV2Api_control_success(
        event_loop: AbstractEventLoop,
        tcp_connection: Tuple[StreamReader, StreamWriter],
        api_stage_success_control: List[str]) -> None:
    """Test the SwitcherV2Api tcp connection."""
    async with SwitcherV2Api(
            event_loop, DUMMY_IP_ADDRESS, DUMMY_PHONE_ID,
            DUMMY_DEVICE_ID, DUMMY_DEVICE_PASSWORD) as swapi:
        reader, writer = tcp_connection
        reader.read.side_effect = api_stage_success_control
        response = await swapi.control_device(COMMAND_ON)

        await assert_api_messege_base_type(
            response, ResponseMessageType.CONTROL)


@mark.asyncio
async def test_SwitcherV2Api_set_device_name_success(
        event_loop: AbstractEventLoop,
        tcp_connection: Tuple[StreamReader, StreamWriter],
        api_stage_success_update_name: List[str]) -> None:
    """Test the SwitcherV2Api tcp connection."""
    async with SwitcherV2Api(
            event_loop, DUMMY_IP_ADDRESS, DUMMY_PHONE_ID,
            DUMMY_DEVICE_ID, DUMMY_DEVICE_PASSWORD) as swapi:
        reader, writer = tcp_connection
        reader.read.side_effect = api_stage_success_update_name
        response = await swapi.set_device_name('irrelevant')

        await assert_api_messege_base_type(
            response, ResponseMessageType.UPDATE_NAME)


@mark.asyncio
async def test_SwitcherV2Api_set_auto_shutdown_success(
        event_loop: AbstractEventLoop,
        tcp_connection: Tuple[StreamReader, StreamWriter],
        api_stage_success_set_auto_off: List[str]) -> None:
    """Test the SwitcherV2Api tcp connection."""
    async with SwitcherV2Api(
            event_loop, DUMMY_IP_ADDRESS, DUMMY_PHONE_ID,
            DUMMY_DEVICE_ID, DUMMY_DEVICE_PASSWORD) as swapi:
        reader, writer = tcp_connection
        reader.read.side_effect = api_stage_success_set_auto_off
        response = await swapi.set_auto_shutdown(timedelta(hours=1))

        await assert_api_messege_base_type(
            response, ResponseMessageType.AUTO_OFF)


@mark.asyncio
async def test_SwitcherV2Api_get_schedules_success(
        event_loop: AbstractEventLoop,
        tcp_connection: Tuple[StreamReader, StreamWriter],
        api_stage_success_get_schedules: List[str]) -> None:
    """Test the SwitcherV2Api tcp connection."""
    async with SwitcherV2Api(
            event_loop, DUMMY_IP_ADDRESS, DUMMY_PHONE_ID,
            DUMMY_DEVICE_ID, DUMMY_DEVICE_PASSWORD) as swapi:
        reader, writer = tcp_connection
        reader.read.side_effect = api_stage_success_get_schedules
        response = await swapi.get_schedules()

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
            ['0001fc01e871a35cf87fa35c', '01010201e06aa35cf078a35c'])

        await assert_api_messege_base_type(
            response, ResponseMessageType.GET_SCHEDULES)


@mark.asyncio
async def test_SwitcherV2Api_delete_schedule_success(
        event_loop: AbstractEventLoop,
        tcp_connection: Tuple[StreamReader, StreamWriter],
        api_stage_success_delete_schedule: List[str]) -> None:
    """Test the SwitcherV2Api tcp connection."""
    async with SwitcherV2Api(
            event_loop, DUMMY_IP_ADDRESS, DUMMY_PHONE_ID,
            DUMMY_DEVICE_ID, DUMMY_DEVICE_PASSWORD) as swapi:
        reader, writer = tcp_connection
        reader.read.side_effect = api_stage_success_delete_schedule
        response = await swapi.delete_schedule(0)

        await assert_api_messege_base_type(
            response, ResponseMessageType.DELETE_SCHEDULE)


@mark.asyncio
async def test_SwitcherV2Api_create_schedule_success(
        event_loop: AbstractEventLoop,
        tcp_connection: Tuple[StreamReader, StreamWriter],
        api_stage_success_create_schedule: List[str]) -> None:
    """Test the SwitcherV2Api tcp connection."""
    async with SwitcherV2Api(
            event_loop, DUMMY_IP_ADDRESS, DUMMY_PHONE_ID,
            DUMMY_DEVICE_ID, DUMMY_DEVICE_PASSWORD) as swapi:
        reader, writer = tcp_connection
        reader.read.side_effect = api_stage_success_create_schedule
        response = await swapi.create_schedule('')

        await assert_api_messege_base_type(
            response, ResponseMessageType.CREATE_SCHEDULE)


@mark.asyncio
async def test_SwitcherV2Api_disable_enable_schedule_success(
        event_loop: AbstractEventLoop,
        tcp_connection: Tuple[StreamReader, StreamWriter],
        api_stage_success_en_disable_schedule: List[str]) -> None:
    """Test the SwitcherV2Api tcp connection."""
    async with SwitcherV2Api(
            event_loop, DUMMY_IP_ADDRESS, DUMMY_PHONE_ID,
            DUMMY_DEVICE_ID, DUMMY_DEVICE_PASSWORD) as swapi:
        reader, writer = tcp_connection
        reader.read.side_effect = api_stage_success_en_disable_schedule
        response = await swapi.disable_enable_schedule('')

        await assert_api_messege_base_type(
            response, ResponseMessageType.DISABLE_ENABLE_SCHEDULE)
