"""Test cases for the aioswitcher.tools module."""

from asyncio import AbstractEventLoop
from binascii import unhexlify
from datetime import datetime, timedelta
from struct import unpack

from pytest import fail, mark, raises

from aioswitcher.api.packets import GET_STATE_PACKET
from aioswitcher.consts import (ENCODING_CODEC, SCHEDULE_CREATE_DATA_FORMAT,
                                STRUCT_PACKING_FORMAT)
from aioswitcher.errors import CalculationError, DecodingError, EncodingError
from aioswitcher.tools import (
    convert_seconds_to_iso_time, crc_sign_full_packet_com_key,
    convert_minutes_to_timer, convert_string_to_device_name,
    convert_timedelta_to_auto_off, create_weekdays_value, get_timestamp,
    timedelta_str_to_schedule_time, get_days_list_from_bytes,
    get_time_from_bytes)

from .asserters import assert_seconds_to_iso_time, assert_lists_equal
from .common import create_random_time
from .consts import (DUMMY_DEVICE_NAME, DUMMY_DEVICE_ID, DUMMY_SESSION_ID,
                     DUMMY_TIMESTAMP, RESULT_CRC_SIGNATURE,
                     SCHEDULE_WEEKDAY_LIST, TEST_MINUTES,
                     TEST_TIMEDELTA_MIN_FAILURE,
                     TEST_TIMEDELTA_SUCCESS_SECONDS,
                     TEST_TIMEDELTA_SUCCESS_NO_SECONDS,
                     TEST_TIMEDELTA_MAX_FAILURE, TEST_SECONDS,
                     TIMESTAMP_COMPARE_FORMAT, TEST_HEX_WEEKDAYS_SET_LIST,
                     DUMMY_START_TIME_SET)


@mark.asyncio
async def test_convert_seconds_to_iso_time(
        event_loop: AbstractEventLoop) -> None:
    """Test the convert_seconds_to_iso_time tool."""
    try:
        result = await convert_seconds_to_iso_time(event_loop, TEST_SECONDS)
        await assert_seconds_to_iso_time(TEST_SECONDS, result)
    except CalculationError as exc:
        fail("failed converting seconds to iso time string, {}".format(exc))


@mark.asyncio
async def test_crc_sign_full_packet_com_key(
        event_loop: AbstractEventLoop) -> None:
    """Test the crc_sign_full_packet_com_key tool."""
    try:
        packet = GET_STATE_PACKET.format(
            DUMMY_SESSION_ID, DUMMY_TIMESTAMP, DUMMY_DEVICE_ID)
        result = await crc_sign_full_packet_com_key(event_loop, packet)
        assert packet == result[:-8]
        assert RESULT_CRC_SIGNATURE == result[-8:]
    except EncodingError as exc:
        fail("failed checking crc signature, {}".format(exc))


@mark.asyncio
async def test_convert_minutes_to_timer(event_loop: AbstractEventLoop) -> None:
    """Test the convert_minutes_to_timer tool."""
    try:
        result = await convert_minutes_to_timer(event_loop, TEST_MINUTES)
        unpacked = unpack(
            STRUCT_PACKING_FORMAT,
            unhexlify(result.encode(ENCODING_CODEC)))
        assert TEST_MINUTES == str(int(unpacked[0] / 60))
    except EncodingError as exc:
        fail("failed converting minutes to timer, {}".format(exc))


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
        fail("failed converting timedelta to auto off, {}".format(exc))


@mark.asyncio
async def test_convert_string_to_device_name(
        event_loop: AbstractEventLoop) -> None:
    """Test the convert_string_to_device_name tool."""
    try:
        result = await convert_string_to_device_name(
            event_loop, DUMMY_DEVICE_NAME)
        unhexed = \
            unhexlify(result).decode(ENCODING_CODEC)[:len(DUMMY_DEVICE_NAME)]
        assert len(result) == 64
        assert DUMMY_DEVICE_NAME == unhexed
    except EncodingError as exc:
        fail("failed converting string to device name, {}".format(exc))


@mark.asyncio
async def test_get_days_list_from_bytes(event_loop: AbstractEventLoop) -> None:
    """Test the get_days_list_from_bytes tool."""
    try:
        for test_set in TEST_HEX_WEEKDAYS_SET_LIST:
            result = await get_days_list_from_bytes(event_loop, test_set[0])
            await assert_lists_equal(result, test_set[1])
    except DecodingError as exc:
        fail("failed converting int to days list, {}".format(exc))


@mark.asyncio
async def test_get_time_from_bytes(event_loop: AbstractEventLoop) -> None:
    """Test the get_time_from_bytes tool."""
    result = await get_time_from_bytes(event_loop, DUMMY_START_TIME_SET[0])
    assert result == DUMMY_START_TIME_SET[1]


@mark.asyncio
async def test_get_timestamp(event_loop: AbstractEventLoop) -> None:
    """Test the get_timestamp tool."""
    try:
        result = await get_timestamp(event_loop)
        unpacked = unpack(
            STRUCT_PACKING_FORMAT,
            unhexlify(result.encode(ENCODING_CODEC)))

        approx_datetime = datetime.fromtimestamp(unpacked[0])

        assert approx_datetime.strftime(TIMESTAMP_COMPARE_FORMAT) == \
            datetime.now().strftime(TIMESTAMP_COMPARE_FORMAT)

    except EncodingError as exc:
        fail("failed creating timestamp string, {}".format(exc))


@mark.asyncio
async def test_create_weekdays_value(event_loop: AbstractEventLoop) -> None:
    """Test the create_weekdays_value tool."""
    try:
        result = await create_weekdays_value(event_loop, SCHEDULE_WEEKDAY_LIST)
        assert int(result, 16) == int(sum(SCHEDULE_WEEKDAY_LIST))
    except EncodingError as exc:
        fail("failed creating weekdays from list, {}".format(exc))


@mark.asyncio
async def test_timedelta_str_to_schedule_time(
        event_loop: AbstractEventLoop) -> None:
    """Test the timedelta_str_to_schedule_time tool."""
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
        fail("failed converting timedelta to schedule time string, {}"
             .format(exc))
