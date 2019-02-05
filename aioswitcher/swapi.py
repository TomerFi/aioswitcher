"""Switcher Manager Functions."""

from logging import getLogger
from socket import socket
from typing import Tuple, Optional
from datetime import timedelta
from aioswitcher.tools import (get_socket, get_timestamp,
                               close_socket_connection)
from aioswitcher.packets import handlers
from aioswitcher.packets.messages import SwitcherV2BaseResponseMSG

_LOGGER = getLogger(__name__)


# when return type hint is Tuple[...] and python version is < 3.6
# a false positive 'invalid-sequence-index' will be picked up by pylint
# for workaround, disable the error for the specific functions

# pylint: disable=invalid-sequence-index
async def _get_socket_and_timestamp(ip_address: str) -> Tuple[str, socket]:
    """Connect to socket and create timestamp."""
    sock = get_socket(ip_address)
    timestamp = get_timestamp()

    if sock is not None:
        return timestamp, sock

    raise Exception("failed to get socket connection")


async def _login_to_device(
    sock: socket, phone_id: str, device_id: str,
    device_password: str, timestamp: str) \
        -> Tuple[str, SwitcherV2BaseResponseMSG]:
    """Use for login to the switcher v2 device."""
    try:
        _LOGGER.debug("sending login packet")
        response = await handlers.send_login_packet(phone_id, device_password,
                                                    sock, timestamp)

        if response.successful:
            session_id = response.session_id
            _LOGGER.debug("login packet successful retreived session id "
                          + session_id + ", sending state packet")
            response2 = await handlers.send_get_state_packet(
                device_id, sock, timestamp, session_id)

            return session_id, response2

        return session_id, response

    except Exception as ex:
        raise Exception("failed login to device") from ex
# pylint: enable=invalid-sequence-index


async def get_state_of_device(
    ip_address: str, phone_id: str, device_id: str, device_password: str) \
        -> SwitcherV2BaseResponseMSG:
    """Use for getting the current state the switcher v2 device."""
    sock = None
    try:
        timestamp, sock = await _get_socket_and_timestamp(ip_address)
        # There is no use for the session id when only getting the state.
        # pylint: disable=unused-variable
        session_id, response = await _login_to_device(
            sock, phone_id, device_id, device_password, timestamp)
        # pylint: enable=unused-variable

        return response

    except Exception as ex:
        raise Exception("failed to control the device ") from ex

    finally:
        if sock is not None:
            close_socket_connection(sock)


# noqa'd flake8's 'E252' (missing whitespace around parameter equals),
# it contradicts pylint's 'C0326' (bad-whitespace).
async def send_command_to_device(
    ip_address: str, phone_id: str, device_id: str, device_password: str,
    cmd: str, timer: Optional[str]=None  # noqa E252
    ) -> SwitcherV2BaseResponseMSG:
    """Use for sending on/off/on+timer commands to the switcher v2 device."""
    sock = None
    try:
        timestamp, sock = await _get_socket_and_timestamp(ip_address)
        session_id, response = await _login_to_device(
            sock, phone_id, device_id, device_password, timestamp)

        if response.successful:
            _LOGGER.debug("sending control packet")
            response = await handlers.send_control_packet(
                device_id, phone_id, device_password, sock,
                timestamp, session_id, cmd, timer)

            if response.successful:
                _LOGGER.debug("control packet successful")

        return response

    except Exception as ex:
        raise Exception("failed to control the device ") from ex

    finally:
        if sock is not None:
            close_socket_connection(sock)


async def set_auto_off_to_device(
    ip_address: str, phone_id: str, device_id: str,
    device_password: str, full_time: timedelta) \
        -> SwitcherV2BaseResponseMSG:
    """Use for setting the auto-off on the switcher v2 device."""
    sock = None
    try:
        timestamp, sock = await _get_socket_and_timestamp(ip_address)
        session_id, response = await _login_to_device(
            sock, phone_id, device_id, device_password, timestamp)

        if response.successful:
            _LOGGER.debug("sending auto-off config packet")
            response = await handlers.send_set_auto_off_packet(
                device_id, phone_id, device_password, full_time,
                sock, timestamp, session_id)
            if response.successful:
                _LOGGER.debug("auto-off config packet successful")

        return response

    except Exception as ex:
        raise Exception("failed to set auto-off for the device") from ex
    finally:
        if sock is not None:
            close_socket_connection(sock)


