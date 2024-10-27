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

"""Switcher integration device module."""

from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto, unique
from typing import List, final


@unique
class DeviceCategory(Enum):
    """Enum for relaying the device category."""

    WATER_HEATER = auto()
    POWER_PLUG = auto()
    THERMOSTAT = auto()
    SHUTTER = auto()
    SINGLE_SHUTTER_DUAL_LIGHT = auto()
    DUAL_SHUTTER_SINGLE_LIGHT = auto()
    LIGHT = auto()


@unique
class DeviceType(Enum):
    """Enum for relaying the type of the switcher devices."""

    MINI = "Switcher Mini", "030f", 1, DeviceCategory.WATER_HEATER, False
    POWER_PLUG = "Switcher Power Plug", "01a8", 1, DeviceCategory.POWER_PLUG, False
    TOUCH = "Switcher Touch", "030b", 1, DeviceCategory.WATER_HEATER, False
    V2_ESP = "Switcher V2 (esp)", "01a7", 1, DeviceCategory.WATER_HEATER, False
    V2_QCA = "Switcher V2 (qualcomm)", "01a1", 1, DeviceCategory.WATER_HEATER, False
    V4 = "Switcher V4", "0317", 1, DeviceCategory.WATER_HEATER, False
    BREEZE = "Switcher Breeze", "0e01", 2, DeviceCategory.THERMOSTAT, False
    RUNNER = "Switcher Runner", "0c01", 2, DeviceCategory.SHUTTER, False
    RUNNER_MINI = "Switcher Runner Mini", "0c02", 2, DeviceCategory.SHUTTER, False
    RUNNER_S11 = (
        "Switcher Runner S11",
        "0f01",
        2,
        DeviceCategory.SINGLE_SHUTTER_DUAL_LIGHT,
        True,
    )
    RUNNER_S12 = (
        "Switcher Runner S12",
        "0f02",
        2,
        DeviceCategory.DUAL_SHUTTER_SINGLE_LIGHT,
        True,
    )
    LIGHT_SL01 = (
        "Switcher Light SL01",
        "0f04",
        2,
        DeviceCategory.LIGHT,
        True,
    )
    LIGHT_SL01_MINI = (
        "Switcher Light SL01 Mini",
        "0f07",
        2,
        DeviceCategory.LIGHT,
        True,
    )
    LIGHT_SL02 = (
        "Switcher Light SL02",
        "0f05",
        2,
        DeviceCategory.LIGHT,
        True,
    )
    LIGHT_SL02_MINI = (
        "Switcher Light SL02 Mini",
        "0f08",
        2,
        DeviceCategory.LIGHT,
        True,
    )
    LIGHT_SL03 = (
        "Switcher Light SL03",
        "0f06",
        2,
        DeviceCategory.LIGHT,
        True,
    )

    def __new__(
        cls,
        value: str,
        hex_rep: str,
        protocol_type: int,
        category: DeviceCategory,
        token_needed: bool,
    ) -> "DeviceType":
        """Override the default enum constructor and include extra properties."""
        new_enum = object.__new__(cls)
        new_enum._value = value  # type: ignore
        new_enum._hex_rep = hex_rep  # type: ignore
        new_enum._protocol_type = protocol_type  # type: ignore
        new_enum._category = category  # type: ignore
        new_enum._token_needed = token_needed  # type: ignore
        return new_enum

    @property
    def value(self) -> str:
        """Return the value of the state."""
        return self._value  # type: ignore

    @property
    def hex_rep(self) -> str:
        """Return the hexadecimal representation of the device type."""
        return self._hex_rep  # type: ignore

    @property
    def protocol_type(self) -> int:
        """Return the protocol type of the device."""
        return self._protocol_type  # type: ignore

    @property
    def category(self) -> DeviceCategory:
        """Return the category of the device type."""
        return self._category  # type: ignore

    @property
    def token_needed(self) -> bool:
        """Return true if token in needed for the device."""
        return self._token_needed  # type: ignore


@unique
class DeviceState(Enum):
    """Enum class representing the device's state."""

    ON = "01", "on"
    OFF = "00", "off"

    def __new__(cls, value: str, display: str) -> "DeviceState":
        """Override the default enum constructor and include extra properties."""
        new_enum = object.__new__(cls)
        new_enum._value = value  # type: ignore
        new_enum._display = display  # type: ignore
        return new_enum

    @property
    def display(self) -> str:
        """Return the display name of the state."""
        return self._display  # type: ignore

    @property
    def value(self) -> str:
        """Return the value of the state."""
        return self._value  # type: ignore


