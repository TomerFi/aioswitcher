"""Switcher water heater unofficial API and bridge, Device classes.

.. codeauthor:: Tomer Figenblat <tomer.figenblat@gmail.com>

"""

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
      phone_id: the phone id retrieved from the device.
      device_password: the password retrieved from the device.
      last_state_change: datetime of the last state change.

    Attributes:
      auto_off_set(str): returns the auto-off configuration value.
      device_id(str): returns the device id.
      device_password(str): returns the device password.
      electric_current(float): returns the power consumption in amps.
      ip_addr(str): returns the ip address.
      last_data_update(datetime): returns the timestamp of the last update received.
      last_state_change(datetime): returns the timestamp of the last state change.
      mac_addr(str): returns the mac address.
      name(str): returns the device name.
      phone_id(str): returns the phone id.
      power_consumption(int):  returns the power consumption in watts.
      remaining_time(Optional[str]): returns the time left to auto shutdown.
      state(str): returns the device state (on/off).

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
        phone_id: str,
        device_password: str,
        last_state_change: datetime,
    ) -> None:
        """Initialize the Switcher V2 Device."""
        self._device_id = device_id
        self._mac_addr = mac_address
        self._phone_id = phone_id
        self._device_password = device_password
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
        """Returns the device id."""
        return self._device_id

    @property
    def ip_addr(self) -> str:
        """Returns the ip address."""
        return self._ip_address

    @property
    def mac_addr(self) -> str:
        """Returns the mac address."""
        return self._mac_addr

    @property
    def name(self) -> str:
        """Returns the device name."""
        return self._name

    @property
    def state(self) -> str:
        """Returns the device state (on/off)."""
        return self._state

    @property
    def remaining_time(self) -> Optional[str]:
        """Returns the time left to auto shutdown."""
        return self._remaining_time

    @property
    def auto_off_set(self) -> str:
        """Returns the auto-off configuration value."""
        return self._auto_off_set

    @property
    def power_consumption(self) -> int:
        """Returns the power consumption in watts."""
        return self._power_consumption

    @property
    def electric_current(self) -> float:
        """Returns the power consumption in amps."""
        return self._electric_current

    @property
    def phone_id(self) -> str:
        """Returns the phone id."""
        return self._phone_id

    @property
    def device_password(self) -> str:
        """Returns the device password."""
        return self._device_password

    @property
    def last_data_update(self) -> datetime:
        """Returns the timestamp of the last update received."""
        return self._last_data_update

    @property
    def last_state_change(self) -> datetime:
        """Returns the timestamp of the last state change."""
        return self._last_state_change

    def as_dict(self):
        """
        Returns:
          A dictionary represntation of the object properties, used to make
          the object json serializable.

        """
        return self.__dict__
