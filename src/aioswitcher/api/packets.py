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

"""Switcher integration TCP socket API packet formats."""

# weekdays sum, start-time timestamp, end-time timestamp
SCHEDULE_CREATE_DATA_FORMAT = "01{}01{}{}"

NO_TIMER_REQUESTED = "00000000"
NON_RECURRING_SCHEDULE = "00"
# format values are local session id, timestamp
REQUEST_FORMAT_TYPE1 = "{}340001000000000000000000{}00000000000000000000f0fe"
REQUEST_FORMAT2_TYPE2 = "{}390001000000000000000000{}00000000000000000000f0fe"

REQUEST_FORMAT_BREEZE = "{}000001000000000000000000{}00000000000000000000f0fe"
PAD_72_ZEROS = "0" * 72
# format value just timestamp (initial session id is "00000000")
LOGIN_PACKET_TYPE1 = (
    "fef052000232a10000000000" + REQUEST_FORMAT_TYPE1[2:] + "1c" + PAD_72_ZEROS + "00"
)

LOGIN2_PACKET_TYPE2 = (
    "fef030000305a60000000000ff0301000000000000000000{}00000000000000000000f0fe{}00"
)

# format values are local session id, timestamp, device id
GET_STATE_PACKET_TYPE1 = "fef0300002320103" + REQUEST_FORMAT_TYPE1 + "{}00"

# format values are local session id, timestamp, device id
GET_STATE_PACKET2_TYPE2 = "fef0300003050103" + REQUEST_FORMAT2_TYPE2 + "{}00"

# format values are local session id, timestamp, device id, command, timer
SEND_CONTROL_PACKET = (
    "fef05d0002320102" + REQUEST_FORMAT_TYPE1 + "{}" + PAD_72_ZEROS + "000106000{}00{}"
)
# format values are local session id, timestamp, device id, auto-off seconds
SET_AUTO_OFF_SET_PACKET = (
    "fef05b0002320102" + REQUEST_FORMAT_TYPE1 + "{}" + PAD_72_ZEROS + "00040400{}"
)
# format values are local session id, timestamp, device id, name
UPDATE_DEVICE_NAME_PACKET = (
    "fef0740002320202" + REQUEST_FORMAT_TYPE1 + "{}" + PAD_72_ZEROS + "00{}"
)
# format values are local session id, timestamp, device id
GET_SCHEDULES_PACKET = (
    "fef0570002320102" + REQUEST_FORMAT_TYPE1 + "{}" + PAD_72_ZEROS + "00060000"
)
# format values are local session id, timestamp, device id, schedule id
DELETE_SCHEDULE_PACKET = (
    "fef0580002320102" + REQUEST_FORMAT_TYPE1 + "{}" + PAD_72_ZEROS + "000801000{}"
)
# format values are local session id, timestamp, device id,
# schedule data =
#                   (on_off + week + timestamp + start_time + end_time)
CREATE_SCHEDULE_PACKET = (
    "fef0630002320102" + REQUEST_FORMAT_TYPE1 + "{}" + PAD_72_ZEROS + "00030c00ff{}"
)
# format values are local session id, timestamp, device id, phone id, device-
# password, command length, command
BREEZE_COMMAND_PACKET = (
    "fef0000003050102" + REQUEST_FORMAT_BREEZE + "{}" + PAD_72_ZEROS + "3701" + "{}{}"
)

# format values are local session id, timestamp, device id
RUNNER_STOP_COMMAND = (
    "fef0590003050102"
    + "{}"
    + "232301"
    + "000000000000000000"
    + "{}"
    + "00000000000000000000f0fe"
    + "{}"
    + PAD_72_ZEROS
    + "370202000000"
)

RUNNER_SET_POSITION = (
    "fef0580003050102{}290401"
    + "000000000000000000"
    + "{}"
    + "00000000000000000000f0fe"
    + "{}"
    + PAD_72_ZEROS
    + "3701"
    + "0100"
    + "{}"
)
