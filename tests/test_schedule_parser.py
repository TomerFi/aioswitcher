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

"""Switcher integration schedule parser module test cases."""

import time
from binascii import unhexlify
from datetime import datetime, timedelta
from pathlib import Path

import pytz
from assertpy import assert_that

from aioswitcher.schedule import Days, ScheduleState
from aioswitcher.schedule.parser import ScheduleParser, SwitcherSchedule, get_schedules


def test_switcher_schedule_dataclass_to_verify_the_post_initialization_of_the_dispaly_and_duration():
    sut = SwitcherSchedule("1", False, set(), "13:00", "14:00")
    assert_that(sut.duration).is_equal_to("1:00:00")
    assert_that(sut.display).is_equal_to("Due today at 13:00")


def test_switcher_schedule_dataclass_to_verify_equality_and_hashing():
    sut0 = SwitcherSchedule("0", False, set(), "13:00", "14:00")
    sut1 = SwitcherSchedule("1", False, set(), "13:00", "14:00")
    assert_that(sut0.__eq__(sut0)).is_true()
    assert_that(sut0.__eq__(sut1)).is_false()
    assert_that(sut0.__eq__(object())).is_false()


def test_schedule_parser_with_a_weekly_recurring_enabled_schedule_data():
    schedule_data = b"01010201e06aa35cf078a35cce0e0000"
    sut = ScheduleParser(schedule_data)
    assert_that(sut.get_id()).is_equal_to("1")
    assert_that(sut.is_enabled()).is_true()
    assert_that(sut.is_recurring()).is_true()
    assert_that(sut.get_days()).contains_only(Days.MONDAY)
    assert_that(sut.get_start_time()).is_equal_to(
        local_time_for_time_in_timezone("17:00", "Asia/Jerusalem"))
    assert_that(sut.get_end_time()).is_equal_to(
        local_time_for_time_in_timezone("18:00", "Asia/Jerusalem"))
    assert_that(sut.get_state()).is_equal_to(ScheduleState.ENABLED)
    assert_that(sut.schedule).is_equal_to(schedule_data)


def test_schedule_parser_with_a_daily_recurring_enabled_schedule_data():
    schedule_data = b"0101fe01e06aa35cf078a35cce0e0000"
    sut = ScheduleParser(schedule_data)
    assert_that(sut.get_id()).is_equal_to("1")
    assert_that(sut.is_enabled()).is_true()
    assert_that(sut.is_recurring()).is_true()
    assert_that(sut.get_days()).is_equal_to(set(Days))
    assert_that(sut.get_start_time()).is_equal_to(
        local_time_for_time_in_timezone("17:00", "Asia/Jerusalem"))
    assert_that(sut.get_end_time()).is_equal_to(
        local_time_for_time_in_timezone("18:00", "Asia/Jerusalem"))
    assert_that(sut.get_state()).is_equal_to(ScheduleState.ENABLED)
    assert_that(sut.schedule).is_equal_to(schedule_data)


def test_schedule_parser_with_a_partial_daily_recurring_enabled_schedule_data():
    schedule_data = b"0001fc01e871a35cf87fa35cce0e0000"
    sut = ScheduleParser(schedule_data)
    assert_that(sut.get_id()).is_equal_to("0")
    assert_that(sut.is_enabled()).is_true()
    assert_that(sut.is_recurring()).is_true()
    assert_that(sut.get_days()).contains_only(Days.SUNDAY, Days.SATURDAY, Days.FRIDAY, Days.THURSDAY, Days.TUESDAY, Days.WEDNESDAY)
    assert_that(sut.get_start_time()).is_equal_to(
        local_time_for_time_in_timezone("17:30", "Asia/Jerusalem"))
    assert_that(sut.get_end_time()).is_equal_to(
        local_time_for_time_in_timezone("18:30", "Asia/Jerusalem"))
    assert_that(sut.get_state()).is_equal_to(ScheduleState.ENABLED)
    assert_that(sut.schedule).is_equal_to(schedule_data)


def test_schedule_parser_with_a_non_recurring_enabled_schedule_data():
    schedule_data = b"01010001e06aa35cf078a35cce0e0000"
    sut = ScheduleParser(schedule_data)
    assert_that(sut.get_id()).is_equal_to("1")
    assert_that(sut.is_enabled()).is_true()
    assert_that(sut.is_recurring()).is_false()
    assert_that(sut.get_days()).is_empty()
    assert_that(sut.get_start_time()).is_equal_to(
        local_time_for_time_in_timezone("17:00", "Asia/Jerusalem"))
    assert_that(sut.get_end_time()).is_equal_to(
        local_time_for_time_in_timezone("18:00", "Asia/Jerusalem"))
    assert_that(sut.get_state()).is_equal_to(ScheduleState.ENABLED)
    assert_that(sut.schedule).is_equal_to(schedule_data)


def test_get_schedules_with_a_two_schedules_packet(resource_path):
    response = Path(f'{resource_path}.txt').read_text().replace('\n', '').encode()
    set_of_schedules = get_schedules(unhexlify(response))
    assert_that(set_of_schedules).is_length(2)
    for schedule in set_of_schedules:
        assert_that(schedule).is_instance_of(SwitcherSchedule)


# local_time_for_time_in_timezone is a utility function taking a time and a timezone,
# and returning the local time matching the given time in the given timezone.
#
# Examples, assuming my local timezone is EST:
# local_time_for_time_in_timezone("17:00", "Asia/Jerusalem") will return 10:00
# local_time_for_time_in_timezone("17:00", "Asia/Kolkata") will return 06:30
# local_time_for_time_in_timezone("17:00", "US/Pacific") will return 20:00
# local_time_for_time_in_timezone("17:00", "EST") will return 17:00
def local_time_for_time_in_timezone(val, tz):
    local_ts = datetime.now().replace(tzinfo=None, second=0, microsecond=0)
    remote_ts = (datetime.now(pytz.timezone(tz))
                 .replace(tzinfo=None, second=0, microsecond=0))

    fmt = "%H:%M"
    parsed = time.strptime(val, fmt)
    target = timedelta(hours=parsed.tm_hour, minutes=parsed.tm_min)
    delta = local_ts - remote_ts
    diff = target + timedelta(seconds=delta.total_seconds())

    return (datetime.min + diff).strftime(fmt)
