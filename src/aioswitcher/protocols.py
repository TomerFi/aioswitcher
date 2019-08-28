"""Switcher water heater unofficial API and bridge, Network protocols.

.. codeauthor:: Tomer Figenblat <tomer.figenblat@gmail.com>

"""

# fmt: off
from asyncio import (
    AbstractEventLoop, BaseTransport, DatagramProtocol, Event, Future, Queue,
    QueueEmpty, QueueFull, Transport, ensure_future)
from datetime import datetime
from functools import partial
from typing import Optional, Tuple, Union, cast

from .bridge.messages import SwitcherV2BroadcastMSG
from .devices import SwitcherV2Device

# fmt: on


class SwitcherV2UdpProtocolFactory(DatagramProtocol):
    """Represntation of the Asyncio UDP protocol factory.

    Args:
      loop: the event loop for the factory to run in.
      phone_id: the phone id of the desired device.
      device_id: the id of the desired device.
      device_password: the password of the desired device.
      queue: a ``asyncio.Queue`` for the factory to save messages in.
      run_factory_evt ``asyncio.Event`` for signaling the factory to run.

    Todo:
      * replace ``factory_future`` attribute with ``get_factory_future``
        method.

    """

    def __init__(
        self,
        loop: AbstractEventLoop,
        phone_id: str,
        device_id: str,
        device_password: str,
        queue: Queue,
        run_factory_evt: Event,
    ) -> None:
        """Initialize the protocol."""
        self._loop = loop
        self._phone_id = phone_id
        self._device_id = device_id
        self._device_password = device_password
        self._queue = queue
        self._run_factory = run_factory_evt
        self._factory_future = self._loop.create_future()
        self._factory_future.add_done_callback(self.close_transport)
        self._accept_datagrams = Event()
        self.transport = None  # type: Optional[Transport]
        self._device = None  # type: Optional[SwitcherV2Device]

    def connection_made(self, transport: BaseTransport) -> None:
        """Call on connection established."""
        self.transport = cast(Transport, transport)
        self._accept_datagrams.set()

    def datagram_received(self, data: Union[bytes, str], addr: Tuple) -> None:
        """Call on datagram recieved."""
        if self._run_factory.is_set() and self._accept_datagrams.is_set():
            ensure_future(
                self.handle_incoming_messages(data, addr), loop=self._loop
            )

    def error_received(self, exc: Optional[Exception]) -> None:
        """Call on exception recieved."""
        if exc:
            self.factory_future.set_exception(exc)
        else:
            self.factory_future.set_result(None)

    def connection_lost(self, exc: Optional[Exception]) -> None:
        """Call on connection lost."""
        self.factory_future.set_result(exc if exc else None)

    def close_transport(self, future: Future) -> None:
        """Call for closing the transport."""
        if self.transport:
            self.transport.close()

    async def handle_incoming_messages(
        self, data: Union[bytes, str], addr: Tuple
    ) -> None:
        """Use for Handling incoming messages."""
        self._accept_datagrams.clear()
        msg = SwitcherV2BroadcastMSG(self._loop, data)
        msg.init_future.add_done_callback(
            partial(self.get_device_from_message, addr[0])
        )

        return None

    def get_device_from_message(self, ip_addr: str, future: Future) -> None:
        """Use for extracting the device from the broadcast message."""
        msg = future.result()
        if msg.verified:
            if self._device_id == msg.device_id:
                if self._device:
                    # Update known device
                    self._device.update_device_data(
                        ip_addr,
                        msg.name,
                        msg.device_state,
                        msg.remaining_time_to_off,
                        msg.auto_off_set,
                        msg.power,
                        msg.current,
                        (
                            self._device.last_state_change
                            if msg.device_state == self._device.state
                            else datetime.now()
                        ),
                    )
                else:
                    # New device discoverd
                    self._device = SwitcherV2Device(
                        msg.device_id,
                        ip_addr,
                        msg.mac_address,
                        msg.name,
                        msg.device_state,
                        msg.remaining_time_to_off,
                        msg.auto_off_set,
                        msg.power,
                        msg.current,
                        self._phone_id.lower(),
                        self._device_password.lower(),
                        datetime.now(),
                    )
                try:
                    self._queue.put_nowait(self._device)
                except QueueFull:
                    try:
                        self._queue.get_nowait()
                    except QueueEmpty:
                        pass
                    ensure_future(
                        self._queue.put(self._device), loop=self._loop
                    )
        self._accept_datagrams.set()

    @property
    def factory_future(self) -> Future:
        """asyncio.Future: Representing the initialization status."""
        return self._factory_future
