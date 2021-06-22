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

"""Switcher unofficial integration schedule module tools."""

import time
from datetime import datetime
from typing import Set, Union, cast

from .. import Days


def pretty_next_run(start_time: str, days: Set[Days] = set()) -> str:
    """Create a literal for displaying the next run time.

    Args:
        start_time: the start of the schedule in "%H:%M" format, e.g. "17:00".
        days: for recurring schedules, a list of days when none, will be today.

    Returns:
        A pretty string describing the next due run.
        e.g. "Due next Sunday at 17:00".

    """
    if not days:
        return f"Due today at {start_time}"

    current_datetime = datetime.utcnow()
    current_weekday = current_datetime.weekday()

    current_time = datetime.strptime(
        current_datetime.time().strftime("%H:%M"), "%H:%M"
    ).time()
    schedule_time = datetime.strptime(start_time, "%H:%M").time()

    print("debug")
    print(start_time)
    print(days)
    print(list(days)[0].weekday)

    print("debug")
    print(current_datetime)
    print(current_weekday)
    print(current_time)
    print(schedule_time)

    found_day = -1
    for day in days:
        # if scheduled for later on today, return "due today"
        if day.weekday == current_weekday and current_time < schedule_time:
            return f"Due today at {start_time}"

        # get the closest day to today by saving the lowest weekday as "found_day"
        if found_day == -1 or found_day > day.weekday:
            found_day = day.weekday

    # if found day is tommorow for the current day, or this is the week end (today is
    # sunday and tommorow is monday)  return "due tommorow"
    if found_day - 1 == current_weekday or (
        found_day == Days.MONDAY.weekday and current_weekday == Days.SUNDAY.weekday
    ):
        return f"Due tommorow at {start_time}"

    # if here, then the scuedle is due some other day this week, return "due at..."
    weekdays = dict(map(lambda d: (d.weekday, d), Days))
    return f"Due next {weekdays[found_day].value} at {start_time}"


def calc_duration(start_time: str, end_time: str) -> str:
    """Use to calculate the delta between two time values formated as %H:%M."""
    start_datetime = datetime.strptime(start_time, "%H:%M")
    end_datetime = datetime.strptime(end_time, "%H:%M")
    if end_datetime > start_datetime:
        return str(end_datetime - start_datetime)
    raise ValueError("end_time should be greater the start_time")


def bit_summary_to_days(sum_weekdays_bit: int) -> Set[Days]:
    """Decode a weekdays bit summary to a set of weekdays.

    Args:
        sum_weekdays: the sum of all weekdays

    Return:
        Set of Weekday memebers decoded from the summary value.

    Todo:
        Should an existing remainder in the sum value throw an error?
        E.g. 3 will result in a set of MONDAY and the remainder will be 1.

    """
    if 1 < sum_weekdays_bit < 255:
        return_weekdays = set()
        weekdays_by_hex = map(lambda w: (w.hex_rep, w), Days)
        for weekday_hex in weekdays_by_hex:
            if weekday_hex[0] & sum_weekdays_bit != 0:
                return_weekdays.add(weekday_hex[1])
        return return_weekdays
    raise ValueError("weekdays bit sum should be between 2 and 254")


def hexadecimale_timestamp_to_localtime(hex_timestamp: bytes) -> str:
    """Decode an hexadecimale timestamp to localtime with the format %H:%M.

    Args:
        hex_timestamp: the hexadecimale timestamp.

    Return:
        Localtime string with %H:%M format. e.g. "20:30".
    """
    hex_time = (
        hex_timestamp[6:8]
        + hex_timestamp[4:6]
        + hex_timestamp[2:4]
        + hex_timestamp[0:2]
    )
    int_time = int(hex_time, 16)
    local_time = time.localtime(int_time)
    print(local_time)
    return time.strftime("%H:%M", local_time)


def weekdays_to_hexadecimal(days: Union[Days, Set[Days]]) -> str:
    """Sum the requested weekdays bit represntation and return as hexadecimal value.

    Args:
        days: the requested Weekday members.

    Return:
        Hexadecimale represntation of the sum of all requested day's bit representation.

    """
    if days:
        if type(days) is Days:
            return "{:02x}".format(cast(Days, days).bit_rep)
        elif type(days) is set or len(days) == len(set(days)):  # type: ignore
            map_to_bits = map(lambda w: w.bit_rep, days)  # type: ignore
            return "{:02x}".format(int(sum(map_to_bits)))
    raise ValueError("no days requested")
