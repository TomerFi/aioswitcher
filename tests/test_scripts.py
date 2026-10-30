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

"""Switcher integration CLI scripts entry points test cases."""

from importlib.metadata import entry_points
from unittest.mock import patch

from assertpy import assert_that
from pytest import mark, raises

EXPECTED_CONSOLE_SCRIPTS = {
    "switcher-control-device": "aioswitcher.scripts.control_device:main",
    "switcher-discover-devices": "aioswitcher.scripts.discover_devices:main",
    "switcher-get-device-login-key": "aioswitcher.scripts.get_device_login_key:main",
    "switcher-validate-token": "aioswitcher.scripts.validate_token:main",
}


def _aioswitcher_console_scripts():
    return {
        ep.name: ep
        for ep in entry_points(group="console_scripts")
        if ep.dist is not None and ep.dist.name == "aioswitcher"
    }


def test_console_scripts_are_registered_with_the_expected_targets():
    sut = {name: ep.value for name, ep in _aioswitcher_console_scripts().items()}
    assert_that(sut).is_equal_to(EXPECTED_CONSOLE_SCRIPTS)


@mark.parametrize("command", EXPECTED_CONSOLE_SCRIPTS)
def test_console_script_help_should_print_usage_with_the_command_name(command, capsys):
    sut = _aioswitcher_console_scripts()[command].load()
    with patch("sys.argv", [command, "--help"]), raises(SystemExit) as sut_exit:
        sut()
    assert_that(sut_exit.value.code).is_equal_to(0)
    assert_that(capsys.readouterr().out).starts_with(f"usage: {command} ")
