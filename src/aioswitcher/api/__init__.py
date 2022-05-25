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
from binascii import unhexlify, hexlify
from datetime import timedelta
from enum import Enum, unique
from logging import getLogger
from socket import AF_INET
from types import TracebackType
from typing import Optional, Set, Tuple, Type, final
from aiohttp import FormData, ClientSession
import re

from aioswitcher.device import (
    DeviceCategory,
    DeviceType,
    DeviceState,
    SwitcherThermostat,
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
    SwitcherThermostatStateResponse,
    SwitcherGetSchedulesResponse,
    SwitcherLoginResponse,
    SwitcherShutterStateResponse,
    SwitcherStateResponse,
)

logger = getLogger(__name__)

SWITCHER_TCP_PORT2 = 10000
SWITCHER_TCP_PORT = 9957


SWITCHER_DEVICE_TO_TCP_PORT = {
    DeviceCategory.THERMOSTAT: SWITCHER_TCP_PORT2,
    DeviceCategory.SHUTTER: SWITCHER_TCP_PORT2,
    DeviceCategory.WATER_HEATER: SWITCHER_TCP_PORT,
    DeviceCategory.POWER_PLUG: SWITCHER_TCP_PORT,
}


@unique
class Command(Enum):
    """Enum for turning the device on or off."""

    ON = "1"
    OFF = "0"


@final
class SwitcherBreezeCommand:
    """Representations of the Switcher Breeze command message."""

    def __init__(self, command):
        self.command = command
        self.length = self._get_command_length(command)

    def _get_command_length(self):
        hex = "{:x}".format(int(len(self.command) / 2)).ljust(4, "0")
        return hex


