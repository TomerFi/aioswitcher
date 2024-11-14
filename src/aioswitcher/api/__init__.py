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

from asyncio import open_connection
from binascii import unhexlify
from datetime import timedelta
from enum import Enum, unique
from logging import getLogger
from socket import AF_INET
from types import TracebackType
from typing import Optional, Set, Tuple, Type, Union, final

from ..device import (
    DeviceState,
    DeviceType,
    ShutterChildLock,
    ThermostatFanLevel,
    ThermostatMode,
    ThermostatSwing,
)
from ..device.tools import (
    convert_token_to_packet,
    current_timestamp_to_hexadecimal,
    get_light_api_packet_index,
    get_shutter_api_packet_index,
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
    SwitcherLightStateResponse,
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


@unique
class Command(Enum):
    """Enum for turning the device on or off."""

    ON = "1"
    OFF = "0"


@final
class SwitcherApi:
    """Switcher TCP based API.

    Args:
        device_type: the type of the device.
        ip_address: the ip address assigned to the device.
        device_id: the id of the desired device.
        device_key: the login key of the device.

    """

    def __init__(
        self,
        device_type: DeviceType,
        ip_address: str,
        device_id: str,
        device_key: str,
        token: Union[str, None] = None,
    ) -> None:
        """Initialize the Switcher TCP connection API."""
        self._device_type = device_type
        self._ip_address = ip_address
        self._device_id = device_id
        self._device_key = device_key
        self._port = SWITCHER_TCP_PORT_TYPE1
        if device_type.protocol_type == 2:
            self._port = SWITCHER_TCP_PORT_TYPE2
        self._connected = False
        self._token = None
        if self._device_type.token_needed:
            if not token:
                raise RuntimeError("A token is needed but is missing")
            self._token = convert_token_to_packet(str(token))

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

    async def _login(self) -> Tuple[str, SwitcherLoginResponse]:
        """Use for sending the login packet to the device.

        Returns:
            A tuple of the hex timestamp and an instance of ``SwitcherLoginResponse``.

        Note:
            This is a private function used by other functions, do not call this
            function directly.

        """
        timestamp = current_timestamp_to_hexadecimal()
        if bool(self._token):
            packet = packets.LOGIN_TOKEN_PACKET_TYPE2.format(
                self._token, timestamp, self._device_id
            )
        elif (
            self._device_type == DeviceType.BREEZE
            or self._device_type == DeviceType.RUNNER
            or self._device_type == DeviceType.RUNNER_MINI
        ):
            packet = packets.LOGIN_PACKET_TYPE2.format(timestamp, self._device_id)
        else:
            packet = packets.LOGIN_PACKET_TYPE1.format(timestamp, self._device_key)
        signed_packet = sign_packet_with_crc_key(packet)

        logger.debug("sending a login packet")
        self._writer.write(unhexlify(signed_packet))
        response = await self._reader.read(1024)

        if bool(self._token):
            packet = packets.LOGIN2_TOKEN_PACKET_TYPE2.format(
                self._device_id, timestamp, self._token
            )
            signed_packet = sign_packet_with_crc_key(packet)
            logger.debug("sending a login2 packet")
            self._writer.write(unhexlify(signed_packet))
            response = await self._reader.read(1024)
        return timestamp, SwitcherLoginResponse(response)

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

    async def control_breeze_device(
        self,
        remote: SwitcherBreezeRemote,
        state: Union[DeviceState, None] = None,
        mode: Union[ThermostatMode, None] = None,
        target_temp: int = 0,
        fan_level: Union[ThermostatFanLevel, None] = None,
        swing: Union[ThermostatSwing, None] = None,
        update_state: bool = False,
    ) -> SwitcherBaseResponse:
        """Use for sending the control packet to the Breeze device.

        Args:
            remote: the remote for the breeze device
            state: optionally the desired state of the device
            mode: optionally the desired mode of the device
            target_temp: optionally the target temperature
            fan_level: optionally the desired fan level
            swing: optionally the desired swing state
            update_state: update the device state without controlling the device

        Returns:
            An instance of ``SwitcherBaseResponse``.

        """
        timestamp, login_resp = await self._login()
        if not login_resp.successful:
            logger.error("Failed to log into device id %s", self._device_id)
            raise RuntimeError("login request was not successful")

        logger.debug(
            "logged in session_id=%s, timestamp=%s", login_resp.session_id, timestamp
        )

        cmd_response: Union[SwitcherBaseResponse, None] = None
        if (
            state
            or mode
            or target_temp
            or fan_level
            or (swing and not remote._separated_swing_command)
        ):
            current_state = await self._get_breeze_state(timestamp, login_resp)
            if not current_state.successful:
                raise RuntimeError("get state request was not successful")

            logger.debug("got current breeze device state")

            state = state or current_state.state
            mode = mode or current_state.mode
            target_temp = target_temp or current_state.target_temperature
            fan_level = fan_level or current_state.fan_level
            set_swing = swing or current_state.swing
            if remote._separated_swing_command:
                set_swing = ThermostatSwing.OFF
            if update_state:
                packet = packets.BREEZE_UPDATE_STATUS_PACKET.format(
                    login_resp.session_id,
                    timestamp,
                    self._device_id,
                    state.value,
                    mode.value,
                    target_temp,
                    fan_level.value,
                    set_swing.value,
                )
                logger.debug("sending a set status packet")
            else:
                command = remote.build_command(
                    state, mode, target_temp, fan_level, set_swing, current_state.state
                )

                packet = packets.BREEZE_COMMAND_PACKET.format(
                    login_resp.session_id,
                    timestamp,
                    self._device_id,
                    command.length,
                    command.command,
                )
                logger.debug("sending a control packet")

            packet = set_message_length(packet)
            signed_packet = sign_packet_with_crc_key(packet)

            self._writer.write(unhexlify(signed_packet))
            response = await self._reader.read(1024)
            cmd_response = SwitcherBaseResponse(response)

            if not cmd_response.successful:
                raise RuntimeError("set state request was not successful")

        if remote._separated_swing_command and swing and not update_state:
            # if device is SPECIAL SWING device and user requested a swing change
            cmd_response = await self._control_breeze_swing_device(
                timestamp, login_resp.session_id, remote, swing
            )

        if cmd_response:
            return cmd_response
        raise RuntimeError("control breeze device failed")

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

    async def stop_shutter(self, index: int = 0) -> SwitcherBaseResponse:
        """Use for stopping the shutter.

        Args:
            index: which runner to stop position, default to 0.

        Returns:
            An instance of ``SwitcherBaseResponse``.

        """
        index_packet = get_shutter_api_packet_index(self._device_type, index)
        logger.debug("about to send stop shutter command")
        timestamp, login_resp = await self._login()
        if not login_resp.successful:
            logger.error("Failed to log into device with id %s", self._device_id)
            raise RuntimeError("login request was not successful")

        logger.debug(
            "logged in session_id=%s, timestamp=%s", login_resp.session_id, timestamp
        )

        if bool(self._token):
            command = "0000"
            hex_pos = f"0{index_packet}{command}"

            packet = packets.GENERAL_TOKEN_COMMAND.format(
                timestamp,
                self._device_id,
                self._token,
                packets.STOP_SHUTTER_PRECOMMAND,
                hex_pos,
            )
        else:
            packet = packets.RUNNER_STOP_COMMAND.format(
                login_resp.session_id, timestamp, self._device_id
            )

        packet = set_message_length(packet)
        signed_packet = sign_packet_with_crc_key(packet)

        logger.debug("sending a stop control packet")

        self._writer.write(unhexlify(signed_packet))
        response = await self._reader.read(1024)
        return SwitcherBaseResponse(response)

    async def set_position(
        self, position: int = 0, index: int = 0
    ) -> SwitcherBaseResponse:
        """Use for setting the shutter position of the Runners devices.

        Args:
            position: the position to set the device to, default to 0.
            index: which runner to set position, default to 0.

        Returns:
            An instance of ``SwitcherBaseResponse``.

        """
        index_packet = get_shutter_api_packet_index(self._device_type, index)
        hex_pos = "{0:0{1}x}".format(position, 2)

        logger.debug("about to send set position command")
        timestamp, login_resp = await self._login()
        if not login_resp.successful:
            logger.error("Failed to log into device with id %s", self._device_id)
            raise RuntimeError("login request was not successful")

        logger.debug(
            "logged in session_id=%s, timestamp=%s", login_resp.session_id, timestamp
        )

        if bool(self._token):
            hex_pos = f"0{index_packet}{hex_pos}"

            packet = packets.GENERAL_TOKEN_COMMAND.format(
                timestamp,
                self._device_id,
                self._token,
                packets.SET_POSITION_PRECOMMAND,
                hex_pos,
            )
        else:
            packet = packets.RUNNER_SET_POSITION.format(
                login_resp.session_id, timestamp, self._device_id, hex_pos
            )

        packet = set_message_length(packet)
        signed_packet = sign_packet_with_crc_key(packet)

        logger.debug("sending a control packet")

        self._writer.write(unhexlify(signed_packet))
        response = await self._reader.read(1024)
        return SwitcherBaseResponse(response)

    async def set_shutter_child_lock(
        self, command: ShutterChildLock, index: int = 0
    ) -> SwitcherBaseResponse:
        """Use for turn on/off shutter child lock.

        Args:
            command: use the ``aioswitcher.api.ShutterChildLock`` enum.
            index: which shutter child lock to turn on/off, default to 0.

        Returns:
            An instance of ``SwitcherBaseResponse``.

        """
        index_packet = get_shutter_api_packet_index(self._device_type, index)
        hex_pos = f"0{index_packet}{command.value}"

        logger.debug("about to send set shutter child lock command")
        timestamp, login_resp = await self._login()
        if not login_resp.successful:
            logger.error("Failed to log into device with id %s", self._device_id)
            raise RuntimeError("login request was not successful")

        logger.debug(
            "logged in session_id=%s, timestamp=%s", login_resp.session_id, timestamp
        )

        if bool(self._token):
            packet = packets.GENERAL_TOKEN_COMMAND.format(
                timestamp,
                self._device_id,
                self._token,
                packets.SET_CHILD_LOCK_PRECOMMAND,
                hex_pos,
            )
        else:
            packet = packets.RUNNER_SET_CHILD_LOCK.format(
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
        timestamp, login_resp = await self._login()
        if login_resp.successful:
            return await self._get_breeze_state(timestamp, login_resp)
        raise RuntimeError("login request was not successful")

    async def _get_breeze_state(
        self, timestamp: str, login_resp: SwitcherLoginResponse
    ) -> SwitcherThermostatStateResponse:
        packet = packets.GET_STATE_PACKET2_TYPE2.format(
            login_resp.session_id, timestamp, self._device_id
        )

        signed_packet = sign_packet_with_crc_key(packet)

        logger.debug("sending a get state packet")
        self._writer.write(unhexlify(signed_packet))
        state_resp = await self._reader.read(1024)
        try:
            response = SwitcherThermostatStateResponse(state_resp)
            return response
        except (KeyError, ValueError) as ve:
            raise RuntimeError("get breeze state request was not successful") from ve

    async def get_shutter_state(self, index: int = 0) -> SwitcherShutterStateResponse:
        """Use for sending the get state packet to the Runners devices.

        Args:
            index: which runner to set get state, default to 0.

        Returns:
            An instance of ``SwitcherShutterStateResponse``.

        """
        timestamp, login_resp = await self._login()
        if login_resp.successful:
            packet = packets.GET_STATE_PACKET2_TYPE2.format(
                login_resp.session_id, timestamp, self._device_id
            )

            signed_packet = sign_packet_with_crc_key(packet)

            logger.debug("sending a get state packet")
            self._writer.write(unhexlify(signed_packet))
            state_resp = await self._reader.read(1024)
            try:
                response = SwitcherShutterStateResponse(
                    state_resp, self._device_type, index
                )
                return response
            except (KeyError, ValueError) as ve:
                raise RuntimeError(
                    "get shutter state request was not successful"
                ) from ve
        raise RuntimeError("login request was not successful")

    async def get_light_state(self, index: int = 0) -> SwitcherLightStateResponse:
        """Use for sending the get state packet to the Light devices.

        Args:
            index: which light to set get state, default to 0.

        Returns:
            An instance of ``SwitcherLightStateResponse``.

        """
        timestamp, login_resp = await self._login()
        if login_resp.successful:
            packet = packets.GET_STATE_PACKET2_TYPE2.format(
                login_resp.session_id, timestamp, self._device_id
            )

            signed_packet = sign_packet_with_crc_key(packet)

            logger.debug("sending a get state packet")
            self._writer.write(unhexlify(signed_packet))
            state_resp = await self._reader.read(1024)
            try:
                response = SwitcherLightStateResponse(
                    state_resp, self._device_type, index
                )
                return response
            except (KeyError, ValueError) as ve:
                raise RuntimeError("get light state request was not successful") from ve
        raise RuntimeError("login request was not successful")

    async def set_light(
        self, command: DeviceState, index: int = 0
    ) -> SwitcherBaseResponse:
        """Use for turn on/off light.

        Args:
            command: use the ``aioswitcher.api.DeviceState`` enum.
            index: which light to turn on/off, default to 0.

        Returns:
            An instance of ``SwitcherBaseResponse``.

        """
        index_packet = get_light_api_packet_index(self._device_type, index)
        hex_pos = f"0{index_packet}{command.value}"

        logger.debug("about to send set light command")
        timestamp, login_resp = await self._login()
        if not login_resp.successful:
            logger.error("Failed to log into device with id %s", self._device_id)
            raise RuntimeError("login request was not successful")

        logger.debug(
            "logged in session_id=%s, timestamp=%s", login_resp.session_id, timestamp
        )

        if bool(self._token):
            packet = packets.GENERAL_TOKEN_COMMAND.format(
                timestamp,
                self._device_id,
                self._token,
                packets.SET_LIGHT_PRECOMMAND,
                hex_pos,
            )
        else:
            logger.error("Failed to set light device with id %s", self._device_id)
            raise RuntimeError("a token is needed but missing or not valid")

        packet = set_message_length(packet)
        signed_packet = sign_packet_with_crc_key(packet)

        logger.debug("sending a control packet")

        self._writer.write(unhexlify(signed_packet))
        response = await self._reader.read(1024)
        return SwitcherBaseResponse(response)
