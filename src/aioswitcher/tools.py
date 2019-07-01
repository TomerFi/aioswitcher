"""Switcher water heater unofficial API and bridge, Tools and Helpers.

.. codeauthor:: Tomer Figenblat <tomer.figenblat@gmail.com>

"""

# fmt: off
from asyncio import AbstractEventLoop
from binascii import crc_hqx, hexlify, unhexlify
from datetime import time as datetime_time
from datetime import timedelta
from struct import pack
from time import localtime, mktime, strftime, strptime
from time import time as time_time
from typing import List

from .consts import (ENCODING_CODEC, HANDLED_EXCEPTIONS, HEX_TO_DAY_DICT,
                     REMOTE_KEY, STRUCT_PACKING_FORMAT)
from .errors import CalculationError, DecodingError, EncodingError

# fmt: on


def _convert_seconds_to_iso_time(all_seconds: int) -> str:
    """Convert seconds to iso time.

    Args:
      all_seconds: the total number of seconds to convert.

    Return:
      A string represnting the converted iso time in %H:%M:%S format.
      e.g. "02:24:37".

    Raises:
      aioswitcher.erros.CalculationError: when failed to convert the argument.

    Note:
      This is a private function containing blocking code.
      Please consider using ``convert_seconds_to_iso_time`` (without the `_`),
      to schedule as a task in the event loop.

    """
    try:
        minutes, seconds = divmod(int(all_seconds), 60)
        hours, minutes = divmod(minutes, 60)

        return datetime_time(
            hour=hours, minute=minutes, second=seconds
        ).isoformat()
    except HANDLED_EXCEPTIONS as ex:
        raise CalculationError("failed to convert seconds to iso time") from ex


async def convert_seconds_to_iso_time(
    loop: AbstractEventLoop, all_seconds: int
) -> str:
    """Asynchronous wrapper for _convert_seconds_to_iso_time.

    Use as async wrapper for calling _convert_seconds_to_iso_time,
    calculating the next runtime of the schedule.

    Args:
      loop: the event loop to execute the function in.
      all_seconds: the total number of seconds to convert.

    Returns:
      A string represnting the converted iso time in %H:%M:%S format.
      e.g. "02:24:37".

    """
    return await loop.run_in_executor(
        None, _convert_seconds_to_iso_time, all_seconds
    )


def _crc_sign_full_packet_com_key(data: str) -> str:
    """Calculate the crc for packets before send.

    Args:
      data: packet data to sign.

    Return:
      The calculated and signed packet data.

    Raises:
      aioswitcher.erros.EncodingError: when failed to sign the packet.

    Note:
      This is a private function containing blocking code.
      Please consider using ``crc_sign_full_packet_com_key``
      (without the `_`), to schedule as a task in the event loop.

    """
    try:
        crc = hexlify(pack(">I", crc_hqx(unhexlify(data), 0x1021))).decode(
            ENCODING_CODEC
        )
        data = data + crc[6:8] + crc[4:6]
        crc = (
            crc[6:8] + crc[4:6] + (hexlify(REMOTE_KEY)).decode(ENCODING_CODEC)
        )
        crc = hexlify(pack(">I", crc_hqx(unhexlify(crc), 0x1021))).decode(
            ENCODING_CODEC
        )
        data = data + crc[6:8] + crc[4:6]

        return data
    except HANDLED_EXCEPTIONS as ex:
        raise EncodingError("failed to sign crc") from ex


async def crc_sign_full_packet_com_key(
    loop: AbstractEventLoop, data: str
) -> str:
    """Asynchronous wrapper for _crc_sign_full_packet_com_key.

    Use as async wrapper for calling _crc_sign_full_packet_com_key,
    performing crc sign to the packet data.

    Args:
      data: packet data to sign.

    Return:
      The calculated and signed packet data.

    """
    return await loop.run_in_executor(
        None, _crc_sign_full_packet_com_key, data
    )


def _convert_minutes_to_timer(minutes: str) -> str:
    """Convert on-timer minutes to hexadecimal before sending.

    Args:
      minutes: on-timer minutes to convert.

    Return:
      Hexadecimal represntation of the mintues argument.

    Raises:
      aioswitcher.erros.EncodingError: when failed hexlify.

    Note:
      This is a private function containing blocking code.
      Please consider using ``convert_minutes_to_timer``
      (without the `_`), to schedule as a task in the event loop.

    """
    try:
        return hexlify(pack(STRUCT_PACKING_FORMAT, int(minutes) * 60)).decode(
            ENCODING_CODEC
        )
    except HANDLED_EXCEPTIONS as ex:
        raise EncodingError(
            "failed to create timer from {} minutes".format(str(minutes))
        ) from ex


