"""Switcher water heater Utility functions test cases."""

import time
from binascii import hexlify, unhexlify
from datetime import datetime, timedelta
from struct import pack, unpack

from assertpy import assert_that
from pytest import mark

from aioswitcher import Weekday, utils
from aioswitcher.errors import CalculationError, DecodingError, EncodingError


def test_seconds_to_iso_time_with_a_valid_seconds_value_should_return_a_time_string():
    assert_that(utils.seconds_to_iso_time(86399)).is_equal_to("23:59:59")


def test_seconds_to_iso_time_with_a_nagative_value_should_throw_a_calculation_error():
    assert_that(utils.seconds_to_iso_time).raises(
        CalculationError
    ).when_called_with(-1).is_equal_to("failed to convert seconds to iso time")


def test_minutes_to_hexadecimal_seconds_with_correct_minutes_should_return_expected_hex_seconds():
    # TODO: replace the equality assertion with an unhexlified unpacked value
    hex_sut = utils.minutes_to_hexadecimal_seconds(90)
    assert_that(hex_sut).is_equal_to("18150000")


def test_minutes_to_hexadecimal_seconds_with_a_negative_value_should_throw_an_encoding_error():
    assert_that(utils.minutes_to_hexadecimal_seconds).raises(
        EncodingError
    ).when_called_with(-1).is_equal_to("failed to encode -1 minutes")


def test_timedelta_to_hexadecimal_seconds_with_an_allowed_timedelta_should_return_an_hex_timestamp():
    # TODO: replace the equality assertion with an unhexlified unpacked value
    hex_timestamp = utils.timedelta_to_hexadecimal_seconds(timedelta(hours=1, minutes=30))
    assert_that(hex_timestamp).is_equal_to("18150000")


@mark.parametrize("out_of_range", [timedelta(minutes=59), timedelta(hours=24)])
def test_timedelta_to_hexadecimal_seconds_with_an_out_of_range_value_should_throw_an_encoding_error(out_of_range):
    assert_that(utils.timedelta_to_hexadecimal_seconds).raises(
        EncodingError
    ).when_called_with(out_of_range).starts_with("failed to encode")


def test_string_to_hexadecimale_device_name_with_a_correct_length_name_should_return_a_right_zero_padded_hex_name():
    str_name = "my device cool name"
    hex_name = utils.string_to_hexadecimale_device_name(str_name)
    unhexed_name = unhexlify(hex_name.rstrip("0")).decode()
    assert_that(unhexed_name).is_equal_to(str_name)


@mark.parametrize("unsupported_length_value", ["t", "t" * 33])
def test_string_to_hexadecimale_device_name_with_an_unsupported_length_value_should_throw_an_encoding_error(unsupported_length_value):
    assert_that(utils.string_to_hexadecimale_device_name).raises(
        EncodingError
    ).when_called_with(unsupported_length_value).starts_with("failed to encode")


def test_current_timestamp_to_hexadecimal_should_return_the_current_timestamp():
    hex_timestamp = utils.current_timestamp_to_hexadecimal()

    binary_timestamp = unhexlify(hex_timestamp.encode())
    unpacked_timestamp = unpack("<I", binary_timestamp)
    sut_datetime = datetime.fromtimestamp(unpacked_timestamp[0])

    assert_that(sut_datetime).is_equal_to_ignoring_time(datetime.now())


def test_current_timestamp_to_hexadecimal_with_errornous_value_should_throw_a_decoding_error(monkeypatch):
    # patch the time method to return a nagative value instead of the actuall timestamp
    monkeypatch.setattr(time, "time", lambda: -1)

    assert_that(utils.current_timestamp_to_hexadecimal).raises(
        DecodingError
    ).when_called_with().is_equal_to("failed to generate timestamp")


def test_time_to_hexadecimal_timestamp_with_correct_time_should_return_the_expected_timestamp():
    hex_timestamp = utils.time_to_hexadecimal_timestamp("21:00")

    binary_timestamp = unhexlify(hex_timestamp.encode())
    unpacked_timestamp = unpack("<I", binary_timestamp)
    sut_datetime = datetime.fromtimestamp(unpacked_timestamp[0])
    assert_that(
        sut_datetime
    ).is_equal_to_ignoring_time(datetime.now()).has_hour(21).has_minute(0)


def test_time_to_hexadecimal_timestamp_with_incorrect_time_should_throw_an_encoding_error():
    assert_that(utils.time_to_hexadecimal_timestamp).raises(
        EncodingError
    ).when_called_with("2100").is_equal_to("failed to encode 2100")


