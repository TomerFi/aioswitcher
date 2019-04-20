"""Test cases for the aioswitcher.tools module."""

from asyncio import AbstractEventLoop
from binascii import unhexlify
from datetime import datetime, timedelta
from struct import unpack

from asynctest import patch
from pytest import fail, mark, raises

from aioswitcher.api.packets import GET_STATE_PACKET
from aioswitcher.consts import ENCODING_CODEC, STRUCT_PACKING_FORMAT
from aioswitcher.errors import CalculationError, DecodingError, EncodingError
from aioswitcher.tools import (
    convert_minutes_to_timer, convert_seconds_to_iso_time,
    convert_string_to_device_name, convert_timedelta_to_auto_off,
    crc_sign_full_packet_com_key, create_weekdays_value,
    get_days_list_from_bytes, get_time_from_bytes, get_timestamp,
    timedelta_str_to_schedule_time)

from .asserters import assert_lists_equal, assert_seconds_to_iso_time
from .common import create_random_time
from .consts import (DUMMY_DEVICE_ID, DUMMY_DEVICE_NAME, DUMMY_SESSION_ID,
                     DUMMY_START_TIME_SET, DUMMY_TIMESTAMP,
                     RESULT_CRC_SIGNATURE, SCHEDULE_WEEKDAY_LIST,
                     TEST_HEX_WEEKDAYS_SET_LIST, TEST_MINUTES, TEST_SECONDS,
                     TEST_TIMEDELTA_MAX_FAILURE, TEST_TIMEDELTA_MIN_FAILURE,
                     TEST_TIMEDELTA_SUCCESS_NO_SECONDS,
                     TEST_TIMEDELTA_SUCCESS_SECONDS, TIMESTAMP_COMPARE_FORMAT)


@mark.asyncio
async def test_convert_seconds_to_iso_time(
        event_loop: AbstractEventLoop) -> None:
    """Test the convert_seconds_to_iso_time tool."""
    with raises(CalculationError) as exc_info:
        await convert_seconds_to_iso_time(event_loop, -1)

    assert exc_info.type is CalculationError

    try:
        result = await convert_seconds_to_iso_time(event_loop, TEST_SECONDS)
        await assert_seconds_to_iso_time(TEST_SECONDS, result)
    except CalculationError as exc:
        fail(str(exc))


@mark.asyncio
async def test_crc_sign_full_packet_com_key(
        event_loop: AbstractEventLoop) -> None:
    """Test the crc_sign_full_packet_com_key tool."""
    with raises(EncodingError) as exc_info:
        await crc_sign_full_packet_com_key(event_loop, "notlongenough")

    assert exc_info.type is EncodingError

    try:
        packet = GET_STATE_PACKET.format(
            DUMMY_SESSION_ID, DUMMY_TIMESTAMP, DUMMY_DEVICE_ID)
        result = await crc_sign_full_packet_com_key(event_loop, packet)
        assert packet == result[:-8]
        assert RESULT_CRC_SIGNATURE == result[-8:]
    except EncodingError as exc:
        fail(str(exc))


@mark.asyncio
async def test_convert_minutes_to_timer(event_loop: AbstractEventLoop) -> None:
    """Test the convert_minutes_to_timer tool."""
    with raises(EncodingError) as exc_info:
        await convert_minutes_to_timer(event_loop, "notintconvertable")

    assert exc_info.type is EncodingError

    try:
        result = await convert_minutes_to_timer(event_loop, TEST_MINUTES)
        unpacked = unpack(
            STRUCT_PACKING_FORMAT,
            unhexlify(result.encode(ENCODING_CODEC)))
        assert TEST_MINUTES == str(int(unpacked[0] / 60))
    except EncodingError as exc:
        fail(str(exc))


@mark.asyncio
async def test_convert_timedelta_to_auto_off(
        event_loop: AbstractEventLoop) -> None:
    """Test the convert_timedelta_to_auto_off tool."""
    with raises(EncodingError) as exc_info_min:
        await convert_timedelta_to_auto_off(
            event_loop, TEST_TIMEDELTA_MIN_FAILURE)

    assert exc_info_min.type is EncodingError

    with raises(EncodingError) as exc_info_max:
        await convert_timedelta_to_auto_off(
            event_loop, TEST_TIMEDELTA_MAX_FAILURE)

    assert exc_info_max.type is EncodingError

    try:
        result = await convert_timedelta_to_auto_off(
            event_loop, TEST_TIMEDELTA_SUCCESS_SECONDS)
        unpacked = unpack(
            STRUCT_PACKING_FORMAT,
            unhexlify(result.encode(ENCODING_CODEC)))
        new_timedelta = timedelta(seconds=int(unpacked[0]))
        assert new_timedelta != TEST_TIMEDELTA_SUCCESS_SECONDS
        assert new_timedelta == TEST_TIMEDELTA_SUCCESS_NO_SECONDS
    except EncodingError as exc:
        fail(str(exc))


