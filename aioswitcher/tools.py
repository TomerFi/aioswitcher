"""Switcher Tools and Helpers."""

from asyncio import AbstractEventLoop
from binascii import crc_hqx, hexlify, unhexlify
from datetime import time as datetime_time, timedelta
from struct import pack
from time import localtime, mktime, strftime, strptime, time as time_time
from typing import List

from .consts import (HANDLED_EXCEPTIONS, HEX_TO_DAY_DICT, ENCODING_CODEC,
                     REMOTE_KEY, STRUCT_PACKING_FORMAT)
from .errors import CalculationError, DecodingError, EncodingError


def _convert_seconds_to_iso_time(all_seconds: int) -> str:
    """Convert seconds to iso time (%H:%M:%S)."""
    try:
        minutes, seconds = divmod(int(all_seconds), 60)
        hours, minutes = divmod(minutes, 60)

        return datetime_time(hour=hours, minute=minutes,
                             second=seconds).isoformat()
    except HANDLED_EXCEPTIONS as ex:
        raise CalculationError("failed to convert seconds to iso time") from ex


async def convert_seconds_to_iso_time(loop: AbstractEventLoop,
                                      all_seconds: int) -> str:
    """Use as async wrapper for calling _convert_seconds_to_iso_time."""
    return await loop.run_in_executor(
        None, _convert_seconds_to_iso_time, all_seconds)


def _crc_sign_full_packet_com_key(data: str) -> str:
    """Crc calculation."""
    try:
        crc = hexlify(pack(
            '>I',
            crc_hqx(unhexlify(data), 0x1021))).decode(ENCODING_CODEC)
        data = data + crc[6:8] + crc[4:6]
        crc = crc[6:8] + crc[4:6] + (hexlify(REMOTE_KEY)).decode(
            ENCODING_CODEC)
        crc = hexlify(
            pack('>I', crc_hqx(unhexlify(crc), 0x1021))).decode(ENCODING_CODEC)
        data = data + crc[6:8] + crc[4:6]

        return data
    except HANDLED_EXCEPTIONS as ex:
        raise EncodingError("failed to sign crc") from ex


async def crc_sign_full_packet_com_key(loop: AbstractEventLoop, data: str) \
        -> str:
    """Use as async wrapper for calling _crc_sign_full_packet_com_key."""
    return await loop.run_in_executor(
        None, _crc_sign_full_packet_com_key, data)


def _convert_minutes_to_timer(minutes: str) -> str:
    """Convert minutes to hex for timer."""
    try:
        return hexlify(pack(
            STRUCT_PACKING_FORMAT, int(minutes) * 60)).decode(ENCODING_CODEC)
    except HANDLED_EXCEPTIONS as ex:
        raise EncodingError(
            "failed to create timer from {} minutes".format(
                str(minutes))) from ex


async def convert_minutes_to_timer(loop: AbstractEventLoop, minutes: str) \
        -> str:
    """Use as async wrapper for calling _convert_minutes_to_timer."""
    return await loop.run_in_executor(None, _convert_minutes_to_timer, minutes)


def _convert_timedelta_to_auto_off(full_time: timedelta) -> str:
    """Convert timedelta seconds to hex for auto-off."""
    try:
        minutes = full_time.total_seconds() / 60
        hours, minutes = divmod(minutes, 60)
        seconds = int(hours) * 3600 + int(minutes) * 60
        if 3599 < seconds < 86341:
            return hexlify(pack(
                STRUCT_PACKING_FORMAT, int(seconds))).decode(ENCODING_CODEC)
        raise ValueError("can only handle 1 to 24 hours on auto-off set")
    except HANDLED_EXCEPTIONS as ex:
        raise EncodingError(
            "failed to create auto-off from {} timedelta".format(
                str(full_time))) from ex


async def convert_timedelta_to_auto_off(
        loop: AbstractEventLoop, full_time: timedelta) -> str:
    """Use as async wrapper for calling _convert_timedelta_to_auto_off."""
    return await loop.run_in_executor(
        None, _convert_timedelta_to_auto_off, full_time)


