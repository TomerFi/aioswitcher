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

from argparse import ArgumentParser, RawDescriptionHelpFormatter

from aioswitcher.device.tools import validate_token

_examples = """example usage:

python validate_token.py -u "email" -t "zvVvd7JxtN7CgvkD1Psujw=="\n
python validate_token.py --username "email" --token "zvVvd7JxtN7CgvkD1Psujw=="\n
"""  # noqa E501

parser = ArgumentParser(
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


def main() -> None:
    """Validate the personal Token of the user."""
    try:
        args = parser.parse_args()

        response = validate_token(args.username, args.token)
        if response:
            print("Your Personal Token is valid")
        else:
            print("Your Personal Token is invalid")

    except KeyboardInterrupt:
        exit()


if __name__ == "__main__":
    main()
