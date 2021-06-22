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

from dataclasses import dataclass, field
from enum import Enum, unique
from typing import Set

from .. import Days
from . import tools

__all__ = ["ScheduleStatus", "SwitcherSchedule", "get_schedules", "tools"]

# weekdays sum, start-time timestamp, end-time timestamp
SCHEDULE_CREATE_DATA_FORMAT = "01{}01{}{}"


@unique
class ScheduleStatus(Enum):
    """Enum representing the status of the schedule."""

    ENABLED = "01"
    DISABLED = "00"


@dataclass
class SwitcherSchedule:
    """Represnation of the Switcher schedule slot.

    Args:
        schedule_id: the id of the schedule
        enabled: is the shcedule enabled
        recurring: is a recurring schedule
        days: a set of schedule days, or empty set for non recurring schedules
        start_time: the start time of the schedule
        end_time: the end time of the schedule
        schedule_data: bytes data to communuicate with the device

    """

    schedule_id: str
    enabled: bool
    recurring: bool
    days: Set[Days]
    start_time: str
    end_time: str
    schedule_data: bytes
    duration: str = field(init=False)
    display: str = field(init=False)

    def __post_init__(self) -> None:
        """Post initialization, set duration and display."""
        self._duration = tools.calc_duration(self.start_time, self.end_time)
        self._display = tools.pretty_next_run(self.start_time, self.days)


@dataclass(frozen=True)
class ScheduleParser:
    """Schedule parsing tool."""

    schedule: bytes

    def get_id(self) -> str:
        """Return the id of the schedule."""
        return str(int(self.schedule[0:2], 16))

    def is_enabled(self) -> bool:
        """Return true if enbaled."""
        return int(self.schedule[2:4], 16) == 1

    def is_recurring(self) -> bool:
        """Return true if a recurring schedule."""
        return self.schedule[4:6] != "00"

    def get_days(self) -> Set[Days]:
        """Retun a set of the scheduled Days."""
        return tools.bit_summary_to_days(int(self.schedule[4:6], 16))

    def get_start_time(self) -> str:
        """Return the schedule start time in %H:%M format."""
        return tools.hexadecimale_timestamp_to_localtime(self.schedule[8:16])

    def get_end_time(self) -> str:
        """Return the schedule end time in %H:%M format."""
        return tools.hexadecimale_timestamp_to_localtime(self.schedule[16:24])

    def get_data(self) -> bytes:
        """Get the bytes data for communication with device."""
        schedule_id = self.schedule[0:2]
        enabled = self.schedule[2:4]
        days = self.schedule[4:6]
        state = self.schedule[6:8]
        start_time = self.schedule[8:16]
        end_time = self.schedule[16:24]

        return schedule_id + enabled + days + state + start_time + end_time


def get_schedules(message: bytes) -> Set[SwitcherSchedule]:
    """Use to create a list of schedule from a response message from the device."""
    schedule_data = message[90:-8].decode()
    schedule_list = [
        schedule_data[i : i + 32] for i in range(0, len(schedule_data), 32)  # noqa E203
    ]
    ret_set = set()
    for schedule in schedule_list:
        parser = ScheduleParser(schedule.encode())
        ret_set.add(
            SwitcherSchedule(
                parser.get_id(),
                parser.is_enabled(),
                parser.is_recurring(),
                parser.get_days(),
                parser.get_start_time(),
                parser.get_end_time(),
                parser.get_data(),
            )
        )

    return ret_set
