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

"""Switcher unofficial integration broadcast message parsing utility functions test cases."""

from binascii import unhexlify

from assertpy import assert_that
from aioswitcher.bridge.parser_utils import broadcast_originator_is_switcher
from pytest import mark


@mark.skip
def test_broadcast_originator_is_switcher_with_valid_message_should_return_true():
    valid_message = unhexlify("fef0".encode() + ("0" * 325).encode())
    assert_that(broadcast_originator_is_switcher(valid_message)).is_true()
