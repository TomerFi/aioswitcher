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
P_SESSION = "00000000"
PHONE_ID = "0000"
DEVICE_PASS = "00000000"
STOP_SHUTTER_PRECOMMAND = "3702"
SET_POSITION_PRECOMMAND = "3701"
SET_CHILD_LOCK_PRECOMMAND = "3707"
SET_LIGHT_PRECOMMAND = "370a"

# login packet for Type1 devices
# format value just timestamp (initial session id is P_SESSION)
LOGIN_PACKET_TYPE1 = (
    "fef052000232a100"
    + P_SESSION
    + REQUEST_FORMAT_TYPE1[2:]
    + "{}"
    + PAD_72_ZEROS
    + "00"
)

# login packet for Type2 devices
# format values are timestamp, device id
LOGIN_PACKET_TYPE2 = (
    "fef030000305a600"
    + P_SESSION
    + "ff0301000000"
    + PHONE_ID
    + "00000000{}00000000000000000000f0fe{}00"
)

# login packet for token-based Type2 devices
# format values are token, timestamp, device id
LOGIN_TOKEN_PACKET_TYPE2 = (
    "fef030000305a600"
    + P_SESSION
    + "ff0301000000"
    + "00"
    + "{}"
    + "00"
    + "{}00000000000000000000f0fe{}00"
)

# second login packet for token-based Type2 devices
# format values are device id, timestamp, token
LOGIN2_TOKEN_PACKET_TYPE2 = (
    "fef053000305a100"
    + P_SESSION
    + "f50301000000"
    + "{}"
    + "000000"
    + "{}"
    + "00000000000000000000f0fe"
    + "0000"
    + "{}"
    + "000000000000000000000000000000000000000000000000000000000000000001"
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

# format values are local session id, timestamp, device id, phone id, device-
# password, state, mode, target temp, fan level, swing
BREEZE_UPDATE_STATUS_PACKET = (
    "fef000000305010e"
    + REQUEST_FORMAT_BREEZE
    + "{}"
    + PAD_72_ZEROS
    + "370100030b0400"
    + "{}{}{:02x}{}{}"
)

# used for old runners devices that are not require a token within the packet.
# used in this action: stop_shutter
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

# used for old runners devices that are not require a token within the packet.
# used in this action: set_position
# format values are local session id, timestamp, device id, hex_pos
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

# used for old runners devices that are not require a token within the packet.
# used in this action: set_position
# format values are local session id, timestamp, device id, hex_pos
RUNNER_SET_CHILD_LOCK = (
    "fef0580003050102{}000000"
    + "000000000000000000"
    + "{}"
    + "00000000000000000000f0fe"
    + "{}"
    + PAD_72_ZEROS
    + "3707"
    + "0100"
    + "{}"
)

# used for new devices that require a token within the packet.
# used in those actions: set_position, stop_shutter, set_light
# format values are timestamp, device id, token, precommand, hex_pos
GENERAL_TOKEN_COMMAND = (
    "fef0000003050102"
    + "00000000"
    + "000000"
    + "000000000000000000"
    + "{}"
    + "00000000000000000000f0fe"
    + "{}"
    + "00"
    + "{}"
    + DEVICE_PASS
    + "000000000000000000000000000000000000000000000000000000"
    + "{}"
    + "0600"
    + "{}"
    + "00000000"
)
