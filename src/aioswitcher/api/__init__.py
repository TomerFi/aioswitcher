"""Switcher Manager API Functions."""

from asyncio import AbstractEventLoop, Event, open_connection, wait
from binascii import unhexlify
from datetime import timedelta
from socket import AF_INET
from types import TracebackType
from typing import TYPE_CHECKING, Optional, Tuple, Type

from ..consts import NO_TIMER_REQUESTED, REMOTE_SESSION_ID, SOCKET_PORT
from ..tools import (convert_minutes_to_timer, convert_string_to_device_name,
                     convert_timedelta_to_auto_off,
                     crc_sign_full_packet_com_key, get_timestamp)
from . import messages, packets

if TYPE_CHECKING:
    from asyncio import StreamReader, StreamWriter


class SwitcherV2Api():
    """Represntation of the Switcher API."""

    def __init__(self, loop: AbstractEventLoop, ip_addr: str, phone_id: str,
                 device_id: str, device_password: str) -> None:
        """Initialize the Switcher V2 API."""
        self._loop = loop
        self._ip_addr = ip_addr
        self._phone_id = phone_id
        self._device_id = device_id
        self._device_password = device_password
        self._reader = None  # type: Optional[StreamReader]
        self._writer = None  # type: Optional[StreamWriter]
        self._connected_evt = Event()

    async def __aenter__(self) -> 'SwitcherV2Api':
        """Enter SwitcherV2Api context manager."""
        await self.connect()
        return await self.__await__()

    async def __await__(self) -> 'SwitcherV2Api':
        """Return SwitcherV2Api awaitable object."""
        return self

    async def __aexit__(self, exc_type: Optional[Type[BaseException]],
                        exc_value: Optional[BaseException],
                        traceback: Optional[TracebackType]) -> None:
        """Exit SwitcherV2Api context manager."""
        return await self.disconnect()

    async def connect(self) -> None:
        """Connect to socket."""
        self._reader, self._writer = await open_connection(
            host=self._ip_addr, port=SOCKET_PORT, loop=self._loop,
            family=AF_INET)

        self._connected_evt.set()
        return None

    async def disconnect(self) -> None:
        """Disconnect from socket."""
        if self._writer:
            self._writer.close()
        self._connected_evt.clear()
        return None

    async def _full_login(self) \
            -> Tuple[str, Optional[messages.SwitcherV2LoginResponseMSG]]:
        """Use for sending the login packet to the device."""
        timestamp = await get_timestamp(self._loop)

        packet = packets.LOGIN_PACKET.format(
            REMOTE_SESSION_ID, timestamp,
            self._phone_id, self._device_password)

        signed_packet = await crc_sign_full_packet_com_key(self._loop, packet)

        if self._writer and self._reader:
            self._writer.write(unhexlify(signed_packet))

            response = await self._reader.read(1024)

            return timestamp, messages.SwitcherV2LoginResponseMSG(
                self._loop, response)

        return timestamp, None

    async def login(self) -> Optional[messages.SwitcherV2LoginResponseMSG]:
        """Use as wrapper for sending the login packet to the device."""
        full_login_tuple = await self._full_login()
        return full_login_tuple[1]

    async def _full_get_state(self) \
            -> Tuple[str, Optional[messages.SwitcherV2LoginResponseMSG],
                     Optional[messages.SwitcherV2StateResponseMSG]]:
        """Use for sending the get state packet to the device."""
        timestamp, login_response = await self._full_login()

        if login_response and login_response.successful:
            packet = packets.GET_STATE_PACKET.format(
                login_response.session_id, timestamp, self._device_id)

            signed_packet = await crc_sign_full_packet_com_key(
                self._loop, packet)

            if self._writer and self._reader:
                self._writer.write(unhexlify(signed_packet))

                response = await self._reader.read(1024)

                state_response = messages.SwitcherV2StateResponseMSG(
                    self._loop, response)
                await wait([state_response.init_future])
                return (timestamp, login_response, state_response)

        return timestamp, login_response, None

    async def get_state(self) -> Optional[messages.SwitcherV2StateResponseMSG]:
        """Use as wrapper for sending the get state packet to the device."""
        full_state_tuple = await self._full_get_state()
        return full_state_tuple[2]

    async def control_device(self, command: str, timer: Optional[str] = None) \
            -> Optional[messages.SwitcherV2ControlResponseMSG]:
        """Use for sending the control packet to the device."""
        timestamp, login_response, get_state_response = \
            await self._full_get_state()

        if (login_response
                and login_response.successful
                and get_state_response
                and get_state_response.successful):

            if timer:
                minutes_timer = await convert_minutes_to_timer(
                    self._loop, timer)
            else:
                minutes_timer = NO_TIMER_REQUESTED

            packet = packets.SEND_CONTROL_PACKET.format(
                login_response.session_id,
                timestamp,
                self._device_id,
                self._phone_id,
                self._device_password,
                command,
                minutes_timer)

            signed_packet = await crc_sign_full_packet_com_key(
                self._loop, packet)

            if self._writer and self._reader:
                self._writer.write(unhexlify(signed_packet))

                response = await self._reader.read(1024)

                return messages.SwitcherV2ControlResponseMSG(
                    self._loop, response)

        return None

    async def set_auto_shutdown(self, full_time: timedelta) \
            -> Optional[messages.SwitcherV2SetAutoOffResponseMSG]:
        """Use for sending the set auto-off packet to the device."""
        timestamp, login_response, get_state_response = \
            await self._full_get_state()

        if (login_response
                and login_response.successful
                and get_state_response
                and get_state_response.successful):
            auto_off = await convert_timedelta_to_auto_off(
                self._loop, full_time)

            packet = packets.SET_AUTO_OFF_SET_PACKET.format(
                login_response.session_id,
                timestamp,
                self._device_id,
                self._phone_id,
                self._device_password,
                auto_off)

            signed_packet = await crc_sign_full_packet_com_key(
                self._loop, packet)

            if self._writer and self._reader:
                self._writer.write(unhexlify(signed_packet))

                response = await self._reader.read(1024)

                return messages.SwitcherV2SetAutoOffResponseMSG(
                    self._loop, response)

        return None

    async def set_device_name(self, name: str) \
            -> Optional[messages.SwitcherV2UpdateNameResponseMSG]:
        """Use for sending the set name packet to the device."""
        timestamp, login_response, get_state_response = \
            await self._full_get_state()

        if (login_response
                and login_response.successful
                and get_state_response
                and get_state_response.successful):
            device_name = await convert_string_to_device_name(self._loop, name)

            packet = packets.UPDATE_DEVICE_NAME_PACKET.format(
                login_response.session_id,
                timestamp,
                self._device_id,
                self._phone_id,
                self._device_password,
                device_name)

            signed_packet = await crc_sign_full_packet_com_key(
                self._loop, packet)

            if self._writer and self._reader:
                self._writer.write(unhexlify(signed_packet))

                response = await self._reader.read(1024)

                return messages.SwitcherV2UpdateNameResponseMSG(
                    self._loop, response)

        return None

    async def get_schedules(self) -> \
            Optional[messages.SwitcherV2GetScheduleResponseMSG]:
        """Use for retrival of the schedules from the device."""
        timestamp, login_response, get_state_response = \
            await self._full_get_state()

        if (login_response
                and login_response.successful
                and get_state_response
                and get_state_response.successful):
            packet = packets.GET_SCHEDULES_PACKET.format(
                login_response.session_id,
                timestamp,
                self._device_id,
                self._phone_id,
                self._device_password)

            signed_packet = await crc_sign_full_packet_com_key(
                self._loop, packet)

            if self._writer and self._reader:
                self._writer.write(unhexlify(signed_packet))

                response = await self._reader.read(1024)

                return messages.SwitcherV2GetScheduleResponseMSG(
                    self._loop, response)

        return None

    async def disable_enable_schedule(self, schedule_data: str) \
            -> Optional[messages.SwitcherV2DisableEnableScheduleResponseMSG]:
        """Use for disabling or enabling a schedule on the device."""
        timestamp, login_response, get_state_response = \
            await self._full_get_state()

        if (login_response
                and login_response.successful
                and get_state_response
                and get_state_response.successful):
            packet = packets.DISABLE_ENABLE_SCHEDULE_PACKET.format(
                login_response.session_id,
                timestamp,
                self._device_id,
                self._phone_id,
                self._device_password,
                schedule_data)

            signed_packet = await crc_sign_full_packet_com_key(
                self._loop, packet)

            if self._writer and self._reader:
                self._writer.write(unhexlify(signed_packet))

                response = await self._reader.read(1024)

                return messages.SwitcherV2DisableEnableScheduleResponseMSG(
                    self._loop, response)

        return None

    async def delete_schedule(self, schedule_id: str) \
            -> Optional[messages.SwitcherV2DeleteScheduleResponseMSG]:
        """Use for deleting a schedule from the device."""
        timestamp, login_response, get_state_response = \
            await self._full_get_state()
        if (login_response
                and login_response.successful
                and get_state_response
                and get_state_response.successful):
            packet = packets.DELETE_SCHEDULE_PACKET.format(
                login_response.session_id,
                timestamp,
                self._device_id,
                self._phone_id,
                self._device_password,
                schedule_id)

            signed_packet = await crc_sign_full_packet_com_key(
                self._loop, packet)

            if self._writer and self._reader:
                self._writer.write(unhexlify(signed_packet))

                response = await self._reader.read(1024)

                return messages.SwitcherV2DeleteScheduleResponseMSG(
                    self._loop, response)

        return None

    async def create_schedule(self, schedule_data: str) \
            -> Optional[messages.SwitcherV2CreateScheduleResponseMSG]:
        """Use for deleting a schedule from the device."""
        timestamp, login_response, get_state_response = \
            await self._full_get_state()

        if (login_response
                and login_response.successful
                and get_state_response
                and get_state_response.successful):
            packet = packets.CREATE_SCHEDULE_PACKET.format(
                login_response.session_id,
                timestamp,
                self._device_id,
                self._phone_id,
                self._device_password,
                schedule_data)

            signed_packet = await crc_sign_full_packet_com_key(
                self._loop, packet)

            if self._writer and self._reader:
                self._writer.write(unhexlify(signed_packet))

                response = await self._reader.read(1024)

                return messages.SwitcherV2CreateScheduleResponseMSG(
                    self._loop, response)

        return None

    @property
    def connected(self) -> bool:
        """Return true if api is connected."""
        return self._connected_evt.is_set()