async def convert_minutes_to_timer(
    loop: AbstractEventLoop, minutes: str
) -> str:
    """Asynchronous wrapper for _convert_minutes_to_timer.

    Use as async wrapper for calling _convert_minutes_to_timer,
    converting on-timer minutes to hexadecimal.

    Args:
      minutes: on-timer minutes to convert.

    Return:
      Hexadecimal represntation of the mintues argument.

    """
    return await loop.run_in_executor(None, _convert_minutes_to_timer, minutes)


def _convert_timedelta_to_auto_off(full_time: timedelta) -> str:
    """Convert timedelta object for auto-shutdown to hexadecimal.

    Args:
      full_time: timedelta object represnting the auto-shutdown time.

    Return:
      Hexadecimal represntation of the full_time argument.

    Raises:
      aioswitcher.erros.EncodingError: when failed hexlify.

    Note:
      This is a private function containing blocking code.
      Please consider using ``convert_timedelta_to_auto_off``
      (without the `_`), to schedule as a task in the event loop.

    """
    try:
        minutes = full_time.total_seconds() / 60
        hours, minutes = divmod(minutes, 60)
        seconds = int(hours) * 3600 + int(minutes) * 60
        if 3599 < seconds < 86341:
            return hexlify(pack(STRUCT_PACKING_FORMAT, int(seconds))).decode(
                ENCODING_CODEC
            )
        raise ValueError("can only handle 1 to 24 hours on auto-off set")
    except HANDLED_EXCEPTIONS as ex:
        raise EncodingError(
            "failed to create auto-off from {} timedelta".format(
                str(full_time)
            )
        ) from ex


async def convert_timedelta_to_auto_off(
    loop: AbstractEventLoop, full_time: timedelta
) -> str:
    """Asynchronous wrapper for _convert_timedelta_to_auto_off.

    Use as async wrapper for calling _convert_timedelta_to_auto_off,
    converting timedelta auto-shutdown configuration to hexadecimal.

    Args:
      full_time: timedelta object represnting the auto-shutdown time.

    Return:
      Hexadecimal represntation of the full_time argument.

    """
    return await loop.run_in_executor(
        None, _convert_timedelta_to_auto_off, full_time
    )


def _convert_string_to_device_name(name: str) -> str:
    """Convert string device name to hexadecimal before sending.

    Args:
      name: the desired name for conerting.

    Return:
      Hexadecimal represntation of the name argument.

    Raises:
      aioswitcher.erros.EncodingError: when failed hexlify.

    Note:
      This is a private function containing blocking code.
      Please consider using ``convert_string_to_device_name``
      (without the `_`), to schedule as a task in the event loop.

    """
    try:
        if 1 < len(name) < 33:
            return (
                hexlify(name.encode(ENCODING_CODEC))
                + ((32 - len(name)) * "00").encode(ENCODING_CODEC)
            ).decode(ENCODING_CODEC)
        raise ValueError("name length can vary from 2 to 32.")
    except HANDLED_EXCEPTIONS as ex:
        raise EncodingError(
            "failed to convert " + str(name) + " to device name"
        ) from ex


async def convert_string_to_device_name(
    loop: AbstractEventLoop, name: str
) -> str:
    """Asynchronous wrapper for _convert_string_to_device_name.

    Use as async wrapper for calling _convert_string_to_device_name,
    converting name to hexadecimal.

    Args:
      name: the desired name for conerting.

    Return:
      Hexadecimal represntation of the name argument.

    """
    return await loop.run_in_executor(
        None, _convert_string_to_device_name, name
    )


def _get_days_list_from_bytes(data: int) -> List[str]:
    """Extract week days from shcedule bytes data.

    Args:
      data: bytes representing the days list.

    Return:
      List of string represntation the week days included in the list.
      See ``aioswitcher.consts`` for days literals.

    Raises:
      aioswitcher.erros.DecodingError: when failed to analyze the argument.

    Note:
      This is a private function containing blocking code.
      Please consider using ``get_days_list_from_bytes``
      (without the `_`), to schedule as a task in the event loop.

    """
    days_list = []
    try:
        for day in HEX_TO_DAY_DICT:
            if day & data != 0x00:
                days_list.append(HEX_TO_DAY_DICT[day])

        return days_list
    except HANDLED_EXCEPTIONS as ex:
        raise DecodingError(
            "failed to extract week days from schedule"
        ) from ex


async def get_days_list_from_bytes(
    loop: AbstractEventLoop, data: int
) -> List[str]:
    """Asynchronous wrapper for _get_days_list_from_bytes.

    Use as async wrapper for calling _get_days_list_from_bytes,
    extracting week days from shcedule bytes data.

    Args:
      data: bytes representing the days list.

    Return:
      List of string represntation the week days included in the list.
      See ``aioswitcher.consts`` for days literals.

    """
    return await loop.run_in_executor(None, _get_days_list_from_bytes, data)