def _convert_string_to_device_name(name: str) -> str:
    """Convert string to device name."""
    try:
        if 1 < len(name) < 33:
            return (hexlify(name.encode(
                ENCODING_CODEC)) + ((32 - len(name)) * "00").encode(
                    ENCODING_CODEC)).decode(ENCODING_CODEC)
        raise ValueError("name length can vary from 2 to 32.")
    except HANDLED_EXCEPTIONS as ex:
        raise EncodingError(
            "failed to convert " + str(name) + " to device name") from ex


async def convert_string_to_device_name(loop: AbstractEventLoop, name: str) \
        -> str:
    """Use as async wrapper for calling _convert_string_to_device_name."""
    return await loop.run_in_executor(
        None, _convert_string_to_device_name, name)


def _get_days_list_from_bytes(data: int) -> List[str]:
    """Extract week days from shcedule bytes."""
    days_list = []
    try:
        for day in HEX_TO_DAY_DICT:
            if day & data != 0x00:
                days_list.append(HEX_TO_DAY_DICT[day])

        return days_list
    except HANDLED_EXCEPTIONS as ex:
        raise DecodingError("failed to extract week days from schedule") \
            from ex


async def get_days_list_from_bytes(loop: AbstractEventLoop, data: int) \
        -> List[str]:
    """Use as async wrapper for calling _get_days_list_from_bytes."""
    return await loop.run_in_executor(None, _get_days_list_from_bytes, data)


def _get_time_from_bytes(data: bytes) -> str:
    """Extract start/end time from schedule bytes."""
    try:
        timestamp = int(data[6:8] + data[4:6] + data[2:4] + data[0:2], 16)

        return strftime("%H:%M", localtime(timestamp))
    except HANDLED_EXCEPTIONS as ex:
        raise DecodingError("failed to extract time from schedule") from ex


async def get_time_from_bytes(loop: AbstractEventLoop, data: bytes) -> str:
    """Use as async wrapper for calling _get_time_from_bytes."""
    return await loop.run_in_executor(None, _get_time_from_bytes, data)


def _get_timestamp() -> str:
    """Generate timestamp."""
    try:
        return hexlify(pack(
            STRUCT_PACKING_FORMAT, int(round(time_time())))).decode(
                ENCODING_CODEC)
    except HANDLED_EXCEPTIONS as ex:
        raise EncodingError('failed to generate timestamp') from ex


async def get_timestamp(loop: AbstractEventLoop) -> str:
    """Use as async wrapper for calling _get_timestamp."""
    return await loop.run_in_executor(None, _get_timestamp)


def _create_weekdays_value(requested_days: List[int]) -> str:
    """Create weekdays value for creating a new schedule."""
    try:
        if requested_days:
            return "{:02x}".format(int(sum(requested_days)))
        raise ValueError("days list is empty")
    except HANDLED_EXCEPTIONS as ex:
        raise EncodingError('failed to create weekdays value') from ex


async def create_weekdays_value(loop: AbstractEventLoop,
                                requested_days: List[int]) -> str:
    """Use as async wrapper for calling _create_weekdays_value."""
    return await loop.run_in_executor(
        None, _create_weekdays_value, requested_days)


def _timedelta_str_to_schedule_time(time_value: str) -> str:
    """Convert timedelta string to schedule start/end time."""
    try:
        return_time = mktime(strptime(
            strftime("%d/%m/%Y")
            + " "
            + time_value.split(":")[0]
            + ":"
            + time_value.split(":")[1], "%d/%m/%Y %H:%M"))

        return hexlify(pack(
            STRUCT_PACKING_FORMAT, int(return_time))).decode(ENCODING_CODEC)
    except HANDLED_EXCEPTIONS as ex:
        raise EncodingError(
            "failed to convert time value to schedule time") from ex


async def timedelta_str_to_schedule_time(loop: AbstractEventLoop,
                                         time_value: str) -> str:
    """Use as async wrapper for calling timedelta_str_to_schedule_time."""
    return await loop.run_in_executor(
        None, _timedelta_str_to_schedule_time, time_value)
