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

"""Python script for discovering Switcher devices."""

import asyncio
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from dataclasses import asdict
from pprint import PrettyPrinter

from aioswitcher.bridge import SwitcherBridge
from aioswitcher.device import SwitcherBase

printer = PrettyPrinter(indent=4)

_examples = """Executing this script will print a serialized version of the discovered Switcher
devices broadcasting on the local network for 60 seconds.
You can change the delay by passing an int argument: discover_devices.py 30

Note:
    WILL PRINT PRIVATE INFO SUCH AS DEVICE ID AND MAC.

Example output:
    Switcher devices broadcast a status message every approximately 4 seconds. This
    script listens for these messages and prints a serialized version of the to the
    standard output, for example (note the ``device_id`` and ``mac_address`` properties)::
    ```
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
    ```
Print devices for 30 seconds:
    python discover_devices.py 30\n
"""  # noqa E501

parser = ArgumentParser(
    description="Discover and print info of Switcher devices",
    epilog=_examples,
    formatter_class=RawDescriptionHelpFormatter,
)
parser.add_argument(
    "delay",
    help="number of seconds to run, defaults to 60",
    type=int,
    nargs="?",
    default=60,
)


async def print_devices(delay: int) -> None:
    """Run the Switcher bridge and register callback for discovered devices."""

    def on_device_found_callback(device: SwitcherBase) -> None:
        """Use as a callback printing found devices."""
        printer.pprint(asdict(device))
        print()

    async with SwitcherBridge(on_device_found_callback):
        await asyncio.sleep(delay)


def main() -> None:
    """Run the device discovery script."""
    args = parser.parse_args()

    try:
        asyncio.run(print_devices(args.delay))
    except KeyboardInterrupt:
        exit()


if __name__ == "__main__":
    main()
