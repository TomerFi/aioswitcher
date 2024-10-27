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

"""Switcher integration device module tools test cases."""

from binascii import unhexlify
from datetime import datetime, timedelta
from struct import unpack
from unittest.mock import patch

import pytest_asyncio
from assertpy import assert_that
from pytest import mark

from aioswitcher.device import DeviceType, tools


def test_seconds_to_iso_time_with_a_valid_seconds_value_should_return_a_time_string():
    assert_that(tools.seconds_to_iso_time(86399)).is_equal_to("23:59:59")


def test_seconds_to_iso_time_with_a_nagative_value_should_throw_an_error():
    assert_that(tools.seconds_to_iso_time).raises(
        ValueError
    ).when_called_with(-1).is_equal_to("hour must be in 0..23")


def test_minutes_to_hexadecimal_seconds_with_correct_minutes_should_return_expected_hex_seconds():
    # TODO: replace the equality assertion with an unhexlified unpacked value
    hex_sut = tools.minutes_to_hexadecimal_seconds(90)
    assert_that(hex_sut).is_equal_to("18150000")


def test_minutes_to_hexadecimal_seconds_with_a_negative_value_should_throw_an_error():
    assert_that(tools.minutes_to_hexadecimal_seconds).raises(
        Exception
    ).when_called_with(-1).is_equal_to("argument out of range")


def test_timedelta_to_hexadecimal_seconds_with_an_allowed_timedelta_should_return_an_hex_timestamp():
    # TODO: replace the equality assertion with an unhexlified unpacked value
    hex_timestamp = tools.timedelta_to_hexadecimal_seconds(timedelta(hours=1, minutes=30))
    assert_that(hex_timestamp).is_equal_to("18150000")


@mark.parametrize("out_of_range", [timedelta(minutes=59), timedelta(hours=24)])
def test_timedelta_to_hexadecimal_seconds_with_an_out_of_range_value_should_throw_an_error(out_of_range):
    assert_that(tools.timedelta_to_hexadecimal_seconds).raises(
        ValueError
    ).when_called_with(out_of_range).starts_with("can only handle 1 to 24 hours")


def test_string_to_hexadecimale_device_name_with_a_correct_length_name_should_return_a_right_zero_padded_hex_name():
    str_name = "my device cool name"
    hex_name = tools.string_to_hexadecimale_device_name(str_name)
    unhexed_name = unhexlify(hex_name.rstrip("0")).decode()
    assert_that(unhexed_name).is_equal_to(str_name)


@mark.parametrize("unsupported_length_value", ["t", "t" * 33])
def test_string_to_hexadecimale_device_name_with_an_unsupported_length_value_should_throw_an_error(unsupported_length_value):
    assert_that(tools.string_to_hexadecimale_device_name).raises(
        ValueError
    ).when_called_with(unsupported_length_value).starts_with("name length can vary from 2 to 32")


def test_current_timestamp_to_hexadecimal_should_return_the_current_timestamp():
    hex_timestamp = tools.current_timestamp_to_hexadecimal()

    binary_timestamp = unhexlify(hex_timestamp.encode())
    unpacked_timestamp = unpack("<I", binary_timestamp)
    sut_datetime = datetime.fromtimestamp(unpacked_timestamp[0])

    assert_that(sut_datetime).is_equal_to_ignoring_time(datetime.now())


@patch("time.time", return_value=-1)
def test_current_timestamp_to_hexadecimal_with_errornous_value_should_throw_an_error(_):
    assert_that(tools.current_timestamp_to_hexadecimal).raises(
        Exception
    ).when_called_with().is_equal_to("argument out of range")


@mark.parametrize("watts, amps", [(1608, 7.3), (2600, 11.8), (3489, 15.9)])
def test_watts_to_amps_with_parameterized_watts_should_procude_expected_amps(watts, amps):
    assert_that(tools.watts_to_amps(watts)).is_equal_to(amps)


@mark.parametrize("str, type", [
    ("Switcher Mini", DeviceType.MINI),
    ("Switcher Power Plug", DeviceType.POWER_PLUG),
    ("Switcher Touch", DeviceType.TOUCH),
    ("Switcher V2 (esp)", DeviceType.V2_ESP),
    ("Switcher V2 (qualcomm)", DeviceType.V2_QCA),
    ("Switcher V4", DeviceType.V4),
    ("Switcher Breeze", DeviceType.BREEZE),
    ("Switcher Runner", DeviceType.RUNNER),
    ("Switcher Runner Mini", DeviceType.RUNNER_MINI),
    ("Switcher Runner S11", DeviceType.RUNNER_S11),
    ("Switcher Runner S12", DeviceType.RUNNER_S12),
    ("Switcher Light SL01", DeviceType.LIGHT_SL01),
    ("Switcher Light SL01 Mini", DeviceType.LIGHT_SL01_MINI),
    ("Switcher Light SL02", DeviceType.LIGHT_SL02),
    ("Switcher Light SL02 Mini", DeviceType.LIGHT_SL02_MINI),
    ])
