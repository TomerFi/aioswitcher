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

"""Python script for getting Token from Switcher."""

from argparse import ArgumentParser, RawDescriptionHelpFormatter

from aioswitcher.device.tools import get_token

_examples = """example usage:

python get_token.py -u "username" -p "password"\n
python get_token.py --username "username" -p "password"\n

"""  # noqa E501

parser = ArgumentParser(
    description="Get user's Token from Switcher by username and password",
    epilog=_examples,
    formatter_class=RawDescriptionHelpFormatter,
)

parser.add_argument(
    "-u",
    "--username",
    required=True,
    help="the username of the user",
    type=str,
)

parser.add_argument(
    "-p",
    "--password",
    required=True,
    help="the password of the user",
    type=str,
)


if __name__ == "__main__":
    try:
        args = parser.parse_args()

        token = get_token(args.username, args.password).to_json()
        print("Your Token is: " + token)

    except KeyboardInterrupt:
        exit()
