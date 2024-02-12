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

"""Switcher integration pretty next run tool test cases."""

from binascii import hexlify, unhexlify
from datetime import datetime, timedelta
from struct import pack, unpack

import time_machine
from assertpy import assert_that
from pytest import fixture, mark

from aioswitcher.schedule import Days, tools

days_by_weekdays = dict(map(lambda d: (d.weekday, d), Days))


@fixture()
def today():
    return datetime.utcnow()


@fixture
def todays_day(today):
    return days_by_weekdays[today.weekday()]


@fixture
def one_hour_from_now(today):
    return datetime.strftime(today + timedelta(hours=1), "%H:%M")


def test_pretty_next_run_with_no_selected_days_should_return_due_today(one_hour_from_now):
    expected_return = f"Due today at {one_hour_from_now}"
    assert_that(tools.pretty_next_run(one_hour_from_now)).is_equal_to(expected_return)


def test_pretty_next_run_with_todays_day_should_return_due_today(todays_day, one_hour_from_now):
    expected_return = f"Due today at {one_hour_from_now}"
    assert_that(tools.pretty_next_run(one_hour_from_now, {todays_day})).is_equal_to(expected_return)


def test_pretty_next_run_with_multiple_days_should_return_due_the_closest_day(today):
    two_days_from_now = today + timedelta(days=2)
    four_days_from_now = today + timedelta(days=4)

    two_days_from_now_day = days_by_weekdays[two_days_from_now.weekday()]
    four_days_from_now_day = days_by_weekdays[four_days_from_now.weekday()]

    expected_return = f"Due next {two_days_from_now_day.value} at 13:00"

    assert_that(tools.pretty_next_run("13:00", {four_days_from_now_day, two_days_from_now_day})).is_equal_to(expected_return)


def test_pretty_next_run_on_yesterday_with_todays_day_should_return_due_tomorrow(today, todays_day):
    expected_return = "Due tomorrow at 13:00"
    yesterday = today - timedelta(days=1)
    with time_machine.travel(yesterday):
        assert_that(tools.pretty_next_run("13:00", {todays_day})).is_equal_to(expected_return)


def test_pretty_next_run_on_two_days_ago_with_todays_day_should_return_due_on_next_day(today, todays_day):
    expected_return = f"Due next {todays_day.value} at 13:00"
    two_days_ago = today - timedelta(days=2)
    with time_machine.travel(two_days_ago):
        assert_that(tools.pretty_next_run("13:00", {todays_day})).is_equal_to(expected_return)


def test_pretty_next_run_on_last_sunday_with_monday_selected_should_return_due_tomorrow(today):
    expected_return = "Due tomorrow at 13:00"
    last_sunday = today - timedelta(days=((today.weekday() + 1) % 7))
    with time_machine.travel(last_sunday):
        assert_that(tools.pretty_next_run("13:00", {Days.MONDAY})).is_equal_to(expected_return)


def test_calc_duration_with_valid_start_and_end_time_should_return_the_duration():
    assert_that(tools.calc_duration("13:00", "14:00")).is_equal_to("1:00:00")


def test_calc_duration_with_greater_start_time_than_end_time_should_assume_next_day():
    assert_that(tools.calc_duration("14:00", "13:00")).is_equal_to("23:00:00")


def test_hexadecimale_timestamp_to_localtime_with_the_current_timestamp_should_return_a_time_string():
    sut_datetime = datetime.now()
    hex_timestamp = hexlify(pack("<I", round(sut_datetime.timestamp())))
    assert_that(
        tools.hexadecimale_timestamp_to_localtime(hex_timestamp)
    ).is_equal_to(sut_datetime.time().strftime("%H:%M"))


def test_hexadecimale_timestamp_to_localtime_with_wrong_value_should_throw_an_error():
    assert_that(tools.hexadecimale_timestamp_to_localtime).raises(
        ValueError
    ).when_called_with("wrongvalue".encode()).starts_with("invalid literal for int() with base 16")


