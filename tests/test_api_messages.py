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

"""Switcher integration TCP socket API messages test cases."""

from binascii import unhexlify
from pathlib import Path
from unittest.mock import Mock, patch

from assertpy import assert_that
from pytest import mark

from aioswitcher.api import messages
from aioswitcher.api.messages import (
    StateMessageParser,
    SwitcherBaseResponse,
    SwitcherGetSchedulesResponse,
    SwitcherLoginResponse,
    SwitcherStateResponse,
)
from aioswitcher.device import DeviceState


@mark.parametrize("faulty_response", [b'', bytearray(), None])
def test_switcher_base_response_with_an_empty_bytes_value_should_return_not_succefull(faulty_response):
    assert_that(SwitcherBaseResponse(faulty_response).successful).is_false()


def test_switcher_login_response_dataclass(resource_path):
    response = Path(f'{resource_path}.txt').read_text().replace('\n', '').encode()
    sut = SwitcherLoginResponse(unhexlify(response))

    assert_that(sut.unparsed_response).is_equal_to(unhexlify(response))
    assert_that(sut.session_id).is_equal_to("f050834e")


def test_switcher_login_response_dataclass_without_a_valid_input_will_throw_an_error():
    assert_that(SwitcherLoginResponse).raises(
        ValueError
    ).when_called_with("this message will generate an excetpion").is_equal_to("failed to parse login response message")


@patch.object(StateMessageParser, "get_state", return_value=DeviceState.ON)
@patch.object(StateMessageParser, "get_time_left", return_value="00:45")
@patch.object(StateMessageParser, "get_time_on", return_value="00:45")
@patch.object(StateMessageParser, "get_auto_shutdown", return_value="03:00")
@patch.object(StateMessageParser, "get_power_consumption", return_value=1640)
def test_switcher_state_response_dataclass(get_power_consumption, get_auto_shutdown, get_time_on, get_time_left, get_state):
    sut = SwitcherStateResponse(b'moot binary data1')

    assert_that(sut.state).is_equal_to(DeviceState.ON)
    assert_that(sut.time_left).is_equal_to("00:45")
    assert_that(sut.time_on).is_equal_to("00:45")
    assert_that(sut.auto_shutdown).is_equal_to("03:00")
    assert_that(sut.power_consumption).is_equal_to(1640)
    assert_that(sut.electric_current).is_equal_to(7.5)

    for mock_method in [get_power_consumption, get_time_on, get_time_left, get_state]:
        mock_method.assert_called_once()
    get_auto_shutdown.assert_called()
    assert get_auto_shutdown.call_count == 2


@patch(messages.__name__ + ".get_schedules", return_value={Mock(), Mock()})
def test_switcher_get_schedules_response_dataclass_with_two_schedules(get_schedules):
    sut = SwitcherGetSchedulesResponse(b'moot binary data2')

    assert_that(sut.found_schedules).is_true()
    assert_that(sut.schedules).is_length(2)
    for schedule in sut.schedules:
        assert_that(schedule).is_instance_of(Mock)
    get_schedules.assert_called_once()


@patch(messages.__name__ + ".get_schedules", return_value=set())
def test_switcher_get_schedules_response_dataclass_with_no_schedules(get_schedules):
    sut = SwitcherGetSchedulesResponse(b'moot binary data3')

    assert_that(sut.found_schedules).is_false()
    assert_that(sut.schedules).is_length(0)
    get_schedules.assert_called_once()


def test_the_state_message_parser(resource_path):
    response = Path(f'{resource_path}_device_off.txt').read_text().replace('\n', '').encode()
    sut = StateMessageParser(unhexlify(response))

    assert_that(sut.get_state()).is_equal_to(DeviceState.OFF)
    assert_that(sut.get_time_left()).is_equal_to("00:00:00")
    assert_that(sut.get_time_on()).is_equal_to("00:00:00")
    assert_that(sut.get_auto_shutdown()).is_equal_to("01:30:00")
    assert_that(sut.get_power_consumption()).is_equal_to(0)
