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

import re
from asyncio import open_connection
from binascii import hexlify, unhexlify
from datetime import timedelta
from enum import Enum, unique
from json import load
from logging import getLogger
from os import path
from pathlib import Path
from socket import AF_INET
from types import TracebackType
from typing import Dict, Iterable, Mapping, Optional, Set, Tuple, Type, Union, final

from aioswitcher.device import (
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

logger = getLogger(__name__)

BREEZE_REMOTE_DB_FPATH = str(Path(__file__).parent.parent) + "/resources/irset_db.json"

# Type 1 devices: Heaters (v2, touch, v4, Heater), Plug
SWITCHER_TCP_PORT_TYPE1 = 9957
# Type 2 devices: Breeze, Runners
SWITCHER_TCP_PORT_TYPE2 = 10000

# The following are remote IDs (list provided by Switcher) which
# behaves differently in commanding their swing.
# with the following IDs, the swing is transmitted as a separate command.
SPECIAL_SWING_COMMAND_REMOTE_IDS = [
    "ELEC7022",
    "ZM079055",
    "ZM079065",
    "ZM079049",
    "ZM079065",
]

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


@final
class SwitcherBreezeCommand:
    """Representations of the Switcher Breeze command message."""

    def __init__(self, command):
        """Initialize the Breeze command."""
        self.command = command
        self.length = self._get_command_length()

    def _get_command_length(self) -> str:
        """Get command length."""
        return "{:x}".format(int(len(self.command) / 2)).ljust(4, "0")


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
            packet = packets.LOGIN2_PACKET_TYPE2.format(timestamp, self._device_id)
        else:
            packet = packets.LOGIN_PACKET_TYPE1.format(timestamp)
        signed_packet = sign_packet_with_crc_key(packet)

        logger.debug("sending a login packet")
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
            logger.error("Failed to log into device id %s", self._device_id)
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


class BreezeRemote(object):
    """Class that represent a remote for a Breeze device/s."""

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
        """Initiliaze the remote by parsing the ir_set data."""
        self._min_temp = 100  # ridiculously high number
        self._max_temp = -100  # ridiculously low number
        self._on_off_type = False
        self._remote_id = ir_set["IRSetID"]
        # _ir_wave_map hosts a shrunk version of the ir_set file which ignores
        # unused data and map key to dict{"HexCode": str, "Para": str}
        # this is being built by the _resolve_capabilities method
        self._ir_wave_map = {}  # type: Mapping[str, Mapping[str, str]]
        self._modes_features = (
            {}
        )  # type: Mapping[ThermostatMode, Mapping[str, Union[bool, set]]]
        """
        self._modes_features basically explains the available features
            (Swing/Fan levels/ temp control of each mode)
        Example of _modes_features for ELEC7022 IRSet remote
        {
            < ThermostatMode.AUTO: ('01', 'auto') >: {
                'swing': False,
                'fan_levels': set(),
                'temperature_control': False
            }, < ThermostatMode.DRY: ('02', 'dry') >: {
                'swing': False,
                'fan_levels': set(),
                'temperature_control': False
            }, < ThermostatMode.FAN: ('03', 'fan') >: {
                'swing': False,
                'fan_levels': {
                    < ThermostatFanLevel.HIGH: ('3', 'high') > ,
                    < ThermostatFanLevel.AUTO: ('0', 'auto') > ,
                    < ThermostatFanLevel.MEDIUM: ('2', 'medium') > ,
                    < ThermostatFanLevel.LOW: ('1', 'low') >
                },
                'temperature_control': False
            }, < ThermostatMode.COOL: ('04', 'cool') >: {
                'swing': False,
                'fan_levels': {
                    < ThermostatFanLevel.HIGH: ('3', 'high') > ,
                    < ThermostatFanLevel.AUTO: ('0', 'auto') > ,
                    < ThermostatFanLevel.MEDIUM: ('2', 'medium') > ,
                    < ThermostatFanLevel.LOW: ('1', 'low') >
                },
                'temperature_control': True
            }, < ThermostatMode.HEAT: ('05', 'heat') >: {
                'swing': True,
                'fan_levels': {
                    < ThermostatFanLevel.HIGH: ('3', 'high') > ,
                    < ThermostatFanLevel.AUTO: ('0', 'auto') > ,
                    < ThermostatFanLevel.MEDIUM: ('2', 'medium') > ,
                    < ThermostatFanLevel.LOW: ('1', 'low') >
                },
                'temperature_control': True
            }
        }
        """
        self._separated_swing_command = (
            self._remote_id in SPECIAL_SWING_COMMAND_REMOTE_IDS
        )

        self._resolve_capabilities(ir_set)

    @property
    def modes_features(
        self,
    ) -> Mapping[ThermostatMode, Mapping[str, Union[bool, set]]]:
        """Getter for supported featuer per mode."""
        return self._modes_features

    @property
    def supported_modes(self) -> Iterable:
        """Getter for supported modes."""
        return self.modes_features.keys()

    @property
    def max_temperature(self) -> int:
        """Getter for Maximum supported temperature."""
        return self._max_temp

    @property
    def min_temperature(self) -> int:
        """Getter for Miniumum supported temperature."""
        return self._min_temp

    @property
    def remote_id(self) -> str:
        """Getter for remote id."""
        return self._remote_id

    @property
    def separated_swing_command(self) -> bool:
        """Getter for which indicates if the AC has a separated swing command."""
        return self._separated_swing_command

    def _lookup_key_in_irset(self, key: list) -> None:
        # start looking up for such key in the IRSet file
        while (
            len(key) != 1
        ):  # we match this condition with the key contains at least the mode
            # Try to lookup the key as is in the ir set map
            if "".join(key) not in self._ir_wave_map:
                # we didn't find a key, remove feature from the key and try to
                # look again.
                # The first feature removed is the swing "_d1"
                # Secondly is the fan level (_f0, _f1, _f2, _f3)
                # lastly we stay atleast with the mode part
                removed_element = key.pop()
                logger.debug(f"Removed {removed_element} from the key")
            else:
                # found a match, with modified list
                return

    def get_swing_command(self, swing: ThermostatSwing) -> SwitcherBreezeCommand:
        """Build a special command to control swing on special remotes."""
        if self._separated_swing_command:
            key = "FUN_d0" if swing == ThermostatSwing.OFF else "FUN_d1"
            try:
                command = (
                    self._ir_wave_map["".join(key)]["Para"]
                    + "|"
                    + self._ir_wave_map["".join(key)]["HexCode"]
                )
            except KeyError:
                logger.error(
                    f'The special swing key "{key}"        \
                        does not exist in the IRSet database!'
                )
                raise RuntimeError(
                    f'The special swing key "{key}"'
                    " does not exist in the IRSet database!"
                )

            return SwitcherBreezeCommand(
                "00000000" + hexlify(str(command).encode()).decode()
            )
        else:
            raise RuntimeWarning(
                f"Swing special function doesn't apply on this remote {self.remote_id}"
            )

    def get_command(
        self,
        state: DeviceState,
        mode: ThermostatMode,
        target_temp: int,
        fan_level: ThermostatFanLevel,
        swing: ThermostatSwing,
        current_state: DeviceState,
    ) -> SwitcherBreezeCommand:
        """Build command that controls the Breeze device."""
        key = []
        command = ""
        # verify the target temp and set maximum if we provided with higher number
        if target_temp > self._max_temp:
            target_temp = self._max_temp

        # verify the target temp and set minimum if we provided with lower number
        elif target_temp < self._min_temp:
            target_temp = self._min_temp

        if mode not in self.supported_modes:
            raise RuntimeError(
                f'Invalid mode "{mode.display}", available modes for this device are: '
                f"{', '.join([x.display for x in self.supported_modes])}"
            )

        # non toggle AC, just turn it off
        if not self._on_off_type and state == DeviceState.OFF:
            key.append("off")
        else:
            # This is a toggle mode AC, we determine here whether the first bit should
            # be on or off in order to change the AC state based on its current state.
            if self._on_off_type and current_state and current_state != state:
                # This is a toggle mode AC.
                key.append("on_")

            # for toggle mode AC - set state. for non toggel AC mode set state and turn
            # it on.
            if self._on_off_type or (not self._on_off_type and state == DeviceState.ON):
                # Auto and Dry can sometimes have a FAN level and in other cases
                # it might not have. in any case we try to add the request fan
                # level to the key, if we get a match we fulfill the request, otherwise
                # we remove the fan and lookup the key again
                if mode in [
                    ThermostatMode.AUTO,
                    ThermostatMode.DRY,
                    ThermostatMode.FAN,
                ]:
                    # the command key should start with mode (aa/ad/ar/ah)
                    key.append(BreezeRemote.MODE_TO_COMMAND[mode])
                    # add the requested fan level (_f0, _f1, _f2, _f3)
                    key.append("_" + BreezeRemote.FAN_LEVEL_TO_COMMAND[fan_level])

                    # add the swing On (_d1) to the key
                    if swing == ThermostatSwing.ON:
                        key.append("_d1")

                    self._lookup_key_in_irset(key)

                if mode in [ThermostatMode.COOL, ThermostatMode.HEAT]:
                    key.append(BreezeRemote.MODE_TO_COMMAND[mode])
                    key.append(str(target_temp))
                    key.append("_" + BreezeRemote.FAN_LEVEL_TO_COMMAND[fan_level])
                    if swing == ThermostatSwing.ON:
                        key.append("_d1")

                    self._lookup_key_in_irset(key)

        command = (
            self._ir_wave_map["".join(key)]["Para"]
            + "|"
            + self._ir_wave_map["".join(key)]["HexCode"]
        )
        return SwitcherBreezeCommand(
            "00000000" + hexlify(str(command).encode()).decode()
        )

    def _resolve_capabilities(self, ir_set):
        """Parse the ir_set of the remote and build capability data struct."""
        if ir_set["OnOffType"] == 1:
            self._on_off_type = True

        mode = None

        for wave in ir_set["IRWaveList"]:
            key = wave["Key"]
            try:
                mode = BreezeRemote.COMMAND_TO_MODE[key[0:2]]
                if mode not in self._modes_features:
                    self._modes_features[mode] = {
                        "swing": False,
                        "fan_levels": set(),
                        "temperature_control": False,
                    }

                    # This type of ACs support swing mode in every mode
                    if self.separated_swing_command:
                        self._modes_features[mode]["swing"] = True

            except KeyError:
                pass

            fan_level = re.match(r".+(f\d)", key)
            if fan_level:
                if mode:
                    self._modes_features[mode]["fan_levels"].add(
                        BreezeRemote.COMMAND_TO_FAN_LEVEL[fan_level.group(1)]
                    )

            temp = key[2:4]
            if temp.isdigit():
                if mode and not self._modes_features[mode]["temperature_control"]:
                    self._modes_features[mode]["temperature_control"] = True
                temp = int(temp)
                if temp > self._max_temp:
                    self._max_temp = temp
                if temp < self._min_temp:
                    self._min_temp = temp

            if mode:
                self._modes_features[mode]["swing"] |= "d1" in key

            self._ir_wave_map[key] = {"Para": wave["Para"], "HexCode": wave["HexCode"]}


class BreezeRemoteManager(object):
    """Class the used to download and hold all Breeze remotes."""

    def __init__(self, remotes_db_path: str = BREEZE_REMOTE_DB_FPATH):
        """Initialize the Remote manager."""
        self._remotes_db: Dict[str, BreezeRemote] = {}
        self._remotes_db_fpath = remotes_db_path
        # verify the file exists
        if not path.isfile(self._remotes_db_fpath):
            raise OSError(
                f"The specified remote db path {self._remotes_db_fpath} does not exist"
            )

    def get_remote(self, remote_id: str) -> BreezeRemote:
        """Get Breeze remote by the remote id."""
        # check if the remote was already loaded
        if remote_id not in self._remotes_db:
            # load the remote into the memory
            with open(self._remotes_db_fpath) as remotes_fd:
                self._remotes_db[remote_id] = BreezeRemote(load(remotes_fd)[remote_id])

        return self._remotes_db[remote_id]
