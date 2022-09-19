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

"""Switcher integration TCP socket API module."""

from abc import ABC
from asyncio import open_connection
from binascii import unhexlify
from datetime import timedelta
from enum import Enum, unique
from logging import getLogger
from socket import AF_INET
from types import TracebackType
from typing import Optional, Set, Tuple, Type, final

from ..device import (
    DeviceCategory,
    DeviceState,
    DeviceType,
    ThermostatFanLevel,
    ThermostatMode,
    ThermostatSwing,
)
from ..device.tools import (
    current_timestamp_to_hexadecimal,
    minutes_to_hexadecimal_seconds,
    set_message_length,
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
    SwitcherShutterStateResponse,
    SwitcherStateResponse,
    SwitcherThermostatStateResponse,
)
from .remotes import SwitcherBreezeRemote

logger = getLogger(__name__)

# Type 1 devices: Heaters (v2, touch, v4, Heater), Plug
SWITCHER_TCP_PORT_TYPE1 = 9957
# Type 2 devices: Breeze, Runners
SWITCHER_TCP_PORT_TYPE2 = 10000

SWITCHER_DEVICE_TO_TCP_PORT = {
    DeviceCategory.THERMOSTAT: SWITCHER_TCP_PORT_TYPE2,
    DeviceCategory.SHUTTER: SWITCHER_TCP_PORT_TYPE2,
    DeviceCategory.WATER_HEATER: SWITCHER_TCP_PORT_TYPE1,
    DeviceCategory.POWER_PLUG: SWITCHER_TCP_PORT_TYPE1,
}


@unique
class Command(Enum):
    """Enum for turning the device on or off."""

    ON = "1"
    OFF = "0"


