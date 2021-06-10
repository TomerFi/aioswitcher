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

"""Switcher unofficial integration utility functions."""

import datetime
import time
from binascii import crc_hqx, hexlify, unhexlify
from struct import pack
from typing import Set, Union, cast

from . import Days
from .errors import CalculationError, DecodingError, EncodingError


def seconds_to_iso_time(all_seconds: int) -> str:
    """Convert seconds to iso time.

    Args:
        all_seconds: the total number of seconds to convert.

    Return:
        A string represnting the converted iso time in %H:%M:%S format.
        e.g. "02:24:37".

    Raises:
        aioswitcher.erros.CalculationError: when failed to convert the
        argument.

    """
    try:
        minutes, seconds = divmod(int(all_seconds), 60)
        hours, minutes = divmod(minutes, 60)

        return datetime.time(hour=hours, minute=minutes, second=seconds).isoformat()
    except Exception as ex:
        raise CalculationError("failed to convert seconds to iso time") from ex


def sign_packet_with_crc_key(hex_packet: str) -> str:
    """Sign the packets with the designated crc key.

    Args:
        packet: packet to sign.

    Return:
        The calculated and signed packet.

    Raises:
        aioswitcher.erros.EncodingError: when failed to sign the packet.

    """
    try:
        binary_packet = unhexlify(hex_packet)
        binary_packet_crc = pack(">I", crc_hqx(binary_packet, 0x1021))
        hex_packet_crc = hexlify(binary_packet_crc).decode()
        hex_packet_crc_sliced = hex_packet_crc[6:8] + hex_packet_crc[4:6]

        binary_key = unhexlify(hex_packet_crc_sliced + "30" * 32)
        binary_key_crc = pack(">I", crc_hqx(binary_key, 0x1021))
        hex_key_crc = hexlify(binary_key_crc).decode()
        hex_key_crc_sliced = hex_key_crc[6:8] + hex_key_crc[4:6]

        return hex_packet + hex_packet_crc_sliced + hex_key_crc_sliced
    except Exception as ex:
        raise EncodingError("failed to sign crc") from ex


def minutes_to_hexadecimal_seconds(minutes: int) -> str:
    """Encode minutes to an hexadecimal packed as little endian unsinged int.

    Args:
        minutes: minutes to encode.

    Return:
        Hexadecimal represntation of the mintues argument.

    Raises:
        aioswitcher.erros.EncodingError: when failed encoding.

    """
    try:
        return hexlify(pack("<I", minutes * 60)).decode()
    except Exception as ex:
        raise EncodingError("failed to encode {} minutes".format(str(minutes))) from ex


def timedelta_to_hexadecimal_seconds(full_time: datetime.timedelta) -> str:
    """Encode timedelta as seconds to an hexadecimal packed as little endian unsinged int.

    Args:
        full_time: timedelta time between 1 and 24 hours, seconds are ignored.

    Return:
        Hexadecimal represntation of the seconds built fom the full_time argument.

    Raises:
        aioswitcher.erros.EncodingError: when not between 1 and 24 hours or when failed
        encoding.

    """
    try:
        minutes = full_time.total_seconds() / 60
        hours, minutes = divmod(minutes, 60)
        seconds = int(hours) * 3600 + int(minutes) * 60

        if 3599 < seconds < 86341:
            return hexlify(pack("<I", int(seconds))).decode()

        raise ValueError("can only handle 1 to 24 hours on auto-off set")
    except Exception as ex:
        raise EncodingError("failed to encode {}".format(str(full_time))) from ex


def string_to_hexadecimale_device_name(name: str) -> str:
    """Encode string device name to an apropriate hexadecimal value.

    Args:
        name: the desired name for encoding.

    Return:
        Hexadecimal represntation of the name argument.

    Raises:
        aioswitcher.erros.EncodingError: when the length of the string is not between 2
        and 32 or when failed encoding.

    """
    try:
        length = len(name)
        if 1 < length < 33:
            hex_name = hexlify(name.encode())
            zeros_pad = ("00" * (32 - length)).encode()
            return (hex_name + zeros_pad).decode()
        raise ValueError("name length can vary from 2 to 32.")
    except Exception as ex:
        raise EncodingError("failed to encode " + str(name)) from ex


