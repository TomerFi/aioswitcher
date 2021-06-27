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

"""Python script for controlling Switcher devices."""

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from asyncio import get_event_loop
from binascii import hexlify
from pprint import PrettyPrinter
from typing import Any, Dict

from pkg_resources import require

from aioswitcher.api import SwitcherApi

require("aioswitcher>=2.0.0-dev")

printer = PrettyPrinter(indent=4)


def asdict(dc: object, verbose: bool = False) -> Dict[str, Any]:
    """Use for custom implementation of the asdict utility method."""
    return {
        k: v
        for k, v in dc.__dict__.items()
        if not (not verbose and k == "unparsed_response")
    }


async def get_state(device_id: str, device_ip: str, verbose: bool) -> None:
    """Use to launch a get_state request."""
    async with SwitcherApi(device_ip, device_id) as api:
        printer.pprint(asdict(await api.get_state(), verbose))


async def get_schedules(device_id: str, device_ip: str, verbose: bool) -> None:
    """Use to launch a get_schedules request."""
    async with SwitcherApi(device_ip, device_id) as api:
        response = await api.get_schedules()
        if verbose:
            printer.pprint(
                {"unparsed_response": hexlify(response.unparsed_response).decode()}
            )
            print()
        for schedule in response.schedules:
            printer.pprint(asdict(schedule))
            print()


if __name__ == "__main__":
    try:
        examples = """example usage:

        python control_device.py -d ab1c2d -i "111.222.11.22" get_state
        python control_device.py -d ab1c2d -i "111.222.11.22" get_schedules"""

        parent_parser = ArgumentParser(
            description="Control your Switcher device",
            epilog=examples,
            formatter_class=RawDescriptionHelpFormatter,
        )
        parent_parser.add_argument(
            "-v", "--verbose", default=False, action="store_true"
        )
        parent_parser.add_argument(
            "-d",
            "--device-id",
            type=str,
            required=True,
            help="the identification of the device",
        )
        parent_parser.add_argument(
            "-i",
            "--ip-address",
            type=str,
            required=True,
            help="the ip address assigned to the device",
        )

        subparsers = parent_parser.add_subparsers(
            dest="action", description="supported actions"
        )
        subparsers.add_parser("get_state", help="get the current state of a device")
        subparsers.add_parser("get_schedules", help="retrive a device's schedules")

        parent_args = parent_parser.parse_args()

        if parent_args.action == "get_state":
            get_event_loop().run_until_complete(
                get_state(
                    parent_args.device_id, parent_args.ip_address, parent_args.verbose
                )
            )
        elif parent_args.action == "get_schedules":
            get_event_loop().run_until_complete(
                get_schedules(
                    parent_args.device_id, parent_args.ip_address, parent_args.verbose
                )
            )
    except KeyboardInterrupt:
        exit()
