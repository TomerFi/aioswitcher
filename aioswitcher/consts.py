"""Switcher Constants."""

ENCODING_CODEC = 'utf-8'
REMOTE_SESSION_ID = '00000000'
REMOTE_KEY = b'00000000000000000000000000000000'
SOCKET_PORT = 9957
SOCKET_BIND_TUP = ('0.0.0.0', 20002)
STATE_RESPONSE_ON = '0100'
STATE_ON = 'on'
STATE_RESPONSE_OFF = '0000'
STATE_OFF = 'off'
STATE_UNKNOWN = 'unknown'
COMMAND_ON = '1'
COMMAND_OFF = '0'
NO_TIMER_REQUESTED = '00000000'
ENABLE_SCHEDULE = '01'
DISABLE_SCHEDULE = '00'

SUNDAY = 'Sunday'
MONDAY = 'Monday'
TUESDAY = 'Tuesday'
WEDNESDAY = 'Wednesday'
THURSDAY = 'Thursday'
FRIDAY = 'Friday'
SATURDAY = 'Saturday'
ALL_DAYS = "Every day"

WEEKDAY_TUP = (MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY)

HEX_TO_DAY_DICT = {0x02: MONDAY, 0x04: TUESDAY, 0x08: WEDNESDAY,
                   0x10: THURSDAY, 0x20: FRIDAY, 0x40: SATURDAY, 0x80: SUNDAY}

DAY_TO_INT_DICT = {MONDAY: 2, TUESDAY: 4, WEDNESDAY: 8, THURSDAY: 16,
                   FRIDAY: 32, SATURDAY: 64, SUNDAY: 128}

# weekdays, start-time, end-time
SCHEDULE_CREATE_DATA_FORMAT = '01{}01{}{}'

WAITING_TEXT = 'waiting_for_data'

SCHEDULE_DUE_TODAY_FORMAT = "Due today at {}"
SCHEDULE_DUE_TOMMOROW_FORMAT = "Due tommorow at {}"
SCHEDULE_DUE_ANOTHER_DAY_FORMAT = "Due next {} at {}"

STRUCT_PACKING_FORMAT = '<I'  # little-endian unsigned int

HANDLED_EXCEPTIONS = (AttributeError, FloatingPointError, IndexError,
                      LookupError, OverflowError, TypeError,
                      UnicodeDecodeError, ValueError, ZeroDivisionError)