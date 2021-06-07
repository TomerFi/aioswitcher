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

"""Verify the custom enum of Days."""

from assertpy import assert_that
from pytest import mark

from aioswitcher import Days


@mark.parametrize("sut_day,expected_value,expected_hex_rep,expected_bit_rep,expected_weekday", [
    (Days.MONDAY, "Monday", 0x2, 2, 0),
    (Days.TUESDAY, "Tuesday", 0x4, 4, 1),
    (Days.WEDNESDAY, "Wednesday", 0x8, 8, 2),
    (Days.THURSDAY, "Thursday", 0x10, 16, 3),
    (Days.FRIDAY, "Friday", 0x20, 32, 4),
    (Days.SATURDAY, "Saturday", 0x40, 64, 5),
    (Days.SUNDAY, "Sunday", 0x80, 128, 6),
])
def test_the_and_verify_the_paramerized_member_of_the_days_enum(sut_day, expected_value, expected_hex_rep, expected_bit_rep, expected_weekday):
    assert_that(sut_day.value).is_equal_to(expected_value)
    assert_that(sut_day.hex_rep).is_equal_to(expected_hex_rep)
    assert_that(sut_day.bit_rep).is_equal_to(expected_bit_rep)
    assert_that(sut_day.weekday).is_equal_to(expected_weekday)
