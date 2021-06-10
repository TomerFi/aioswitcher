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

"""Switcher unofficial integration broadcast message parsing utility functions."""

from binascii import hexlify
from socket import inet_ntoa
from struct import pack

from ..devices import DeviceState, DeviceType
from ..utils import seconds_to_iso_time


def is_switcher_originator(message: bytes) -> bool:
    """Verify the broadcast message had originated from a switcher device."""
    try:
        return hexlify(message)[0:4].decode() == "fef0" and len(message) == 165
    except Exception:
        return False


def get_ip(message: bytes) -> str:
    """Extract the IP address from the broadcast message."""
    hex_ip = hexlify(message)[152:160]
    ip_addr = int(hex_ip[6:8] + hex_ip[4:6] + hex_ip[2:4] + hex_ip[0:2], 16)
    return inet_ntoa(pack("<L", ip_addr))


def get_mac(message: bytes) -> str:
    """Extract the MAC address from the broadcast message."""
    hex_mac = hexlify(message)[160:172].decode().upper()
    return (
        hex_mac[0:2]
        + ":"
        + hex_mac[2:4]
        + ":"
        + hex_mac[4:6]
        + ":"
        + hex_mac[6:8]
        + ":"
        + hex_mac[8:10]
        + ":"
        + hex_mac[10:12]
    )


def get_name(message: bytes) -> str:
    """Extract the device name from the braodcast message."""
    return message[42:74].decode().rstrip("\x00")


def get_device_id(message: bytes) -> str:
    """Extract the device id from the broadcast message."""
    return hexlify(message)[36:42].decode()


def get_device_state(message: bytes) -> DeviceState:
    """Extract the device state from the broadcast message."""
    hex_device_state = hexlify(message)[266:270].decode()
    return (
        DeviceState.ON if hex_device_state == DeviceState.ON.value else DeviceState.OFF
    )


def get_auto_shutdown_value(message: bytes) -> str:
    """Extract the auto shutdown value from the broadcast message."""
    hex_auto_shutdown_val = hexlify(message)[310:318]
    int_auto_shutdown_val_secs = int(
        hex_auto_shutdown_val[6:8]
        + hex_auto_shutdown_val[4:6]
        + hex_auto_shutdown_val[2:4]
        + hex_auto_shutdown_val[0:2],
        16,
    )
    return seconds_to_iso_time(int_auto_shutdown_val_secs)


def get_power_consumption(message: bytes) -> int:
    """Extract the power consumption from the broadcast message."""
    hex_power_consumption = hexlify(message)[270:278]
    return int(hex_power_consumption[2:4] + hex_power_consumption[0:2], 16)


def get_remaining_time(message: bytes) -> str:
    """Extract the time remains for the current execution."""
    hex_remaining_time = hexlify(message)[294:302]
    int_remaining_time_seconds = int(
        hex_remaining_time[6:8]
        + hex_remaining_time[4:6]
        + hex_remaining_time[2:4]
        + hex_remaining_time[0:2],
        16,
    )
    return seconds_to_iso_time(int_remaining_time_seconds)


def get_device_type(message: bytes) -> DeviceType:
    """Extract the device type from the broadcast message."""
    hex_model = hexlify(message[75:76]).decode()
    devices = dict(map(lambda d: (d.hex_rep, d), DeviceType))
    return devices[hex_model]