def test_convert_str_to_devicetype_should_return_expected_devicetype(str, type):
    assert_that(tools.convert_str_to_devicetype(str)).is_equal_to(type)


@mark.parametrize("str, type", [
    ("Switcher new device does not define", DeviceType.MINI)
    ])
def test_convert_str_to_devicetype_with_unknown_device_should_return_mini(str, type):
    assert_that(tools.convert_str_to_devicetype(str)).is_equal_to(type)


@mark.parametrize("token, token_packet", [
    ("zvVvd7JxtN7CgvkD1Psujw==", "eafc3e34")
    ])
def test_convert_token_to_packet_should_return_expected_packet(token, token_packet):
    assert_that(tools.convert_token_to_packet(token)).is_equal_to(token_packet)


@mark.parametrize("token, error_type, response", [
    ("zvVvd7JxtN7Cg==", RuntimeError, "convert token to packet was not successful"),
    ("zvVvd7J", RuntimeError, "convert token to packet was not successful")
    ])
def test_convert_token_to_packet_with_false_token_should_throw_an_error(token, error_type, response):
    assert_that(tools.convert_token_to_packet).raises(
        error_type
    ).when_called_with(token).is_equal_to(response)


@pytest_asyncio.fixture
@mark.parametrize("username, token, is_token_valid", [
    ("test@switcher.com", "zvVvd7JxtN7CgvkD1Psujw==", True)
    ])
async def test_validate_token_should_return_token_valid(mock_post, username, token, is_token_valid):
    mock_response = mock_post.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": "True"}
    assert_that(tools.validate_token(username, token)).is_equal_to(is_token_valid)


@pytest_asyncio.fixture
@mark.parametrize("username, token, is_token_valid", [
    ("test@switcher.com", "", False),
    ("test@switcher.com", "notvalidtoken", False),
    ("", "notvalidtoken", False),
    ("", "", False)
    ])
async def test_validate_token_should_return_token_invalid(mock_post, username, token, is_token_valid):
    mock_response = mock_post.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": "False"}
    assert_that(tools.validate_token(username, token)).is_equal_to(is_token_valid)


@mark.parametrize("device_type, circuit_number, index", [
    (DeviceType.RUNNER, 0, 0),
    (DeviceType.RUNNER_MINI, 0, 0),
    (DeviceType.RUNNER_S11, 0, 2),
    (DeviceType.RUNNER_S12, 0, 1),
    (DeviceType.RUNNER_S12, 1, 2),
    ])
def test_get_shutter_discovery_packet_index_should_return_expected_index(device_type, circuit_number, index):
    assert_that(tools.get_shutter_discovery_packet_index(device_type, circuit_number)).is_equal_to(index)


@mark.parametrize("device_type, circuit_number, error, error_msg", [
    (DeviceType.RUNNER, 1, ValueError, "Invalid circuit number"),
    (DeviceType.RUNNER_MINI, 1, ValueError, "Invalid circuit number"),
    (DeviceType.RUNNER_S11, 1, ValueError, "Invalid circuit number"),
    (DeviceType.RUNNER_S12, 2, ValueError, "Invalid circuit number"),
    ])
def test_get_shutter_discovery_packet_index_with_invalid_circuit_number_should_raise_error(device_type, circuit_number, error, error_msg):
    assert_that(tools.get_shutter_discovery_packet_index).raises(error).when_called_with(
        device_type,
        circuit_number
    ).is_equal_to(error_msg)


@mark.parametrize("device_type, circuit_number, error, error_msg", [
    (DeviceType.TOUCH, 0, ValueError, "only shutters are allowed")
    ])
def test_get_shutter_discovery_packet_index_with_different_device_should_raise_error(device_type, circuit_number, error, error_msg):
    assert_that(tools.get_shutter_discovery_packet_index).raises(error).when_called_with(
        device_type,
        circuit_number
    ).is_equal_to(error_msg)


@mark.parametrize("device_type, circuit_number, index", [
    (DeviceType.RUNNER_S11, 0, 0),
    (DeviceType.RUNNER_S11, 1, 1),
    (DeviceType.RUNNER_S12, 0, 0),
    (DeviceType.LIGHT_SL01, 0, 0),
    (DeviceType.LIGHT_SL01_MINI, 0, 0),
    (DeviceType.LIGHT_SL02, 0, 0),
    (DeviceType.LIGHT_SL02, 1, 1),
    (DeviceType.LIGHT_SL02_MINI, 0, 0),
    (DeviceType.LIGHT_SL02_MINI, 1, 1),
    ])
def test_get_light_discovery_packet_index_should_return_expected_index(device_type, circuit_number, index):
    assert_that(tools.get_light_discovery_packet_index(device_type, circuit_number)).is_equal_to(index)


@mark.parametrize("device_type, circuit_number, error, error_msg", [
    (DeviceType.RUNNER_S11, 2, ValueError, "Invalid circuit number"),
    (DeviceType.RUNNER_S12, 1, ValueError, "Invalid circuit number"),
    (DeviceType.LIGHT_SL01, 1, ValueError, "Invalid circuit number"),
    (DeviceType.LIGHT_SL01_MINI, 1, ValueError, "Invalid circuit number"),
    (DeviceType.LIGHT_SL02, 2, ValueError, "Invalid circuit number"),
    (DeviceType.LIGHT_SL02_MINI, 2, ValueError, "Invalid circuit number"),
    ])
