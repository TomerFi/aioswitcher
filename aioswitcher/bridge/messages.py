"""Switcher Bridge Response Messages."""

from asyncio import AbstractEventLoop, ensure_future, Future
from binascii import hexlify
from socket import inet_ntoa
from struct import pack
from typing import Optional, Union

from ..consts import (ENCODING_CODEC, STATE_OFF, STATE_ON,
                      STATE_RESPONSE_ON, WAITING_TEXT)
from ..tools import convert_seconds_to_iso_time


class SwitcherV2BroadcastMSG():
    """represntation of the switcherv2 broadcast message."""

    def __init__(self,
                 loop: AbstractEventLoop,
                 message: Union[bytes, str]) -> None:
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
        fixed_msg = message \
            if isinstance(message, bytes) \
            else message.encode(ENCODING_CODEC)
        ensure_future(self.initialize(fixed_msg), loop=loop)

    async def initialize(self, message: bytes) -> None:
        """Finish the initialization of the broadcast message."""
        try:
            self._verified = (
                hexlify(message)[0:4].decode(ENCODING_CODEC) == 'fef0'
                and len(message) == 165)
            if self._verified:
                temp_ip = hexlify(message)[152:160]
                ip_addr = int(temp_ip[6:8] + temp_ip[4:6]
                              + temp_ip[2:4] + temp_ip[0:2], 16)
                self._ip_address = inet_ntoa(pack("<L", ip_addr))

                mac = (
                    hexlify(message)[160:172]
                    .decode(ENCODING_CODEC).upper())
                self._mac_address = (
                    mac[0:2] + ':' + mac[2:4] + ':' + mac[4:6] + ':'
                    + mac[6:8] + ':' + mac[8:10] + ':' + mac[10:12])

                self._name = (
                    message[42:74].decode(ENCODING_CODEC).rstrip('\x00'))

                self._device_id = (
                    hexlify(message)[36:42].decode(ENCODING_CODEC))

                self._device_state = (
                    STATE_ON if hexlify(message)[266:270]
                    .decode(ENCODING_CODEC) == STATE_RESPONSE_ON
                    else STATE_OFF)

                temp_auto_off_set = hexlify(message)[310:318]
                temp_auto_off_set_seconds = int(temp_auto_off_set[6:8]
                                                + temp_auto_off_set[4:6]
                                                + temp_auto_off_set[2:4]
                                                + temp_auto_off_set[0:2], 16)
                self._auto_off_set = await convert_seconds_to_iso_time(
                    self._loop,
                    temp_auto_off_set_seconds)

                if self._device_state == STATE_ON:
                    temp_power = hexlify(message)[270:278]
                    self._power_consumption = int(temp_power[2:4]
                                                  + temp_power[0:2], 16)
                    self._electric_current = round((
                        self._power_consumption / float(220)), 1)

                    temp_remaining_time = hexlify(message)[294:302]
                    temp_remaining_time_seconds = int(
                        temp_remaining_time[6:8]
                        + temp_remaining_time[4:6]
                        + temp_remaining_time[2:4]
                        + temp_remaining_time[0:2], 16)
                    self._remaining_time_to_off = \
                        await convert_seconds_to_iso_time(
                            self._loop,
                            temp_remaining_time_seconds)

            self._validated = True
            self.init_future.set_result(self)
        except (ValueError, IndexError, RuntimeError) as ex:
            self.init_future.set_exception(ex)
        return None

    @property
    def verified(self) -> bool:
        """Return rather or not the message is a switcher v2 message."""
        return self._verified if self._validated else self._validated

    @property
    def ip_address(self) -> str:
        """Return the ip address."""
        return self._ip_address

    @property
    def mac_address(self) -> str:
        """Return the mac address."""
        return self._mac_address

    @property
    def name(self) -> str:
        """Return the device name."""
        return self._name

    @property
    def device_id(self) -> str:
        """Return the device id."""
        return self._device_id

    @property
    def device_state(self) -> str:
        """Return the state of the device."""
        return self._device_state

    @property
    def remaining_time_to_off(self) -> Optional[str]:
        """Return the time left to auto-off."""
        return self._remaining_time_to_off

    @property
    def auto_off_set(self) -> str:
        """Return the auto-off configuration value."""
        return self._auto_off_set

    @property
    def power(self) -> int:
        """Return the power consumptionin watts."""
        return self._power_consumption

    @property
    def current(self) -> float:
        """Return the power consumptionin amps."""
        return self._electric_current

    @property
    def init_future(self) -> Future:
        """Return the future of the device initialization."""
        return self._init_future
