"""Common assertion tools for use with the Switcher integration test cases."""


async def assert_seconds_to_iso_time(total_seconds: int,
                                     iso_time: str) -> None:
    """Use as assertion tool for comaring seconds to iso time %H:%M:%S."""
    time_split = iso_time.split(':')
    calc_seconds = (int(time_split[0]) * 3600
                    + int(time_split[1]) * 60
                    + int(time_split[2]))
    assert calc_seconds == total_seconds
