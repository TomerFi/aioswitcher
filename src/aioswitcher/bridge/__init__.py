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

"""Switcher unofficial integration, UDP Bridge."""

from asyncio import BaseTransport, DatagramProtocol, Event, Transport, get_running_loop
from functools import partial
from socket import AF_INET
from types import TracebackType
from typing import Any, Callable, Optional, Tuple, Type, cast

from ..devices import (
    DeviceCategory,
    SwitcherBase,
    SwitcherPowerPlug,
    SwitcherWaterHeater,
)
from .messages import BroadcastMessage

LOCAL_ADDRESS = ("0.0.0.0", 20002)  # nosec


def parse_device_from_message(
    device_callback: Callable[[SwitcherBase], Any], message: BroadcastMessage
) -> None:
    """Use as callback function to be called for every broadcast message.

    Will create devices and send to the on_device callback.

    Args:
        device_callback: callable for sending SwitcherBase devices parsed from message.
        broadcast_message: the BroadcastMessage to parse.

    """
    if message.device_type.category == DeviceCategory.WATER_HEATER:
        device_callback(
            SwitcherWaterHeater(
                message.device_type,
                message.device_state,
                message.device_id,
                message.ip_address,
                message.mac_address,
                message.name,
                message.power_consumption,
                message.electric_current,
                message.remaining_time,
                message.auto_shutdown,
            )
        )

    elif message.device_type.category == DeviceCategory.POWER_PLUG:
        device_callback(
            SwitcherPowerPlug(
                message.device_type,
                message.device_state,
                message.device_id,
                message.ip_address,
                message.mac_address,
                message.name,
                message.power_consumption,
                message.electric_current,
            )
        )


class SwitcherBridge:
    """Represntation of the Switcher Bridge object."""

    def __init__(self, on_device: Callable[[SwitcherBase], Any]) -> None:
        """Initialize the switcher bridge."""
        self._on_device = on_device
        self._bridge_running_evt = Event()

    async def __aenter__(self) -> "SwitcherBridge":
        """Enter SwitcherBridge asynchronous context manager.

        Returns:
            This instance of ``aioswitcher.bridge.SwitcherBridge`` as an awaitable.

        """
        await self.start()
        return await self.__await__()

    async def __await__(self) -> "SwitcherBridge":
        """Return SwitcherBridge awaitable object.

        Returns:
            This instance of ``aioswitcher.bridge.SwitcherBridge``.

        """
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Exit the SwitcherBridge asynchronous context manager."""
        return await self.stop()

    async def start(self) -> None:
        """Create an asynchronous listenr and start the bridge event."""
        await get_running_loop().create_datagram_endpoint(
            lambda: UdpClientProtocol(
                partial(parse_device_from_message, self._on_device)
            ),
            local_addr=LOCAL_ADDRESS,
            family=AF_INET,
        )

        self._bridge_running_evt.set()
        return None

    async def stop(self) -> None:
        """Stop the asynchronous bridge."""
        self._bridge_running_evt.clear()
        return None

    @property
    def is_running(self) -> bool:
        """bool: Return true if bridge is running."""
        return self._bridge_running_evt.is_set()


class UdpClientProtocol(DatagramProtocol):
    """Implementation of the Asyncio UDP DatagramProtocol."""

    def __init__(self, on_datagram: Callable[[BroadcastMessage], None]) -> None:
        """Initialize the protocol."""
        self.transport = None  # type: Optional[Transport]
        self._on_datagram = on_datagram

    def connection_made(self, transport: BaseTransport) -> None:
        """Call on connection established."""
        self.transport = cast(Transport, transport)

    def datagram_received(self, data: bytes, addr: Tuple) -> None:
        """Call on datagram recieved."""
        self._on_datagram(BroadcastMessage(data))

    def error_received(self, exc: Optional[Exception]) -> None:
        """Call on exception recieved."""
        # TODO: replace the following
        print("error_received")

    def connection_lost(self, exc: Optional[Exception]) -> None:
        """Call on connection lost."""
        # TODO: replace the following
        print("connection_lost")
