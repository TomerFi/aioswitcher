"""Switcher water heater unofficial API and bridge, Bridge Object.

.. codeauthor:: Tomer Figenblat <tomer.figenblat@gmail.com>

"""

from asyncio import AbstractEventLoop, Event, Queue
from functools import partial
from socket import AF_INET
from types import TracebackType
from typing import TYPE_CHECKING, Optional, Type

from ..protocols import SwitcherV2UdpProtocolFactory

if TYPE_CHECKING:
    from ..devices import SwitcherV2Device

SOCKET_BIND_TUP = ("0.0.0.0", 20002)  # nosec


class SwitcherV2Bridge:
    """Represntation of the SwitcherV2 Bridge object.

    Args:
      loop: the event loop for the factory to run in.
      device_id: the id of the desired device.

    Todo:
      * replace ``queue`` attribute with ``get_queue`` method.

    """

    def __init__(
        self,
        loop: AbstractEventLoop,
        device_id: str,
    ) -> None:
        """Initialize the switcherv2 bridge."""
        self._loop = loop
        self._device_id = device_id

        self._device = None  # type: Optional[SwitcherV2Device]
        self._running_evt = Event()
        self._queue = Queue(maxsize=1)  # type: Queue

    async def __aenter__(self) -> "SwitcherV2Bridge":
        """Enter SwitcherV2Bridge asynchronous context manager.

        Returns:
          This instance of ``aioswitcher.bridge.SwitcherV2Bridge`` as an
          awaitable.

        """
        await self.start()
        return await self.__await__()

    async def __await__(self) -> "SwitcherV2Bridge":
        """Return SwitcherV2Bridge awaitable object.

        Returns:
          This instance of ``aioswitcher.bridge.SwitcherV2Bridge``.

        """
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Exit the SwitcherV2Bridge asynchronous context manager."""
        return await self.stop()

    async def start(self) -> None:
        """Create an asynchronous listenr and start the bridge event."""
        await self._loop.create_datagram_endpoint(
            partial(
                SwitcherV2UdpProtocolFactory,
                *[
                    self._loop,
                    self._device_id,
                    self.queue,
                    self._running_evt,
                ],
            ),
            local_addr=SOCKET_BIND_TUP,
            family=AF_INET,
        )

        self._running_evt.set()
        return None

    async def stop(self) -> None:
        """Stop the asynchronous bridge."""
        self._running_evt.clear()
        return None

    @property
    def running(self) -> bool:
        """bool: Return true if bridge is running."""
        return self._running_evt.is_set()

    @property
    def queue(self) -> Queue:
        """asyncio.Queue: Return the queue storing updated device objects."""
        return self._queue
