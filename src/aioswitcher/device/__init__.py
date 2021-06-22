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

"""Switcher unofficial integration device module."""

from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto, unique


@unique
class DeviceCategory(Enum):
    """Enum for relaying the device category."""

    WATER_HEATER = auto()
    POWER_PLUG = auto()


@unique
class DeviceType(Enum):
    """Enum for relaying the type of the switcher devices."""

    MINI = "Switcher Mini", "0f", DeviceCategory.WATER_HEATER
    POWER_PLUG = "Switcher Power Plug", "a8", DeviceCategory.POWER_PLUG
    TOUCH = "Switcher Touch", "0b", DeviceCategory.WATER_HEATER
    V2_ESP = "Switcher V2 (esp)", "a7", DeviceCategory.WATER_HEATER
    V2_QCA = "Switcher V2 (qualcomm)", "a1", DeviceCategory.WATER_HEATER
    V4 = "Switcher V4", "17", DeviceCategory.WATER_HEATER

    def __new__(
        cls, value: str, hex_rep: str, category: DeviceCategory
    ) -> "DeviceType":
        """Override the default enum constructor and include extra properties."""
        new_enum = object.__new__(cls)
        new_enum._value = value
        new_enum._hex_rep = hex_rep
        new_enum._category = category
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
    def category(self) -> DeviceCategory:
        """Return the category of the device type."""
        return self._category  # type: ignore


@unique
class DeviceState(Enum):
    """Enum class represnting the device's state."""

    ON = "0100", "on"
    OFF = "0000", "off"

    def __new__(cls, value: str, display: str) -> "DeviceState":
        """Override the default enum constructor and include extra properties."""
        new_enum = object.__new__(cls)
        new_enum._value = value
        new_enum._display = display
        return new_enum

    @property
    def display(self) -> str:
        """Return the display name of the state."""
        return self._display  # type: ignore

    @property
    def value(self) -> str:
        """Return the value of the state."""
        return self._value  # type: ignore


@dataclass
class SwitcherBase(ABC):
    """Abstraction for all switcher devices.

    Args:
        device_type: the DeviceType appropriate member.
        device_state: the DeviceState appropriate member.
        device_id: the id retrieved from the device.
        ip_address: the ip address assigned to the device.
        mac_address: the mac address assigned to the device.
        name: the name of the device.

    """

    device_type: DeviceType
    device_state: DeviceState
    device_id: str
    ip_address: str
    mac_address: str
    name: str
    last_data_update: datetime = field(init=False)

    def __post_init__(self) -> None:
        """Post initialization, set last_data_update to the instantiation datetime."""
        self.last_data_update = datetime.now()


@dataclass
class SwitcherPowerBase(ABC):
    """Abstraction for all switcher devices reporting power data.

    Args:
        power_consumption: the current power consumpstion in watts.
        electric_current: the current power consumpstion in amps.

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
