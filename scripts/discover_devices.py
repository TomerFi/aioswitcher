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

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from asyncio import get_event_loop, sleep
from dataclasses import asdict
from pprint import PrettyPrinter

from aioswitcher.bridge import (
    SWITCHER_UDP_PORT_TYPE1,
    SWITCHER_UDP_PORT_TYPE2,
    DeviceType,
    SwitcherBridge,
)
from aioswitcher.device import SwitcherBase

printer = PrettyPrinter(indent=4)

_examples = (
    """Executing this script will print a serialized version of the discovered Switcher
devices broadcasting on the local network for 60 seconds.
You can change the delay by passing an int argument: discover_devices.py 30

Switcher devices uses two protocol types:
    Protocol type 1 (UDP port 20002), used by: """
    + ", ".join(d.value for d in DeviceType if d.protocol_type == 1)
    + """
    Protocol type 2 (UDP port 20003), used by: """
    + ", ".join(d.value for d in DeviceType if d.protocol_type == 2)
    + """
You can change the scanned protocol type by passing an int argument: discover_devices.py -t 1

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
Print all protocol types devices for 30 seconds:
    python discover_devices.py 30 -t all\n

Print only protocol type 1 devices:
    python discover_devices.py -t 1\n

Print only protocol type 2 devices:
    python discover_devices.py -t 2\n
"""  # noqa E501
)

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
possible_types = ["1", "2", "all"]
parser.add_argument(
    "-t",
    "--type",
    required=False,
    choices=possible_types,
    help=f"set protocol type: {possible_types}",
    type=str,
)


async def print_devices(delay: int, ports: list[int]) -> None:
    """Run the Switcher bridge and register callback for discovered devices."""

    def on_device_found_callback(device: SwitcherBase) -> None:
        """Use as a callback printing found devices."""
        printer.pprint(asdict(device))
        print()

    async with SwitcherBridge(on_device_found_callback, broadcast_ports=ports):
        await sleep(delay)


if __name__ == "__main__":
    args = parser.parse_args()

    if args.type == "1":
        ports = [SWITCHER_UDP_PORT_TYPE1]
    elif args.type == "2":
        ports = [SWITCHER_UDP_PORT_TYPE2]
    else:
        ports = [SWITCHER_UDP_PORT_TYPE1, SWITCHER_UDP_PORT_TYPE2]

    try:
        get_event_loop().run_until_complete(print_devices(args.delay, ports))
    except KeyboardInterrupt:
        exit()