@mark.asyncio
async def test_convert_string_to_device_name(
        event_loop: AbstractEventLoop) -> None:
    """Test the convert_string_to_device_name tool."""
    with raises(EncodingError) as exc_info_min:
        await convert_string_to_device_name(event_loop, 'x')

    assert exc_info_min.type is EncodingError

    with raises(EncodingError) as exc_info_max:
        await convert_string_to_device_name(event_loop, 'x' * 33)

    assert exc_info_max.type is EncodingError

    try:
        result = await convert_string_to_device_name(
            event_loop, DUMMY_DEVICE_NAME)
        unhexed = \
            unhexlify(result).decode(ENCODING_CODEC)[:len(DUMMY_DEVICE_NAME)]
        assert len(result) == 64
        assert DUMMY_DEVICE_NAME == unhexed
    except EncodingError as exc:
        fail(str(exc))


@mark.asyncio
async def test_get_days_list_from_bytes(event_loop: AbstractEventLoop) -> None:
    """Test the get_days_list_from_bytes tool."""
    with patch('aioswitcher.tools.HEX_TO_DAY_DICT', 999):
        with raises(DecodingError) as exc_info:
            await get_days_list_from_bytes(event_loop, 0)

        assert exc_info.type is DecodingError

    try:
        for test_set in TEST_HEX_WEEKDAYS_SET_LIST:
            result = await get_days_list_from_bytes(event_loop, test_set[0])
            await assert_lists_equal(result, test_set[1])
    except DecodingError as exc:
        fail(str(exc))


@mark.asyncio
async def test_get_time_from_bytes(event_loop: AbstractEventLoop) -> None:
    """Test the get_time_from_bytes tool."""
    with raises(DecodingError) as exc_info:
        await get_time_from_bytes(event_loop, "notbytes")  # type: ignore

    assert exc_info.type is DecodingError

    try:
        result = await get_time_from_bytes(event_loop, DUMMY_START_TIME_SET[0])
        assert result == DUMMY_START_TIME_SET[1]
    except DecodingError as exc:
        fail(str(exc))


@mark.asyncio
async def test_get_timestamp(event_loop: AbstractEventLoop) -> None:
    """Test the get_timestamp tool."""
    with patch('aioswitcher.tools.ENCODING_CODEC', 'bin'):
        with raises(EncodingError) as exc_info:
            await get_timestamp(event_loop)

        assert exc_info.type is EncodingError

    try:
        result = await get_timestamp(event_loop)
        unpacked = unpack(
            STRUCT_PACKING_FORMAT,
            unhexlify(result.encode(ENCODING_CODEC)))

        approx_datetime = datetime.fromtimestamp(unpacked[0])

        assert approx_datetime.strftime(TIMESTAMP_COMPARE_FORMAT) == \
            datetime.now().strftime(TIMESTAMP_COMPARE_FORMAT)

    except EncodingError as exc:
        fail(str(exc))


@mark.asyncio
async def test_create_weekdays_value(event_loop: AbstractEventLoop) -> None:
    """Test the create_weekdays_value tool."""
    with raises(EncodingError) as exc_info:
        await create_weekdays_value(event_loop, [])

    assert exc_info.type is EncodingError

    try:
        result = await create_weekdays_value(event_loop, SCHEDULE_WEEKDAY_LIST)
        assert int(result, 16) == int(sum(SCHEDULE_WEEKDAY_LIST))
    except EncodingError as exc:
        fail(str(exc))


@mark.asyncio
async def test_timedelta_str_to_schedule_time(
        event_loop: AbstractEventLoop) -> None:
    """Test the timedelta_str_to_schedule_time tool."""
    with raises(EncodingError) as exc_info:
        await timedelta_str_to_schedule_time(event_loop, "24:59")

    assert exc_info.type is EncodingError

    try:
        random_time = create_random_time()
        result = await timedelta_str_to_schedule_time(event_loop, random_time)

        unpacked = unpack(
            STRUCT_PACKING_FORMAT,
            unhexlify(result.encode(ENCODING_CODEC)))

        approx_datetime = datetime.fromtimestamp(unpacked[0])

        assert random_time == '{}:{}'.format(
            '00{}'.format(approx_datetime.hour)[-2:],
            '00{}'.format(approx_datetime.minute)[-2:])

        assert approx_datetime.date() == datetime.now().date()

    except EncodingError as exc:
        fail(str(exc))