class SwitcherApi(ABC):
    """Switcher TCP based API.

    Args:
        ip_address: the ip address assigned to the device.
        device_id: the id of the desired device.
        port: the port of the device, default is 9957.

    """

    def __init__(
        self, ip_address: str, device_id: str, port: int = SWITCHER_TCP_PORT_TYPE1
    ) -> None:
        """Initialize the Switcher TCP connection API."""
        self._ip_address = ip_address
        self._device_id = device_id
        self._port = port
        self._connected = False

    @property
    def connected(self) -> bool:
        """Return true if api is connected."""
        return self._connected

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
        logger.info("connecting to the switcher device")
        self._reader, self._writer = await open_connection(
            host=self._ip_address,
            port=self._port,
            family=AF_INET,
        )

        self._connected = True
        logger.info("switcher device connected")

    async def disconnect(self) -> None:
        """Disconnect from asynchronous socket."""
        if hasattr(self, "_writer") and self._writer:
            logger.info("disconnecting from the switcher device")
            self._writer.close()
            await self._writer.wait_closed()
        else:
            logger.info("switcher device not connected")
        self._connected = False

    async def _login(
        self, device_type: DeviceType = None
    ) -> Tuple[str, SwitcherLoginResponse]:
        """Use for sending the login packet to the device.

        Returns:
            A tuple of the hex timestamp and an instance of ``SwitcherLoginResponse``.

        Note:
            This is a private function used by other functions, do not call this
            function directly.

        """
        timestamp = current_timestamp_to_hexadecimal()
        if (
            device_type
            and device_type == DeviceType.BREEZE
            or device_type == DeviceType.RUNNER
            or device_type == DeviceType.RUNNER_MINI
        ):
            packet = packets.LOGIN2_PACKET_TYPE2.format(timestamp, self._device_id)
        else:
            packet = packets.LOGIN_PACKET_TYPE1.format(timestamp)
        signed_packet = sign_packet_with_crc_key(packet)

        logger.debug("sending a login packet")
        self._writer.write(unhexlify(signed_packet))
        response = await self._reader.read(1024)
        return timestamp, SwitcherLoginResponse(response)

    async def stop(self) -> SwitcherBaseResponse:
        """Use for stopping the shutter.

        Returns:
            An instance of ``SwitcherBaseResponse``.
        """
        logger.debug("about to send stop shutter command")
        timestamp, login_resp = await self._login(DeviceType.RUNNER)
        if not login_resp.successful:
            logger.error("Failed to log into device with id %s", self._device_id)
            raise RuntimeError("login request was not successful")

        logger.debug(
            "logged in session_id=%s, timestamp=%s", login_resp.session_id, timestamp
        )

        packet = packets.RUNNER_STOP_COMMAND.format(
            login_resp.session_id, timestamp, self._device_id
        )

        packet = set_message_length(packet)
        signed_packet = sign_packet_with_crc_key(packet)

        logger.debug("sending a stop control packet")

        self._writer.write(unhexlify(signed_packet))
        response = await self._reader.read(1024)
        return SwitcherBaseResponse(response)

    async def get_state(self) -> SwitcherStateResponse:
        """Use for sending the get state packet to the device.

        Returns:
            An instance of ``SwitcherStateResponse``.
        """
        raise NotImplementedError

    async def get_breeze_state(self) -> SwitcherThermostatStateResponse:
        """Use for sending the get state packet to the Breeze device.

        Returns:
            An instance of ``SwitcherThermostatStateResponse``.

        """
        raise NotImplementedError

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
        raise NotImplementedError

    async def control_breeze_device(
        self,
        remote: SwitcherBreezeRemote,
        state: DeviceState = None,
        mode: ThermostatMode = None,
        target_temp: int = 0,
        fan_level: ThermostatFanLevel = None,
        swing: ThermostatSwing = None,
    ) -> SwitcherBaseResponse:
        """Use for sending the control packet to the Breeze device.

        Args:
            remote: the remote for the breeze device
            state: the desired state of the device
            mode: the desired mode of the device
            target_temp: the target temperature
            fan_level: the desired fan level
            swing: the desired swing state

        Returns:
            An instance of ``SwitcherBaseResponse``.

        """
        raise NotImplementedError

    async def set_position(self, position: int = 0) -> SwitcherBaseResponse:
        """Use for setting the shutter position of the Runner and Runner Mini devices.

        Args:
            position: the position to set the device to, default to 0.

        Returns:
            An instance of ``SwitcherBaseResponse``.

        """
        raise NotImplementedError

    async def set_device_name(self, name: str) -> SwitcherBaseResponse:
        """Use for sending the set name packet to the device.

        Args:
            name: string name with the length of 2 >= x >= 32.

        Returns:
            An instance of ``SwitcherBaseResponse``.

        """
        raise NotImplementedError

    async def set_auto_shutdown(self, full_time: timedelta) -> SwitcherBaseResponse:
        """Use for sending the set auto-off packet to the device.

        Args:
            full_time: timedelta value containing the configuration value for
                auto-shutdown.

        Returns:
            An instance of ``SwitcherBaseResponse``.

        """
        raise NotImplementedError

    async def get_schedules(self) -> SwitcherGetSchedulesResponse:
        """Use for retrieval of the schedules from the device.

        Returns:
            An instance of ``SwitcherGetSchedulesResponse``.

        """
        raise NotImplementedError

    async def delete_schedule(self, schedule_id: str) -> SwitcherBaseResponse:
        """Use for deleting a schedule from the device.

        Use ``get_schedules`` to retrieve the schedule instance.

        Args:
            schedule_id: the identification of the schedule for deletion.

        Returns:
            An instance of ``SwitcherBaseResponse``.

        """
        raise NotImplementedError

    async def create_schedule(
        self, start_time: str, end_time: str, days: Set[Days] = set()
    ) -> SwitcherBaseResponse:
        """Use for creating a new schedule in the next empty schedule slot.

        Args:
            start_time: a string start time in %H:%M format. e.g. 13:00.
            end_time: a string start time in %H:%M format. e.g. 13:00.
            days: for recurring schedules, add ``Days``.

        Returns:
            An instance of ``SwitcherBaseResponse``.

        """
        raise NotImplementedError


