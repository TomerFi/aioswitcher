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

"""Switcher integration device module tools."""

import datetime
import ssl
import time
from base64 import b64decode
from binascii import crc_hqx, hexlify, unhexlify
from logging import getLogger
from struct import pack

import aiohttp
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from ..device import DeviceType

logger = getLogger(__name__)


def seconds_to_iso_time(all_seconds: int) -> str:
    """Convert seconds to iso time.

    Args:
        all_seconds: the total number of seconds to convert.

    Return:
        A string representing the converted iso time in %H:%M:%S format.
        e.g. "02:24:37".

    """
    minutes, seconds = divmod(int(all_seconds), 60)
    hours, minutes = divmod(minutes, 60)

    return datetime.time(hour=hours, minute=minutes, second=seconds).isoformat()


def sign_packet_with_crc_key(hex_packet: str) -> str:
    """Sign the packets with the designated crc key.

    Args:
        hex_packet: packet to sign.

    Return:
        The calculated and signed packet.

    """
    binary_packet = unhexlify(hex_packet)
    binary_packet_crc = pack(">I", crc_hqx(binary_packet, 0x1021))
    hex_packet_crc = hexlify(binary_packet_crc).decode()
    hex_packet_crc_sliced = hex_packet_crc[6:8] + hex_packet_crc[4:6]

    binary_key = unhexlify(hex_packet_crc_sliced + "30" * 32)
    binary_key_crc = pack(">I", crc_hqx(binary_key, 0x1021))
    hex_key_crc = hexlify(binary_key_crc).decode()
    hex_key_crc_sliced = hex_key_crc[6:8] + hex_key_crc[4:6]

    return hex_packet + hex_packet_crc_sliced + hex_key_crc_sliced


def minutes_to_hexadecimal_seconds(minutes: int) -> str:
    """Encode minutes to an hexadecimal packed as little endian unsigned int.

    Args:
        minutes: minutes to encode.

    Return:
        Hexadecimal representation of the minutes argument.

    """
    return hexlify(pack("<I", minutes * 60)).decode()


def timedelta_to_hexadecimal_seconds(full_time: datetime.timedelta) -> str:
    """Encode timedelta as seconds to an hexadecimal packed as little endian unsigned.

    Args:
        full_time: timedelta time between 1 and 24 hours, seconds are ignored.

    Return:
        Hexadecimal representation of the seconds built fom the full_time argument.

    """
    minutes = full_time.total_seconds() / 60
    hours, minutes = divmod(minutes, 60)
    seconds = int(hours) * 3600 + int(minutes) * 60

    if 3599 < seconds < 86341:
        return hexlify(pack("<I", int(seconds))).decode()

    raise ValueError("can only handle 1 to 24 hours")


def string_to_hexadecimale_device_name(name: str) -> str:
    """Encode string device name to an appropriate hexadecimal value.

    Args:
        name: the desired name for encoding.

    Return:
        Hexadecimal representation of the name argument.

    """
    length = len(name)
    if 1 < length < 33:
        hex_name = hexlify(name.encode())
        zeros_pad = ("00" * (32 - length)).encode()
        return (hex_name + zeros_pad).decode()
    raise ValueError("name length can vary from 2 to 32")


def current_timestamp_to_hexadecimal() -> str:
    """Generate hexadecimal representation of the current timestamp.

    Return:
        Hexadecimal representation of the current unix time retrieved by ``time.time``.

    """
    round_timestamp = int(round(time.time()))
    binary_timestamp = pack("<I", round_timestamp)
    hex_timestamp = hexlify(binary_timestamp)
    return hex_timestamp.decode()


def watts_to_amps(watts: int) -> float:
    """Convert power consumption to watts to electric current in amps."""
    return round((watts / float(220)), 1)


def set_message_length(message: str) -> str:
    """Set the message length."""
    length = "{:x}".format(len(unhexlify(message + "00000000"))).ljust(4, "0")
    return "fef0" + str(length) + message[8:]


def convert_str_to_devicetype(device_type: str) -> DeviceType:
    """Convert string name to DeviceType."""
    if device_type == DeviceType.MINI.value:
        return DeviceType.MINI
    elif device_type == DeviceType.POWER_PLUG.value:
        return DeviceType.POWER_PLUG
    elif device_type == DeviceType.TOUCH.value:
        return DeviceType.TOUCH
    elif device_type == DeviceType.V2_ESP.value:
        return DeviceType.V2_ESP
    elif device_type == DeviceType.V2_QCA.value:
        return DeviceType.V2_QCA
    elif device_type == DeviceType.V4.value:
        return DeviceType.V4
    elif device_type == DeviceType.BREEZE.value:
        return DeviceType.BREEZE
    elif device_type == DeviceType.RUNNER.value:
        return DeviceType.RUNNER
    elif device_type == DeviceType.RUNNER_MINI.value:
        return DeviceType.RUNNER_MINI
    elif device_type == DeviceType.RUNNER_S11.value:
        return DeviceType.RUNNER_S11
    elif device_type == DeviceType.RUNNER_S12.value:
        return DeviceType.RUNNER_S12
    elif device_type == DeviceType.LIGHT_SL01.value:
        return DeviceType.LIGHT_SL01
    elif device_type == DeviceType.LIGHT_SL01_MINI.value:
        return DeviceType.LIGHT_SL01_MINI
    elif device_type == DeviceType.LIGHT_SL02.value:
        return DeviceType.LIGHT_SL02
    elif device_type == DeviceType.LIGHT_SL02_MINI.value:
        return DeviceType.LIGHT_SL02_MINI
    return DeviceType.MINI


