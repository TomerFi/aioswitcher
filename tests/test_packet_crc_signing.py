"""Switcher water heater packet crc signing test cases."""

from binascii import hexlify
from struct import pack

from assertpy import assert_that

from aioswitcher import consts
from aioswitcher.api import packets
from aioswitcher.errors import EncodingError
from aioswitcher.utils import sign_packet_with_crc_key

SUT_DEVICE_ID = "a123bc"
SUT_SESSION_ID = "01000000"
SUT_TIMESTAMP = "ef8db35c"


def test_sign_packet_with_crc_key_for_a_random_string_throws_error():
    """Test the sign_packet_with_crc_key tool with a random string unqualified as a packet."""
    assert_that(sign_packet_with_crc_key).raises(
        EncodingError
    ).when_called_with("just a regular string").is_equal_to("failed to sign crc")


def test_sign_packet_with_crc_key_for_login_packet_returns_signed_packet():
    """Test the sign_packet_with_crc_key tool for the LOGIN_PACKET."""
    packet = packets.LOGIN_PACKET.format(SUT_SESSION_ID, SUT_TIMESTAMP)
    assert_that(sign_packet_with_crc_key(packet)).is_equal_to(packet + "c40a4188")


def test_sign_packet_with_crc_key_for_get_state_packet_returns_signed_packet():
    """Test the sign_packet_with_crc_key tool for the GET_STATE_PACKET."""
    packet = packets.GET_STATE_PACKET.format(SUT_SESSION_ID, SUT_TIMESTAMP, SUT_DEVICE_ID)
    assert_that(sign_packet_with_crc_key(packet)).is_equal_to(packet + "42a9a1b2")


def test_sign_packet_with_crc_key_for_send_control_on_with_no_timer_packet_returns_signed_packet():
    """Test the sign_packet_with_crc_key tool for the SEND_CONTROL_PACKET for on state with no timer."""
    packet = packets.SEND_CONTROL_PACKET.format(
        SUT_SESSION_ID, SUT_TIMESTAMP, SUT_DEVICE_ID, consts.COMMAND_ON, consts.NO_TIMER_REQUESTED)
    assert_that(sign_packet_with_crc_key(packet)).is_equal_to(packet + "cc06bb10")


def test_sign_packet_with_crc_key_for_send_control_off_packet_returns_signed_packet():
    """Test the sign_packet_with_crc_key tool for the SEND_CONTROL_PACKET for off state."""
    packet = packets.SEND_CONTROL_PACKET.format(
        SUT_SESSION_ID, SUT_TIMESTAMP, SUT_DEVICE_ID, consts.COMMAND_OFF, consts.NO_TIMER_REQUESTED)
    assert_that(sign_packet_with_crc_key(packet)).is_equal_to(packet + "6c432cf4")


def test_sign_packet_with_crc_key_for_send_control_on_with_timer_packet_returns_signed_packet():
    """Test the sign_packet_with_crc_key tool for the SEND_CONTROL_PACKET for on state with a 90 minutes timer."""
    timer_minutes = hexlify(pack("<I", 5400)).decode()
    packet = packets.SEND_CONTROL_PACKET.format(
        SUT_SESSION_ID, SUT_TIMESTAMP, SUT_DEVICE_ID, consts.COMMAND_ON, timer_minutes)
    assert_that(sign_packet_with_crc_key(packet)).is_equal_to(packet + "3b30141e")


def test_sign_packet_with_crc_key_for_set_auto_off_packet_returns_signed_packet():
    """Test the sign_packet_with_crc_key tool for the SET_AUTO_OFF_SET_PACKET with a 90 minutes auto-shutdown."""
    auto_shutdown = hexlify(pack("<I", 5400)).decode()
    packet = packets.SET_AUTO_OFF_SET_PACKET.format(SUT_SESSION_ID, SUT_TIMESTAMP, SUT_DEVICE_ID, auto_shutdown)
    assert_that(sign_packet_with_crc_key(packet)).is_equal_to(packet + "3bb1ca55")


def test_sign_packet_with_crc_key_for_set_device_name_packet_returns_signed_packet():
    """Test the sign_packet_with_crc_key tool for the UPDATE_DEVICE_NAME_PACKET with a 'my device cool name'."""
    desired_name = "my device cool name"
    hex_name = hexlify(desired_name.encode())
    zeros_pad = ("00" * (32 - len(desired_name))).encode()
    packet = packets.UPDATE_DEVICE_NAME_PACKET.format(SUT_SESSION_ID, SUT_TIMESTAMP, SUT_DEVICE_ID, (hex_name + zeros_pad).decode())
    assert_that(sign_packet_with_crc_key(packet)).is_equal_to(packet + "1039bc0e")


def test_sign_packet_with_crc_key_for_get_schedules_packet_returns_signed_packet():
    """Test the sign_packet_with_crc_key tool for the GET_SCHEDULES_PACKET."""
    packet = packets.GET_SCHEDULES_PACKET.format(SUT_SESSION_ID, SUT_TIMESTAMP, SUT_DEVICE_ID)
    assert_that(sign_packet_with_crc_key(packet)).is_equal_to(packet + "0efde536")
