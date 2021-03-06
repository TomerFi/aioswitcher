"""Common assertion tools for use with the Switcher integration test cases."""

# fmt: off
from typing import Any, List, Optional

from aioswitcher.api.messages import (ResponseMessageType,
                                      SwitcherV2BaseResponseMSG)

# fmt: on


async def assert_seconds_to_iso_time(
    total_seconds: int, iso_time: str
) -> None:
    """Use as assertion tool for comaring seconds to iso time %H:%M:%S."""
    time_split = iso_time.split(":")
    calc_seconds = (
        int(time_split[0]) * 3600
        + int(time_split[1]) * 60
        + int(time_split[2])
    )
    assert calc_seconds == total_seconds


async def assert_lists_equal(list1: List[Any], list2: List[Any]) -> None:
    """Compare two lists."""
    assert len(list1) == len(list2)
    for item in list1:
        assert item in list2


async def assert_api_messege_base_type(
    msg: Optional[SwitcherV2BaseResponseMSG], msg_type: ResponseMessageType
) -> None:
    """Assert the basic aioswitcher.api.messages.SwitcherV2BaseResponseMSG."""
    assert msg
    assert isinstance(msg.unparsed_response, bytes)
    assert msg.successful
    assert msg.msg_type == msg_type