@final
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

    @property
    def connected(self) -> bool:
        """Return true if api is connected."""
        return self._connected

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
            packet = packets.LOGIN2_PACKET.format(timestamp, self._device_id)
        else:
            packet = packets.LOGIN_PACKET.format(timestamp)
        signed_packet = sign_packet_with_crc_key(packet)

        logger.debug("sending a login packet")
        self._writer.write(unhexlify(signed_packet))
        response = await self._reader.read(1024)
        return timestamp, SwitcherLoginResponse(response)

    async def get_state(self, device_type: DeviceType = None) -> SwitcherStateResponse:
        """Use for sending the get state packet to the device.

        Returns:
            An instance of ``SwitcherThermostatStateResponse`` for DeviceType.BREEZE
            An instance of ``SwitcherShutterStateResponse`` for DeviceType.RUNNER
                and DeviceType.RUNNER_MIN
            An instance of ``SwitcherStateResponse`` for the rest of the devices.
        """

        timestamp, login_resp = await self._login(device_type)
        if login_resp.successful:
            if device_type and device_type in [
                DeviceType.BREEZE,
                device_type == DeviceType.RUNNER,
                DeviceType.RUNNER_MINI,
            ]:
                packet = packets.GET_STATE_PACKET2.format(
                    login_resp.session_id, timestamp, self._device_id
                )
            else:
                packet = packets.GET_STATE_PACKET.format(
                    login_resp.session_id, timestamp, self._device_id
                )

            signed_packet = sign_packet_with_crc_key(packet)

            logger.debug("sending a get state packet")
            self._writer.write(unhexlify(signed_packet))
            state_resp = await self._reader.read(1024)
            try:
                if device_type == DeviceType.BREEZE:
                    response = SwitcherThermostatStateResponse(state_resp)

                elif device_type in [DeviceType.RUNNER, DeviceType.RUNNER_MINI]:
                    response = SwitcherShutterStateResponse(state_resp)
                else:
                    response = SwitcherStateResponse(state_resp)
                if response.successful:
                    return response
            except (KeyError, ValueError) as ve:
                raise RuntimeError("get state request was not successful") from ve
        raise RuntimeError("login request was not successful")

    async def get_breeze_state(self) -> SwitcherThermostatStateResponse:
        """Use for sending the get state packet to the Breeze device.

        Returns:
            An instance of ``SwitcherThermostatStateResponse``.

        """
        return await self.get_state(DeviceType.BREEZE)

    async def get_shutter_state(self) -> SwitcherShutterStateResponse:
        """Use for sending the get state packet to the Runner device.

        Returns:
            An instance of ``SwitcherShutterStateResponse``.

        """
        return await self.get_state(DeviceType.RUNNER)

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

    async def control_breeze_device(
        self,
        device: SwitcherThermostat,
        command: SwitcherBreezeCommand,
    ) -> SwitcherBaseResponse:
        """Use for sending the control packet to the Breeze device.

        Args:
            command: use the ``aioswitcher.api.SwitcherBreezeCommand`` class.

        Returns:
            An instance of ``SwitcherBaseResponse``.

        """
        logger.debug("about to send Breeze command")
        timestamp, login_resp = await self._login(DeviceType.BREEZE)
        if not login_resp.successful:
            logger.error(
                "Failed to log into device %s with id %s", device.name, device.device_id
            )
            raise RuntimeError("login request was not successful")

        logger.debug(
            "logged in session_id=%s, timestamp=%s", login_resp.session_id, timestamp
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

    async def download_breeze_remote_ir_set(self) -> dict:
        """Use for downloading the IRSet json data of the Switcher Breeze.

        Returns:
            dictionary representing the IRSet json file

        """
        udp_message = await self.get_state(DeviceType.BREEZE)
        if not udp_message.successful:
            raise RuntimeError("Failed to fetch UDP message for remote")

        logger.debug("Building HTTP Post Request for downloading the IR Set file")
        form = FormData()
        form.add_field("token", "d41d8cd98f00b204e9800998ecf8427e")
        form.add_field("rtps", hexlify(udp_message.unparsed_response).decode())
        async with ClientSession() as session:
            async with session.post(
                "https://switcher.co.il/misc/irGet/getIR.php", data=form
            ) as resp:
                if resp.status == 200:
                    logger.debug(
                        "IR Set file succesfully downloaded from Switcher (length=%s)",
                        resp.content_length,
                    )
                    return await resp.json(content_type=None)
                else:
                    raise RuntimeError(
                        f"Failed to Download the IR set file for {self._device_id}"
                    )

    async def set_position(self, position: int = 0) -> SwitcherBaseResponse:
        """Use for setting the shutter position of the Runner and Runner Mini devices.

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

    async def stop(self) -> SwitcherBaseResponse:
        """Use for stopping the shutter from being rolled for the Runner and Runner Mini devices.

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


class BreezeRemote(object):
    """
    Class that represent a remote for a Breeze device/s.
    """
    COMMAND_TO_MODE = {
        "aa": ThermostatMode.AUTO,
        "ad": ThermostatMode.DRY,
        "aw": ThermostatMode.FAN,
        "ar": ThermostatMode.COOL,
        "ah": ThermostatMode.HEAT,
    }

    MODE_TO_COMMAND = {
        ThermostatMode.AUTO: "aa",
        ThermostatMode.DRY: "ad",
        ThermostatMode.FAN: "aw",
        ThermostatMode.COOL: "ar",
        ThermostatMode.HEAT: "ah",
    }

    COMMAND_TO_FAN_LEVEL = {
        "f0": ThermostatFanLevel.AUTO,
        "f1": ThermostatFanLevel.LOW,
        "f2": ThermostatFanLevel.MEDIUM,
        "f3": ThermostatFanLevel.HIGH,
    }

    FAN_LEVEL_TO_COMMAND = {
        ThermostatFanLevel.AUTO: "f0",
        ThermostatFanLevel.LOW: "f1",
        ThermostatFanLevel.MEDIUM: "f2",
        ThermostatFanLevel.HIGH: "f3",
    }

    def __init__(self, ir_set: dict) -> None:
        """
        Initiliaze the remote by parsing the ir_set data
        """
        self.cap_min_temp = 100
        self.cap_max_temp = -100
        self.cap_swingable = False
        self.cap_fan_levels = set()
        self.cap_modes = set()
        self.on_off_type = False
        self.remote_id = ["IRSetID"]
        self.brand = ir_set["BrandName"]
        self._ir_wave_map = {}
        self._resolve_capabilities(ir_set)

    def _construct_breeze_key(
        self,
        mode: ThermostatMode,
        target_temp: int,
        fan_level: ThermostatFanLevel,
        swing: ThermostatSwing,
    ):
        """
        Construct a command key for a specific command
        """
        command = ""
        command += BreezeRemote.MODE_TO_COMMAND[mode]
        command += str(target_temp)
        if fan_level in self.cap_fan_levels:
            command += "_" + BreezeRemote.FAN_LEVEL_TO_COMMAND[fan_level]

        if self.cap_swingable and not command:
            command += "_d1"

        return command

    def get_command(
        self,
        device: SwitcherThermostat,
        state: DeviceState,
        mode: ThermostatMode,
        target_temp: int,
        fan_level: ThermostatFanLevel,
        swing: ThermostatSwing,
    ) -> SwitcherBreezeCommand:
        """
        Create a command to be sent to the Breeze device.

        Returns:
            Instance of ``SwitcherBreezeCommand``.
        """

        if target_temp > self.cap_max_temp or target_temp < self.cap_min_temp:
            raise RuntimeError(
                f"Invalid temprature, the range is between {self.cap_min_temp} \
                    and {self.cap_max_temp}"
            )

        if mode not in self.cap_modes:
            raise RuntimeError(
                f"Invalid mode, available cap_modes for this device are: \
                    {', '.join(self.cap_modes)}"
            )

        if swing.value == ThermostatSwing.ON and not self.cap_swingable:
            raise RuntimeError("This device doesn't have Swing capability")

        if state == DeviceState.OFF:
            key = "off"

        elif (
            state == DeviceState.ON
            and device.device_state != DeviceState.ON
            and not self.on_off_type
        ):
            key = "on_" + self._construct_breeze_key(
                mode, target_temp, fan_level, swing
            )
        else:
            key = self._construct_breeze_key(mode, target_temp, fan_level, swing)

        try:
            command = (
                self._ir_wave_map[key]["Para"]
                + "|"
                + self._ir_wave_map["off"]["HexCode"]
            )
        except KeyError:
            raise RuntimeError(
                "Failed to locate command for key=%s in IRSet file!", key
            )

        logger.debug("command key=%s", key)
        logger.debug("command=%s", command)
        return SwitcherBreezeCommand(
            "00000000" + hexlify(str(command).encode()).decode()
        )

    def _resolve_capabilities(self, ir_set):
        """
        Parses the ir_set of the rmeote and 
        """

        if ir_set["OnOffType"] == 0:
            self.on_off_type = True

        for wave in ir_set["IRWaveList"]:
            key = wave["Key"]
            try:
                mode = BreezeRemote.COMMAND_TO_MODE[key[0:2]]
                self.cap_modes.add(mode)
            except KeyError:
                pass

            fan_level = re.match(r".+(f\d)", key)
            if fan_level:
                self.cap_fan_levels.add(
                    BreezeRemote.COMMAND_TO_FAN_LEVEL[fan_level.group(1)]
                )

            temp = key[2:4]
            if temp.isdigit():
                temp = int(temp)
                if temp > self.cap_max_temp:
                    self.cap_max_temp = temp
                if temp < self.cap_min_temp:
                    self.cap_min_temp = temp

            self.cap_swingable = not self.cap_swingable and "d1" in key

            self._ir_wave_map[key] = {"Para": wave["Para"], "HexCode": wave["HexCode"]}


class BreezeRemoteManager(object):
    def __init__(self):
        self._remotes_db = {}

    async def get_remote(
        self, device: SwitcherThermostat, api: SwitcherApi
    ) -> BreezeRemote:
        if device.remote_id not in self._remotes_db:
            ir_set = await api.download_breeze_remote_ir_set()
            self._remotes_db[device.remote_id] = BreezeRemote(ir_set)
            logger.debug(
                "Remote %s was downloaded and added to that DB", device.remote_id
            )

        return self._remotes_db[device.remote_id]
