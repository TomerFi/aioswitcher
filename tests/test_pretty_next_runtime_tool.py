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

"""Switcher unofficial integration pretty next run tool test cases."""

from datetime import datetime, timedelta

import time_machine
from assertpy import assert_that
from pytest import fixture

from aioswitcher import Days
from aioswitcher.schedules import _pretty_next_run

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
    assert_that(_pretty_next_run(one_hour_from_now)).is_equal_to(expected_return)


def test_pretty_next_run_with_todays_day_should_return_due_today(todays_day, one_hour_from_now):
    expected_return = f"Due today at {one_hour_from_now}"
    assert_that(_pretty_next_run(one_hour_from_now, {todays_day})).is_equal_to(expected_return)


def test_pretty_next_run_with_multiple_days_should_return_due_the_closest_day(today):
    two_days_from_now = today + timedelta(days=2)
    four_days_from_now = today + timedelta(days=4)

    two_days_from_now_day = days_by_weekdays[two_days_from_now.weekday()]
    four_days_from_now_day = days_by_weekdays[four_days_from_now.weekday()]

    expected_return = f"Due next {two_days_from_now_day.value} at 13:00"

    assert_that(_pretty_next_run("13:00", {four_days_from_now_day, two_days_from_now_day})).is_equal_to(expected_return)


def test_pretty_next_run_on_yesterday_with_todays_day_should_return_due_tommorow(today, todays_day):
    expected_return = "Due tommorow at 13:00"
    yesterday = today - timedelta(days=1)
    with time_machine.travel(yesterday):
        assert_that(_pretty_next_run("13:00", {todays_day})).is_equal_to(expected_return)


def test_pretty_next_run_on_two_days_ago_with_todays_day_should_return_due_on_next_day(today, todays_day):
    expected_return = f"Due next {todays_day.value} at 13:00"
    two_days_ago = today - timedelta(days=2)
    with time_machine.travel(two_days_ago):
        assert_that(_pretty_next_run("13:00", {todays_day})).is_equal_to(expected_return)


def test_pretty_next_run_on_last_sunday_with_monday_selected_should_return_due_tommorow(today):
    expected_return = "Due tommorow at 13:00"
    last_sunday = today - timedelta(days=((today.weekday() + 1) % 7))
    with time_machine.travel(last_sunday):
        assert_that(_pretty_next_run("13:00", {Days.MONDAY})).is_equal_to(expected_return)
