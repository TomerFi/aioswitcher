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

"""Switcher unofficial integration, UDP Bridge module."""

from asyncio import BaseTransport, DatagramProtocol, get_running_loop
from binascii import hexlify
from dataclasses import dataclass
from functools import partial
from logging import critical, debug, error, info
from socket import AF_INET, inet_ntoa
from struct import pack
from types import TracebackType
from typing import Any, Callable, Optional, Tuple, Type
from warnings import warn

from .device import (
    DeviceCategory,
    DeviceState,
    DeviceType,
    SwitcherBase,
    SwitcherPowerPlug,
    SwitcherWaterHeater,
)
from .device.tools import seconds_to_iso_time, watts_to_amps

__all__ = ["SwitcherBridge"]


def _parse_device_from_datagram(
    device_callback: Callable[[SwitcherBase], Any], datagram: bytes
) -> None:
    """Use as callback function to be called for every broadcast message.

    Will create devices and send to the on_device callback.

    Args:
        device_callback: callable for sending SwitcherBase devices parsed from message.
        broadcast_message: the bytes message to parse.

    """
    parser = DatagramParser(datagram)
    if not parser.is_switcher_originator():
        error("received datagram from an unknown source")
    else:
        device_type = parser.get_device_type()
        device_state = parser.get_device_state()
        if device_state == DeviceState.ON:
            power_consumption = parser.get_power_consumption()
            electric_current = watts_to_amps(power_consumption)
        else:
            power_consumption = 0
            electric_current = 0.0

        if device_type and device_type.category == DeviceCategory.WATER_HEATER:
            debug("discovered a water heater switcher device")
            device_callback(
                SwitcherWaterHeater(
                    device_type,
                    device_state,
                    parser.get_device_id(),
                    parser.get_ip(),
                    parser.get_mac(),
                    parser.get_name(),
                    power_consumption,
                    electric_current,
                    (
                        parser.get_remaining()
                        if device_state == DeviceState.ON
                        else "00:00:00"
                    ),
                    parser.get_auto_shutdown(),
                )
            )

        elif device_type and device_type.category == DeviceCategory.POWER_PLUG:
            debug("discovered a power plug switcher device")
            device_callback(
                SwitcherPowerPlug(
                    device_type,
                    device_state,
                    parser.get_device_id(),
                    parser.get_ip(),
                    parser.get_mac(),
                    parser.get_name(),
                    power_consumption,
                    electric_current,
                )
            )
        else:
            warn("discovered an unknown switcher device")