def test_hexadecimale_timestamp_to_localtime_with_the_current_timestamp_should_return_a_time_string():
    sut_datetime = datetime.now()
    hex_timestamp = hexlify(pack("<I", round(sut_datetime.timestamp())))
    assert_that(
        utils.hexadecimale_timestamp_to_localtime(hex_timestamp)
    ).is_equal_to(sut_datetime.time().strftime("%H:%M"))


def test_hexadecimale_timestamp_to_localtime_with_wrong_value_should_throw_a_decoding_error():
    assert_that(utils.hexadecimale_timestamp_to_localtime).raises(
        DecodingError
    ).when_called_with("wrongvalue".encode()).is_equal_to("failed to decode timestamp")


@mark.parametrize("weekdays, expected_sum", [
    (Weekday.MONDAY, 2),
    ({Weekday.MONDAY, Weekday.TUESDAY}, 6),
    ({Weekday.MONDAY, Weekday.TUESDAY, Weekday.WEDNESDAY}, 14),
    ({Weekday.MONDAY, Weekday.TUESDAY, Weekday.WEDNESDAY, Weekday.THURSDAY}, 30),
    ({Weekday.MONDAY, Weekday.TUESDAY, Weekday.WEDNESDAY, Weekday.THURSDAY, Weekday.FRIDAY}, 62),
    ({Weekday.MONDAY, Weekday.TUESDAY, Weekday.WEDNESDAY, Weekday.THURSDAY, Weekday.FRIDAY, Weekday.SATURDAY}, 126),
    ({Weekday.MONDAY, Weekday.TUESDAY, Weekday.WEDNESDAY, Weekday.THURSDAY, Weekday.FRIDAY, Weekday.SATURDAY, Weekday.SUNDAY}, 254),
])
def test_weekdays_to_hexadecimal_with_parameterized_weekday_set_should_return_the_expected_sum(weekdays, expected_sum):
    sut_hex = utils.weekdays_to_hexadecimal(weekdays)
    sut_int = int(sut_hex, 16)
    assert_that(sut_int).is_equal_to(expected_sum)


@mark.parametrize("empty_collection", [set(), (), {}, []])
def test_weekdays_to_hexadecimal_with_empty_collections_should_throw_an_encoding_error(empty_collection):
    assert_that(utils.weekdays_to_hexadecimal).raises(
        EncodingError
    ).when_called_with(empty_collection).is_equal_to("failed to calculate weekdays")


@mark.parametrize("duplicate_members", [(Weekday.MONDAY, Weekday.MONDAY), [Weekday.MONDAY, Weekday.MONDAY]])
def test_weekdays_to_hexadecimal_with_duplicate_members_should_throw_an_encoding_error(duplicate_members):
    assert_that(utils.weekdays_to_hexadecimal).raises(
        EncodingError
    ).when_called_with(duplicate_members).is_equal_to("failed to calculate weekdays")


@mark.parametrize("sum, expected_weekdays", [
    (2, {Weekday.MONDAY}),
    (6, {Weekday.MONDAY, Weekday.TUESDAY}),
    (14, {Weekday.MONDAY, Weekday.TUESDAY, Weekday.WEDNESDAY},),
    (30, {Weekday.MONDAY, Weekday.TUESDAY, Weekday.WEDNESDAY, Weekday.THURSDAY}),
    (62, {Weekday.MONDAY, Weekday.TUESDAY, Weekday.WEDNESDAY, Weekday.THURSDAY, Weekday.FRIDAY}),
    (126, {Weekday.MONDAY, Weekday.TUESDAY, Weekday.WEDNESDAY, Weekday.THURSDAY, Weekday.FRIDAY, Weekday.SATURDAY}),
    (254, {Weekday.MONDAY, Weekday.TUESDAY, Weekday.WEDNESDAY, Weekday.THURSDAY, Weekday.FRIDAY, Weekday.SATURDAY, Weekday.SUNDAY}),
])
def test_bit_summary_to_weekdays_with_parameterized_sum_should_return_the_expected_weekday_set(sum, expected_weekdays):
    assert_that(utils.bit_summary_to_weekdays(sum)).is_equal_to(expected_weekdays)


@mark.parametrize("wrong_bit_sum", [1, 255])
def test_bit_summary_to_weekdays_with_wrong_bit_sum_parameterized_value(wrong_bit_sum):
    assert_that(utils.bit_summary_to_weekdays).raises(
        DecodingError
    ).when_called_with(wrong_bit_sum).is_equal_to("failed to decode value to weekdays")
