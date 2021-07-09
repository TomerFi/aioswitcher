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

"""Switcher integration udp client protocol test cases."""

from unittest.mock import Mock, patch

from assertpy import assert_that
from pytest import fixture, warns

from aioswitcher.bridge import UdpClientProtocol


@fixture
def mock_callback():
    return Mock()


@fixture
def sut_protocol(mock_callback):
    return UdpClientProtocol(mock_callback)


def test_given_transport_when_connection_made_then_transport_should_be_served(sut_protocol):
    mock_transport = Mock()
    sut_protocol.connection_made(mock_transport)
    assert_that(sut_protocol.transport).is_equal_to(mock_transport)


def test_given_datagram_when_sut_received_then_the_callback_is_called(sut_protocol, mock_callback):
    mock_datagram = Mock()
    sut_protocol.datagram_received(mock_datagram, Mock())
    mock_callback.assert_called_once_with(mock_datagram)


def test_error_received_with_no_error_should_issue_a_warning(sut_protocol):
    with warns(UserWarning, match="udp client received error"):
        sut_protocol.error_received(None)


@patch("logging.Logger.error")
def test_error_received_with_an_actual_error_should_write_to_the_error_output(mock_error, sut_protocol):
    sut_protocol.error_received(Exception("dummy"))
    mock_error.assert_called_once_with("udp client received error dummy")


@patch("logging.Logger.info")
def test_connection_lost_with_no_error_should_write_to_the_info_output(mock_info, sut_protocol):
    sut_protocol.connection_lost(None)
    mock_info.assert_called_once_with("udp connection stopped")


@patch("logging.Logger.critical")
def test_connection_lost_with_an_actual_error_should_write_to_the_critical_output(mock_critical, sut_protocol):
    sut_protocol.connection_lost(Exception("dummy"))
    mock_critical.assert_called_once_with("udp bridge lost its connection dummy")
