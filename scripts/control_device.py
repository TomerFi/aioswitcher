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
from datetime import timedelta
from pprint import PrettyPrinter
from typing import Any, Dict, List

from pkg_resources import require

from aioswitcher.api import SwitcherApi
from aioswitcher.schedule import Days

require("aioswitcher>=2.0.0-dev")

printer = PrettyPrinter(indent=4)


def asdict(dc: object, verbose: bool = False) -> Dict[str, Any]:
    """Use as custom implementation of the asdict utility method."""
    return {
        k: v
        for k, v in dc.__dict__.items()
        if not (not verbose and k == "unparsed_response")
    }


async def get_state(device_id: str, device_ip: str, verbose: bool) -> None:
    """Use to launch a get_state request."""
    async with SwitcherApi(device_ip, device_id) as api:
        printer.pprint(asdict(await api.get_state(), verbose))


async def set_auto_shutdown(
    device_id: str, device_ip: str, hours: int, minutes: int, verbose: bool
):
    """Use to launch a set_auto_shutdown request."""
    td_val = timedelta(hours=hours, minutes=minutes)
    async with SwitcherApi(device_ip, device_id) as api:
        printer.pprint(asdict(await api.set_auto_shutdown(td_val), verbose))


async def get_schedules(device_id: str, device_ip: str, verbose: bool) -> None:
    """Use to launch a get_schedules request."""
    async with SwitcherApi(device_ip, device_id) as api:
        response = await api.get_schedules()
        if verbose:
            printer.pprint({"unparsed_response": response.unparsed_response})
            print()
        for schedule in response.schedules:
            printer.pprint(asdict(schedule))
            print()


async def delete_schedule(
    device_id: str, device_ip: str, schedule_id: str, verbose: bool
) -> None:
    """Use to launch a delete_schedule request."""
    async with SwitcherApi(device_ip, device_id) as api:
        printer.pprint(asdict(await api.delete_schedule(schedule_id), verbose))


async def create_schedule(
    device_id: str,
    device_ip: str,
    start_time: str,
    end_time: str,
    weekdays: List[str],
    verbose: bool,
):
    """Use to launch a create_schedule request."""
    async with SwitcherApi(device_ip, device_id) as api:
        printer.pprint(
            asdict(
                await api.create_schedule(
                    start_time,
                    end_time,
                    set([Days(w) for w in weekdays]),  # type: ignore
                ),
                verbose,
            )
        )


if __name__ == "__main__":
    try:
        examples = """example usage:

        python control_device.py -d ab1c2d -i "111.222.11.22" get_state
        python control_device.py -d ab1c2d -i "111.222.11.22" set_auto_shutdown -r 2 -m 30
        python control_device.py -d ab1c2d -i "111.222.11.22" get_schedules
        python control_device.py -d ab1c2d -i "111.222.11.22" delete_schedule -s 3
        python control_device.py -d ab1c2d -i "111.222.11.22" create_schedule -n "14:00" -f "14:30"
        python control_device.py -d ab1c2d -i "111.222.11.22" create_schedule -n "17:30" -f "18:30" -w Sunday Monday Friday"""  # noqa E501

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
        set_auto_shutdown_parser = subparsers.add_parser(
            "set_auto_shutdown", help="set the auto shutdown property (1h-24h)"
        )
        set_auto_shutdown_parser.add_argument(
            "-r",
            "--hours",
            choices=range(1, 24),
            type=int,
            required=True,
            help="number hours for the auto shutdown",
        )
        set_auto_shutdown_parser.add_argument(
            "-m",
            "--minutes",
            choices=range(0, 60),
            type=int,
            nargs="?",
            default=0,
            help="number hours for the auto shutdown",
        )

        subparsers.add_parser("get_schedules", help="retrive a device schedules")

        delete_schedule_parser = subparsers.add_parser(
            "delete_schedule", help="delete a device schedule"
        )
        delete_schedule_parser.add_argument(
            "-s",
            "--schedule-id",
            type=str,
            required=True,
            help="the id of the schedule for deletion",
        )

        create_schedule_parser = subparsers.add_parser(
            "create_schedule", help="create a new schedule"
        )
        create_schedule_parser.add_argument(
            "-n",
            "--start-time",
            type=str,
            required=True,
            help="the on time for the schedule, e.g. 13:00",
        )
        create_schedule_parser.add_argument(
            "-f",
            "--end-time",
            type=str,
            required=True,
            help="the off time for the schedule, e.g. 13:30",
        )
        possible_weekdays = [d.value for d in Days]
        create_schedule_parser.add_argument(
            "-w",
            "--weekdays",
            choices=possible_weekdays,
            nargs="*",
            required=False,
            help=f"days for recurring scheduels, possible values: {possible_weekdays}",
            default=list(),
        )

        args = parent_parser.parse_args()

        if args.action == "get_state":
            get_event_loop().run_until_complete(
                get_state(args.device_id, args.ip_address, args.verbose)
            )
        elif args.action == "set_auto_shutdown":
            get_event_loop().run_until_complete(
                set_auto_shutdown(
                    args.device_id,
                    args.ip_address,
                    args.hours,
                    args.minutes,
                    args.verbose,
                )
            )
        elif args.action == "get_schedules":
            get_event_loop().run_until_complete(
                get_schedules(args.device_id, args.ip_address, args.verbose)
            )
        elif args.action == "delete_schedule":
            get_event_loop().run_until_complete(
                delete_schedule(
                    args.device_id, args.ip_address, args.schedule_id, args.verbose
                )
            )
        elif args.action == "create_schedule":
            get_event_loop().run_until_complete(
                create_schedule(
                    args.device_id,
                    args.ip_address,
                    args.start_time,
                    args.end_time,
                    args.weekdays,
                    args.verbose,
                )
            )
    except KeyboardInterrupt:
        exit()
