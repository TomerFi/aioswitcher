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

"""Switcher unofficial integration TCP socket API module."""

from asyncio import open_connection
from binascii import unhexlify
from datetime import timedelta
from enum import Enum, unique
from logging import debug, info
from socket import AF_INET
from types import TracebackType
from typing import Optional, Set, Tuple, Type

from ..device.tools import (
    current_timestamp_to_hexadecimal,
    minutes_to_hexadecimal_seconds,
    sign_packet_with_crc_key,
    string_to_hexadecimale_device_name,
    timedelta_to_hexadecimal_seconds,
)
from ..schedule import Days
from ..schedule.tools import time_to_hexadecimal_timestamp, weekdays_to_hexadecimal
from . import packets
from .messages import (
    SwitcherBaseResponse,
    SwitcherGetSchedulesResponse,
    SwitcherLoginResponse,
    SwitcherStateResponse,
)


@unique
class Command(Enum):
    """Enum for turning the device on or off."""

    ON = "1"
    OFF = "0"


class SwitcherApi:
    """Switcher TCP based API.

    Args:
        ip_address: the ip address assigned to the device.
        device_id: the id of the desired device.
        port: the port of the device, default is 9957.

    """

    def __init__(self, ip_address: str, device_id: str, port: int = 9957) -> None:
        """Initialize the Switcher TCP connection API."""
        self._ip_address = ip_address
        self._device_id = device_id
        self._port = port
        self._connected = False

    async def __aenter__(self) -> "SwitcherApi":
        """Enter SwitcherApi asynchronous context manager.

        Returns:
            This instance of ``aioswitcher.api.SwitcherApi``.

        """
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Exit SwitcherApi asynchronous context manager."""
        await self.disconnect()

    async def connect(self) -> None:
        """Connect to asynchronous socket and get reader and writer object."""
        info("connecting to the switcher device")
        self._reader, self._writer = await open_connection(
            host=self._ip_address,
            port=self._port,
            family=AF_INET,
        )

        self._connected = True
        info("switcher device connected")

    async def disconnect(self) -> None:
        """Disconnect from asynchronous socket."""
        if hasattr(self, "_writer") and self._writer:
            info("disconnecting from the switcher device")
            self._writer.close()
            await self._writer.wait_closed()
        else:
            info("switcher device not connected")
        self._connected = False

    @property
    def connected(self) -> bool:
        """Return true if api is connected."""
        return self._connected

    async def _login(self) -> Tuple[str, SwitcherLoginResponse]:
        """Use for sending the login packet to the device.

        Returns:
            A tuple of the hex timestamp and an instance of ``SwitcherLoginResponse``.

        Note:
            This is a private function used by other functions, do not call this
            function directly.

        """
        timestamp = current_timestamp_to_hexadecimal()
        packet = packets.LOGIN_PACKET.format(timestamp)
        signed_packet = sign_packet_with_crc_key(packet)

        debug("sending a login packet")
        self._writer.write(unhexlify(signed_packet))
        response = await self._reader.read(1024)
        return timestamp, SwitcherLoginResponse(response)

    async def _get_full_state(self) -> Tuple[str, str, SwitcherStateResponse]:
        """Use for sending the get state packet to the device.

        Will return extra information needed for other packets.

        Returns:
            A tuple of the hex timestamp, session id and an instance of
            ``SwitcherStateResponse``.

        Note:
            This is a private function, please use get_state instead.

        """
        timestamp, login_resp = await self._login()
        if login_resp.successful:
            packet = packets.GET_STATE_PACKET.format(
                login_resp.session_id, timestamp, self._device_id
            )
            signed_packet = sign_packet_with_crc_key(packet)

            debug("sending a get state packet")
            self._writer.write(unhexlify(signed_packet))
            state_resp = await self._reader.read(1024)
            try:
                response = SwitcherStateResponse(state_resp)
                if response.successful:
                    return timestamp, login_resp.session_id, response
            except (KeyError, ValueError) as ve:
                raise RuntimeError("get state request was not successful") from ve
        raise RuntimeError("login request was not successful")

    async def get_state(self) -> SwitcherStateResponse:
        """Use for sending the get state packet to the device.

        Returns:
            An instance of ``SwitcherStateResponse``.

        """
        _, _, state_response = await self._get_full_state()
        return state_response

    async def control_device(
        self, command: Command, minutes: int = 0
    ) -> SwitcherBaseResponse:
        """Use for sending the control packet to the device.

        Args:
            command: use the ``aioswitcher.api.Command`` enum.
            minutes: if turning-on optionally incorporate a timer.

        Returns:
            An instance of ``SwitcherBaseResponse``.

        """
        timestamp, session_id, _ = await self._get_full_state()
        timer = (
            minutes_to_hexadecimal_seconds(minutes)
            if minutes > 0
            else packets.NO_TIMER_REQUESTED
        )
        packet = packets.SEND_CONTROL_PACKET.format(
            session_id,
            timestamp,
            self._device_id,
            command.value,
            timer,
        )
        signed_packet = sign_packet_with_crc_key(packet)

        debug("sending a control packet")
        self._writer.write(unhexlify(signed_packet))
        response = await self._reader.read(1024)
        return SwitcherBaseResponse(response)

    async def set_auto_shutdown(self, full_time: timedelta) -> SwitcherBaseResponse:
        """Use for sending the set auto-off packet to the device.

        Args:
            full_time: timedelta value containg the configuration value for
            auto-shutdown.

        Returns:
            An instance of ``SwitcherBaseResponse``.

        """
        timestamp, session_id, _ = await self._get_full_state()
        auto_shutdown = timedelta_to_hexadecimal_seconds(full_time)
        packet = packets.SET_AUTO_OFF_SET_PACKET.format(
            session_id,
            timestamp,
            self._device_id,
            auto_shutdown,
        )
        signed_packet = sign_packet_with_crc_key(packet)

        debug("sending a set auto shutdown packet")
        self._writer.write(unhexlify(signed_packet))
        response = await self._reader.read(1024)
        return SwitcherBaseResponse(response)

    async def set_device_name(self, name: str) -> SwitcherBaseResponse:
        """Use for sending the set name packet to the device.

        Args:
            name: string name with the length of 2 >= x >= 32.

        Returns:
            An instance of ``SwitcherBaseResponse``.

        """
        timestamp, session_id, _ = await self._get_full_state()
        device_name = string_to_hexadecimale_device_name(name)
        packet = packets.UPDATE_DEVICE_NAME_PACKET.format(
            session_id,
            timestamp,
            self._device_id,
            device_name,
        )
        signed_packet = sign_packet_with_crc_key(packet)

        debug("sending a set name packet")
        self._writer.write(unhexlify(signed_packet))
        response = await self._reader.read(1024)
        return SwitcherBaseResponse(response)

    async def get_schedules(self) -> SwitcherGetSchedulesResponse:
        """Use for retrival of the schedules from the device.

        Returns:
            An instance of ``SwitcherGetSchedulesResponse``.

        """
        timestamp, session_id, _ = await self._get_full_state()
        packet = packets.GET_SCHEDULES_PACKET.format(
            session_id,
            timestamp,
            self._device_id,
        )
        signed_packet = sign_packet_with_crc_key(packet)

        debug("sending a get schedules packet")
        self._writer.write(unhexlify(signed_packet))
        response = await self._reader.read(1024)
        return SwitcherGetSchedulesResponse(response)

    async def delete_schedule(self, schedule_id: str) -> SwitcherBaseResponse:
        """Use for deleting a schedule from the device.

        Use ``get_schedules`` to retrieve the schedule instance.

        Args:
            schedule_id: the identification of the schedule for deletion.

        Returns:
            An instance of ``SwitcherBaseResponse``.

        """
        timestamp, session_id, _ = await self._get_full_state()
        packet = packets.DELETE_SCHEDULE_PACKET.format(
            session_id, timestamp, self._device_id, schedule_id
        )
        signed_packet = sign_packet_with_crc_key(packet)

        debug("sending a delete schedule packet")
        self._writer.write(unhexlify(signed_packet))
        response = await self._reader.read(1024)
        return SwitcherBaseResponse(response)

    async def create_schedule(
        self, start_time: str, end_time: str, days: Set[Days] = set()
    ) -> SwitcherBaseResponse:
        """Use for creating a new schedule in the next empty schedule slot.

        Args:
            start_time: a string start time in %H:%M formst. e.g. 13:00.
            end_time: a string start time in %H:%M formst. e.g. 13:00.
            days: for recurring schedules, add ``Days``.

        Returns:
            An instance of ``SwitcherBaseResponse``.

        """
        timestamp, session_id, _ = await self._get_full_state()

        start_time_hex = time_to_hexadecimal_timestamp(start_time)
        end_time_hex = time_to_hexadecimal_timestamp(end_time)
        weekdays = (
            weekdays_to_hexadecimal(days)
            if len(days) > 0
            else packets.NON_RECURRING_SCHEDULE
        )
        new_schedule = packets.SCHEDULE_CREATE_DATA_FORMAT.format(
            weekdays, start_time_hex, end_time_hex
        )
        packet = packets.CREATE_SCHEDULE_PACKET.format(
            session_id,
            timestamp,
            self._device_id,
            new_schedule,
        )
        signed_packet = sign_packet_with_crc_key(packet)

        debug("sending a create schedule packet")
        self._writer.write(unhexlify(signed_packet))
        response = await self._reader.read(1024)
        return SwitcherBaseResponse(response)
