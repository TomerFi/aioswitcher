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

"""Switcher smart switch unofficial API and bridge, Schedules."""

from asyncio import AbstractEventLoop, Future, ensure_future
from binascii import unhexlify
from datetime import datetime
from enum import Enum, unique
from typing import List

from . import Days
from .utils import bit_summary_to_days, hexadecimale_timestamp_to_localtime

ALL_DAYS = "Every day"
WAITING_TEXT = "waiting_for_schedule_data"
SCHEDULE_DUE_TODAY_FORMAT = "Due today at {}"
SCHEDULE_DUE_TOMMOROW_FORMAT = "Due tommorow at {}"
SCHEDULE_DUE_ANOTHER_DAY_FORMAT = "Due next {} at {}"
# weekdays sum, start-time timestamp, end-time timestamp
SCHEDULE_CREATE_DATA_FORMAT = "01{}01{}{}"


@unique
class ScheduleStatus(Enum):
    """Enum representing the status of the schedule."""

    ENABLED = "01"
    DISABLED = "00"


class SwitcherV2Schedule:
    """Represnation of the SwitcherV2 schedule slot.

    Args:
      loop: the event loop to perform schedule operation in.
      idx: the index of the schedule slot (0-7).
      schedule_details: the string raw schedule data details.

    Todo:
      * Replace ``init_future`` attribute with ``get_init_future`` method.

    """

    def __init__(
        self, loop: AbstractEventLoop, idx: int, schedule_details: List[bytes]
    ) -> None:
        """Initialize the schedule."""
        self._loop = loop
        self._enabled = False
        self._recurring = False
        self._schedule_id = str(int(schedule_details[idx][0:2], 16))
        self._days = []  # type: List[str]
        self._schedule_data = b""
        self._start_time = WAITING_TEXT
        self._end_time = WAITING_TEXT
        self._duration = WAITING_TEXT
        self._init_future = loop.create_future()
        ensure_future(self.initialize(idx, schedule_details), loop=loop)

    async def initialize(self, idx: int, schedule_details: List[bytes]) -> None:
        """Finish the initialization of the schedule."""
        try:
            if int(schedule_details[idx][2:4], 16) == 1:
                self._enabled = True
            if not schedule_details[idx][4:6] == "00":
                self._recurring = True
                if schedule_details[idx][4:6] == "fe":
                    self._days.append(ALL_DAYS)
                else:
                    days = bit_summary_to_days(
                        bytearray(unhexlify((schedule_details[idx][4:6])))[0]
                    )
                    self._days = [day.value for day in days]  # type: ignore

            self._start_time = hexadecimale_timestamp_to_localtime(
                schedule_details[idx][8:16]
            )
            self._end_time = hexadecimale_timestamp_to_localtime(
                schedule_details[idx][16:24]
            )
            self._duration = str(
                datetime.strptime(self._end_time, "%H:%M")
                - datetime.strptime(self._start_time, "%H:%M")
            )

            time_id = schedule_details[idx][0:2]
            on_off = schedule_details[idx][2:4]
            week = schedule_details[idx][4:6]
            timestate = schedule_details[idx][6:8]
            start_time = schedule_details[idx][8:16]
            end_time = schedule_details[idx][16:24]
            self._schedule_data = (
                time_id + on_off + week + timestate + start_time + end_time
            )

            self.init_future.set_result(self)
        except RuntimeError as exc:
            self.init_future.set_exception(exc)

        return None

    @property
    def schedule_id(self) -> str:
        """str: Return the schedule id."""
        return self._schedule_id

    @property
    def enabled(self) -> bool:
        """bool: Return true if enabled, setter included."""
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        """Setter to set the device as enabled or disabled."""
        if isinstance(value, bool):
            self._enabled = value
        else:
            raise TypeError("enabled is of type bool")

    @property
    def recurring(self) -> bool:
        """bool: Return true if recurring."""
        return self._recurring

    @property
    def days(self) -> List[str]:
        """list(str): Return the weekdays of the schedule."""
        return self._days

    @property
    def start_time(self) -> str:
        """str: Return the start time of the schedule."""
        return self._start_time

    @property
    def end_time(self) -> str:
        """str: Return the end time of the schedule."""
        return self._end_time

    @property
    def duration(self) -> str:
        """str: Return the duration of the schedule."""
        return self._duration

    @property
    def schedule_data(self) -> bytes:
        """bytes: Return the schedule data, setter included."""
        return self._schedule_data

    @schedule_data.setter
    def schedule_data(self, data: bytes) -> None:
        """Setter to set the schedule data for managing the schedule."""
        if isinstance(data, bytes):
            self._schedule_data = data
        else:
            raise TypeError("schedeule_data is of type bytes")

    @property
    def init_future(self) -> Future:
        """asyncio.Future: Return the future of the initialization."""
        return self._init_future

    def as_dict(self):
        """Return as dict.

        Returns:
          A dictionary represntation of the object properties.
          Used to make the object json serializable.

        """
        return self.__dict__


def _calc_next_run_for_schedule(schedule_details: SwitcherV2Schedule) -> str:
    """Calculate the next runtime of the schedule.

    Args:
      schedule_details: ``SwitcherV2Schedule`` representing the schedule slot.

    Returns:
      A pretty string describing the next due run.
      e.g. "Due tommorow at 17:00".

    Note:
      This is a private function containing blocking code.
      Please consider using ``calc_next_run_for_schedule`` (without the `_`),
      to schedule as a task on the event loop.

    """
    if schedule_details.recurring:
        today_datetime = datetime.now()

        start_time = datetime.strptime(schedule_details.start_time, "%H:%M")
        current_time = datetime.strptime(
            ("0" + str(today_datetime.hour))[-2:]
            + ":"
            + ("0" + str(today_datetime.minute))[-2:],
            "%H:%M",
        )

        current_weekday = today_datetime.weekday()
        found_day = -1
        if schedule_details.days == [ALL_DAYS]:
            if current_time < start_time:
                return SCHEDULE_DUE_TODAY_FORMAT.format(schedule_details.start_time)
            return SCHEDULE_DUE_TOMMOROW_FORMAT.format(schedule_details.start_time)

        for day in Days:
            if day.weekday == current_weekday and current_time < start_time:
                return SCHEDULE_DUE_TODAY_FORMAT.format(schedule_details.start_time)

            if found_day == -1 or found_day > day.weekday:
                found_day = day.weekday

        if found_day - 1 == current_weekday or (
            found_day == Days.MONDAY.weekday and current_weekday == Days.SUNDAY.weekday
        ):

            return SCHEDULE_DUE_TOMMOROW_FORMAT.format(schedule_details.start_time)

        weekdays = dict(map(lambda d: (d.weekday, d), Days))
        return SCHEDULE_DUE_ANOTHER_DAY_FORMAT.format(
            weekdays[found_day].value, schedule_details.start_time
        )

    return SCHEDULE_DUE_TODAY_FORMAT.format(schedule_details.start_time)


async def calc_next_run_for_schedule(
    loop: AbstractEventLoop, schedule_details: SwitcherV2Schedule
) -> str:
    """Asynchronous wrapper for _calc_next_run_for_schedule.

    Use as async wrapper for calling _calc_next_run_for_schedule,
    calculating the next runtime of the schedule.

    Args:
      loop: the event loop to execute the function in.
      schedule_details: ``SwitcherV2Schedule`` representing the schedule slot.

    Returns:
      A pretty string describing the next due run.
      e.g. "Due tommorow at 17:00".

    """
    return await loop.run_in_executor(
        None, _calc_next_run_for_schedule, schedule_details
    )