def convert_token_to_packet(token: str) -> str:
    """Convert a token to token packet.

    Args:
        token: the token of the user sent by Email

    Return:
        Token packet if token is valid,
        otherwise empty string or raise error.

    """
    try:
        token_key = b"jzNrAOjc%lpg3pVr5cF!5Le06ZgOdWuJ"
        encrypted_value = b64decode(bytes(token, "utf-8"))
        cipher = AES.new(token_key, AES.MODE_ECB)
        decrypted_value = cipher.decrypt(encrypted_value)
        unpadded_decrypted_value = unpad(decrypted_value, AES.block_size)
        return hexlify(unpadded_decrypted_value).decode()
    except (KeyError, ValueError) as ve:
        raise RuntimeError("convert token to packet was not successful") from ve


async def validate_token(username: str, token: str) -> bool:
    """Make an asynchronous API call to validate a Token by username and token."""
    request_url = "https://switcher.co.il/ValidateToken/"
    request_data = {"email": username, "token": token}
    is_token_valid = False
    # Preload the SSL context
    ssl_context = ssl.SSLContext()

    logger.debug("calling API call for Switcher to validate the token")

    async with aiohttp.ClientSession() as session:
        async with session.post(
            request_url, data=request_data, ssl=ssl_context
        ) as response:
            if response.status == 200:
                logger.debug("request successful")
                try:
                    response_json = await response.json()
                    result = response_json.get("result", None)
                    if result is not None:
                        is_token_valid = result.lower() == "true"
                except aiohttp.ContentTypeError:
                    logger.debug("response content is not valid JSON")
            else:
                logger.debug("request failed with status code: %s", response.status)

    return is_token_valid


# More info about get_shutter_discovery_packet_index
# and get_light_discovery_packet_index functions
# Those functions return the index of the circuit sub device,
#   used in retreving state from the packet.
# Used for Switcher Runners and Switcher Lights
# Runner and Runner Mini: has no lights circuits & one shutter circuits ->
#   shutter circuit is 0, get_light_discovery_packet_index would raise an error.
# Runner S11: has two lights circuits & one shutter circuits ->
#   Lights circuits are numbered 0 & 1, shutter circuit is 2.
# Runner S12: has one lights circuits & two shutter circuits ->
#   Lights circuit is 0, shutter circuits are numbered 1 & 2.
# Light SL01 and Light SL01 Mini: has one lights circuits & has no shutter circuits ->
#   Lights circuit is 0, get_shutter_discovery_packet_index would raise an error.
# Light SL02 and Light SL02 Mini: has two lights circuits & has no shutter circuits ->
#   Lights circuits are numbered 0 & 1,
#   get_shutter_discovery_packet_index would raise an error.
def get_shutter_discovery_packet_index(
    device_type: DeviceType, circuit_number: int
) -> int:
    """Return the correct shutter discovery packet index.

    Used in retriving the shutter position/direction from the packet
    (based of device type and circuit number).
    """
    if device_type != DeviceType.RUNNER_S12 and circuit_number != 0:
        raise ValueError("Invalid circuit number")
    if device_type == DeviceType.RUNNER_S12 and circuit_number not in [0, 1]:
        raise ValueError("Invalid circuit number")

    if device_type in (DeviceType.RUNNER, DeviceType.RUNNER_MINI):
        return 0
    elif device_type == DeviceType.RUNNER_S11:
        return 2
    elif device_type == DeviceType.RUNNER_S12:
        return circuit_number + 1

    raise ValueError("only shutters are allowed")


def get_light_discovery_packet_index(
    device_type: DeviceType, circuit_number: int
) -> int:
    """Return the correct light discovery packet index.

    Used in retriving the light on/off status from the packet
    (based of device type and circuit number).
    """
    if device_type in (
        DeviceType.RUNNER_S11,
        DeviceType.LIGHT_SL02,
        DeviceType.LIGHT_SL02_MINI,
    ):
        if circuit_number not in [0, 1]:
            raise ValueError("Invalid circuit number")
        return circuit_number
    if device_type in (
        DeviceType.RUNNER_S12,
        DeviceType.LIGHT_SL01,
        DeviceType.LIGHT_SL01_MINI,
    ):
        if circuit_number != 0:
            raise ValueError("Invalid circuit number")
        return 0

    raise ValueError("only devices that has lights are allowed")


def get_shutter_api_packet_index(device_type: DeviceType, circuit_number: int) -> int:
    """Return the correct shutter api packet index.

    Used in sending the shutter position/direction with the packet
    (based of device type and circuit number).
    """
    # We need to convert selected circuit number to actual place in the packet.
    # That is why we add + 1
    return get_shutter_discovery_packet_index(device_type, circuit_number) + 1


def get_light_api_packet_index(device_type: DeviceType, circuit_number: int) -> int:
    """Return the correct light api packet index.

    Used in sending the light on/off status with the packet
    (based of device type and circuit number).
    """
    # We need to convert selected circuit number to actual place in the packet.
    # That is why we add + 1
    return get_light_discovery_packet_index(device_type, circuit_number) + 1
