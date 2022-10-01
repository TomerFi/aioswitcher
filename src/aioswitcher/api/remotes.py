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

"""Switcher integration API remote related classes and functions."""

import re
from binascii import hexlify
from json import load
from logging import getLogger
from os import path
from pathlib import Path
from typing import Any, Dict, List, Union, final

from ..device import DeviceState, ThermostatFanLevel, ThermostatMode, ThermostatSwing

logger = getLogger(__name__)

BREEZE_REMOTE_DB_FPATH = str(Path(__file__).parent.parent) + "/resources/irset_db.json"

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


@final
class SwitcherBreezeCommand:
    """Representations of the Switcher Breeze command message.

    Args:
        command: a string command ready to be parsed and sent

    """

    def __init__(self, command: str) -> None:
        """Initialize the Breeze command."""
        self.command = command
        self.length = self._get_command_length()

    def _get_command_length(self) -> str:
        """Get command length.

        Note:
            This is a private function used by other functions, do not call this
            function directly.

        """
        return "{:x}".format(int(len(self.command) / 2)).ljust(4, "0")


@final
class SwitcherBreezeRemote:
    """Class that represent a remote for a Breeze device/s.

    Args:
        ir_set: a dictionary for all supported remotes

    """

    def __init__(self, ir_set: Dict[str, Any]) -> None:
        """Initialize the remote by parsing the ir_set data."""
        self._min_temp = 100  # ridiculously high number
        self._max_temp = -100  # ridiculously low number
        self._on_off_type = False
        self._remote_id: str = ir_set["IRSetID"]
        # _ir_wave_map hosts a shrunk version of the ir_set file which ignores
        # unused data and map key to dict{"HexCode": str, "Para": str}
        # this is being built by the _resolve_capabilities method
        self._ir_wave_map: Dict[str, Dict[str, str]] = {}
        self._modes_features: Dict[ThermostatMode, Dict[str, Any]] = {}
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
    ) -> Dict[ThermostatMode, Dict[str, Any]]:
        """Getter for supported feature per mode."""
        return self._modes_features

    @property
    def supported_modes(self) -> List[ThermostatMode]:
        """Getter for supported modes."""
        return list(self.modes_features.keys())

    @property
    def max_temperature(self) -> int:
        """Getter for Maximum supported temperature."""
        return self._max_temp

    @property
    def min_temperature(self) -> int:
        """Getter for Minimum supported temperature."""
        return self._min_temp

    @property
    def remote_id(self) -> str:
        """Getter for remote id."""
        return self._remote_id

    @property
    def separated_swing_command(self) -> bool:
        """Getter for which indicates if the AC has a separated swing command."""
        return self._separated_swing_command

    def _lookup_key_in_irset(self, key: List[str]) -> None:
        """Use this to look for a key in the IRSet file.

        Args:
            key: a reference to List of strings representing parts of the command.

        Note:
            This is a private function used by other functions, do not call this
            function directly.

        """
        while (
            len(key) != 1
        ):  # we match this condition with the key contains at least the mode
            # Try to lookup the key as is in the ir set map
            if "".join(key) not in self._ir_wave_map:
                # we didn't find a key, remove feature from the key and try to
                # look again.
                # The first feature removed is the swing "_d1"
                # Secondly is the fan level (_f0, _f1, _f2, _f3)
                # lastly we stay at least with the mode part
                removed_element = key.pop()
                logger.debug(f"Removed {removed_element} from the key")
            else:
                # found a match, with modified list
                return

    def build_swing_command(self, swing: ThermostatSwing) -> SwitcherBreezeCommand:
        """Build a special command to control swing on special remotes.

        Args:
            swing: the desired swing state

        Returns:
            An instance of ``SwitcherBreezeCommand``

        """
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

    def build_command(
        self,
        state: DeviceState,
        mode: ThermostatMode,
        target_temp: int,
        fan_level: ThermostatFanLevel,
        swing: ThermostatSwing,
        current_state: Union[DeviceState, None] = None,
    ) -> SwitcherBreezeCommand:
        """Build command that controls the Breeze device.

        Args:
            state: the desired state of the device
            mode: the desired mode of the device
            target_temp: the target temperature
            fan_level: the desired fan level
            swing: the desired swing state
            current_state: optionally, for toggle device, pass previous state to avoid
                redundant requests

        Returns:
            An instance of ``SwitcherBreezeCommand``

        """
        key: List[str] = []
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

            # for toggle mode AC - set state. for non toggle AC mode set state and turn
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
                    key.append(MODE_TO_COMMAND[mode])
                    # add the requested fan level (_f0, _f1, _f2, _f3)
                    key.append("_" + FAN_LEVEL_TO_COMMAND[fan_level])

                    # add the swing On (_d1) to the key
                    if swing == ThermostatSwing.ON:
                        key.append("_d1")

                    self._lookup_key_in_irset(key)

                if mode in [ThermostatMode.COOL, ThermostatMode.HEAT]:
                    key.append(MODE_TO_COMMAND[mode])
                    key.append(str(target_temp))
                    key.append("_" + FAN_LEVEL_TO_COMMAND[fan_level])
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

    def _resolve_capabilities(self, ir_set: Dict[str, Any]) -> None:
        """Parse the ir_set of the remote and build capability data struct.

        Args:
            ir_set: a dictionary for all supported remotes

        Note:
            This is a private function used by other functions, do not call this
            function directly.

        """
        if ir_set["OnOffType"] == 1:
            self._on_off_type = True

        mode = None

        for wave in ir_set["IRWaveList"]:
            key = wave["Key"]
            try:
                mode = COMMAND_TO_MODE[key[0:2]]
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
            if fan_level and mode:
                self._modes_features[mode]["fan_levels"].add(
                    COMMAND_TO_FAN_LEVEL[fan_level.group(1)]
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


class SwitcherBreezeRemoteManager:
    """Class for managing Breeze remotes.

    Args:
        remotes_db_path: optional path of supported remote json file

    """

    def __init__(self, remotes_db_path: str = BREEZE_REMOTE_DB_FPATH) -> None:
        """Initialize the Remote manager."""
        self._remotes_db: Dict[str, SwitcherBreezeRemote] = {}
        self._remotes_db_fpath = remotes_db_path
        # verify the file exists
        if not path.isfile(self._remotes_db_fpath):
            raise OSError(
                f"The specified remote db path {self._remotes_db_fpath} does not exist"
            )

    def get_remote(self, remote_id: str) -> SwitcherBreezeRemote:
        """Get Breeze remote by the remote id.

        Args:
            remote_id: the id of the desired remote

        Returns:
            an instance of ``SwitcherBreezeRemote``

        """
        # check if the remote was already loaded
        if remote_id not in self._remotes_db:
            # load the remote into the memory
            with open(self._remotes_db_fpath) as remotes_fd:
                self._remotes_db[remote_id] = SwitcherBreezeRemote(
                    load(remotes_fd)[remote_id]
                )

        return self._remotes_db[remote_id]
