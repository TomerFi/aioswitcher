"""Switcher API Bridges."""

from asyncio import AbstractEventLoop, Event, Queue
from functools import partial
from socket import AF_INET
from types import TracebackType
from typing import Optional, Type

from ..consts import SOCKET_BIND_TUP
from ..devices import SwitcherV2Device  # noqa F401
from ..protocols import SwitcherV2UdpProtocolFactory


class SwitcherV2Bridge():
    """Represntation of the SwitcherV2 Bridge."""

    def __init__(self, loop: AbstractEventLoop, phone_id: str,
                 device_id: str, device_password: str) -> None:
        """Initialize the switcherv2 bridge."""
        self._loop = loop
        self._phone_id = phone_id
        self._device_id = device_id
        self._device_password = device_password

        self._device = None  # type: Optional[SwitcherV2Device]
        self._running_evt = Event()
        self._queue = Queue(maxsize=1)  # type: Queue

    async def __aenter__(self) -> 'SwitcherV2Bridge':
        """Enter SwitcherV2Bridge context manager."""
        await self.start()
        return await self.__await__()

    async def __await__(self) -> 'SwitcherV2Bridge':
        """Return SwitcherV2Bridge awaitable object."""
        return self

    async def __aexit__(self, exc_type: Optional[Type[BaseException]],
                        exc_value: Optional[BaseException],
                        traceback: Optional[TracebackType]) -> None:
        """Exit SwitcherV2Bridge context manager."""
        return await self.stop()

    async def start(self) -> None:
        """Create the connection and start the bridge."""
        await self._loop.create_datagram_endpoint(
            partial(
                SwitcherV2UdpProtocolFactory,
                *[self._loop, self._phone_id, self._device_id,
                  self._device_password, self.queue, self._running_evt]),
            local_addr=SOCKET_BIND_TUP, family=AF_INET)

        self._running_evt.set()
        return None

    async def stop(self) -> None:
        """Stop the bridge."""
        self._running_evt.clear()
        return None

    @property
    def running(self) -> bool:
        """Return true if bridge is running."""
        return self._running_evt.is_set()

    @property
    def queue(self) -> Queue:
        """Return the queue containing the SwitcherV2 updated device object."""
        return self._queue
