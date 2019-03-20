"""Switcher Devices Represntation Classes."""

from datetime import datetime
from typing import Optional


class SwitcherV2Device:
    """Represntation of the switcherv2 data object."""

    def __init__(self, device_id: str, ip_address: str, mac_address: str,
                 name: str, state: str, remaining_time: Optional[str],
                 auto_off_set: str, power_consumption: int,
                 electric_current: float, phone_id: str,
                 device_password: str, last_state_change: datetime) -> None:
        """Initialize the Switcher V2 Device."""
        self._device_id = device_id
        self._mac_addr = mac_address
        self._phone_id = phone_id
        self._device_password = device_password
        self.update_device_data(ip_address, name, state, remaining_time,
                                auto_off_set, power_consumption,
                                electric_current, last_state_change)

    def update_device_data(self, ip_address: str, name: str, state: str,
                           remaining_time: Optional[str], auto_off_set: str,
                           power_consumption: int, electric_current: float,
                           last_state_change: datetime) -> None:
        """Update device data."""
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
        """Return the device id."""
        return self._device_id

    @property
    def ip_addr(self) -> str:
        """Return the ip address."""
        return self._ip_address

    @property
    def mac_addr(self) -> str:
        """Return the mac address."""
        return self._mac_addr

    @property
    def name(self) -> str:
        """Return the device name."""
        return self._name

    @property
    def state(self) -> str:
        """Return the device state."""
        return self._state

    @property
    def remaining_time(self) -> Optional[str]:
        """Return the time left to auto-off."""
        return self._remaining_time

    @property
    def auto_off_set(self) -> str:
        """Return the auto-off configuration value."""
        return self._auto_off_set

    @property
    def power_consumption(self) -> int:
        """Return the power consumption in watts."""
        return self._power_consumption

    @property
    def electric_current(self) -> float:
        """Return the power consumption in amps."""
        return self._electric_current

    @property
    def phone_id(self) -> str:
        """Return the phone id."""
        return self._phone_id

    @property
    def device_password(self) -> str:
        """Return the device password."""
        return self._device_password

    @property
    def last_data_update(self) -> datetime:
        """Return the timestamp of the last update."""
        return self._last_data_update

    @property
    def last_state_change(self) -> datetime:
        """Return the timestamp of the state change."""
        return self._last_state_change

    def as_dict(self):
        """Make object json serializable."""
        return self.__dict__