class ThermostatMode(Enum):
    """Enum class representing the thermostat device's position."""

    AUTO = "01", "auto"
    DRY = "02", "dry"
    FAN = "03", "fan"
    COOL = "04", "cool"
    HEAT = "05", "heat"

    def __new__(cls, value: str, display: str) -> "ThermostatMode":
        """Override the default enum constructor and include extra properties."""
        new_enum = object.__new__(cls)
        new_enum._value = value  # type: ignore
        new_enum._display = display  # type: ignore
        return new_enum

    @property
    def display(self) -> str:
        """Return the display name of the mode."""
        return self._display  # type: ignore

    @property
    def value(self) -> str:
        """Return the value of the mode."""
        return self._value  # type: ignore


class ThermostatFanLevel(Enum):
    """Enum class representing the thermostat device's fan level."""

    LOW = "1", "low"
    MEDIUM = "2", "medium"
    HIGH = "3", "high"
    AUTO = "0", "auto"

    def __new__(cls, value: str, display: str) -> "ThermostatFanLevel":
        """Override the default enum constructor and include extra properties."""
        new_enum = object.__new__(cls)
        new_enum._value = value  # type: ignore
        new_enum._display = display  # type: ignore
        return new_enum

    @property
    def display(self) -> str:
        """Return the display name of the fan level."""
        return self._display  # type: ignore

    @property
    def value(self) -> str:
        """Return the value of the fan level."""
        return self._value  # type: ignore


class ThermostatSwing(Enum):
    """Enum class representing the thermostat device's swing state."""

    OFF = "0", "off"
    ON = "1", "on"

    def __new__(cls, value: str, display: str) -> "ThermostatSwing":
        """Override the default enum constructor and include extra properties."""
        new_enum = object.__new__(cls)
        new_enum._value = value  # type: ignore
        new_enum._display = display  # type: ignore
        return new_enum

    @property
    def display(self) -> str:
        """Return the display name of the swing."""
        return self._display  # type: ignore

    @property
    def value(self) -> str:
        """Return the value of the swing."""
        return self._value  # type: ignore


@final
class ShutterDirection(Enum):
    """Enum class representing the shutter device's position."""

    SHUTTER_STOP = "0000", "stop"
    SHUTTER_UP = "0100", "up"
    SHUTTER_DOWN = "0001", "down"

    def __new__(cls, value: str, display: str) -> "ShutterDirection":
        """Override the default enum constructor and include extra properties."""
        new_enum = object.__new__(cls)
        new_enum._value = value  # type: ignore
        new_enum._display = display  # type: ignore
        return new_enum

    @property
    def display(self) -> str:
        """Return the display name of the direction."""
        return self._display  # type: ignore

    @property
    def value(self) -> str:
        """Return the value of the direction."""
        return self._value  # type: ignore


@dataclass
class SwitcherBase(ABC):
    """Abstraction for all switcher devices.

    Args:
        device_type: the DeviceType appropriate member.
        device_state: the DeviceState appropriate member.
        device_id: the id retrieved from the device.
        device_key: the login key of the device.
        ip_address: the ip address assigned to the device.
        mac_address: the mac address assigned to the device.
        name: the name of the device.

    """

    device_type: DeviceType
    device_state: DeviceState
    device_id: str
    device_key: str
    ip_address: str
    mac_address: str
    name: str
    token_needed: bool
    last_data_update: datetime = field(init=False)

    def __post_init__(self) -> None:
        """Post initialization, set last_data_update to the instantiation datetime."""
        self.last_data_update = datetime.now()


@dataclass
class SwitcherPowerBase(ABC):
    """Abstraction for all switcher devices reporting power data.

    Args:
        power_consumption: the current power consumption in watts.
        electric_current: the current power consumption in amps.

    """

    power_consumption: int
    electric_current: float


@dataclass
class SwitcherTimedBase(ABC):
    """Abstraction for all switcher devices supporting timed operations.

    Args:
        remaining_time: remaining time to current run.
        auto_shutdown: configured value for auto shutdown.

    """

    remaining_time: str
    auto_shutdown: str

    @property
    def auto_off_set(self) -> str:
        """Fix for backward compatibility issues with home assistant."""
        return self.auto_shutdown


@dataclass
class SwitcherThermostatBase(ABC):
    """Abstraction for switcher thermostat devices.

    Args:
        mode: the mode of the thermostat.
        temperature: the current temperature in celsius.
        target_temperature: the current target temperature in celsius.
        fan_level: the current fan level in celsius.
        swing: the current swing state.
        remote_id: the id of the remote used to control this thermostat
    """

    mode: ThermostatMode
    temperature: float
    target_temperature: int
    fan_level: ThermostatFanLevel
    swing: ThermostatSwing
    remote_id: str


