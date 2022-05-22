#! python3

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

"""Python script for printing discovered Swithcer devices info.

Executing this script will print a serialized version of the discovered Switcher
devices broadcasting on the local network for 60 seconds. You can change the delay
by passing an int argument: ``discover_devices.py 30``.

Note:
    WILL PRINT PRIVATE INFO SUCH AS DEVICE ID AND MAC.

Example:
    Switcher devices broadcast a status message every approximantly 4 seconds. This
    script listens for these messages and prints a serialized version of the to the
    standard output, for example (note the ``device_id`` and ``mac_address`` properties)::
        {   'auto_shutdown': '03:00:00',
            'device_id': 'aaaaaa',
            'device_state': <DeviceState.OFF: ('0000', 'off')>,
            'device_type': <DeviceType.V2_ESP: ('Switcher V2 (esp)', 'a7', <DeviceCategory.WATER_HEATER: 1>)>,
            'electric_current': 0.0,
            'ip_address': '192.168.1.33',
            'last_data_update': datetime.datetime(2021, 6, 13, 11, 11, 44, 883003),
            'mac_address': '12:A1:A2:1A:BC:1A',
            'name': 'My Switcher Boiler',
            'power_consumption': 0,
            'remaining_time': '00:00:00'}

"""  # noqa: E501

from asyncio import get_event_loop, sleep
from dataclasses import asdict
from pprint import PrettyPrinter
from aioswitcher.api import (
    SWITCHER_DEVICE_TO_TCP_PORT,
    SwitcherApi,
    BreezeRemoteManager,
    BreezeRemote,
    ThermostatMode,
    ThermostatSwing,
    ThermostatFanLevel,
    DeviceState,
)

from aioswitcher.bridge import SWITCHER_DEVICE_TO_UDP_PORT, SwitcherBridge
from aioswitcher.device import DeviceCategory, SwitcherBase

import logging
import sys

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
root.addHandler(handler)

printer = PrettyPrinter(indent=4)


async def main() -> None:
    """Run the Switcher bridge and register callback for discovered devices."""

    my_devices = {}

    def on_device_found_callback(device: SwitcherBase) -> None:
        """Use as a callback printing found devices."""
        if device.device_id not in my_devices:
            my_devices[device.device_id] = device

    rm = BreezeRemoteManager()

    async with SwitcherBridge(
        on_device_found_callback, SWITCHER_DEVICE_TO_UDP_PORT[DeviceCategory.THERMOSTAT]
    ):
        await sleep(3)

    for device_id in my_devices.keys():
        device: SwitcherBase = my_devices[device_id]
        printer.pprint(asdict(device))
        print()

        async with SwitcherApi(
            device.ip_address,
            device_id,
            SWITCHER_DEVICE_TO_TCP_PORT[DeviceCategory.THERMOSTAT],
        ) as api:

            remote: BreezeRemote = await rm.get_remote(device, api)

            cmd = remote.get_command(
                device,
                DeviceState.ON,
                ThermostatMode.COOL,
                23,
                ThermostatFanLevel.HIGH,
                ThermostatSwing.ON,
            )
            await api.control_breeze_device(device, cmd)

            print(await api.get_breeze_state())
            await api.disconnect()


if __name__ == "__main__":

    try:
        get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        exit()
