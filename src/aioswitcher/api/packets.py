"""Switcher water heater unofficial API and bridge, API Packet formats.

.. codeauthor:: Tomer Figenblat <tomer.figenblat@gmail.com>

"""
# format values are local session id, timestamp
REQUEST_FORMAT = "{}340001000000000000000000{}00000000000000000000f0fe"
PAD_74_ZEROS = "0" * 74

# format values are remote session id, timestamp
LOGIN_PACKET = "fef052000232a100" + REQUEST_FORMAT + "1c" + PAD_74_ZEROS
# format values are local session id, timestamp, device id
GET_STATE_PACKET = "fef0300002320103" + REQUEST_FORMAT + "{}00"
# format values are local session id, timestamp, device id, command, timer
SEND_CONTROL_PACKET = (
    "fef05d0002320102" + REQUEST_FORMAT + "{}" + PAD_74_ZEROS + "0106000{}00{}"
)
# format values are local session id, timestamp, device id, auto-off seconds
SET_AUTO_OFF_SET_PACKET = (
    "fef05b0002320102" + REQUEST_FORMAT + "{}" + PAD_74_ZEROS + "040400{}"
)
# format values are local session id, timestamp, device id, name
UPDATE_DEVICE_NAME_PACKET = (
    "fef0740002320202" + REQUEST_FORMAT + "{}" + PAD_74_ZEROS + "{}"
)
# format values are local session id, timestamp, device id
GET_SCHEDULES_PACKET = (
    "fef0570002320102" + REQUEST_FORMAT + "{}" + PAD_74_ZEROS + "060000"
)
# format values are local session id, timestamp, device id, schedule id
DELETE_SCHEDULE_PACKET = (
    "fef0580002320102" + REQUEST_FORMAT + "{}" + PAD_74_ZEROS + "0801000{}"
)
# format values are local session id, timestamp, device id,
# schedule data =
#         (time_id + on_off + week + timstate + start_time + end_time)
DISABLE_ENABLE_SCHEDULE_PACKET = (
    "fef0630002320102" + REQUEST_FORMAT + "{}" + PAD_74_ZEROS + "070c00{}"
)
# format values are local session id, timestamp, device id,
# schedule data =
#                   (on_off + week + timstate + start_time + end_time)
CREATE_SCHEDULE_PACKET = (
    "fef0630002320102" + REQUEST_FORMAT + "{}" + PAD_74_ZEROS + "030c00ff{}"
)
