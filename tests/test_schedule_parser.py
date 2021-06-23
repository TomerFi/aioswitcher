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

"""Switcher unofficial integration schedule parser module test cases."""

from assertpy import assert_that
from aioswitcher.schedule import Days, ScheduleState

from aioswitcher.schedule.parser import ScheduleParser, SwitcherSchedule


def test_switcher_schedule_dataclass_to_verify_the_post_initialization_of_the_dispaly_and_duration():
    sut = SwitcherSchedule("1", True, False, set(), "13:00", "14:00", b"")
    assert_that(sut.duration).is_equal_to("1:00:00")
    assert_that(sut.display).is_equal_to("Due today at 13:00")


def test_schedule_parser_with_a_weekly_recurring_enabled_schedule_data():
    schedule_data = b"01010201e06aa35cf078a35c"
    sut = ScheduleParser(schedule_data)
    assert_that(sut.get_id()).is_equal_to("1")
    assert_that(sut.is_enabled()).is_true()
    assert_that(sut.is_recurring()).is_true()
    assert_that(sut.get_days()).contains_only(Days.MONDAY)
    assert_that(sut.get_start_time()).is_equal_to("17:00")
    assert_that(sut.get_end_time()).is_equal_to("18:00")
    assert_that(sut.get_state()).is_equal_to(ScheduleState.ENABLED)
    assert_that(sut.schedule).is_equal_to(schedule_data)


def test_schedule_parser_with_a_daily_recurring_enabled_schedule_data():
    schedule_data = b"0101fe01e06aa35cf078a35c"
    sut = ScheduleParser(schedule_data)
    assert_that(sut.get_id()).is_equal_to("1")
    assert_that(sut.is_enabled()).is_true()
    assert_that(sut.is_recurring()).is_true()
    assert_that(sut.get_days()).is_equal_to(set(Days))
    assert_that(sut.get_start_time()).is_equal_to("17:00")
    assert_that(sut.get_end_time()).is_equal_to("18:00")
    assert_that(sut.get_state()).is_equal_to(ScheduleState.ENABLED)
    assert_that(sut.schedule).is_equal_to(schedule_data)


def test_schedule_parser_with_a_non_recurring_enabled_schedule_data():
    schedule_data = b"01010001e06aa35cf078a35c"
    sut = ScheduleParser(schedule_data)
    assert_that(sut.get_id()).is_equal_to("1")
    assert_that(sut.is_enabled()).is_true()
    assert_that(sut.is_recurring()).is_false()
    assert_that(sut.get_days()).is_empty()
    assert_that(sut.get_start_time()).is_equal_to("17:00")
    assert_that(sut.get_end_time()).is_equal_to("18:00")
    assert_that(sut.get_state()).is_equal_to(ScheduleState.ENABLED)
    assert_that(sut.schedule).is_equal_to(schedule_data)
