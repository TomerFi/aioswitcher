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

"""Switcher smart switch unofficial API and bridge, Device classes."""

from datetime import datetime
from typing import Optional


class SwitcherV2Device:
    """Represntation of the switcherv2 device.

    Args:
      device_id: the id retrieved from the device.
      ip_address: the ip address assigned to the device.
      mac_address: the mac address assigned to the device.
      name: the name of the device.
      state: the current state of the device (in/off).
      remaining_time: remaining time (if on).
      auto_off_set: configured value for auto shutdown.
      power_consumption: the current power consumpstion in watts.
      electric_current: the current power consumpstion in amps.
      last_state_change: datetime of the last state change.

    """

    def __init__(
        self,
        device_id: str,
        ip_address: str,
        mac_address: str,
        name: str,
        state: str,
        remaining_time: Optional[str],
        auto_off_set: str,
        power_consumption: int,
        electric_current: float,
        last_state_change: datetime,
    ) -> None:
        """Initialize the Switcher V2 Device."""
        self._device_id = device_id
        self._mac_addr = mac_address
        self.update_device_data(
            ip_address,
            name,
            state,
            remaining_time,
            auto_off_set,
            power_consumption,
            electric_current,
            last_state_change,
        )

    def update_device_data(
        self,
        ip_address: str,
        name: str,
        state: str,
        remaining_time: Optional[str],
        auto_off_set: str,
        power_consumption: int,
        electric_current: float,
        last_state_change: datetime,
    ) -> None:
        """Update the device state and data.

        Args:
          ip_address: the ip address assigned to the device.
          name: the name of the device.
          state: the current state of the device (on/off).
          remaining_time: remaining time (if on).
          auto_off_set: configured value for auto shutdown.
          power_consumption: the current power consumpstion in watts.
          electric_current: the current power consumpstion in amps.
          last_state_change: datetime of the last state change.

        """
        self._ip_address = ip_address
        self._name = name
        self._state = state
        self._remaining_time = remaining_time
        self._auto_off_set = auto_off_set
        self._power_consumption = power_consumption
        self._electric_current = electric_current
        self._last_data_update = datetime.now()
        self._last_state_change = last_state_change

    @property
    def device_id(self) -> str:
        """str: Returns the device id."""
        return self._device_id

    @property
    def ip_addr(self) -> str:
        """str: Returns the ip address."""
        return self._ip_address

    @property
    def mac_addr(self) -> str:
        """str: Returns the mac address."""
        return self._mac_addr

    @property
    def name(self) -> str:
        """str: Returns the device name."""
        return self._name

    @property
    def state(self) -> str:
        """str: Returns the device state."""
        return self._state

    @property
    def remaining_time(self) -> Optional[str]:
        """str: Returns the time left to auto shutdown."""
        return self._remaining_time

    @property
    def auto_off_set(self) -> str:
        """str: Returns the auto-off configuration value."""
        return self._auto_off_set

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

    @property
    def last_state_change(self) -> datetime:
        """datetime: Returns timestamp of the last state change."""
        return self._last_state_change

    def as_dict(self):
        """Return as dict.

        Returns:
          A dictionary represntation of the object properties.
          Used to make the object json serializable.


        """
        return self.__dict__
