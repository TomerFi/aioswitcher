"""Switcher Device Schedule Objects."""

from asyncio import AbstractEventLoop, ensure_future, Future
from binascii import unhexlify
from datetime import datetime
from typing import List

from .consts import (ALL_DAYS, MONDAY, SCHEDULE_DUE_ANOTHER_DAY_FORMAT,
                     SCHEDULE_DUE_TODAY_FORMAT, SCHEDULE_DUE_TOMMOROW_FORMAT,
                     SUNDAY, WAITING_TEXT, WEEKDAY_TUP)
from .tools import get_days_list_from_bytes, get_time_from_bytes


class SwitcherV2Schedule:
    """Represnation of the switcher version 2 schedule."""

    def __init__(self, loop: AbstractEventLoop, idx: int,
                 schedule_details: List[bytes]) -> None:
        """Initialize the schedule."""
        self._loop = loop
        self._enabled = False
        self._recurring = False
        self._schedule_id = str(int(schedule_details[idx][0:2], 16))
        self._days = []  # type: List[str]
        self._schedule_data = b''
        self._start_time = WAITING_TEXT
        self._end_time = WAITING_TEXT
        self._duration = WAITING_TEXT
        self._init_future = loop.create_future()
        ensure_future(self.initialize(idx, schedule_details), loop=loop)

    async def initialize(
            self, idx: int, schedule_details: List[bytes]) -> None:
        """Finish the initialization of the schedule."""
        try:
            if int(schedule_details[idx][2:4], 16) == 1:
                self._enabled = True
            if not schedule_details[idx][4:6] == "00":
                self._recurring = True
                if schedule_details[idx][4:6] == "fe":
                    self._days.append(ALL_DAYS)
                else:
                    self._days = await get_days_list_from_bytes(
                        self._loop,
                        bytearray(
                            unhexlify((schedule_details[idx][4:6])))[0])

            self._start_time = await get_time_from_bytes(
                self._loop, schedule_details[idx][8:16])
            self._end_time = await get_time_from_bytes(
                self._loop, schedule_details[idx][16:24])
            self._duration = str(
                datetime.strptime(
                    self._end_time, '%H:%M') - datetime.strptime(
                        self._start_time, '%H:%M'))

            time_id = schedule_details[idx][0:2]
            on_off = schedule_details[idx][2:4]
            week = schedule_details[idx][4:6]
            timestate = schedule_details[idx][6:8]
            start_time = schedule_details[idx][8:16]
            end_time = schedule_details[idx][16:24]
            self._schedule_data = (
                time_id + on_off + week + timestate + start_time + end_time)

            self.init_future.set_result(self)
        except RuntimeError as exc:
            self.init_future.set_exception(exc)

        return None

    @property
    def schedule_id(self) -> str:
        """Return the schedule id."""
        return self._schedule_id

    @property
    def enabled(self) -> bool:
        """Return true if enabled."""
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
        """Return true if recurring."""
        return self._recurring

    @property
    def days(self) -> List[str]:
        """Return the weekdays of the schedule."""
        return self._days

    @property
    def start_time(self) -> str:
        """Return the start time of the schedule."""
        return self._start_time

    @property
    def end_time(self) -> str:
        """Return the end time of the schedule."""
        return self._end_time

    @property
    def duration(self) -> str:
        """Return the duration of the schedule."""
        return self._duration

    @property
    def schedule_data(self) -> bytes:
        """Return the schedule data for managing the schedule."""
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
        """Return the future of the initialization."""
        return self._init_future

    def as_dict(self):
        """Make object json serializable."""
        return self.__dict__


def _calc_next_run_for_schedule(schedule_details: SwitcherV2Schedule) -> str:
    """Calculate the next runtime of the schedule."""
    if schedule_details.recurring:
        today_datetime = datetime.now()

        start_time = datetime.strptime(schedule_details.start_time, "%H:%M")
        current_time = datetime.strptime(("0" + str(today_datetime.hour))[-2:]
                                         + ":"
                                         + ("0" + str(
                                             today_datetime.minute))[-2:],
                                         "%H:%M")

        current_weekday = today_datetime.weekday()
        found_day = -1
        if schedule_details.days == [ALL_DAYS]:
            if current_time < start_time:
                return SCHEDULE_DUE_TODAY_FORMAT.format(
                    schedule_details.start_time)
            return SCHEDULE_DUE_TOMMOROW_FORMAT.format(
                schedule_details.start_time)

        for day in schedule_details.days:
            set_weekday = WEEKDAY_TUP.index(day)

            if set_weekday == current_weekday and current_time < start_time:
                return SCHEDULE_DUE_TODAY_FORMAT.format(
                    schedule_details.start_time)

            if found_day == -1 or found_day > set_weekday:
                found_day = set_weekday

        if (found_day - 1 == current_weekday
                or (found_day == WEEKDAY_TUP.index(MONDAY)
                    and current_weekday == WEEKDAY_TUP.index(SUNDAY))):

            return SCHEDULE_DUE_TOMMOROW_FORMAT.format(
                schedule_details.start_time)

        return SCHEDULE_DUE_ANOTHER_DAY_FORMAT.format(
            WEEKDAY_TUP[found_day], schedule_details.start_time)

    return SCHEDULE_DUE_TODAY_FORMAT.format(schedule_details.start_time)


async def calc_next_run_for_schedule(
        loop: AbstractEventLoop, schedule_details: SwitcherV2Schedule) -> str:
    """Use as async wrapper for calling _calc_next_run_for_schedule."""
    return await loop.run_in_executor(
        None, _calc_next_run_for_schedule, schedule_details)
