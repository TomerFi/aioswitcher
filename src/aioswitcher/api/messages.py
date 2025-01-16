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

from binascii import hexlify, unhexlify
from dataclasses import InitVar, dataclass, field
from typing import Set, final

from ..device import (
    DeviceState,
    DeviceType,
    ShutterChildLock,
    ShutterDirection,
    ThermostatFanLevel,
    ThermostatMode,
    ThermostatSwing,
)
from ..device.tools import (
    get_light_discovery_packet_index,
    get_shutter_discovery_packet_index,
    seconds_to_iso_time,
    watts_to_amps,
)
from ..schedule.parser import SwitcherSchedule, get_schedules


@final
@dataclass
class StateMessageParser:
    """Use for parsing api messages."""

    response: InitVar[bytes]

    def __post_init__(self, response: bytes) -> None:
        """Post initialization of the parser."""
        self._hex_response = hexlify(response)

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
        hex_state = self._hex_response[150:152].decode()
        states = dict(map(lambda s: (s.value, s), DeviceState))
        return states[hex_state]

    def get_thermostat_state(self) -> DeviceState:
        """Return the current thermostat state."""
        hex_power = self._hex_response[156:158].decode()
        return DeviceState.OFF if hex_power == DeviceState.OFF.value else DeviceState.ON

    def get_thermostat_mode(self) -> ThermostatMode:
        """Return the current thermostat mode."""
        hex_mode = self._hex_response[158:160]
        modes = dict(map(lambda s: (s.value, s), ThermostatMode))
        try:
            return modes[hex_mode.decode()]
        except KeyError:
            return ThermostatMode.COOL

    def get_thermostat_temp(self) -> float:
        """Return the current temp of the thermostat."""
        return int(self._hex_response[154:156] + self._hex_response[152:154], 16) / 10

    def get_thermostat_target_temp(self) -> int:
        """Return the current temperature of the thermostat."""
        hex_temp = self._hex_response[160:162]
        return int(hex_temp, 16)

    def get_thermostat_fan_level(self) -> ThermostatFanLevel:
        """Return the current thermostat fan level."""
        hex_level = self._hex_response[162:163].decode()
        levels = dict(map(lambda s: (s.value, s), ThermostatFanLevel))
        try:
            return levels[hex_level]
        except KeyError:
            return ThermostatFanLevel.LOW

    def get_thermostat_swing(self) -> ThermostatSwing:
        """Return the current thermostat fan swing."""
        hex_swing = self._hex_response[163:164].decode()
        return (
            ThermostatSwing.OFF
            if hex_swing == ThermostatSwing.OFF.value
            else ThermostatSwing.ON
        )

    def get_thermostat_remote_id(self) -> str:
        """Return the current thermostat remote."""
        remote_hex = unhexlify(self._hex_response)
        return remote_hex[84:92].decode().rstrip("\x00")

    def get_shutter_position(self, index: int) -> int:
        """Return the current shutter position."""
        start_index = 152 + (index * 32)
        end_index = start_index + 2
        hex_pos = self._hex_response[start_index:end_index].decode()
        return int(hex_pos, 16)

    def get_shutter_direction(self, index: int) -> ShutterDirection:
        """Return the current shutter direction."""
        start_index = 156 + (index * 32)
        end_index = start_index + 4
        hex_dir = self._hex_response[start_index:end_index].decode()
        directions = dict(map(lambda s: (s.value, s), ShutterDirection))
        return directions[hex_dir]

    def get_shutter_child_lock(self, index: int) -> ShutterChildLock:
        """Return the current shutter child lock."""
        start_index = 154 + (index * 32)
        end_index = start_index + 2
        hex_pos = self._hex_response[start_index:end_index].decode()
        hex_device_state = hex_pos[0:2]
        return (
            ShutterChildLock.ON
            if hex_device_state == ShutterChildLock.ON.value
            else ShutterChildLock.OFF
        )

    def get_light_state(self, index: int) -> DeviceState:
        """Return the current light state."""
        start_index = 152 + (index * 32)
        end_index = start_index + 2
        hex_pos = self._hex_response[start_index:end_index].decode()
        hex_device_state = hex_pos[0:2]
        return (
            DeviceState.ON
            if hex_device_state == DeviceState.ON.value
            else DeviceState.OFF
        )


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
        self.time_left = parser.get_time_left() if self.state == DeviceState.ON and parser.get_auto_shutdown() != "00:00:00" else "00:00:00"
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
class SwitcherThermostatStateResponse(SwitcherBaseResponse):
    """Representation of the Switcher thermostat device state response message."""

    state: DeviceState = field(init=False)
    mode: ThermostatMode = field(init=False)
    fan_level: ThermostatFanLevel = field(init=False)
    temperature: float = field(init=False)
    target_temperature: int = field(init=False)
    swing: ThermostatSwing = field(init=False)
    remote_id: str = field(init=False)

    def __post_init__(self) -> None:
        """Post initialization of the message."""
        parser = StateMessageParser(self.unparsed_response)

        self.state = parser.get_thermostat_state()
        self.mode = parser.get_thermostat_mode()
        self.fan_level = parser.get_thermostat_fan_level()
        self.temperature = parser.get_thermostat_temp()
        self.target_temperature = parser.get_thermostat_target_temp()
        self.swing = parser.get_thermostat_swing()
        self.remote_id = parser.get_thermostat_remote_id()


@final
@dataclass
class SwitcherShutterStateResponse(SwitcherBaseResponse):
    """Representation of the Switcher shutter devices state response message."""

    position: int = field(init=False)
    direction: ShutterDirection = field(init=False)
    child_lock: ShutterChildLock = field(init=False)
    device_type: DeviceType
    index: int

    def __post_init__(self) -> None:
        """Post initialization of the message."""
        parser = StateMessageParser(self.unparsed_response)
        index = get_shutter_discovery_packet_index(self.device_type, self.index)

        self.direction = parser.get_shutter_direction(index)
        self.position = parser.get_shutter_position(index)
        self.child_lock = parser.get_shutter_child_lock(index)


@final
@dataclass
class SwitcherLightStateResponse(SwitcherBaseResponse):
    """Representation of the Switcher light devices state response message."""

    state: DeviceState = field(init=False)
    device_type: DeviceType
    index: int

    def __post_init__(self) -> None:
        """Post initialization of the message."""
        parser = StateMessageParser(self.unparsed_response)
        index = get_light_discovery_packet_index(self.device_type, self.index)

        self.state = parser.get_light_state(index)