def test_get_light_discovery_packet_index_with_invalid_circuit_number_should_raise_error(device_type, circuit_number, error, error_msg):
    assert_that(tools.get_light_discovery_packet_index).raises(error).when_called_with(
        device_type,
        circuit_number
    ).is_equal_to(error_msg)


@mark.parametrize("device_type, circuit_number, error, error_msg", [
    (DeviceType.TOUCH, 0, ValueError, "only devices that has lights are allowed")
    ])
def test_get_light_discovery_packet_index_with_different_device_should_raise_error(device_type, circuit_number, error, error_msg):
    assert_that(tools.get_light_discovery_packet_index).raises(error).when_called_with(
        device_type,
        circuit_number
    ).is_equal_to(error_msg)


@mark.parametrize("device_type, circuit_number, index", [
    (DeviceType.RUNNER, 0, 1),
    (DeviceType.RUNNER_MINI, 0, 1),
    (DeviceType.RUNNER_S11, 0, 3),
    (DeviceType.RUNNER_S12, 0, 2),
    (DeviceType.RUNNER_S12, 1, 3),
    ])
def test_get_shutter_api_packet_index_should_return_expected_index(device_type, circuit_number, index):
    assert_that(tools.get_shutter_api_packet_index(device_type, circuit_number)).is_equal_to(index)


@mark.parametrize("device_type, circuit_number, error, error_msg", [
    (DeviceType.RUNNER, 1, ValueError, "Invalid circuit number"),
    (DeviceType.RUNNER_MINI, 1, ValueError, "Invalid circuit number"),
    (DeviceType.RUNNER_S11, 1, ValueError, "Invalid circuit number"),
    (DeviceType.RUNNER_S12, 2, ValueError, "Invalid circuit number"),
    ])
def test_get_shutter_api_packet_index_with_invalid_circuit_number_should_raise_error(device_type, circuit_number, error, error_msg):
    assert_that(tools.get_shutter_api_packet_index).raises(error).when_called_with(
        device_type,
        circuit_number
    ).is_equal_to(error_msg)


@mark.parametrize("device_type, circuit_number, error, error_msg", [
    (DeviceType.TOUCH, 0, ValueError, "only shutters are allowed")
    ])
def test_get_shutter_api_packet_index_with_different_device_should_raise_error(device_type, circuit_number, error, error_msg):
    assert_that(tools.get_shutter_api_packet_index).raises(error).when_called_with(
        device_type,
        circuit_number
    ).is_equal_to(error_msg)


@mark.parametrize("device_type, circuit_number, index", [
    (DeviceType.RUNNER_S11, 0, 1),
    (DeviceType.RUNNER_S11, 1, 2),
    (DeviceType.RUNNER_S12, 0, 1),
    (DeviceType.LIGHT_SL01, 0, 1),
    (DeviceType.LIGHT_SL01_MINI, 0, 1),
    (DeviceType.LIGHT_SL02, 0, 1),
    (DeviceType.LIGHT_SL02, 1, 2),
    (DeviceType.LIGHT_SL02_MINI, 0, 1),
    (DeviceType.LIGHT_SL02_MINI, 1, 2),
    ])
def test_get_light_api_packet_index_should_return_expected_index(device_type, circuit_number, index):
    assert_that(tools.get_light_api_packet_index(device_type, circuit_number)).is_equal_to(index)


@mark.parametrize("device_type, circuit_number, error, error_msg", [
    (DeviceType.RUNNER_S11, 2, ValueError, "Invalid circuit number"),
    (DeviceType.RUNNER_S12, 1, ValueError, "Invalid circuit number"),
    (DeviceType.LIGHT_SL01, 1, ValueError, "Invalid circuit number"),
    (DeviceType.LIGHT_SL01_MINI, 1, ValueError, "Invalid circuit number"),
    (DeviceType.LIGHT_SL02, 2, ValueError, "Invalid circuit number"),
    (DeviceType.LIGHT_SL02_MINI, 2, ValueError, "Invalid circuit number"),
    ])
def test_get_light_api_packet_index_with_invalid_circuit_number_should_raise_error(device_type, circuit_number, error, error_msg):
    assert_that(tools.get_light_api_packet_index).raises(error).when_called_with(
        device_type,
        circuit_number
    ).is_equal_to(error_msg)


@mark.parametrize("device_type, circuit_number, error, error_msg", [
    (DeviceType.TOUCH, 0, ValueError, "only devices that has lights are allowed")
    ])
def test_get_light_api_packet_index_with_different_device_should_raise_error(device_type, circuit_number, error, error_msg):
    assert_that(tools.get_light_api_packet_index).raises(error).when_called_with(
        device_type,
        circuit_number
    ).is_equal_to(error_msg)
