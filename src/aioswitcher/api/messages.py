"""Switcher Packet Response Messages."""

# fmt: off
from asyncio import AbstractEventLoop, Future, ensure_future
from binascii import hexlify
from enum import Enum
from typing import List

from ..consts import (ENCODING_CODEC, HANDLED_EXCEPTIONS, STATE_OFF, STATE_ON,
                      STATE_RESPONSE_OFF, STATE_RESPONSE_ON, STATE_UNKNOWN)
from ..errors import DecodingError
from ..schedules import SwitcherV2Schedule
from ..tools import convert_seconds_to_iso_time

# fmt: on


ResponseMessageType = Enum(
    "ResponseMessageType",
    [
        "AUTO_OFF",
        "CONTROL",
        "CREATE_SCHEDULE",
        "DELETE_SCHEDULE",
        "DISABLE_ENABLE_SCHEDULE",
        "GET_SCHEDULES",
        "LOGIN",
        "STATE",
        "UPDATE_NAME",
    ],
)


class SwitcherV2BaseResponseMSG:
    """Represntation of the switcher v2 base response message.

    Args:
      loop: the event loop to perform actions in.
      response: the raw response from the device.
      msg_type: the message type as described in the ''ResponseMessageType''
        Enum class.

    """

    def __init__(
        self,
        loop: AbstractEventLoop,
        response: bytes,
        msg_type: ResponseMessageType,
    ) -> None:
        """Initialize the base object."""
        self._loop = loop
        self._unparsed_response = response
        self._msg_type = msg_type

    @property
    def unparsed_response(self) -> bytes:
        """bytes: Return The raw response from the device."""
        return self._unparsed_response

    @property
    def successful(self) -> bool:
        """bool: Indicating whether or not the request was successful."""
        return self._unparsed_response is not None

    @property
    def msg_type(self) -> ResponseMessageType:
        """aioswitcher.api.messages.ResponseMessageType: the message type."""
        return self._msg_type


class SwitcherV2LoginResponseMSG(SwitcherV2BaseResponseMSG):
    """Represntation of the switcher v2 login response message.

    Args:
      loop: the event loop to perform actions in.
      response: the raw response from the device.

    """

    def __init__(self, loop: AbstractEventLoop, response: bytes) -> None:
        """Initialize the login response."""
        super().__init__(loop, response, ResponseMessageType.LOGIN)
        try:
            self._session_id = hexlify(response)[16:24].decode(ENCODING_CODEC)
        except HANDLED_EXCEPTIONS as exc:
            raise DecodingError(
                "failed to parse login response message"
            ) from exc

    @property
    def session_id(self) -> str:
        """str: Return the retrieved session id."""
        return self._session_id


class SwitcherV2StateResponseMSG(SwitcherV2BaseResponseMSG):
    """Represntation of the switcher v2 state response message.

    Args:
      loop: the event loop to perform actions in.
      response: the raw response from the device.

    Todo:
      * replace ``init_future`` attribute with ``get_init_future`` method.

    """

    def __init__(self, loop: AbstractEventLoop, response: bytes) -> None:
        """Initialize the state response message."""
        super().__init__(loop, response, ResponseMessageType.STATE)
        self._power_consumption = 0
        self._electric_current = 0.0
        self._init_future = loop.create_future()
        ensure_future(self.initialize(response), loop=loop)

    async def initialize(self, response: bytes) -> None:
        """Finish the initialization of the message and update the future object.

        Args:
          response: the raw response from the device.

        """
        try:
            temp_power = hexlify(response)[154:162]
            self._power_consumption = int(
                temp_power[2:4] + temp_power[0:2], 16
            )
            self._electric_current = round(
                (self._power_consumption / float(220)), 1
            )

            temp_time_left = hexlify(response)[178:186]
            temp_time_left_seconds = int(
                temp_time_left[6:8]
                + temp_time_left[4:6]
                + temp_time_left[2:4]
                + temp_time_left[0:2],
                16,
            )
            self._time_to_auto_off = await convert_seconds_to_iso_time(
                self._loop, temp_time_left_seconds
            )

            temp_time_on = hexlify(response)[186:194]
            temp_time_on_seconds = int(
                temp_time_on[6:8]
                + temp_time_on[4:6]
                + temp_time_on[2:4]
                + temp_time_on[0:2],
                16,
            )
            self._time_on = await convert_seconds_to_iso_time(
                self._loop, temp_time_on_seconds
            )

            temp_auto_off = hexlify(response)[194:202]
            temp_auto_off_seconds = int(
                temp_auto_off[6:8]
                + temp_auto_off[4:6]
                + temp_auto_off[2:4]
                + temp_auto_off[0:2],
                16,
            )
            self._auto_off_set = await convert_seconds_to_iso_time(
                self._loop, temp_auto_off_seconds
            )

            temp_state = hexlify(response)[150:154].decode(ENCODING_CODEC)
            self._state = (
                STATE_ON
                if temp_state == STATE_RESPONSE_ON
                else STATE_OFF
                if temp_state == STATE_RESPONSE_OFF
                else STATE_UNKNOWN
            )

            self.init_future.set_result(self)
        except HANDLED_EXCEPTIONS as exc:
            self.init_future.set_exception(exc)

        return None

    @property
    def state(self) -> str:
        """str: Return the state."""
        return self._state

    @property
    def time_left(self) -> str:
        """str: Return the time left to auto-off."""
        return self._time_to_auto_off

    @property
    def time_on(self) -> str:
        """str: Return the time in "on" state.

        Relevant only if the current state is "on".
        """
        return self._time_on

    @property
    def auto_off(self) -> str:
        """str: Return the auto-off configuration value."""
        return self._auto_off_set

    @property
    def power(self) -> int:
        """int: Return the current power consumption in watts."""
        return self._power_consumption

    @property
    def current(self) -> float:
        """float: Return the power consumption in amps."""
        return self._electric_current

    @property
    def init_future(self) -> Future:
        """asyncio.Future: Return the future of the initialization."""
        return self._init_future


