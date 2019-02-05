"""Switcher Packet Handlers."""
from logging import getLogger
from binascii import unhexlify
from socket import socket
from typing import Optional
from datetime import timedelta

from aioswitcher.packets import messages

from aioswitcher.packets import formats
from aioswitcher.consts import (REMOTE_SESSION_ID, NO_TIMER_REQUESTED)

from aioswitcher.tools import (
    crc_sign_full_packet_com_key, convert_minutes_to_timer,
    convert_timedelta_to_auto_off, convert_string_to_device_name)

_LOGGER = getLogger(__name__)


# noqa'd flake8's 'E252' (missing whitespace around parameter equals),
# it contradicts pylint's 'C0326' (bad-whitespace).
async def send_login_packet(
    phone_id: str, device_password: str, sock: socket, timestamp: str,
    retry: int=3) -> messages.SwitcherV2LoginResponseMSG:  # noqa E252
    """Send login packet."""
    try:
        packet = crc_sign_full_packet_com_key(formats.LOGIN_PACKET.format(
            REMOTE_SESSION_ID, timestamp, phone_id, device_password))
        sock.send(unhexlify(packet))

        return messages.SwitcherV2LoginResponseMSG(sock.recv(1024))
    except Exception as ex:
        if retry > 0:
            _LOGGER.warning('failed to send login packet, retrying')
            return await send_login_packet(phone_id, device_password,
                                           sock, timestamp, retry - 1)
        else:
            raise Exception("failed to send login packet") from ex


async def send_get_state_packet(
    device_id: str, sock: socket, timestamp: str, session_id: str) \
        -> messages.SwitcherV2StateResponseMSG:
    """Send get state packet."""
    try:
        packet = crc_sign_full_packet_com_key(
            formats.GET_STATE_PACKET.format(session_id, timestamp, device_id))
        sock.send(unhexlify(packet))

        return messages.SwitcherV2StateResponseMSG(sock.recv(1024))
    except Exception as ex:
        raise Exception("failed to send state packet") from ex


# noqa'd flake8's 'E252' (missing whitespace around parameter equals),
# it contradicts pylint's 'C0326' (bad-whitespace).
async def send_control_packet(
    device_id: str, phone_id: str, device_password: str, sock: socket,
    timestamp: str, session_id: str, cmd: str,
    minutes_timer: Optional[str]=None  # noqa E252
    ) -> messages.SwitcherV2ControlResponseMSG:
    """Send control packet."""
    try:
        if minutes_timer is None:
            # No minutes_timer requested.
            packet = crc_sign_full_packet_com_key(
                formats.SEND_CONTROL_PACKET.format(
                    session_id, timestamp, device_id, phone_id,
                    device_password, cmd, NO_TIMER_REQUESTED))
        else:
            # Incorporate minutes_timer in packet.
            packet = crc_sign_full_packet_com_key(
                formats.SEND_CONTROL_PACKET.format(
                    session_id, timestamp, device_id, phone_id,
                    device_password, cmd,
                    convert_minutes_to_timer(minutes_timer)))

        sock.send(unhexlify(packet))
        return messages.SwitcherV2ControlResponseMSG(sock.recv(1024))
    except Exception as ex:
        raise Exception("failed to send control packet") from ex


async def send_set_auto_off_packet(
    device_id: str, phone_id: str, device_password: str, full_time: timedelta,
    sock: socket, timestamp: str, session_id: str) \
        -> messages.SwitcherV2SetAutoOffResponseMSG:
    """Send set auto-off packet."""
    try:
        packet = crc_sign_full_packet_com_key(
            formats.SET_AUTO_OFF_SET_PACKET.format(
                session_id, timestamp, device_id, phone_id, device_password,
                convert_timedelta_to_auto_off(full_time)))

        sock.send(unhexlify(packet))
        return messages.SwitcherV2SetAutoOffResponseMSG(sock.recv(1024))
    except Exception as ex:
        raise Exception("failed to send set auto-off packet ") from ex


async def send_update_name_packet(
    device_id: str, phone_id: str, device_password: str, name: str,
    sock: socket, timestamp: str, session_id: str) \
        -> messages.SwitcherV2UpdateNameResponseMSG:
    """Send set auto-off packet."""
    try:
        packet = crc_sign_full_packet_com_key(
            formats.UPDATE_DEVICE_NAME_PACKET.format(
                session_id, timestamp, device_id, phone_id, device_password,
                convert_string_to_device_name(name)))

        sock.send(unhexlify(packet))
        return messages.SwitcherV2UpdateNameResponseMSG(sock.recv(1024))
    except Exception as ex:
        raise Exception("failed to send update name packet") from ex


async def send_get_schedules_packet(
    device_id: str, phone_id: str, device_password: str, sock: socket,
    timestamp: str, session_id: str) \
        -> messages.SwitcherV2GetScheduleResponseMSG:
    """Send get schedule packet."""
    try:
        packet = crc_sign_full_packet_com_key(
            formats.GET_SCHEDULES_PACKET.format(
                session_id, timestamp, device_id, phone_id, device_password))

        sock.send(unhexlify(packet))
        return messages.SwitcherV2GetScheduleResponseMSG(sock.recv(1024))
    except Exception as ex:
        raise Exception("failed to send get schedules packet") from ex


async def send_dis_ena_schedule_packet(
    device_id: str, phone_id: str, device_password: str,
    sock: socket, timestamp: str, session_id: str, schedule_data: str) \
        -> messages.SwitcherV2DisableEnableScheduleResponseMSG:
    """Send disable enable schedule packet."""
    try:
        packet = crc_sign_full_packet_com_key(
            formats.DISABLE_ENABLE_SCHEDULE_PACKET.format(
                session_id, timestamp, device_id, phone_id,
                device_password, schedule_data))

        sock.send(unhexlify(packet))
        return messages.SwitcherV2DisableEnableScheduleResponseMSG(
            sock.recv(1024))
    except Exception as ex:
        raise Exception("failed to send disable enable schedule packet") \
            from ex


async def send_delete_schedule_packet(
    device_id: str, phone_id: str, device_password: str, sock: socket,
    timestamp: str, session_id: str, schedule_id: str) \
        -> messages.SwitcherV2DeleteScheduleResponseMSG:
    """Send delete schedule packet."""
    try:
        packet = crc_sign_full_packet_com_key(
            formats.DELETE_SCHEDULE_PACKET.format(
                session_id, timestamp, device_id, phone_id,
                device_password, schedule_id))
        sock.send(unhexlify(packet))

        return messages.SwitcherV2DeleteScheduleResponseMSG(sock.recv(1024))
    except Exception as ex:
        raise Exception("failed to send delete schedule packet") from ex


async def send_create_schedule_packet(
    device_id: str, phone_id: str, device_password: str, sock: socket,
    timestamp: str, session_id: str, schedule_data: str) \
        -> messages.SwitcherV2CreateScheduleResponseMSG:
    """Send create schedule packet."""
    try:
        packet = crc_sign_full_packet_com_key(
            formats.CREATE_SCHEDULE_PACKET.format(
                session_id, timestamp, device_id, phone_id,
                device_password, schedule_data))
        sock.send(unhexlify(packet))

        return messages.SwitcherV2CreateScheduleResponseMSG(sock.recv(1024))
    except Exception as ex:
        raise Exception("failed to send create schedule packet") from ex
