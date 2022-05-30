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

"""Switcher integration packet crc signing test cases."""

from binascii import hexlify
from struct import pack

from assertpy import assert_that

from aioswitcher.api import Command, packets
from aioswitcher.device.tools import sign_packet_with_crc_key

SUT_TIMESTAMP = "ef8db35c"
SUT_SESSION_ID = "01000000"
SUT_DEVICE_ID = "a123bc"


def test_sign_packet_with_crc_key_for_a_random_string_throws_error():
    """Test the sign_packet_with_crc_key tool with a random string unqualified as a packet."""
    assert_that(sign_packet_with_crc_key).raises(ValueError).when_called_with(
        "just a regular string"
    ).is_equal_to("Odd-length string")


def test_sign_packet_with_crc_key_for_login_packet_returns_signed_packet():
    """Test the sign_packet_with_crc_key tool for the LOGIN_PACKET."""
    packet = packets.LOGIN_PACKET_TYPE1.format(SUT_TIMESTAMP)
    assert_that(sign_packet_with_crc_key(packet)).is_equal_to(packet + "627f33f1")


def test_sign_packet_with_crc_key_for_get_state_packet_returns_signed_packet():
    """Test the sign_packet_with_crc_key tool for the GET_STATE_PACKET."""
    packet = packets.GET_STATE_PACKET_TYPE1.format(
        SUT_SESSION_ID, SUT_TIMESTAMP, SUT_DEVICE_ID
    )
    assert_that(sign_packet_with_crc_key(packet)).is_equal_to(packet + "42a9a1b2")


def test_sign_packet_with_crc_key_for_send_control_on_with_no_timer_packet_returns_signed_packet():
    """Test the sign_packet_with_crc_key tool for the SEND_CONTROL_PACKET for on state with no timer."""
    packet = packets.SEND_CONTROL_PACKET.format(
        SUT_SESSION_ID,
        SUT_TIMESTAMP,
        SUT_DEVICE_ID,
        Command.ON.value,
        packets.NO_TIMER_REQUESTED,
    )
    assert_that(sign_packet_with_crc_key(packet)).is_equal_to(packet + "cc06bb10")


def test_sign_packet_with_crc_key_for_send_control_off_packet_returns_signed_packet():
    """Test the sign_packet_with_crc_key tool for the SEND_CONTROL_PACKET for off state."""
    packet = packets.SEND_CONTROL_PACKET.format(
        SUT_SESSION_ID,
        SUT_TIMESTAMP,
        SUT_DEVICE_ID,
        Command.OFF.value,
        packets.NO_TIMER_REQUESTED,
    )
    assert_that(sign_packet_with_crc_key(packet)).is_equal_to(packet + "6c432cf4")


def test_sign_packet_with_crc_key_for_send_control_on_with_timer_packet_returns_signed_packet():
    """Test the sign_packet_with_crc_key tool for the SEND_CONTROL_PACKET for on state with a 90 minutes timer."""
    timer_minutes = hexlify(pack("<I", 5400)).decode()
    packet = packets.SEND_CONTROL_PACKET.format(
        SUT_SESSION_ID, SUT_TIMESTAMP, SUT_DEVICE_ID, Command.ON.value, timer_minutes
    )
    assert_that(sign_packet_with_crc_key(packet)).is_equal_to(packet + "3b30141e")


def test_sign_packet_with_crc_key_for_set_auto_off_packet_returns_signed_packet():
    """Test the sign_packet_with_crc_key tool for the SET_AUTO_OFF_SET_PACKET with a 90 minutes auto-shutdown."""
    auto_shutdown = hexlify(pack("<I", 5400)).decode()
    packet = packets.SET_AUTO_OFF_SET_PACKET.format(
        SUT_SESSION_ID, SUT_TIMESTAMP, SUT_DEVICE_ID, auto_shutdown
    )
    assert_that(sign_packet_with_crc_key(packet)).is_equal_to(packet + "3bb1ca55")


def test_sign_packet_with_crc_key_for_set_device_name_packet_returns_signed_packet():
    """Test the sign_packet_with_crc_key tool for the UPDATE_DEVICE_NAME_PACKET with a 'my device cool name'."""
    desired_name = "my device cool name"
    hex_name = hexlify(desired_name.encode())
    zeros_pad = ("00" * (32 - len(desired_name))).encode()
    packet = packets.UPDATE_DEVICE_NAME_PACKET.format(
        SUT_SESSION_ID, SUT_TIMESTAMP, SUT_DEVICE_ID, (hex_name + zeros_pad).decode()
    )
    assert_that(sign_packet_with_crc_key(packet)).is_equal_to(packet + "1039bc0e")


def test_sign_packet_with_crc_key_for_get_schedules_packet_returns_signed_packet():
    """Test the sign_packet_with_crc_key tool for the GET_SCHEDULES_PACKET."""
    packet = packets.GET_SCHEDULES_PACKET.format(
        SUT_SESSION_ID, SUT_TIMESTAMP, SUT_DEVICE_ID
    )
    assert_that(sign_packet_with_crc_key(packet)).is_equal_to(packet + "0efde536")
