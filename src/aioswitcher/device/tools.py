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

"""Switcher integration device module tools."""

import datetime
import time
from binascii import crc_hqx, hexlify, unhexlify
from struct import pack

from ..device import DeviceType


def seconds_to_iso_time(all_seconds: int) -> str:
    """Convert seconds to iso time.

    Args:
        all_seconds: the total number of seconds to convert.

    Return:
        A string representing the converted iso time in %H:%M:%S format.
        e.g. "02:24:37".

    """
    minutes, seconds = divmod(int(all_seconds), 60)
    hours, minutes = divmod(minutes, 60)

    return datetime.time(hour=hours, minute=minutes, second=seconds).isoformat()


def sign_packet_with_crc_key(hex_packet: str) -> str:
    """Sign the packets with the designated crc key.

    Args:
        hex_packet: packet to sign.

    Return:
        The calculated and signed packet.

    """
    binary_packet = unhexlify(hex_packet)
    binary_packet_crc = pack(">I", crc_hqx(binary_packet, 0x1021))
    hex_packet_crc = hexlify(binary_packet_crc).decode()
    hex_packet_crc_sliced = hex_packet_crc[6:8] + hex_packet_crc[4:6]

    binary_key = unhexlify(hex_packet_crc_sliced + "30" * 32)
    binary_key_crc = pack(">I", crc_hqx(binary_key, 0x1021))
    hex_key_crc = hexlify(binary_key_crc).decode()
    hex_key_crc_sliced = hex_key_crc[6:8] + hex_key_crc[4:6]

    return hex_packet + hex_packet_crc_sliced + hex_key_crc_sliced


def minutes_to_hexadecimal_seconds(minutes: int) -> str:
    """Encode minutes to an hexadecimal packed as little endian unsigned int.

    Args:
        minutes: minutes to encode.

    Return:
        Hexadecimal representation of the minutes argument.

    """
    return hexlify(pack("<I", minutes * 60)).decode()


def timedelta_to_hexadecimal_seconds(full_time: datetime.timedelta) -> str:
    """Encode timedelta as seconds to an hexadecimal packed as little endian unsigned.

    Args:
        full_time: timedelta time between 1 and 24 hours, seconds are ignored.

    Return:
        Hexadecimal representation of the seconds built fom the full_time argument.

    """
    minutes = full_time.total_seconds() / 60
    hours, minutes = divmod(minutes, 60)
    seconds = int(hours) * 3600 + int(minutes) * 60

    if 3599 < seconds < 86341:
        return hexlify(pack("<I", int(seconds))).decode()

    raise ValueError("can only handle 1 to 24 hours")


def string_to_hexadecimale_device_name(name: str) -> str:
    """Encode string device name to an appropriate hexadecimal value.

    Args:
        name: the desired name for encoding.

    Return:
        Hexadecimal representation of the name argument.

    """
    length = len(name)
    if 1 < length < 33:
        hex_name = hexlify(name.encode())
        zeros_pad = ("00" * (32 - length)).encode()
        return (hex_name + zeros_pad).decode()
    raise ValueError("name length can vary from 2 to 32")


def current_timestamp_to_hexadecimal() -> str:
    """Generate hexadecimal representation of the current timestamp.

    Return:
        Hexadecimal representation of the current unix time retrieved by ``time.time``.

    """
    round_timestamp = int(round(time.time()))
    binary_timestamp = pack("<I", round_timestamp)
    hex_timestamp = hexlify(binary_timestamp)
    return hex_timestamp.decode()


def watts_to_amps(watts: int) -> float:
    """Convert power consumption to watts to electric current in amps."""
    return round((watts / float(220)), 1)


def set_message_length(message: str) -> str:
    """Set the message length."""
    length = "{:x}".format(len(unhexlify(message + "00000000"))).ljust(4, "0")
    return "fef0" + str(length) + message[8:]


def convert_str_to_devicetype(device_type: str) -> DeviceType:
    """Convert string name to DeviceType."""
    if device_type == "Switcher Mini":
        return DeviceType.MINI
    elif device_type == "Switcher Power Plug":
        return DeviceType.POWER_PLUG
    elif device_type == "Switcher Touch":
        return DeviceType.TOUCH
    elif device_type == "Switcher V2 (esp)":
        return DeviceType.V2_ESP
    elif device_type == "Switcher V2 (qualcomm)":
        return DeviceType.V2_QCA
    elif device_type == "Switcher V4":
        return DeviceType.V4
    elif device_type == "Switcher Breeze":
        return DeviceType.BREEZE
    elif device_type == "Switcher Runner":
        return DeviceType.RUNNER
    elif device_type == "Switcher Runner Mini":
        return DeviceType.RUNNER_MINI
    return DeviceType.MINI
