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

"""Switcher integration broadcast message parsing utility functions test cases."""

from binascii import unhexlify
from pathlib import Path

from assertpy import assert_that
from pytest import mark

from aioswitcher.bridge import DatagramParser
from aioswitcher.device import DeviceState, DeviceType


@mark.parametrize(
    "type_suffix, expected_type",
    [
        ("mini", DeviceType.MINI),
        ("power_plug", DeviceType.POWER_PLUG),
        ("touch", DeviceType.TOUCH),
        ("v2_esp", DeviceType.V2_ESP),
        ("v2_qca", DeviceType.V2_QCA),
        ("v4", DeviceType.V4),
    ],
)
def test_datagram_state_off(resource_path, type_suffix, expected_type):
    sut_datagram = (
        Path(f"{resource_path}_{type_suffix}.txt")
        .read_text()
        .replace("\n", "")
        .encode()
    )

    sut_parser = DatagramParser(unhexlify(sut_datagram))

    assert_that(sut_parser.is_switcher_originator()).is_true()
    assert_that(sut_parser.get_ip_type1()).is_equal_to("192.168.1.33")
    assert_that(sut_parser.get_mac()).is_equal_to("12:A1:A2:1A:BC:1A")
    assert_that(sut_parser.get_name()).is_equal_to("My Switcher Boiler")
    assert_that(sut_parser.get_device_id()).is_equal_to("aaaaaa")
    assert_that(sut_parser.get_device_state()).is_equal_to(DeviceState.OFF)
    assert_that(sut_parser.get_device_type()).is_equal_to(expected_type)
    assert_that(sut_parser.get_power_consumption()).is_equal_to(0)
    if not expected_type == DeviceType.POWER_PLUG:
        assert_that(sut_parser.get_remaining()).is_equal_to("00:00:00")
        assert_that(sut_parser.get_auto_shutdown()).is_equal_to("03:00:00")


@mark.parametrize(
    "type_suffix, expected_type",
    [
        ("mini", DeviceType.MINI),
        ("power_plug", DeviceType.POWER_PLUG),
        ("touch", DeviceType.TOUCH),
        ("v2_esp", DeviceType.V2_ESP),
        ("v2_qca", DeviceType.V2_QCA),
        ("v4", DeviceType.V4),
    ],
)
def test_datagram_state_on(resource_path, type_suffix, expected_type):
    sut_datagram = (
        Path(f"{resource_path}_{type_suffix}.txt")
        .read_text()
        .replace("\n", "")
        .encode()
    )

    sut_parser = DatagramParser(unhexlify(sut_datagram))

    assert_that(sut_parser.is_switcher_originator()).is_true()
    assert_that(sut_parser.get_ip_type1()).is_equal_to("192.168.1.33")
    assert_that(sut_parser.get_mac()).is_equal_to("12:A1:A2:1A:BC:1A")
    assert_that(sut_parser.get_name()).is_equal_to("My Switcher Boiler")
    assert_that(sut_parser.get_device_id()).is_equal_to("aaaaaa")
    assert_that(sut_parser.get_device_state()).is_equal_to(DeviceState.ON)
    assert_that(sut_parser.get_device_type()).is_equal_to(expected_type)
    assert_that(sut_parser.get_power_consumption()).is_equal_to(2600)
    if not expected_type == DeviceType.POWER_PLUG:
        assert_that(sut_parser.get_remaining()).is_equal_to("01:30:00")
        assert_that(sut_parser.get_auto_shutdown()).is_equal_to("03:00:00")


@mark.parametrize("type_suffix", ["too_short", "wrong_start"])
def test_a_faulty_datagram(resource_path, type_suffix):
    sut_datagram = (
        Path(f"{resource_path}_{type_suffix}.txt")
        .read_text()
        .replace("\n", "")
        .encode()
    )
    sut_parser = DatagramParser(unhexlify(sut_datagram))
    assert_that(sut_parser.is_switcher_originator()).is_false()