@final
class SwitcherType1Api(SwitcherApi):
    """Switcher Type1 devices (Plug, V2, Touch, V4) TCP based API.

    Args:
        ip_address: the ip address assigned to the device.
        device_id: the id of the desired device.
    """

    def __init__(self, ip_address: str, device_id: str) -> None:
        """Initialize the Switcher TCP connection API."""
        super().__init__(ip_address, device_id, SWITCHER_TCP_PORT_TYPE1)

    async def get_state(self) -> SwitcherStateResponse:
        """Use for sending the get state packet to the device.

        Returns:
            An instance of ``SwitcherStateResponse``.
        """
        timestamp, login_resp = await self._login()
        if login_resp.successful:
            packet = packets.GET_STATE_PACKET_TYPE1.format(
                login_resp.session_id, timestamp, self._device_id
            )
            signed_packet = sign_packet_with_crc_key(packet)

            logger.debug("sending a get state packet")
            self._writer.write(unhexlify(signed_packet))
            state_resp = await self._reader.read(1024)
            try:
                response = SwitcherStateResponse(state_resp)
                if response.successful:
                    return response
            except (KeyError, ValueError) as ve:
                raise RuntimeError("get state request was not successful") from ve
        raise RuntimeError("login request was not successful")

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
        timestamp, login_resp = await self._login()
        timer = (
            minutes_to_hexadecimal_seconds(minutes)
            if minutes > 0
            else packets.NO_TIMER_REQUESTED
        )
        packet = packets.SEND_CONTROL_PACKET.format(
            login_resp.session_id,
            timestamp,
            self._device_id,
            command.value,
            timer,
        )
        signed_packet = sign_packet_with_crc_key(packet)

        logger.debug("sending a control packet")
        self._writer.write(unhexlify(signed_packet))
        response = await self._reader.read(1024)
        return SwitcherBaseResponse(response)

    async def set_auto_shutdown(self, full_time: timedelta) -> SwitcherBaseResponse:
        """Use for sending the set auto-off packet to the device.

        Args:
            full_time: timedelta value containing the configuration value for
                auto-shutdown.

        Returns:
            An instance of ``SwitcherBaseResponse``.

        """
        timestamp, login_resp = await self._login()
        auto_shutdown = timedelta_to_hexadecimal_seconds(full_time)
        packet = packets.SET_AUTO_OFF_SET_PACKET.format(
            login_resp.session_id,
            timestamp,
            self._device_id,
            auto_shutdown,
        )
        signed_packet = sign_packet_with_crc_key(packet)

        logger.debug("sending a set auto shutdown packet")
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
        timestamp, login_resp = await self._login()
        device_name = string_to_hexadecimale_device_name(name)
        packet = packets.UPDATE_DEVICE_NAME_PACKET.format(
            login_resp.session_id,
            timestamp,
            self._device_id,
            device_name,
        )
        signed_packet = sign_packet_with_crc_key(packet)

        logger.debug("sending a set name packet")
        self._writer.write(unhexlify(signed_packet))
        response = await self._reader.read(1024)
        return SwitcherBaseResponse(response)

    async def get_schedules(self) -> SwitcherGetSchedulesResponse:
        """Use for retrieval of the schedules from the device.

        Returns:
            An instance of ``SwitcherGetSchedulesResponse``.

        """
        timestamp, login_resp = await self._login()
        packet = packets.GET_SCHEDULES_PACKET.format(
            login_resp.session_id,
            timestamp,
            self._device_id,
        )
        signed_packet = sign_packet_with_crc_key(packet)

        logger.debug("sending a get schedules packet")
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
        timestamp, login_resp = await self._login()
        packet = packets.DELETE_SCHEDULE_PACKET.format(
            login_resp.session_id, timestamp, self._device_id, schedule_id
        )
        signed_packet = sign_packet_with_crc_key(packet)

        logger.debug("sending a delete schedule packet")
        self._writer.write(unhexlify(signed_packet))
        response = await self._reader.read(1024)
        return SwitcherBaseResponse(response)

    async def create_schedule(
        self, start_time: str, end_time: str, days: Set[Days] = set()
    ) -> SwitcherBaseResponse:
        """Use for creating a new schedule in the next empty schedule slot.

        Args:
            start_time: a string start time in %H:%M format. e.g. 13:00.
            end_time: a string start time in %H:%M format. e.g. 13:00.
            days: for recurring schedules, add ``Days``.

        Returns:
            An instance of ``SwitcherBaseResponse``.

        """
        timestamp, login_resp = await self._login()

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
            login_resp.session_id,
            timestamp,
            self._device_id,
            new_schedule,
        )
        signed_packet = sign_packet_with_crc_key(packet)

        logger.debug("sending a create schedule packet")
        self._writer.write(unhexlify(signed_packet))
        response = await self._reader.read(1024)
        return SwitcherBaseResponse(response)


