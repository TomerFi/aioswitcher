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

"""Switcher integration TCP socket API messages."""

from binascii import hexlify
from dataclasses import InitVar, dataclass, field
from typing import Set, final

from ..device.tools import seconds_to_iso_time, watts_to_amps
from ..schedule.parser import SwitcherSchedule, get_schedules

from ..device import DeviceState, ThermostatFanLevel, ThermostatMode, ThermostatSwing


@final
@dataclass
class StateMessageParser:
    """Use for parsing api messages."""

    response: InitVar[bytes]

    def __post_init__(self, response) -> None:
        """Post initialization of the parser."""
        self._hex_response = hexlify(response)
        print(self._hex_response)

    def get_power_consumption(self) -> int:
        """Return the current power consumption of the device."""
        hex_power = self._hex_response[154:162]
        return int(hex_power[2:4] + hex_power[0:2], 16)

    def get_time_left(self) -> str:
        """Return the time left for the device current run."""
        hex_time_left = self._hex_response[178:186]
        time_left_seconds = int(
            hex_time_left[6:8]
            + hex_time_left[4:6]
            + hex_time_left[2:4]
            + hex_time_left[0:2],
            16,
        )
        return seconds_to_iso_time(time_left_seconds)

    def get_time_on(self) -> str:
        """Return how long the device has been on."""
        hex_time_on = self._hex_response[186:194]
        time_on_seconds = int(
            hex_time_on[6:8] + hex_time_on[4:6] + hex_time_on[2:4] + hex_time_on[0:2],
            16,
        )
        return seconds_to_iso_time(time_on_seconds)

    def get_auto_shutdown(self) -> str:
        """Return the value of the auto shutdown configuration."""
        hex_auto_off = self._hex_response[194:202]
        auto_off_seconds = int(
            hex_auto_off[6:8]
            + hex_auto_off[4:6]
            + hex_auto_off[2:4]
            + hex_auto_off[0:2],
            16,
        )
        return seconds_to_iso_time(auto_off_seconds)

    def get_state(self) -> DeviceState:
        """Return the current device state."""
        hex_state = self._hex_response[150:154].decode()
        states = dict(map(lambda s: (s.value, s), DeviceState))
        return states[hex_state]

    def get_thermostat_temp(self) -> float:
        """Return the current temp of the thermostat."""
        hex_temp = self._hex_response[77:78] + self._hex_response[76:77]
        return int(hex_temp, 16) / 10

    def get_thermostat_power(self) -> DeviceState:
        """Return the current thermostat power."""
        hex_power = self._hex_response[137:138]
        return DeviceState.ON if hex_power == DeviceState.ON.value else DeviceState.OFF

    def get_thermostat_mode(self) -> ThermostatMode:
        """Return the current thermostat mode."""
        hex_mode = self._hex_response[79:80]
        modes = dict(map(lambda s: (s.value, s), ThermostatMode))

        return "COOL" if hex_mode not in modes else modes[hex_mode]

    def get_thermostat_target_temp(self) -> int:
        """Return the current temp of the thermostat."""
        hex_temp = self._hex_response[80:81]
        return int(hex_temp, 16)

    def get_thermostat_fan_level(self) -> ThermostatFanLevel:
        """Return the current thermostat fan level."""
        hex_level = self._hex_response[81:82]
        states = dict(map(lambda s: (s.value, s), ThermostatFanLevel))

        return "LOW" if hex_level[0:1] not in states else states[hex_level[0:1]]

    def get_thermostat_swing(self) -> ThermostatSwing:
        """Return the current thermostat fan swing."""
        hex_swing = self._hex_response[81:82]

        return (
            ThermostatSwing.OFF
            if hex_swing[1:2] == ThermostatSwing.OFF.value
            else ThermostatSwing.ON
        )

    def get_thermostat_remote(self) -> str:
        """Return the current thermostat remote."""
        remote_hex = hexlify(self._hex_response[42:48]).decode()

        print(remote_hex)
        return str(self._hex_response[40:50].decode())


@dataclass
class SwitcherBaseResponse:
    """Representation of the switcher base response message.

    Applicable for all messages that do no require post initialization.
    e.g. not applicable for SwitcherLoginResponse, SwitcherStateResponse,
    SwitcherGetScheduleResponse.

    Args:
        unparsed_response: the raw response from the device.

    """

    unparsed_response: bytes

    @property
    def successful(self) -> bool:
        """Return true if the response is not empty.

        Partially indicating the request was successful.
        """
        return self.unparsed_response is not None and len(self.unparsed_response) > 0


@final
@dataclass
class SwitcherLoginResponse(SwitcherBaseResponse):
    """Representations of the switcher login response message."""

    session_id: str = field(init=False)

    def __post_init__(self) -> None:
        """Post initialization of the response."""
        try:
            self.session_id = hexlify(self.unparsed_response)[16:24].decode()
        except Exception as exc:
            raise ValueError("failed to parse login response message") from exc


@final
@dataclass
class SwitcherStateResponse(SwitcherBaseResponse):
    """Representation of the switcher state response message."""

    state: DeviceState = field(init=False)
    time_left: str = field(init=False)
    time_on: str = field(init=False)
    auto_shutdown: str = field(init=False)
    power_consumption: int = field(init=False)
    electric_current: float = field(init=False)

    def __post_init__(self) -> None:
        """Post initialization of the message."""
        parser = StateMessageParser(self.unparsed_response)

        self.state = parser.get_state()
        self.time_left = parser.get_time_left()
        self.time_on = parser.get_time_on()
        self.auto_shutdown = parser.get_auto_shutdown()
        self.power_consumption = parser.get_power_consumption()
        self.electric_current = watts_to_amps(self.power_consumption)


@final
@dataclass
class SwitcherGetSchedulesResponse(SwitcherBaseResponse):
    """Representation of the switcher get schedule message."""

    schedules: Set[SwitcherSchedule] = field(init=False)

    def __post_init__(self) -> None:
        """Post initialization of the message."""
        self.schedules = get_schedules(self.unparsed_response)

    @property
    def found_schedules(self) -> bool:
        """Return true if found schedules in the response."""
        return len(self.schedules) > 0


@final
@dataclass
class SwitcherBreezeStateResponse(SwitcherBaseResponse):
    """Representation of the switcher state response message."""

    state: DeviceState = field(init=False)
    mode: ThermostatMode = field(init=False)
    fan_level: ThermostatFanLevel = field(init=False)
    temprature: int = field(init=False)
    target_temprature: float = field(init=False)
    swing: ThermostatSwing = field(init=False)
    remote_id: str = field(init=False)

    def __post_init__(self) -> None:
        """Post initialization of the message."""
        parser = StateMessageParser(self.unparsed_response)

        self.state = parser.get_thermostat_power()
        self.mode = parser.get_thermostat_mode()
        self.fan_level = parser.get_thermostat_fan_level()
        self.temprature = parser.get_thermostat_temp()
        self.target_temprature = parser.get_thermostat_target_temp()
        self.swing = parser.get_thermostat_swing()
        self.remote_id = parser.get_thermostat_remote()
