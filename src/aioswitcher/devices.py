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

"""Switcher unofficial integration devices."""

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum, auto, unique
from typing import Optional


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


class SwitcherBase(ABC):
    """Abstraction for all switcher devices."""

    @property
    @abstractmethod
    def device_type(self) -> DeviceType:
        """Return the switcher device type."""
        raise NotImplementedError

    @property
    @abstractmethod
    def device_state(self) -> DeviceState:
        """Return the switcher device state."""
        raise NotImplementedError

    @property
    @abstractmethod
    def device_id(self) -> str:
        """str: Returns the device id."""
        raise NotImplementedError

    @property
    @abstractmethod
    def ip_address(self) -> str:
        """str: Returns the ip address."""
        raise NotImplementedError

    @property
    @abstractmethod
    def mac_address(self) -> str:
        """str: Returns the mac address."""
        raise NotImplementedError

    @property
    @abstractmethod
    def name(self) -> str:
        """str: Returns the device name."""
        raise NotImplementedError

    @property
    def last_data_update(self) -> datetime:
        """datetime: Returns timestamp of the last update."""
        raise NotImplementedError


class SwitcherPowerBase(ABC):
    """Abstraction for all switcher devices reporting power data."""

    @property
    @abstractmethod
    def power_consumption(self) -> int:
        """int: Returns the power consumption in watts."""
        raise NotImplementedError

    @property
    @abstractmethod
    def electric_current(self) -> float:
        """float: returns the power consumption in amps."""
        raise NotImplementedError


class SwitcherTimedBase(ABC):
    """Abstraction for all switcher devices supporting timed operations."""

    @property
    @abstractmethod
    def remaining_time(self) -> Optional[str]:
        """str: Returns the time left to auto shutdown."""
        raise NotImplementedError

    @property
    @abstractmethod
    def auto_shutdown(self) -> str:
        """str: Returns the auto-shutdown configuration value."""
        raise NotImplementedError


class SwitcherPowerPlug(SwitcherBase, SwitcherPowerBase):
    """Implementation of the Switcher Power Plug device.

    Args:
        device_type: the DeviceType appropriate member.
        device_state: the DeviceState appropriate member.
        device_id: the id retrieved from the device.
        ip_address: the ip address assigned to the device.
        mac_address: the mac address assigned to the device.
        name: the name of the device.
        power_consumption: the current power consumpstion in watts.
        electric_current: the current power consumpstion in amps.

    """

    def __init__(
        self,
        device_type: DeviceType,
        device_state: DeviceState,
        device_id: str,
        ip_address: str,
        mac_address: str,
        name: str,
        power_consumption: int,
        electric_current: float,
    ) -> None:
        """Initialize the Switcher Power Plug Device."""
        if device_type.category != DeviceCategory.POWER_PLUG:
            raise ValueError("only power plugs are allowed")
        self._device_type = device_type
        self._device_state = device_state
        self._device_id = device_id
        self._ip_address = ip_address
        self._mac_address = mac_address
        self._name = name
        self._power_consumption = power_consumption
        self._electric_current = electric_current
        self._last_data_update = datetime.now()

    @property
    def device_type(self) -> DeviceType:
        """Return the switcher device type."""
        return self._device_type

    @property
    def device_state(self) -> DeviceState:
        """Return the switcher device state."""
        return self._device_state

    @property
    def device_id(self) -> str:
        """str: Returns the device id."""
        return self._device_id

    @property
    def ip_address(self) -> str:
        """str: Returns the ip address."""
        return self._ip_address

    @property
    def mac_address(self) -> str:
        """str: Returns the mac address."""
        return self._mac_address

    @property
    def name(self) -> str:
        """str: Returns the device name."""
        return self._name

    @property
    def power_consumption(self) -> int:
        """int: Returns the power consumption in watts."""
        return self._power_consumption

    @property
    def electric_current(self) -> float:
        """float: returns the power consumption in amps."""
        return self._electric_current

    @property
    def last_data_update(self) -> datetime:
        """datetime: Returns timestamp of the last update."""
        return self._last_data_update


class SwitcherWaterHeater(SwitcherBase, SwitcherPowerBase, SwitcherTimedBase):
    """Implementation of the Switcher Water Heater device.

    Args:
        device_type: the DeviceType appropriate member.
        device_state: the DeviceState appropriate member.
        device_id: the id retrieved from the device.
        ip_address: the ip address assigned to the device.
        mac_address: the mac address assigned to the device.
        name: the name of the device.
        power_consumption: the current power consumpstion in watts.
        electric_current: the current power consumpstion in amps.
        remaining_time: remaining time (if on).
        auto_shutdown: configured value for auto shutdown.

    """

    def __init__(
        self,
        device_type: DeviceType,
        device_state: DeviceState,
        device_id: str,
        ip_address: str,
        mac_address: str,
        name: str,
        power_consumption: int,
        electric_current: float,
        remaining_time: Optional[str],
        auto_shutdown: str,
    ) -> None:
        """Initialize the Switcher Water Heater Device."""
        if device_type.category != DeviceCategory.WATER_HEATER:
            raise ValueError("only water heaters are allowed")
        self._device_type = device_type
        self._device_state = device_state
        self._device_id = device_id
        self._ip_address = ip_address
        self._mac_address = mac_address
        self._name = name
        self._power_consumption = power_consumption
        self._electric_current = electric_current
        self._remaining_time = remaining_time
        self._auto_shutdown = auto_shutdown
        self._last_data_update = datetime.now()

    @property
    def device_type(self) -> DeviceType:
        """Return the switcher device type."""
        return self._device_type

    @property
    def device_state(self) -> DeviceState:
        """Return the switcher device state."""
        return self._device_state

    @property
    def device_id(self) -> str:
        """str: Returns the device id."""
        return self._device_id

    @property
    def ip_address(self) -> str:
        """str: Returns the ip address."""
        return self._ip_address

    @property
    def mac_address(self) -> str:
        """str: Returns the mac address."""
        return self._mac_address

    @property
    def name(self) -> str:
        """str: Returns the device name."""
        return self._name

    @property
    def power_consumption(self) -> int:
        """int: Returns the power consumption in watts."""
        return self._power_consumption

    @property
    def electric_current(self) -> float:
        """float: returns the power consumption in amps."""
        return self._electric_current

    @property
    def remaining_time(self) -> Optional[str]:
        """str: Returns the time left to auto shutdown."""
        return self._remaining_time

    @property
    def auto_shutdown(self) -> str:
        """str: Returns the auto-shutdown configuration value."""
        return self._auto_shutdown

    @property
    def last_data_update(self) -> datetime:
        """datetime: Returns timestamp of the last update."""
        return self._last_data_update