class SwitcherBridge:
    """Use for running a UDP client for bridging Switcher devices broadcast messages.

    Args:
        on_device: a callable to which every new SwitcherBase device found will be send.

    """

    def __init__(
        self, on_device: Callable[[SwitcherBase], Any], broadcast_port: int = 20002
    ) -> None:
        """Initialize the switcher bridge."""
        self._on_device = on_device
        self._broadcast_port = broadcast_port
        self._is_running = False
        self._transport = None  # type: Optional[BaseTransport]

    async def __aenter__(self) -> "SwitcherBridge":
        """Enter SwitcherBridge asynchronous context manager."""
        await self.start()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Exit the SwitcherBridge asynchronous context manager."""
        await self.stop()

    async def start(self) -> None:
        """Create an asynchronous listenr and start the bridge event."""
        info("starting the udp bridge")
        protocol_factory = UdpClientProtocol(
            partial(_parse_device_from_datagram, self._on_device)
        )
        transport, protocol = await get_running_loop().create_datagram_endpoint(
            lambda: protocol_factory,
            local_addr=("0.0.0.0", self._broadcast_port),  # nosec
            family=AF_INET,
        )

        self._is_running = True
        info("udp bridge started")
        self._transport = transport
        return None

    async def stop(self) -> None:
        """Stop the asynchronous bridge."""
        if self._transport and not self._transport.is_closing():
            info("stopping the udp bridge")
            self._transport.close()
        else:
            info("udp bridge not started")
        self._is_running = False
        return None

    @property
    def is_running(self) -> bool:
        """bool: Return true if bridge is running."""
        return self._is_running


class UdpClientProtocol(DatagramProtocol):
    """Implementation of the Asyncio UDP DatagramProtocol."""

    def __init__(self, on_datagram: Callable[[bytes], None]) -> None:
        """Initialize the protocol."""
        self.transport = None  # type: Optional[BaseTransport]
        self._on_datagram = on_datagram

    def connection_made(self, transport: BaseTransport) -> None:
        """Call on connection established."""
        self.transport = transport

    def datagram_received(self, data: bytes, addr: Tuple) -> None:
        """Call on datagram recieved."""
        self._on_datagram(data)

    def error_received(self, exc: Optional[Exception]) -> None:
        """Call on exception recieved."""
        if exc:
            error(f"udp client received error {exc}")
        else:
            warn("udp client received error")

    def connection_lost(self, exc: Optional[Exception]) -> None:
        """Call on connection lost."""
        if exc:
            critical(f"udp bridge lost its connection {exc}")
        else:
            info("udp connection stopped")


@dataclass(frozen=True)
class DatagramParser:
    """Utility class for parsing a datagram into various device properties."""

    message: bytes

    def is_switcher_originator(self) -> bool:
        """Verify the broadcast message had originated from a switcher device."""
        return (
            hexlify(self.message)[0:4].decode() == "fef0" and len(self.message) == 165
        )

    def get_ip(self) -> str:
        """Extract the IP address from the broadcast message."""
        hex_ip = hexlify(self.message)[152:160]
        ip_addr = int(hex_ip[6:8] + hex_ip[4:6] + hex_ip[2:4] + hex_ip[0:2], 16)
        return inet_ntoa(pack("<L", ip_addr))

    def get_mac(self) -> str:
        """Extract the MAC address from the broadcast message."""
        hex_mac = hexlify(self.message)[160:172].decode().upper()
        return (
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

    def get_name(self) -> str:
        """Extract the device name from the braodcast message."""
        return self.message[42:74].decode().rstrip("\x00")

    def get_device_id(self) -> str:
        """Extract the device id from the broadcast message."""
        return hexlify(self.message)[36:42].decode()

    def get_device_state(self) -> DeviceState:
        """Extract the device state from the broadcast message."""
        hex_device_state = hexlify(self.message)[266:270].decode()
        return (
            DeviceState.ON
            if hex_device_state == DeviceState.ON.value
            else DeviceState.OFF
        )

    def get_auto_shutdown(self) -> str:
        """Extract the auto shutdown value from the broadcast message."""
        hex_auto_shutdown_val = hexlify(self.message)[310:318]
        int_auto_shutdown_val_secs = int(
            hex_auto_shutdown_val[6:8]
            + hex_auto_shutdown_val[4:6]
            + hex_auto_shutdown_val[2:4]
            + hex_auto_shutdown_val[0:2],
            16,
        )
        return seconds_to_iso_time(int_auto_shutdown_val_secs)

    def get_power_consumption(self) -> int:
        """Extract the power consumption from the broadcast message."""
        hex_power_consumption = hexlify(self.message)[270:278]
        return int(hex_power_consumption[2:4] + hex_power_consumption[0:2], 16)

    def get_remaining(self) -> str:
        """Extract the time remains for the current execution."""
        hex_remaining_time = hexlify(self.message)[294:302]
        int_remaining_time_seconds = int(
            hex_remaining_time[6:8]
            + hex_remaining_time[4:6]
            + hex_remaining_time[2:4]
            + hex_remaining_time[0:2],
            16,
        )
        return seconds_to_iso_time(int_remaining_time_seconds)

    def get_device_type(self) -> DeviceType:
        """Extract the device type from the broadcast message."""
        hex_model = hexlify(self.message[75:76]).decode()
        devices = dict(map(lambda d: (d.hex_rep, d), DeviceType))
        return devices[hex_model]