@final
class SwitcherType2Api(SwitcherApi):
    """Switcher Type2 devices (Breeze, Runners) TCP based API.

    Args:
        ip_address: the ip address assigned to the device.
        device_id: the id of the desired device.
    """

    def __init__(self, ip_address: str, device_id: str) -> None:
        """Initialize the Switcher TCP connection API."""
        super().__init__(ip_address, device_id, SWITCHER_TCP_PORT_TYPE2)

    async def control_breeze_device(
        self,
        remote: SwitcherBreezeRemote,
        state: DeviceState = None,
        mode: ThermostatMode = None,
        target_temp: int = 0,
        fan_level: ThermostatFanLevel = None,
        swing: ThermostatSwing = None,
    ) -> SwitcherBaseResponse:
        """Use for sending the control packet to the Breeze device.

        Args:
            remote: the remote for the breeze device
            state: optionally the desired state of the device
            mode: optionally the desired mode of the device
            target_temp: optionally the target temperature
            fan_level: optionally the desired fan level
            swing: optionally the desired swing state

        Returns:
            An instance of ``SwitcherBaseResponse``.

        """
        timestamp, login_resp = await self._login(DeviceType.BREEZE)
        if not login_resp.successful:
            logger.error("Failed to log into device id %s", self._device_id)
            raise RuntimeError("login request was not successful")

        logger.debug(
            "logged in session_id=%s, timestamp=%s", login_resp.session_id, timestamp
        )

        if (
            state
            or mode
            or target_temp
            or fan_level
            or (swing and not remote._separated_swing_command)
        ):
            current_state = await self.get_breeze_state()
            if not current_state.successful:
                raise RuntimeError("get state request was not successful")

            logger.debug("got current breeze device state")

            if remote._separated_swing_command:
                set_swing = ThermostatSwing.OFF
            else:
                set_swing = swing or current_state.swing

            command = remote.build_command(
                state or current_state.state,
                mode or current_state.mode,
                target_temp or current_state.target_temperature,
                fan_level or current_state.fan_level,
                set_swing,
            )

            packet = packets.BREEZE_COMMAND_PACKET.format(
                login_resp.session_id,
                timestamp,
                self._device_id,
                command.length,
                command.command,
            )

            packet = set_message_length(packet)
            signed_packet = sign_packet_with_crc_key(packet)

            logger.debug("sending a control packet")

            self._writer.write(unhexlify(signed_packet))
            response = await self._reader.read(1024)
            cmd_response = SwitcherBaseResponse(response)

            if not cmd_response.successful:
                raise RuntimeError("set state request was not successful")

        if remote._separated_swing_command and swing:
            # if device is SPECIAL SWING device and user requested a swing change
            return await self._control_breeze_swing_device(
                timestamp, login_resp.session_id, remote, swing
            )

        return cmd_response

    async def _control_breeze_swing_device(
        self,
        timestamp: str,
        session_id: str,
        remote: SwitcherBreezeRemote,
        swing: ThermostatSwing,
    ) -> SwitcherBaseResponse:
        """Use for sending the control packet to the Breeze device.

        Args:
            timestamp: the timestamp from the login response
            session_id: the session_id from the login response
            remote: the remote for the breeze device
            swing: the desired swing state

        Returns:
            An instance of ``SwitcherBaseResponse``.

        """
        logger.debug("about to send Breeze special swing command")
        command = remote.build_swing_command(swing)
        packet = packets.BREEZE_COMMAND_PACKET.format(
            session_id,
            timestamp,
            self._device_id,
            command.length,
            command.command,
        )

        packet = set_message_length(packet)
        signed_packet = sign_packet_with_crc_key(packet)

        logger.debug("sending a control packet")

        self._writer.write(unhexlify(signed_packet))
        response = await self._reader.read(1024)
        return SwitcherBaseResponse(response)

    async def set_position(self, position: int = 0) -> SwitcherBaseResponse:
        """Use for setting the shutter position of the Runner and Runner Mini devices.

        Args:
            position: the position to set the device to, default to 0.

        Returns:
            An instance of ``SwitcherBaseResponse``.

        """
        hex_pos = "{0:0{1}x}".format(position, 2)

        logger.debug("about to send set position command")
        timestamp, login_resp = await self._login(DeviceType.RUNNER)
        if not login_resp.successful:
            logger.error("Failed to log into device with id %s", self._device_id)
            raise RuntimeError("login request was not successful")

        logger.debug(
            "logged in session_id=%s, timestamp=%s", login_resp.session_id, timestamp
        )

        packet = packets.RUNNER_SET_POSITION.format(
            login_resp.session_id, timestamp, self._device_id, hex_pos
        )

        packet = set_message_length(packet)
        signed_packet = sign_packet_with_crc_key(packet)

        logger.debug("sending a control packet")

        self._writer.write(unhexlify(signed_packet))
        response = await self._reader.read(1024)
        return SwitcherBaseResponse(response)

    async def get_breeze_state(self) -> SwitcherThermostatStateResponse:
        """Use for sending the get state packet to the Breeze device.

        Returns:
            An instance of ``SwitcherThermostatStateResponse``.

        """
        timestamp, login_resp = await self._login(DeviceType.BREEZE)
        if login_resp.successful:

            packet = packets.GET_STATE_PACKET2_TYPE2.format(
                login_resp.session_id, timestamp, self._device_id
            )

            signed_packet = sign_packet_with_crc_key(packet)

            logger.debug("sending a get state packet")
            self._writer.write(unhexlify(signed_packet))
            state_resp = await self._reader.read(1024)
            try:
                response = SwitcherThermostatStateResponse(state_resp)
                if response.successful:
                    return response
            except (KeyError, ValueError) as ve:
                raise RuntimeError(
                    "get breeze state request was not successful"
                ) from ve
        raise RuntimeError("login request was not successful")

    async def get_shutter_state(self) -> SwitcherShutterStateResponse:
        """Use for sending the get state packet to the Runner device.

        Returns:
            An instance of ``SwitcherShutterStateResponse``.

        """
        timestamp, login_resp = await self._login(DeviceType.RUNNER)
        if login_resp.successful:

            packet = packets.GET_STATE_PACKET2_TYPE2.format(
                login_resp.session_id, timestamp, self._device_id
            )

            signed_packet = sign_packet_with_crc_key(packet)

            logger.debug("sending a get state packet")
            self._writer.write(unhexlify(signed_packet))
            state_resp = await self._reader.read(1024)
            try:
                response = SwitcherShutterStateResponse(state_resp)
                if response.successful:
                    return response
            except (KeyError, ValueError) as ve:
                raise RuntimeError(
                    "get shutter state request was not successful"
                ) from ve
        raise RuntimeError("login request was not successful")