def current_timestamp_to_hexadecimal() -> str:
    """Generate hexadecimal represntation of the current timestamp.

    Return:
        Hexadecimal represntation of the current unix time retrieved by ``time.time``.

    Raises:
        aioswitcher.erros.DecodingError: when failed to analyze the timestamp.

    """
    try:
        round_timestamp = int(round(time.time()))
        binary_timestamp = pack("<I", round_timestamp)
        hex_timestamp = hexlify(binary_timestamp)
        return hex_timestamp.decode()
    except Exception as ex:
        raise DecodingError("failed to generate timestamp") from ex


def time_to_hexadecimal_timestamp(time_value: str) -> str:
    """Convert hours and minutes to a timestamp with the current date and encode.

    Args:
        time_value: time to convert. e.g. "21:00".

    Return:
        Hexadecimal representation of the timestamp.

    Raises:
        aioswitcher.erros.EncodingError: when failed encoding.

    """
    try:
        tsplit = time_value.split(":")
        str_timedate = time.strftime("%d/%m/%Y") + " " + tsplit[0] + ":" + tsplit[1]
        struct_timedate = time.strptime(str_timedate, "%d/%m/%Y %H:%M")
        timestamp = time.mktime(struct_timedate)
        binary_timestamp = pack("<I", int(timestamp))

        return hexlify(binary_timestamp).decode()
    except Exception as ex:
        raise EncodingError("failed to encode {}".format(time_value)) from ex


def hexadecimale_timestamp_to_localtime(hex_timestamp: bytes) -> str:
    """Decode an hexadecimale timestamp to localtime with the format %H:%M.

    Args:
        hex_timestamp: the hexadecimale timestamp.

    Return:
        Localtime string with %H:%M format. e.g. "20:30".

    Raises:
        aioswitcher.erros.DecodingError: when failed decoding.

    """
    try:
        hex_time = (
            hex_timestamp[6:8]
            + hex_timestamp[4:6]
            + hex_timestamp[2:4]
            + hex_timestamp[0:2]
        )
        int_time = int(hex_time, 16)
        local_time = time.localtime(int_time)
        print(local_time)
        return time.strftime("%H:%M", local_time)
    except Exception as ex:
        raise DecodingError("failed to decode timestamp") from ex


def weekdays_to_hexadecimal(days: Union[Days, Set[Days]]) -> str:
    """Sum the requested weekdays bit represntation and return as hexadecimal value.

    Args:
        days: the requested Weekday members.

    Return:
        Hexadecimale represntation of the sum of all requested day's bit representation.

    Raises:
        aioswitcher.erros.EncodingError: when failed encoding.

    """
    try:
        if days:
            if type(days) is Days:
                return "{:02x}".format(cast(Days, days).bit_rep)
            elif type(days) is set or len(days) == len(set(days)):  # type: ignore
                map_to_bits = map(lambda w: w.bit_rep, days)  # type: ignore
                return "{:02x}".format(int(sum(map_to_bits)))
        raise ValueError("no days requested")
    except Exception as ex:
        raise EncodingError("failed to calculate weekdays") from ex


def bit_summary_to_days(sum_weekdays_bit: int) -> Set[Days]:
    """Decode a weekdays bit summary to a set of weekdays.

    Args:
        sum_weekdays: the sum of all weekdays

    Return:
        Set of Weekday memebers decoded from the summary value.

    Raises:
        aioswitcher.erros.DecodingError: when failed decoding.

    Todo:
        Should an existing remainder in the sum value throw an error?
        E.g. 3 will result in a set of MONDAY and the remainder will be 1.

    """
    try:
        if 1 < sum_weekdays_bit < 255:
            return_weekdays = set()
            weekdays_by_hex = map(lambda w: (w.hex_rep, w), Days)
            for weekday_hex in weekdays_by_hex:
                if weekday_hex[0] & sum_weekdays_bit != 0:
                    return_weekdays.add(weekday_hex[1])
            return return_weekdays
        raise ValueError("weekdays bit sum should be between 2 and 254")
    except Exception as ex:
        raise DecodingError("failed to decode value to weekdays") from ex