class SwitcherV2ControlResponseMSG(SwitcherV2BaseResponseMSG):
    """Represntation of the switcher v2 control response message.

    Args:
      loop: the event loop to perform actions in.
      response: the raw response from the device.

    """

    def __init__(self, loop: AbstractEventLoop, response: bytes) -> None:
        """Initialize the Control response message."""
        super().__init__(loop, response, ResponseMessageType.CONTROL)


class SwitcherV2SetAutoOffResponseMSG(SwitcherV2BaseResponseMSG):
    """Represntation of the switcher v2 set auto-off response message.

    Args:
      loop: the event loop to perform actions in.
      response: the raw response from the device.

    """

    def __init__(self, loop: AbstractEventLoop, response: bytes) -> None:
        """Initialize the Set Auto-Off response message."""
        super().__init__(loop, response, ResponseMessageType.AUTO_OFF)


class SwitcherV2UpdateNameResponseMSG(SwitcherV2BaseResponseMSG):
    """Represntation of the switcher v2 update name response message.

    Args:
      loop: the event loop to perform actions in.
      response: the raw response from the device.

    """

    def __init__(self, loop: AbstractEventLoop, response: bytes) -> None:
        """Initialize the Set Name response message."""
        super().__init__(loop, response, ResponseMessageType.UPDATE_NAME)


class SwitcherV2GetScheduleResponseMSG(SwitcherV2BaseResponseMSG):
    """represnation of the switcher v2 get schedule message.

    Args:
      loop: the event loop to perform actions in.
      response: the raw response from the device.

    Todo:
      * the ``get_schedules`` attribute should be a method.
      * ``schdule_detais`` is ``__init__`` is yielding List[str] instead of
        List[bytes], that's not supposed to happen.

    """

    def __init__(self, loop: AbstractEventLoop, response: bytes) -> None:
        """Initialize the Set Name response message."""
        super().__init__(loop, response, ResponseMessageType.GET_SCHEDULES)
        self._schedule_list = []  # type: List[SwitcherV2Schedule]

        res = hexlify(response)
        idx = res[90:-8].decode(ENCODING_CODEC)
        schedules_details = [
            idx[i : i + 32] for i in range(0, len(idx), 32)  # noqa E203
        ]

        if schedules_details:
            for i in range(len(schedules_details)):
                schedule = SwitcherV2Schedule(
                    loop, i, schedules_details  # type: ignore
                )
                self._schedule_list.append(schedule)

    @property
    def found_schedules(self) -> bool:
        """bool: Return true if found schedules in the response."""
        return self._schedule_list != []

    @property
    def get_schedules(self) -> List[SwitcherV2Schedule]:
        """list(aioswitcher.schedules.SwitcherV2Schedule): Return schedules."""
        return self._schedule_list


class SwitcherV2DisableEnableScheduleResponseMSG(SwitcherV2BaseResponseMSG):
    """Represntation of the switcher v2 dis/en schedule response message.

    Args:
      loop: the event loop to perform actions in.
      response: the raw response from the device.

    """

    def __init__(self, loop: AbstractEventLoop, response: bytes) -> None:
        """Initialize the switcher v2 dis/en schedule response message."""
        super().__init__(
            loop, response, ResponseMessageType.DISABLE_ENABLE_SCHEDULE
        )


class SwitcherV2DeleteScheduleResponseMSG(SwitcherV2BaseResponseMSG):
    """Represntation of the switcher v2 delete schedule response message.

    Args:
      loop: the event loop to perform actions in.
      response: the raw response from the device.

    """

    def __init__(self, loop: AbstractEventLoop, response: bytes) -> None:
        """Initialize the switcher v2 delete schedule response message."""
        super().__init__(loop, response, ResponseMessageType.DELETE_SCHEDULE)


class SwitcherV2CreateScheduleResponseMSG(SwitcherV2BaseResponseMSG):
    """Represntation of the switcher v2 create schedule response message.

    Args:
      loop: the event loop to perform actions in.
      response: the raw response from the device.

    """

    def __init__(self, loop: AbstractEventLoop, response: bytes) -> None:
        """Initialize the switcher v2 create schedule response message."""
        super().__init__(loop, response, ResponseMessageType.CREATE_SCHEDULE)
