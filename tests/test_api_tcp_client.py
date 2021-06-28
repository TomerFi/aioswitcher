# Copyright Tomer Figenblat.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Switcher unofficial integration TCP socket API module test cases."""

from asyncio.streams import StreamReader, StreamWriter
from binascii import unhexlify
from datetime import timedelta
from unittest.mock import AsyncMock, Mock, patch

from assertpy import assert_that
from pytest import fixture, mark, raises

from aioswitcher.api import SwitcherApi
from aioswitcher.api.messages import (
    SwitcherBaseResponse,
    SwitcherGetSchedulesResponse,
    SwitcherLoginResponse,
    SwitcherStateResponse,
)

device_id = "aaaaaa"
device_ip = "1.2.3.4"
pytestmark = mark.asyncio


@fixture
def writer_write():
    return Mock()


@fixture
def reader_mock():
    return AsyncMock(spec_set=StreamReader)


@fixture
def writer_mock(writer_write):
    writer = AsyncMock(spec_set=StreamWriter)
    writer.write = writer_write
    return writer


@fixture
async def connected_api(reader_mock, writer_mock):
    with patch("aioswitcher.api.open_connection", return_value=(reader_mock, writer_mock)):
        api = SwitcherApi(device_ip, device_id)
        await api.connect()
        yield api
        await api.disconnect()


@patch("logging.Logger.info")
async def test_stopping_before_started_and_connected_should_write_to_the_info_output(mock_info):
    api = SwitcherApi(device_ip, device_id)
    assert_that(api.connected).is_false()
    await api.disconnect()
    mock_info.assert_called_with("switcher device not connected")


async def test_api_as_a_context_manager(reader_mock, writer_mock):
    with patch("aioswitcher.api.open_connection", return_value=(reader_mock, writer_mock)):
        async with SwitcherApi(device_ip, device_id) as api:
            assert_that(api.connected).is_true()


async def test_login_function(reader_mock, writer_write, connected_api, resource_path_root):
    response_packet = _load_packet(resource_path_root, "login_response")
    with patch.object(reader_mock, "read", return_value=response_packet):
        response = await connected_api._login()
    writer_write.assert_called_once()
    assert_that(response[1]).is_instance_of(SwitcherLoginResponse)
    assert_that(response[1].unparsed_response).is_equal_to(response_packet)


async def test_get_full_state_function_with_valid_packets(reader_mock, writer_write, connected_api, resource_path_root):
    login_response_packet = _load_packet(resource_path_root, "login_response")
    get_state_response_packet = _load_packet(resource_path_root, "get_state_response")
    with patch.object(reader_mock, "read", side_effect=[login_response_packet, get_state_response_packet]):
        response = await connected_api._get_full_state()
    assert_that(writer_write.call_count).is_equal_to(2)
    assert_that(response[2]).is_instance_of(SwitcherStateResponse)
    assert_that(response[2].unparsed_response).is_equal_to(get_state_response_packet)


async def test_get_full_state_function_with_a_faulty_login_response_should_raise_error(reader_mock, writer_write, connected_api):
    with raises(RuntimeError, match="login request was not successful"):
        with patch.object(reader_mock, "read", return_value=b''):
            await connected_api._get_full_state()
    writer_write.assert_called_once()


async def test_get_full_state_function_with_a_faulty_get_state_response_should_raise_error(reader_mock, writer_write, connected_api, resource_path_root):
    login_response_packet = _load_packet(resource_path_root, "login_response")
    with raises(RuntimeError, match="get state request was not successful"):
        with patch.object(reader_mock, "read", side_effect=[login_response_packet, b'']):
            await connected_api._get_full_state()
    assert_that(writer_write.call_count).is_equal_to(2)


async def test_get_state_function_with_valid_packets(reader_mock, writer_write, connected_api, resource_path_root):
    login_response_packet = _load_packet(resource_path_root, "login_response")
    get_state_response_packet = _load_packet(resource_path_root, "get_state_response")
    with patch.object(reader_mock, "read", side_effect=[login_response_packet, get_state_response_packet]):
        response = await connected_api.get_state()
    assert_that(writer_write.call_count).is_equal_to(2)
    assert_that(response).is_instance_of(SwitcherStateResponse)
    assert_that(response.unparsed_response).is_equal_to(get_state_response_packet)


async def test_set_auto_shutdown_function_with_valid_packets(reader_mock, writer_write, connected_api, resource_path_root):
    three_packets = _get_three_packets(resource_path_root, "set_auto_shutdown_response")
    with patch.object(reader_mock, "read", side_effect=three_packets):
        response = await connected_api.set_auto_shutdown(timedelta(hours=2, minutes=30))
    assert_that(writer_write.call_count).is_equal_to(3)
    assert_that(response).is_instance_of(SwitcherBaseResponse)
    assert_that(response.unparsed_response).is_equal_to(three_packets[-1])


async def test_get_schedules_function_with_valid_packets(reader_mock, writer_write, connected_api, resource_path_root):
    three_packets = _get_three_packets(resource_path_root, "get_schedules_response")
    with patch.object(reader_mock, "read", side_effect=three_packets):
        response = await connected_api.get_schedules()
    assert_that(writer_write.call_count).is_equal_to(3)
    assert_that(response).is_instance_of(SwitcherGetSchedulesResponse)
    assert_that(response.unparsed_response).is_equal_to(three_packets[-1])


async def test_delete_schedule_function_with_valid_packets(reader_mock, writer_write, connected_api, resource_path_root):
    three_packets = _get_three_packets(resource_path_root, "delete_schedule_response")
    with patch.object(reader_mock, "read", side_effect=three_packets):
        response = await connected_api.delete_schedule("0")
    assert_that(writer_write.call_count).is_equal_to(3)
    assert_that(response).is_instance_of(SwitcherBaseResponse)
    assert_that(response.unparsed_response).is_equal_to(three_packets[-1])


async def test_create_schedule_function_with_valid_packets(reader_mock, writer_write, connected_api, resource_path_root):
    three_packets = _get_three_packets(resource_path_root, "create_schedule_response")
    with patch.object(reader_mock, "read", side_effect=three_packets):
        response = await connected_api.create_schedule("18:00", "19:00")
    assert_that(writer_write.call_count).is_equal_to(3)
    assert_that(response).is_instance_of(SwitcherBaseResponse)
    assert_that(response.unparsed_response).is_equal_to(three_packets[-1])


def _get_three_packets(resource_path_root, third_packet):
    return [
        _load_packet(resource_path_root, "login_response"),
        _load_packet(resource_path_root, "get_state_response"),
        _load_packet(resource_path_root, third_packet),
    ]


def _load_packet(path, file_name):
    return unhexlify((path / ("dummy_responses/" + file_name + ".txt")).read_text().replace('\n', '').encode())
