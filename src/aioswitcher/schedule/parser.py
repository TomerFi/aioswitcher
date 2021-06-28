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

"""Switcher unofficial integration schedule parser module."""

from binascii import hexlify
from dataclasses import dataclass, field
from textwrap import wrap
from typing import Set

from typing_extensions import final

from . import Days, ScheduleState, tools


@final
@dataclass
class SwitcherSchedule:
    """representation of the Switcher schedule slot.

    Args:
        schedule_id: the id of the schedule
        recurring: is a recurring schedule
        days: a set of schedule days, or empty set for non recurring schedules
        start_time: the start time of the schedule
        end_time: the end time of the schedule

    """

    schedule_id: str
    recurring: bool
    days: Set[Days]
    start_time: str
    end_time: str
    duration: str = field(init=False)
    display: str = field(init=False)

    def __post_init__(self) -> None:
        """Post initialization, set duration and display."""
        self.duration = tools.calc_duration(self.start_time, self.end_time)
        self.display = tools.pretty_next_run(self.start_time, self.days)

    def __hash__(self) -> int:
        """For usage with set, implementation of the __hash__ magic method."""
        return hash(self.schedule_id)

    def __eq__(self, obj: object) -> bool:
        """For usage with set, implementation of the __eq__ magic method."""
        if isinstance(obj, SwitcherSchedule):
            return self.schedule_id == obj.schedule_id
        return False


@final
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
        return self.schedule[4:6] != b"00"

    def get_days(self) -> Set[Days]:
        """Retun a set of the scheduled Days."""
        return (
            tools.bit_summary_to_days(int(self.schedule[4:6], 16))
            if self.is_recurring()
            else set()
        )

    def get_state(self) -> ScheduleState:
        """Return the current state of the device.

        Not sure if this needs to be included in the schedule object.
        """
        return ScheduleState(self.schedule[6:8].decode())

    def get_start_time(self) -> str:
        """Return the schedule start time in %H:%M format."""
        return tools.hexadecimale_timestamp_to_localtime(self.schedule[8:16])

    def get_end_time(self) -> str:
        """Return the schedule end time in %H:%M format."""
        return tools.hexadecimale_timestamp_to_localtime(self.schedule[16:24])


def get_schedules(message: bytes) -> Set[SwitcherSchedule]:
    """Use to create a list of schedule from a response message from the device."""
    hex_data = hexlify(message)[90:-8].decode()
    hex_data_split = wrap(hex_data, 32)
    ret_set = set()
    for schedule in hex_data_split:
        parser = ScheduleParser(schedule.encode())
        ret_set.add(
            SwitcherSchedule(
                parser.get_id(),
                parser.is_recurring(),
                parser.get_days(),
                parser.get_start_time(),
                parser.get_end_time(),
            )
        )
    return ret_set
