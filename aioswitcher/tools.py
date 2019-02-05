"""Switcher Tools and Helpers."""

from typing import List
from datetime import time as datetime_time, timedelta
from time import mktime, strftime, strptime, localtime, time as time_time
from binascii import hexlify, crc_hqx, unhexlify
from struct import pack
from socket import socket, AF_INET, SOCK_STREAM

from aioswitcher.consts import (ENCODING_CODEC, REMOTE_KEY, DAYS_HEX_DICT,
                                SOCKET_PORT)


def convert_seconds_to_iso_time(all_seconds: int) -> str:
    """Convert seconds to iso time (%H:%M:%S)."""
    try:
        minutes, seconds = divmod(int(all_seconds), 60)
        hours, minutes = divmod(minutes, 60)

        return datetime_time(hour=hours, minute=minutes,
                             second=seconds).isoformat()
    except Exception as ex:
        raise Exception("failed to convert seconds to iso time") from ex


def crc_sign_full_packet_com_key(data: str) -> str:
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
    except Exception as ex:
        raise Exception("failed to sign crc") from ex


def convert_minutes_to_timer(minutes: str) -> str:
    """Convert minutes to hex for timer."""
    try:
        return hexlify(pack('<I', int(minutes) * 60)).decode(ENCODING_CODEC)
    except Exception as ex:
        raise Exception(
            "failed to create timer from " + str(minutes) + " minutes") from ex


def convert_timedelta_to_auto_off(full_time: timedelta) -> str:
    """Convert timedelta seconds to hex for auto-off."""
    try:
        minutes = full_time.total_seconds() / 60
        hours, minutes = divmod(minutes, 60)
        seconds = int(hours) * 3600 + int(minutes) * 60
        if seconds > 3599 and seconds < 86341:
            return hexlify(pack('<I', int(seconds))).decode(ENCODING_CODEC)
        raise Exception("can only handle 1 to 24 hours on auto-off set")
    except Exception as ex:
        raise Exception(
            "failed to create auto-off from" + str(full_time) + "timedelta") \
            from ex


def convert_string_to_device_name(name: str) -> str:
    """Convert string to device name."""
    try:
        return (hexlify(name.encode(
            ENCODING_CODEC)) + ((32 - len(name)) * "00").encode(
                ENCODING_CODEC)).decode(ENCODING_CODEC)
    except Exception as ex:
        raise Exception(
            "failed to convert " + name + " to device name") from ex


def get_days_list_from_bytes(data: int) -> List[str]:
    """Extract week days from shcedule bytes."""
    days_list = []
    try:
        for day in DAYS_HEX_DICT:
            if day & data != 0x00:
                days_list.append(DAYS_HEX_DICT[day])

        return days_list
    except Exception as ex:
        raise Exception("failed to extract week days from schedule") from ex


def get_time_from_bytes(data: str) -> str:
    """Extract start/end time from shcedule bytes."""
    try:
        timestamp = int(data[6:8] + data[4:6] + data[2:4] + data[0:2], 16)

        return strftime("%H:%M", localtime(timestamp))
    except Exception as ex:
        raise Exception("failed to extract time from schedule") from ex


def get_socket(ip_addr: str) -> socket:
    """Connect to socket."""
    try:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((ip_addr, SOCKET_PORT))

        return sock
    except Exception as ex:
        raise Exception("failed to connect socket to " + ip_addr) from ex


def get_timestamp() -> str:
    """Generate timestamp."""
    try:
        return hexlify(pack('<I', int(round(time_time())))).decode(
            ENCODING_CODEC)
    except Exception as ex:
        raise Exception('failed to generate timestamp') from ex


def create_weekdays_value(requested_days: List[int]) -> str:
    """Create weekdays value for creating a new schedule."""
    return "{:02x}".format(int(sum(requested_days)))


def timedelta_str_to_schedule_time(time_value: str) -> str:
    """Convert timedelta string to schedule start/end time."""
    try:
        return_time = mktime(strptime(
            strftime("%d/%m/%Y")
            + " "
            + str(time_value).split(":")[0]
            + ":"
            + str(time_value).split(":")[1], "%d/%m/%Y %H:%M"))

        return hexlify(pack('<I', int(return_time))).decode(ENCODING_CODEC)
    except Exception as ex:
        raise Exception(
            "failed to convert time value to schedule time") from ex


def close_socket_connection(sock: socket) -> None:
    """Close socket."""
    try:
        sock.close()
    except Exception:
        pass
