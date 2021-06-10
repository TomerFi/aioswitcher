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

"""Switcher unofficial integration, UDP Bridge messages."""

from typing import Optional

from ..bridge import message_parser
from ..devices import DeviceState, DeviceType
from ..errors import NotSwitcherDevice


class BroadcastMessage:
    """Represntation of the broadcast message.

    Args:
        message: the raw bytes message from the device.

    """

    def __init__(self, message: bytes) -> None:
        """Initialize the broadcast message."""
        if not message_parser.is_switcher_originator(message):
            raise NotSwitcherDevice(
                "the message originator cannot be identified as a switcher device"
            )
        self._ip_address = message_parser.get_ip(message)
        self._mac_address = message_parser.get_mac(message)
        self._name = message_parser.get_name(message)
        self._device_id = message_parser.get_device_id(message)
        self._device_state = message_parser.get_device_state(message)
        self._device_type = message_parser.get_device_type(message)
        self._auto_shutdown = message_parser.get_auto_shutdown_value(message)
        if self._device_state == DeviceState.ON:
            self._power_consumption = message_parser.get_power_consumption(message)
            self._electric_current = round((self._power_consumption / float(220)), 1)
            self._remaining_time = message_parser.get_remaining_time(
                message
            )  # type: Optional[str]
        else:
            self._power_consumption = 0
            self._electric_current = 0.0
            self._remaining_time = None

    @property
    def ip_address(self) -> str:
        """str: Return the ip address."""
        return self._ip_address

    @property
    def mac_address(self) -> str:
        """str: Return the mac address."""
        return self._mac_address

    @property
    def name(self) -> str:
        """str: Return the device name."""
        return self._name

    @property
    def device_id(self) -> str:
        """str: Return the device id."""
        return self._device_id

    @property
    def device_state(self) -> DeviceState:
        """str: Return the state of the device."""
        return self._device_state

    @property
    def device_type(self) -> DeviceType:
        """str: Return the type of the device."""
        return self._device_type

    @property
    def power_consumption(self) -> int:
        """int: Return the power consumptionin watts."""
        return self._power_consumption

    @property
    def remaining_time(self) -> Optional[str]:
        """str: Return the time left to auto-off."""
        return self._remaining_time

    @property
    def electric_current(self) -> float:
        """float: Return the power consumptionin amps."""
        return self._electric_current

    @property
    def auto_shutdown(self) -> str:
        """str: Return the auto-off configuration value."""
        return self._auto_shutdown
