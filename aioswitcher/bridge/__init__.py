"""Switcher API Bridges."""

from logging import getLogger
from asyncio import AbstractEventLoop, run_coroutine_threadsafe
from socket import socket, AF_INET, SOCK_DGRAM
from datetime import datetime
from traceback import format_exc
from threading import Thread, Event
from typing import TypeVar, Callable, Awaitable, Optional

from aioswitcher.consts import SOCKET_BIND_TUP
from aioswitcher.bridge.messages import SwitcherV2BroadcastMSG
from aioswitcher.devices import SwitcherV2Device

_LOGGER = getLogger(__name__)

T = TypeVar("T")


class SwitcherV2Thread(Thread):
    """represntation of the switcher version 2 connection."""

    # noqa'd flake8's 'E252' (missing whitespace around parameter equals),
    # it contradicts pylint's 'C0326' (bad-whitespace).
    def __init__(self, phone_id: str, device_id: str, device_password: str,
                 initial_callback: Callable, update_callback: Callable,
                 loop: AbstractEventLoop,
                 thread_name: str="SwitcherV2Bridge",  # noqa E252
                 is_daemon: bool=True) -> None:  # noqa E252
        """Initialize the switcherv2 bridge."""
        _LOGGER.debug("initializing the switcherv2 bridge")
        super().__init__(name=thread_name, daemon=is_daemon)

        self._loop = loop
        self._phone_id = phone_id
        self._device_id = device_id
        self._device_password = device_password
        self._initial_callback = initial_callback
        self._update_callback = update_callback
        self._device = None  # type: Optional[SwitcherV2Device]
        self._running_evt = Event()
        self._last_exception_dt = None  # type: Optional[datetime]
        self._exception_count = 0

    def run(self) -> None:
        """Start message loop."""
        try:
            _LOGGER.debug("binding socket")
            tcp_socket = socket(AF_INET, SOCK_DGRAM)
            tcp_socket.bind(SOCKET_BIND_TUP)
            self._running_evt.set()
        except Exception as ex:
            raise Exception("failed to bind tcp socket") from ex

        _LOGGER.debug("starting the switcherv2 bridge")
        while self._running_evt.is_set():
            try:
                raw_msg, address = tcp_socket.recvfrom(1024)
                msg = SwitcherV2BroadcastMSG(raw_msg)

                if msg.verified:
                    if self._device_id == msg.device_id:

                        if self._device is None:
                            # New device disvoverd
                            _LOGGER.debug("found device id " + msg.device_id)

                            self._device = SwitcherV2Device(
                                msg.device_id, address[0], msg.mac_address,
                                msg.name, msg.device_state,
                                msg.remaining_time_to_off, msg.auto_off_set,
                                msg.power, msg.current, self._phone_id.lower(),
                                self._device_password.lower(), datetime.now())

                            run_coroutine_threadsafe(
                                self._initial_callback(self._device),
                                loop=self._loop)

                        else:
                            # Update known device
                            self._device.update_device_data(
                                address[0], msg.name, msg.device_state,
                                msg.remaining_time_to_off, msg.auto_off_set,
                                msg.power, msg.current,
                                (
                                    self._device.last_state_change
                                    if msg.device_state == self._device.state
                                    else datetime.now()
                                ))

                            run_coroutine_threadsafe(
                                self._update_callback(self._device),
                                loop=self._loop)

                    else:
                        if self._exception_count == 0:
                            _LOGGER.error(
                                "device discoverd does not "
                                + "match the provided id")
                        self.check_loop_run()
                else:
                    if self._exception_count == 0:
                        _LOGGER.error(
                            "message not verified as a switcher v2 broadcast")
                    self.check_loop_run()
            except Exception:
                if self._exception_count == 0:
                    _LOGGER.error(format_exc())
                self.check_loop_run()
                continue

    async def check_loop_run(self) -> Optional[Awaitable]:
        """Stop the bridge if too many excption occured.

        (x exception in y minutes).
        """
        # max exceptions allowed in loop before exiting
        max_exceptions_before_stop = 50
        # max minutes to remmember the last excption
        max_minutes_from_last_exception = 1

        current_dt = datetime.now()
        if self._last_exception_dt is not None:
            if (self._last_exception_dt.year == current_dt.year
                    and self._last_exception_dt.month == current_dt.month
                    and self._last_exception_dt.day == current_dt.day):

                calc_dt = current_dt - self._last_exception_dt
                diff = divmod(calc_dt.days * 86400 + calc_dt.seconds, 60)
                if diff[0] > max_minutes_from_last_exception:
                    self._exception_count = 0
                else:
                    self._exception_count += 1
            else:
                self._exception_count = 0
        else:
            self._exception_count = 0

        if not max_exceptions_before_stop > self._exception_count:
            _LOGGER.error("too many excptions, stopping switcherv2 bridge")
            await self.stop()

        self._last_exception_dt = current_dt

        return None

    async def stop(self) -> None:
        """Stop the bridge."""
        _LOGGER.debug("gracefully stopping the switcherv2 bridge")
        self._running_evt.clear()

        return None

    @property
    def running(self) -> bool:
        """Return true if bridge is running."""
        return self._running_evt.is_set()
