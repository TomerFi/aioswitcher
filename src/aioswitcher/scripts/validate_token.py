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

"""Python script for validating a Token from Switcher."""

import asyncio
from argparse import ArgumentParser, RawDescriptionHelpFormatter

from aioswitcher.device.tools import validate_token

_examples = """example usage:

switcher-validate-token -u "email" -t "YOUR_TOKEN"\n
switcher-validate-token --username "email" --token "YOUR_TOKEN"\n
"""  # noqa E501

parser = ArgumentParser(
    prog="switcher-validate-token",
    description="Validate a Token from Switcher by username and token",
    epilog=_examples,
    formatter_class=RawDescriptionHelpFormatter,
)

parser.add_argument(
    "-u",
    "--username",
    required=True,
    help="the username of the user (Email address)",
    type=str,
)

parser.add_argument(
    "-t",
    "--token",
    required=True,
    help="the token of the user sent by Email",
    type=str,
)


async def async_main() -> None:
    """Validate the personal Token of the user."""
    try:
        args = parser.parse_args()

        response = await validate_token(args.username, args.token)
        if response:
            print("Your Personal Token is valid")
        else:
            print("Your Personal Token is invalid")

    except KeyboardInterrupt:
        exit()


def main() -> None:
    """Run the token validation."""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
