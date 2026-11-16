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

"""Address discovery through source-rewriting UDP relays."""

from ipaddress import ip_network
from pathlib import Path
from socket import inet_aton
from unittest.mock import Mock

from assertpy import assert_that
from pytest import mark

from aioswitcher.bridge import _parse_device_from_datagram


@mark.parametrize(
    "fixture_name,offset",
    [
        ("water_heater", 76),
        ("power_plug", 76),
        ("breeze", 77),
        ("runner", 77),
        ("single_runner_dual_light", 77),
        ("dual_runner_single_light", 77),
        ("light", 77),
        ("dual_light", 77),
        ("triple_light", 77),
        ("heater", 77),
    ],
)
@mark.parametrize("use_payload_ip", [False, True])
def test_discovery_address_selection(
    fixture_name, offset, use_payload_ip, resource_path_root
):
    data = bytearray.fromhex(
        Path(
            resource_path_root,
            "test_device_parsing",
            f"test_a_{fixture_name}_datagram_produces_device.txt",
        )
        .read_text()
        .replace("\n", "")
    )
    data[offset : offset + 4] = inet_aton("192.0.2.42")
    callback = Mock()
    _parse_device_from_datagram(
        callback,
        bytes(data),
        "198.51.100.1",
        broadcast_ip_network=ip_network("192.0.2.0/24") if use_payload_ip else None,
    )
    callback.assert_called_once()
    expected = "192.0.2.42" if use_payload_ip else "198.51.100.1"
    assert_that(callback.call_args.args[0].ip_address).is_equal_to(expected)


@mark.parametrize("fixture_name,offset", [("water_heater", 76), ("breeze", 77)])
def test_embedded_address_outside_allowed_network_is_rejected(
    fixture_name, offset, resource_path_root
):
    data = bytearray.fromhex(
        Path(
            resource_path_root,
            "test_device_parsing",
            f"test_a_{fixture_name}_datagram_produces_device.txt",
        )
        .read_text()
        .replace("\n", "")
    )
    data[offset : offset + 4] = inet_aton("203.0.113.9")
    callback = Mock()
    _parse_device_from_datagram(
        callback,
        bytes(data),
        "198.51.100.1",
        broadcast_ip_network=ip_network("192.0.2.0/24"),
    )
    callback.assert_not_called()
