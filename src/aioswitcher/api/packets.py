"""Switcher water heater unofficial API and bridge, API Packet formats.

.. codeauthor:: Tomer Figenblat <tomer.figenblat@gmail.com>

"""

# format values are remote session id, timestamp, phone id, device password
LOGIN_PACKET = (
    "fef052000232a100{}340001000000000000000000{}00000000000000000000"
    + "f0fe1c00{}0000{}000000000000000000000000000000000000000000000000"
    + "00000000"
)

# format values are local session id, timestamp, device id
GET_STATE_PACKET = (
    "fef0300002320103{}340001000000000000000000"
    + "{}00000000000000000000f0fe{}00"
)

# format values are local session id, timestamp, device id, phone id,
# device password, command (1/0), timer
SEND_CONTROL_PACKET = (
    "fef05d0002320102{}340001000000000000000000{}00000000000000000000f0fe"
    + "{}00{}0000{}00000000000000000000000000000000000000000000000000000000"
    + "0106000{}00{}"
)

# format values are local session id, timestamp, device id, phone id,
# device password, auto-off seconds
SET_AUTO_OFF_SET_PACKET = (
    "fef05b0002320102{}340001000000000000000000{}00000000000000000000f0fe"
    + "{}00{}0000{}00000000000000000000000000000000000000000000000000000000"
    + "040400{}"
)

# format values are local session id, timestamp, device id, phone id,
# device password, name
UPDATE_DEVICE_NAME_PACKET = (
    "fef0740002320202{}340001000000000000000000{}00000000000000000000f0fe"
    + "{}00{}0000{}00000000000000000000000000000000000000000000000000000000"
    + "{}"
)

# format values are local session id, timestamp, device id,
# phone id, device password
GET_SCHEDULES_PACKET = (
    "fef0570002320102{}340001000000000000000000{}00000000000000000000f0fe"
    + "{}00{}0000{}00000000000000000000000000000000000000000000000000000000"
    + "060000"
)

# format values are local session id, timestamp, device id,
# phone id, device password, schedule id
DELETE_SCHEDULE_PACKET = (
    "fef0580002320102{}340001000000000000000000{}00000000000000000000f0fe"
    + "{}00{}0000{}00000000000000000000000000000000000000000000000000000000"
    + "0801000{}"
)

# format values are local session id, timestamp, device id, phone id,
# device password, schedule data =
#         (time_id + on_off + week + timstate + start_time + end_time)
DISABLE_ENABLE_SCHEDULE_PACKET = (
    "fef0630002320102{}340001000000000000000000{}00000000000000000000f0fe"
    + "{}00{}0000{}00000000000000000000000000000000000000000000000000000000"
    + "070c00{}"
)

# format values are local session id, timestamp, device id, phone id,
# device password, schedule data =
#                   (on_off + week + timstate + start_time + end_time)
CREATE_SCHEDULE_PACKET = (
    "fef0630002320102{}340001000000000000000000{}00000000000000000000f0fe"
    + "{}00{}0000{}00000000000000000000000000000000000000000000000000000000"
    + "030c00ff{}"
)
