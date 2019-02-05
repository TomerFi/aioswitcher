"""Switcher Device Schedule Objects."""

from typing import List
from datetime import datetime
from binascii import unhexlify
from aioswitcher.tools import get_days_list_from_bytes, get_time_from_bytes
from aioswitcher.consts import ALL_DAYS, WEEKDAY_TUP, SUNDAY, MONDAY


class SwitcherV2Schedule(object):
    """Represnation of the switcher version 2 schedule."""

    def __init__(self, idx, schedule_details: List[str]) -> None:
        """Initialize the schedule."""
        self._enabled = self._recurring = False
        self._days = []  # type: List[str]
        try:
            self._schedule_id = str(int(schedule_details[idx][0:2], 16))
            if int(schedule_details[idx][2:4], 16) == 1:
                self._enabled = True
            if not schedule_details[idx][4:6] == "00":
                self._recurring = True
                if schedule_details[idx][4:6] == "fe":
                    self._days.append(ALL_DAYS)
                else:
                    self._days = get_days_list_from_bytes(
                        bytearray(
                            unhexlify((schedule_details[idx][4:6])))[0])

            self._start_time = get_time_from_bytes(schedule_details[idx][8:16])
            self._end_time = get_time_from_bytes(schedule_details[idx][16:24])
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

        except Exception as ex:
            raise Exception("failed to parse schedule data.") from ex

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
        self._enabled = value

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
    def schedule_data(self) -> str:
        """Return the schedule data for managing the schedule."""
        return self._schedule_data

    @schedule_data.setter
    def schedule_data(self, data: str) -> None:
        """Setter to set the schedule data for managing the schedule."""
        self._schedule_data = data

    def as_dict(self):
        """Make object json serializable."""
        return self.__dict__


def calc_next_run_for_schedule(schedule_details: SwitcherV2Schedule) -> str:
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
                return "Due today at " + schedule_details.start_time
            else:
                return "Due tommorow at " + schedule_details.start_time

        for day in schedule_details.days:
            set_weekday = WEEKDAY_TUP.index(day)

            if set_weekday == current_weekday and current_time < start_time:
                return "Due today at " + schedule_details.start_time

            if found_day == -1 or found_day > set_weekday:
                found_day = set_weekday

        if (found_day - 1 == current_weekday
                or (found_day == WEEKDAY_TUP.index(MONDAY)
                    and current_weekday == WEEKDAY_TUP.index(SUNDAY))):

            return "Due tommorow at " + schedule_details.start_time

        return ("Due next " + WEEKDAY_TUP[found_day]
                + " at " + schedule_details.start_time)

    return "Due today at " + schedule_details.start_time


def create_schedules_list(schedules_raw: str, schedule_length: int) \
        -> List[str]:
    """Convert raw schedules data to list of individual schedules string."""
    return [schedules_raw[i:i + schedule_length] for i in range(
        0, len(schedules_raw), schedule_length)]
