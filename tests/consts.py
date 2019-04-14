"""Constants for the Switcher integration tests."""

from aioswitcher.consts import DAY_TO_INT_DICT, MONDAY, SUNDAY, TUESDAY

DUMMY_DEVICE_ID = 'a123bc'
DUMMY_SESSION_ID = '01000000'
DUMMY_TIMESTAMP = 'ef8db35c'
# result of DUMMY_DEVICE_ID + DUMMY_SESSION_ID + DUMMY_TIMESTAMP
RESULT_CRC_SIGNATURE = '42a9a1b2'

# [2, 4, 128]
SCHEDULE_WEEKDAY_LIST = [DAY_TO_INT_DICT[MONDAY],
                         DAY_TO_INT_DICT[TUESDAY],
                         DAY_TO_INT_DICT[SUNDAY]]


TEST_SECONDS = 86399  # 23:59:59

TIMESTAMP_COMPARE_FORMAT = "%Y-%m-%d %H"
