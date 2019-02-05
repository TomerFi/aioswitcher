"""Switcher Packet Response Messages."""

from typing import Optional, List
from binascii import hexlify

from aioswitcher.consts import ENCODING_CODEC

from aioswitcher.tools import convert_seconds_to_iso_time

from aioswitcher.consts import (STATE_ON, STATE_RESPONSE_ON, STATE_OFF,
                                STATE_RESPONSE_OFF, STATE_UNKNOWN)

from aioswitcher.schedules import SwitcherV2Schedule, create_schedules_list


class SwitcherV2BaseResponseMSG(object):
    """Represntation of the switcher v2 base response message."""

    def __init__(self, response: bytes) -> None:
        """Initialize the base object."""
        self._unparsed_response = response

    @property
    def unparsed_response(self) -> bytes:
        """Return the uparsed response message."""
        return self._unparsed_response

    @property
    def successful(self) -> bool:
        """Return the status of the message."""
        return self._unparsed_response is not None


class SwitcherV2LoginResponseMSG(SwitcherV2BaseResponseMSG):
    """Represntation of the switcher v2 login response message."""

    def __init__(self, response: bytes) -> None:
        """Initialize the login response."""
        super().__init__(response)
        try:
            self._session_id = hexlify(response)[16:24].decode(ENCODING_CODEC)
        except Exception as ex:
            raise Exception("failed to parse login response message") from ex

    @property
    def session_id(self) -> str:
        """Return the retrieved session id."""
        return self._session_id


class SwitcherV2StateResponseMSG(SwitcherV2BaseResponseMSG):
    """represntation of the switcher v2 state response message."""

    def __init__(self, response: bytes) -> None:
        """Initialize the state response message."""
        super().__init__(response)
        self._power_consumption = 0
        self._electric_current = 0.0

        try:
            temp_power = hexlify(response)[154:162]
            self._power_consumption = int(
                temp_power[2:4] + temp_power[0:2], 16)
            self._electric_current = round(
                (self._power_consumption / float(220)), 1)

            temp_time_left = hexlify(response)[178:186]
            temp_time_left_seconds = int(temp_time_left[6:8]
                                         + temp_time_left[4:6]
                                         + temp_time_left[2:4]
                                         + temp_time_left[0:2], 16)
            self._time_to_auto_off = convert_seconds_to_iso_time(
                temp_time_left_seconds)

            temp_auto_off = hexlify(response)[194:202]
            temp_auto_off_seconds = int(temp_auto_off[6:8]
                                        + temp_auto_off[4:6]
                                        + temp_auto_off[2:4]
                                        + temp_auto_off[0:2], 16)
            self._auto_off_set = convert_seconds_to_iso_time(
                temp_auto_off_seconds)

            temp_state = hexlify(response)[150:154].decode(ENCODING_CODEC)
            self._state = STATE_ON if temp_state == STATE_RESPONSE_ON \
                else STATE_OFF if temp_state == STATE_RESPONSE_OFF \
                else STATE_UNKNOWN

        except Exception as ex:
            raise Exception("failed to parse state response message") from ex

    @property
    def state(self) -> str:
        """Return the state."""
        return self._state

    @property
    def time_left(self) -> str:
        """Return the time left to auto-off."""
        return self._time_to_auto_off

    @property
    def auto_off(self) -> str:
        """Return the auto-off configuration value."""
        return self._auto_off_set

    @property
    def power(self) -> Optional[int]:
        """Return the current power consumption in watts."""
        return self._power_consumption

    @property
    def current(self) -> Optional[float]:
        """Return the power consumption in amps."""
        return self._electric_current


class SwitcherV2ControlResponseMSG(SwitcherV2BaseResponseMSG):
    """Represntation of the switcher v2 control response message."""

    def __init__(self, response: bytes) -> None:
        """Initialize the Control response message."""
        super().__init__(response)


class SwitcherV2SetAutoOffResponseMSG(SwitcherV2BaseResponseMSG):
    """Represntation of the switcher v2 set auto-off response message."""

    def __init__(self, response: bytes) -> None:
        """Initialize the Set Auto-Off response message."""
        super().__init__(response)


class SwitcherV2UpdateNameResponseMSG(SwitcherV2BaseResponseMSG):
    """Represntation of the switcher v2 update name response message."""

    def __init__(self, response: bytes) -> None:
        """Initialize the Set Name response message."""
        super().__init__(response)


class SwitcherV2GetScheduleResponseMSG(SwitcherV2BaseResponseMSG):
    """represnation of the switcher v2 get schedule message."""

    def __init__(self, response: bytes) -> None:
        """Initialize the Set Name response message."""
        super().__init__(response)
        self._schedule_list = []  # type: List[SwitcherV2Schedule]
        try:
            res = hexlify(response)
            idx = res[90:-8].decode(ENCODING_CODEC)

            schedules_details = create_schedules_list(idx, 32)
            if not len(schedules_details) == 0:
                for i in range(len(schedules_details)):
                    schedule = SwitcherV2Schedule(i, schedules_details)
                    self._schedule_list.append(schedule)
        except Exception as ex:
            raise Exception(
                "failed to parse get schedules response message") from ex

    @property
    def found_schedules(self) -> bool:
        """Return true if found shedules in the response."""
        return self._schedule_list != []

    @property
    def get_schedules(self) -> List[SwitcherV2Schedule]:
        """Return the schedules list."""
        return self._schedule_list


class SwitcherV2DisableEnableScheduleResponseMSG(SwitcherV2BaseResponseMSG):
    """Represntation of the switcher v2 dis/en schedule response message."""

    def __init__(self, response: bytes) -> None:
        """Initialize the switcher v2 dis/en schedule response message."""
        super().__init__(response)


class SwitcherV2DeleteScheduleResponseMSG(SwitcherV2BaseResponseMSG):
    """Represntation of the switcher v2 delete schedule response message."""

    def __init__(self, response: bytes) -> None:
        """Initialize the switcher v2 delete schedule response message."""
        super().__init__(response)


class SwitcherV2CreateScheduleResponseMSG(SwitcherV2BaseResponseMSG):
    """Represntation of the switcher v2 create schedule response message."""

    def __init__(self, response: bytes) -> None:
        """Initialize the switcher v2 create schedule response message."""
        super().__init__(response)