def _get_time_from_bytes(data: bytes) -> str:
    """Extract start/end time from schedule bytes.

    Args:
      data: bytes representing the start or the end time for the schedule.

    Return:
      Time string in %H:%M format.
      e.g. "20:30".

    Raises:
      aioswitcher.erros.DecodingError: when failed to analyze the argument.

    Note:
      This is a private function containing blocking code.
      Please consider using ``get_time_from_bytes``
      (without the `_`), to schedule as a task in the event loop.

    """
    try:
        timestamp = int(data[6:8] + data[4:6] + data[2:4] + data[0:2], 16)

        return strftime("%H:%M", localtime(timestamp))
    except HANDLED_EXCEPTIONS as ex:
        raise DecodingError("failed to extract time from schedule") from ex


async def get_time_from_bytes(loop: AbstractEventLoop, data: bytes) -> str:
    """Asynchronous wrapper for _get_time_from_bytes.

    Use as async wrapper for calling _get_time_from_bytes,
    extracting start/end time from schedule bytes data.

    Args:
      data: bytes representing the start or the end time for the schedule.

    Return:
      Time string in %H:%M format.
      e.g. "20:30".

    """
    return await loop.run_in_executor(None, _get_time_from_bytes, data)


def _get_timestamp() -> str:
    """Generate hexadecimal represntation of the current timestamp.

    Return:
      Hexadecimal represntation of the current unix time retrieved by
      ``time.time``.

    Raises:
      aioswitcher.erros.DecodingError: when failed to analyze the timestamp.

    Note:
      This is a private function containing blocking code.
      Please consider using ``get_timestamp`` (without the `_`),
      to schedule as a task in the event loop.

    """
    try:
        return hexlify(
            pack(STRUCT_PACKING_FORMAT, int(round(time_time())))
        ).decode(ENCODING_CODEC)
    except HANDLED_EXCEPTIONS as ex:
        raise DecodingError("failed to generate timestamp") from ex


async def get_timestamp(loop: AbstractEventLoop) -> str:
    """Asynchronous wrapper for _get_timestamp.

    Use as async wrapper for calling _get_timestamp,
    creating hexadecimal represntation of the current timestamp.

    Return:
      Hexadecimal represntation of the current unix time retrieved by
      ``time.time``.

    """
    return await loop.run_in_executor(None, _get_timestamp)


def _create_weekdays_value(requested_days: List[int]) -> str:
    """Create hex value from list of requested days for schedule updating.

    Args:
      data: list of integers represnting the requested days.
            check ``aioswitcher.consts`` for the correct values.

    Return:
      Hexadecimal representation of the days list.

    Raises:
      aioswitcher.erros.EncodingError: when failed to convert the argument.

    Note:
      This is a private function containing blocking code.
      Please consider using ``create_weekdays_value``
      (without the `_`), to schedule as a task in the event loop.

    """
    try:
        if requested_days:
            return "{:02x}".format(int(sum(requested_days)))
        raise ValueError("days list is empty")
    except HANDLED_EXCEPTIONS as ex:
        raise EncodingError("failed to create weekdays value") from ex


async def create_weekdays_value(
    loop: AbstractEventLoop, requested_days: List[int]
) -> str:
    """Asynchronous wrapper for _create_weekdays_value.

    Use as async wrapper for calling _create_weekdays_value,
    creating hex value from list of requested days for schedule updating.

    Args:
      data: list of integers represnting the requested days.
            check ``aioswitcher.consts`` for the correct values.

    Return:
      Hexadecimal representation of the days list.

    """
    return await loop.run_in_executor(
        None, _create_weekdays_value, requested_days
    )


def _timedelta_str_to_schedule_time(time_value: str) -> str:
    """Convert time string to schedule start/end time to hexadecimale.

    Args:
      data: time to convert. e.g. "21:00".

    Return:
      Hexadecimal representation of time_value argument.

    Raises:
      aioswitcher.erros.EncodingError: when failed to convert the argument.

    Note:
      This is a private function containing blocking code.
      Please consider using ``timedelta_str_to_schedule_time``
      (without the `_`), to schedule as a task in the event loop.

    """
    try:
        return_time = mktime(
            strptime(
                strftime("%d/%m/%Y")
                + " "
                + time_value.split(":")[0]
                + ":"
                + time_value.split(":")[1],
                "%d/%m/%Y %H:%M",
            )
        )

        return hexlify(pack(STRUCT_PACKING_FORMAT, int(return_time))).decode(
            ENCODING_CODEC
        )
    except HANDLED_EXCEPTIONS as ex:
        raise EncodingError(
            "failed to convert time value to schedule time"
        ) from ex


async def timedelta_str_to_schedule_time(
    loop: AbstractEventLoop, time_value: str
) -> str:
    """Asynchronous wrapper for _timedelta_str_to_schedule_time.

    Use as async wrapper for calling _timedelta_str_to_schedule_time,
    converting time string to schedule start/end time to hexadecimale.

    Args:
      data: time to convert. e.g. "21:00".

    Return:
      Hexadecimal representation of time_value argument.

    """
    return await loop.run_in_executor(
        None, _timedelta_str_to_schedule_time, time_value
    )