@mark.parametrize("sum, expected_weekdays", [
    (2, {Days.MONDAY}),
    (6, {Days.MONDAY, Days.TUESDAY}),
    (14, {Days.MONDAY, Days.TUESDAY, Days.WEDNESDAY},),
    (30, {Days.MONDAY, Days.TUESDAY, Days.WEDNESDAY, Days.THURSDAY}),
    (62, {Days.MONDAY, Days.TUESDAY, Days.WEDNESDAY, Days.THURSDAY, Days.FRIDAY}),
    (126, {Days.MONDAY, Days.TUESDAY, Days.WEDNESDAY, Days.THURSDAY, Days.FRIDAY, Days.SATURDAY}),
    (254, {Days.MONDAY, Days.TUESDAY, Days.WEDNESDAY, Days.THURSDAY, Days.FRIDAY, Days.SATURDAY, Days.SUNDAY}),
])
def test_bit_summary_to_days_with_parameterized_sum_should_return_the_expected_weekday_set(sum, expected_weekdays):
    assert_that(tools.bit_summary_to_days(sum)).is_equal_to(expected_weekdays)


@mark.parametrize("wrong_bit_sum", [1, 255])
def test_bit_summary_to_days_with_wrong_bit_sum_parameterized_value(wrong_bit_sum):
    assert_that(tools.bit_summary_to_days).raises(
        ValueError
    ).when_called_with(wrong_bit_sum).is_equal_to("weekdays bit sum should be between 2 and 254")


@mark.parametrize("weekdays, expected_sum", [
    (Days.MONDAY, 2),
    ({Days.MONDAY, Days.TUESDAY}, 6),
    ({Days.MONDAY, Days.TUESDAY, Days.WEDNESDAY}, 14),
    ({Days.MONDAY, Days.TUESDAY, Days.WEDNESDAY, Days.THURSDAY}, 30),
    ({Days.MONDAY, Days.TUESDAY, Days.WEDNESDAY, Days.THURSDAY, Days.FRIDAY}, 62),
    ({Days.MONDAY, Days.TUESDAY, Days.WEDNESDAY, Days.THURSDAY, Days.FRIDAY, Days.SATURDAY}, 126),
    ({Days.MONDAY, Days.TUESDAY, Days.WEDNESDAY, Days.THURSDAY, Days.FRIDAY, Days.SATURDAY, Days.SUNDAY}, 254),
])
def test_weekdays_to_hexadecimal_with_parameterized_weekday_set_should_return_the_expected_sum(weekdays, expected_sum):
    sut_hex = tools.weekdays_to_hexadecimal(weekdays)
    sut_int = int(sut_hex, 16)
    assert_that(sut_int).is_equal_to(expected_sum)


@mark.parametrize("empty_collection", [set(), (), {}, []])
def test_weekdays_to_hexadecimal_with_empty_collections_should_throw_an_error(empty_collection):
    assert_that(tools.weekdays_to_hexadecimal).raises(
        ValueError
    ).when_called_with(empty_collection).is_equal_to("no days requested")


@mark.parametrize("duplicate_members", [(Days.MONDAY, Days.MONDAY), [Days.MONDAY, Days.MONDAY]])
def test_weekdays_to_hexadecimal_with_duplicate_members_should_throw_an_encoding_error(duplicate_members):
    assert_that(tools.weekdays_to_hexadecimal).raises(
        ValueError
    ).when_called_with(duplicate_members).is_equal_to("no days requested")


def test_time_to_hexadecimal_timestamp_with_correct_time_should_return_the_expected_timestamp():
    hex_timestamp = tools.time_to_hexadecimal_timestamp("21:00")

    binary_timestamp = unhexlify(hex_timestamp.encode())
    unpacked_timestamp = unpack("<I", binary_timestamp)
    sut_datetime = datetime.fromtimestamp(unpacked_timestamp[0])
    assert_that(
        sut_datetime
    ).is_equal_to_ignoring_time(datetime.now()).has_hour(21).has_minute(0)


def test_time_to_hexadecimal_timestamp_with_incorrect_time_should_throw_an_error():
    assert_that(tools.time_to_hexadecimal_timestamp).raises(
        IndexError
    ).when_called_with("2100").is_equal_to("list index out of range")
