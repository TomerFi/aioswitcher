"""Switcher Bridge Response Messages."""

from asyncio import AbstractEventLoop, Future, ensure_future
from binascii import hexlify
from socket import inet_ntoa
from struct import pack
from typing import Optional, Union

from aioswitcher import DeviceState

from ..utils import seconds_to_iso_time

WAITING_TEXT = "waiting_for_data"


class SwitcherV2BroadcastMSG:
    """Represntation of the SwitcherV2 broadcast message.

    Args:
      loop: the event loop to perform actions in.
      message: the raw message from the device.

    Todo:
      * replace ``init_future`` attribute with ``get_init_future`` method.

    """

    def __init__(self, loop: AbstractEventLoop, message: Union[bytes, str]) -> None:
        """Initialize the broadcast message."""
        self._loop = loop
        self._verified = self._validated = False
        self._power_consumption = 0
        self._electric_current = 0.0
        self._ip_address = WAITING_TEXT
        self._mac_address = WAITING_TEXT
        self._name = WAITING_TEXT
        self._device_id = WAITING_TEXT
        self._auto_off_set = WAITING_TEXT
        self._remaining_time_to_off = WAITING_TEXT
        self._init_future = loop.create_future()
        fixed_msg = message if isinstance(message, bytes) else message.encode()
        ensure_future(self.initialize(fixed_msg), loop=loop)

    async def initialize(self, message: bytes) -> None:
        """Finish the initialization and update the future object.

        Args:
          message: the raw message from the device.

        """
        try:
            self._verified = (
                hexlify(message)[0:4].decode() == "fef0" and len(message) == 165
            )
            if self._verified:
                hex_ip = hexlify(message)[152:160]
                ip_addr = int(hex_ip[6:8] + hex_ip[4:6] + hex_ip[2:4] + hex_ip[0:2], 16)
                self._ip_address = inet_ntoa(pack("<L", ip_addr))

                hex_mac = hexlify(message)[160:172].decode().upper()
                self._mac_address = (
                    hex_mac[0:2]
                    + ":"
                    + hex_mac[2:4]
                    + ":"
                    + hex_mac[4:6]
                    + ":"
                    + hex_mac[6:8]
                    + ":"
                    + hex_mac[8:10]
                    + ":"
                    + hex_mac[10:12]
                )

                self._name = message[42:74].decode().rstrip("\x00")

                self._device_id = hexlify(message)[36:42].decode()

                hex_device_state = hexlify(message)[266:270].decode()
                self._device_state = (
                    DeviceState.ON.display
                    if hex_device_state == DeviceState.ON.value
                    else DeviceState.OFF.display
                )

                hex_auto_off_set = hexlify(message)[310:318]
                auto_off_set_seconds = int(
                    hex_auto_off_set[6:8]
                    + hex_auto_off_set[4:6]
                    + hex_auto_off_set[2:4]
                    + hex_auto_off_set[0:2],
                    16,
                )
                self._auto_off_set = seconds_to_iso_time(auto_off_set_seconds)

                if self._device_state == DeviceState.ON.value:
                    hex_power = hexlify(message)[270:278]
                    self._power_consumption = int(hex_power[2:4] + hex_power[0:2], 16)
                    self._electric_current = round(
                        (self._power_consumption / float(220)), 1
                    )

                    hex_remaining_time = hexlify(message)[294:302]
                    remaining_time_seconds = int(
                        hex_remaining_time[6:8]
                        + hex_remaining_time[4:6]
                        + hex_remaining_time[2:4]
                        + hex_remaining_time[0:2],
                        16,
                    )
                    self._remaining_time_to_off = seconds_to_iso_time(
                        remaining_time_seconds
                    )

            self._validated = True
            self.init_future.set_result(self)
        except (ValueError, IndexError, RuntimeError) as ex:
            self.init_future.set_exception(ex)
        return None

    @property
    def verified(self) -> bool:
        """bool: Return whether or not the message is a SwitcherV2 message."""
        return self._verified if self._validated else self._validated

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
    def power(self) -> int:
        """int: Return the power consumptionin watts."""
        return self._power_consumption

    @property
    def device_state(self) -> str:
        """str: Return the state of the device."""
        return self._device_state

    @property
    def remaining_time_to_off(self) -> Optional[str]:
        """str: Return the time left to auto-off."""
        return self._remaining_time_to_off

    @property
    def current(self) -> float:
        """float: Return the power consumptionin amps."""
        return self._electric_current

    @property
    def auto_off_set(self) -> str:
        """str: Return the auto-off configuration value."""
        return self._auto_off_set

    @property
    def init_future(self) -> Future:
        """asyncio.Future: Return the future of the device initialization."""
        return self._init_future
