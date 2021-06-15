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

# flake8: noqa

"""Switcher unofficial integration UDP bridge test cases."""

from asyncio import DatagramProtocol, get_event_loop
from unittest.mock import Mock, patch

from pytest import fixture, mark

from aioswitcher.bridge import SwitcherBridge

pytestmark = mark.asyncio


@fixture
def mock_callback():
    return Mock()


@fixture
def sut_bridge(mock_callback):
    return SwitcherBridge(mock_callback)


@patch("logging.Logger.info")
async def test_stopping_before_started_and_establishing_a_connection_should_write_to_the_info_output(mock_info, sut_bridge):
    await sut_bridge.stop()
    mock_info.assert_called_with("udp bridge not started")
