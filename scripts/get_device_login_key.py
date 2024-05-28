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

"""Python script for retrieving Switcher device login key."""

import socket
import time
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from pprint import PrettyPrinter

printer = PrettyPrinter(indent=4)

_examples = """example usage:

python get_device_login_key.py -i "111.222.11.22" -p 10002\n
"""  # noqa E501

parser = ArgumentParser(
    description="Discover and print info of Switcher devices",
    epilog=_examples,
    formatter_class=RawDescriptionHelpFormatter,
)
parser.add_argument(
    "-p",
    "--port",
    required=True,
    help="the UDP port of the device",
    type=int,
)
parser.add_argument(
    "-i",
    "--ip-address",
    required=True,
    help="the device IP",
    type=str,
)


def extract_device_key(data: bytes) -> str:
    """Get the device_key from the UDP message."""
    return data[40:41].hex()


def listen_udp(specific_ip: str, port: int) -> None:
    """Listen to UDP and try to extract the device_key."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", port))

    start_time = time.time()
    while True:
        if time.time() - start_time > 2:
            print("Stopping the server.")
            break

        sock.settimeout(2 - (time.time() - start_time))

        try:
            data, addr = sock.recvfrom(1024)
            if addr[0] == specific_ip:
                print("Received device key:", extract_device_key(data))
                break
        except socket.timeout:
            print("No packets received, still waiting...")

    sock.close()


def main():
    args = parser.parse_args()
    print("ip address: " + args.ip_address)
    print("port: " + str(args.port))
    listen_udp(args.ip_address, args.port)


if __name__ == "__main__":
    main()
