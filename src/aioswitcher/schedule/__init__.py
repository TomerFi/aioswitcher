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

"""Switcher unofficial integration schedule module."""

from enum import Enum, unique

# weekdays sum, start-time timestamp, end-time timestamp
SCHEDULE_CREATE_DATA_FORMAT = "01{}01{}{}"


@unique
class ScheduleStatus(Enum):
    """Enum representing the status of the schedule."""

    ENABLED = "01"
    DISABLED = "00"


@unique
class Days(Enum):
    """Enum class represnting the day entity."""

    MONDAY = ("Monday", 0x02, 2, 0)
    TUESDAY = ("Tuesday", 0x04, 4, 1)
    WEDNESDAY = ("Wednesday", 0x08, 8, 2)
    THURSDAY = ("Thursday", 0x10, 16, 3)
    FRIDAY = ("Friday", 0x20, 32, 4)
    SATURDAY = ("Saturday", 0x40, 64, 5)
    SUNDAY = ("Sunday", 0x80, 128, 6)

    def __new__(cls, value: str, hex_rep: int, bit_rep: int, weekday: int) -> "Days":
        """Override the default enum constructor and include extra properties."""
        new_enum = object.__new__(cls)
        new_enum._value_ = value
        new_enum._hex_rep = hex_rep
        new_enum._bit_rep = bit_rep
        new_enum._weekday = weekday
        return new_enum

    @property
    def bit_rep(self) -> int:
        """Return the bit represntation of the day."""
        return self._bit_rep  # type: ignore

    @property
    def hex_rep(self) -> int:
        """Return the hexadecimal represntation of the day."""
        return self._hex_rep  # type: ignore

    @property
    def weekday(self) -> int:
        """Return the weekday of the day."""
        return self._weekday  # type: ignore