@dataclass
class SwitcherShutterBase(ABC):
    """Abstraction for all switcher devices controlling shutter.

    Args:
        position: the current array of position of the shutter (integer percentage).
        direction: the current array of direction of the shutter.
    """

    position: List[int]
    direction: List[ShutterDirection]


@dataclass
class SwitcherSingleShutterDualLightBase(ABC):
    """Abstraction for all switcher devices controlling shutter with dual light.

    Args:
        position: the current array of position of the shutter (integer percentage).
        direction: the current array of direction of the shutter.
        light: the current array of light state.
    """

    position: List[int]
    direction: List[ShutterDirection]
    light: List[DeviceState]


@dataclass
class SwitcherDualShutterSingleLightBase(ABC):
    """Abstraction for all switcher devices controlling dual shutter with single light.

    Args:
        position: the current array of position of the shutter (integer percentage).
        direction: the current array of direction of the shutter.
        light: the current array of light state.
    """

    position: List[int]
    direction: List[ShutterDirection]
    light: List[DeviceState]


@dataclass
class SwitcherLightBase(ABC):
    """Abstraction for all switcher devices controlling light.

    Args:
        light: the current array of light state.
    """

    light: List[DeviceState]


@final
@dataclass
class SwitcherPowerPlug(SwitcherPowerBase, SwitcherBase):
    """Implementation of the Switcher Power Plug device.

    Please Note the order of the inherited classes to understand the order of the
    instantiation parameters and the super call.
    """

    def __post_init__(self) -> None:
        """Post initialization validate device type category as POWER_PLUG."""
        if self.device_type.category != DeviceCategory.POWER_PLUG:
            raise ValueError("only power plugs are allowed")
        super().__post_init__()


@final
@dataclass
class SwitcherWaterHeater(SwitcherTimedBase, SwitcherPowerBase, SwitcherBase):
    """Implementation of the Switcher Water Heater device.

    Please Note the order of the inherited classes to understand the order of the
    instantiation parameters and the super call.
    """

    def __post_init__(self) -> None:
        """Post initialization validate device type category as WATER_HEATER."""
        if self.device_type.category != DeviceCategory.WATER_HEATER:
            raise ValueError("only water heaters are allowed")
        super().__post_init__()


@final
@dataclass
class SwitcherThermostat(SwitcherThermostatBase, SwitcherBase):
    """Implementation of the Switcher Thermostat device."""

    def __post_init__(self) -> None:
        """Post initialization validate device type category as THERMOSTAT."""
        if self.device_type.category != DeviceCategory.THERMOSTAT:
            raise ValueError("only thermostats are allowed")
        self.remote = None
        return super().__post_init__()


@final
@dataclass
class SwitcherShutter(SwitcherShutterBase, SwitcherBase):
    """Implementation of the Switcher Shutter device."""

    def __post_init__(self) -> None:
        """Post initialization validate device type category as SHUTTER."""
        if self.device_type.category != DeviceCategory.SHUTTER:
            raise ValueError("only shutters are allowed")
        return super().__post_init__()


@final
@dataclass
class SwitcherSingleShutterDualLight(SwitcherSingleShutterDualLightBase, SwitcherBase):
    """Implementation of the Switcher Shutter with dual light device."""

    def __post_init__(self) -> None:
        """Post initialization.

        Validate device type category as SINGLE_SHUTTER_DUAL_LIGHT.
        """
        if self.device_type.category != DeviceCategory.SINGLE_SHUTTER_DUAL_LIGHT:
            raise ValueError("only shutters with dual lights are allowed")
        return super().__post_init__()


@final
@dataclass
class SwitcherDualShutterSingleLight(SwitcherDualShutterSingleLightBase, SwitcherBase):
    """Implementation of the Switcher dual Shutter with single light device."""

    def __post_init__(self) -> None:
        """Post initialization.

        Validate device type category as DUAL_SHUTTER_SINGLE_LIGHT.
        """
        if self.device_type.category != DeviceCategory.DUAL_SHUTTER_SINGLE_LIGHT:
            raise ValueError("only dual shutters with single lights are allowed")
        return super().__post_init__()


@final
@dataclass
class SwitcherLight(SwitcherLightBase, SwitcherBase):
    """Implementation of the Switcher Light device."""

    def __post_init__(self) -> None:
        """Post initialization validate device type category as LIGHT."""
        if self.device_type.category != DeviceCategory.LIGHT:
            raise ValueError("only lights are allowed")
        return super().__post_init__()