async def update_name_of_device(ip_address: str, phone_id: str,
                                device_id: str, device_password: str,
                                name: str) -> SwitcherV2BaseResponseMSG:
    """Use for setting the name of the switcher v2 device."""
    sock = None
    try:
        timestamp, sock = await _get_socket_and_timestamp(ip_address)
        session_id, response = await _login_to_device(
            sock, phone_id, device_id, device_password, timestamp)

        if response.successful:
            _LOGGER.debug("sending name update packet")
            response = await handlers.send_update_name_packet(
                device_id, phone_id, device_password, name,
                sock, timestamp, session_id)
            if response.successful:
                _LOGGER.debug("name update packet successful")

        return response

    except Exception as ex:
        raise Exception("failed to update the name of the device ") from ex
    finally:
        if sock is not None:
            close_socket_connection(sock)


async def get_schedules(ip_address: str, phone_id: str, device_id: str,
                        device_password: str) -> SwitcherV2BaseResponseMSG:
    """Use for get the schedules from the switcher v2 device."""
    sock = None
    try:
        timestamp, sock = await _get_socket_and_timestamp(ip_address)
        session_id, response = await _login_to_device(
            sock, phone_id, device_id, device_password, timestamp)

        if response.successful:
            _LOGGER.debug("sending get schedule packet")
            response = await handlers.send_get_schedules_packet(
                device_id, phone_id, device_password,
                sock, timestamp, session_id)
            if response.successful:
                _LOGGER.debug("get schedule packet successful")

        return response

    except Exception as ex:
        raise Exception("failed to get schedules from the device") from ex
    finally:
        if sock is not None:
            close_socket_connection(sock)


async def disable_enable_schedule(
    ip_address: str, phone_id: str, device_id: str,
    device_password: str, schedule_data: str) \
        -> SwitcherV2BaseResponseMSG:
    """Use for enabling or disabling a schedule on the switcher v2 device."""
    sock = None
    try:
        timestamp, sock = await _get_socket_and_timestamp(ip_address)
        session_id, response = await _login_to_device(
            sock, phone_id, device_id, device_password, timestamp)

        if response.successful:
            _LOGGER.debug("sending disable enable schedule packet")
            response = await handlers.send_dis_ena_schedule_packet(
                device_id, phone_id, device_password,
                sock, timestamp, session_id, schedule_data)
            if response.successful:
                _LOGGER.debug("disable enable schedule packet successful")

        return response

    except Exception as ex:
        raise Exception("failed to disable enable the schedule") from ex
    finally:
        if sock is not None:
            close_socket_connection(sock)


async def delete_schedule(
    ip_address: str, phone_id: str, device_id: str,
    device_password: str, schedule_id: str) \
        -> SwitcherV2BaseResponseMSG:
    """Use for deleting a schedule on the switcher v2 device."""
    sock = None
    try:
        timestamp, sock = await _get_socket_and_timestamp(ip_address)
        session_id, response = await _login_to_device(
            sock, phone_id, device_id, device_password, timestamp)

        if response.successful:
            _LOGGER.debug("sending delete schedule packet")
            response = await handlers.send_delete_schedule_packet(
                device_id, phone_id, device_password,
                sock, timestamp, session_id, schedule_id)
            if response.successful:
                _LOGGER.debug("delete schedule packet successful")

        return response

    except Exception as ex:
        raise Exception("failed to delete the schedule") from ex
    finally:
        if sock is not None:
            close_socket_connection(sock)


async def create_schedule(
    ip_address: str, phone_id: str, device_id: str,
    device_password: str, schedule_data: str) \
        -> SwitcherV2BaseResponseMSG:
    """Use for creating a schedule on the switcher v2 device."""
    sock = None
    try:
        timestamp, sock = await _get_socket_and_timestamp(ip_address)
        session_id, response = await _login_to_device(
            sock, phone_id, device_id, device_password, timestamp)

        if response.successful:
            _LOGGER.debug("sending create schedule packet")
            response = await handlers.send_create_schedule_packet(
                device_id, phone_id, device_password, sock,
                timestamp, session_id, schedule_data)

        if response.successful:
            _LOGGER.debug("create schedule packet successful, "
                          + "sending get schedules packet")
            response2 = await handlers.send_get_schedules_packet(
                device_id, phone_id, device_password,
                sock, timestamp, session_id)
            if response2.successful:
                _LOGGER.debug("get schedules packet successful")
            return response2

        return response2

    except Exception as ex:
        raise Exception("failed to create the schedule") from ex
    finally:
        if sock is not None:
            close_socket_connection(sock)
