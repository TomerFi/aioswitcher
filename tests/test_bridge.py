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

"""Switcher integration UDP bridge module test cases."""
import socket
from asyncio import sleep
from binascii import unhexlify
from pathlib import Path
from unittest.mock import Mock, patch

from assertpy import assert_that
from pytest import fixture, mark

from aioswitcher.bridge import SwitcherBridge

pytestmark = mark.asyncio


@fixture
def mock_callback():
    return Mock()


@fixture
def udp_broadcast_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.settimeout(0.2)
    return server


@fixture
def unused_udp_broadcast_port(unused_udp_port_factory):
    port = unused_udp_port_factory()
    with patch("aioswitcher.bridge.SWITCHER_UDP_BROADCAST_PORTS", [port]):
        yield port


@patch("logging.Logger.info")
async def test_stopping_before_started_and_establishing_a_connection_should_write_to_the_info_output(mock_info, unused_udp_broadcast_port, mock_callback):
    port = unused_udp_broadcast_port
    bridge = SwitcherBridge(mock_callback)
    assert_that(bridge.is_running).is_false()
    await bridge.stop()
    mock_info.assert_called_with("udp bridge on port %s not started", port)


async def test_bridge_operation_as_a_context_manager(unused_udp_broadcast_port, mock_callback):
    async with SwitcherBridge(mock_callback) as bridge:
        assert_that(bridge.is_running).is_true()


async def test_bridge_start_and_stop_operations(unused_udp_broadcast_port, mock_callback):
    bridge = SwitcherBridge(mock_callback)
    assert_that(bridge.is_running).is_false()
    await bridge.start()
    assert_that(bridge.is_running).is_true()
    await bridge.stop()
    assert_that(bridge.is_running).is_false()


async def test_bridge_callback_loading(udp_broadcast_server, unused_udp_broadcast_port, mock_callback, resource_path):
    port = unused_udp_broadcast_port
    sut_v2_off_datagram = Path(f'{resource_path}_v2_off.txt').read_text().replace('\n', '').encode()
    sut_power_plug_off_datagram = Path(f'{resource_path}_power_plug_off.txt').read_text().replace('\n', '').encode()

    async with SwitcherBridge(mock_callback):
        udp_broadcast_server.sendto(unhexlify(sut_v2_off_datagram), ("localhost", port))
        await sleep(0.2)
        udp_broadcast_server.sendto(unhexlify(sut_power_plug_off_datagram), ("localhost", port))
        await sleep(0.2)

    assert_that(mock_callback.call_count).is_equal_to(2)
