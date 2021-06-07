"""Working with weekdays test cases."""

from assertpy import assert_that

from aioswitcher import Weekday


def test_the_and_verify_monday_member_of_the_weekday_enum():
    """Verify Weekday.MONDAY returns the expected properties."""
    sut_day = Weekday.MONDAY
    assert_that(sut_day.value).is_equal_to("Monday")
    assert_that(sut_day.hex_rep()).is_equal_to(0x2)
    assert_that(sut_day.bit_rep()).is_equal_to(2)


def test_the_and_verify_tuesday_member_of_the_weekday_enum():
    """Verify Weekday.TUESDAY returns the expected properties."""
    sut_day = Weekday.TUESDAY
    assert_that(sut_day.value).is_equal_to("Tuesday")
    assert_that(sut_day.hex_rep()).is_equal_to(0x4)
    assert_that(sut_day.bit_rep()).is_equal_to(4)


def test_the_and_verify_wednesday_member_of_the_weekday_enum():
    """Verify Weekday.WEDNESDAY returns the expected properties."""
    sut_day = Weekday.WEDNESDAY
    assert_that(sut_day.value).is_equal_to("Wednesday")
    assert_that(sut_day.hex_rep()).is_equal_to(0x8)
    assert_that(sut_day.bit_rep()).is_equal_to(8)


def test_the_and_verify_thursday_member_of_the_weekday_enum():
    """Verify Weekday.THURSDAY returns the expected properties."""
    sut_day = Weekday.THURSDAY
    assert_that(sut_day.value).is_equal_to("Thursday")
    assert_that(sut_day.hex_rep()).is_equal_to(0x10)
    assert_that(sut_day.bit_rep()).is_equal_to(16)


def test_the_and_verify_friday_member_of_the_weekday_enum():
    """Verify Weekday.FRIDAY returns the expected properties."""
    sut_day = Weekday.FRIDAY
    assert_that(sut_day.value).is_equal_to("Friday")
    assert_that(sut_day.hex_rep()).is_equal_to(0x20)
    assert_that(sut_day.bit_rep()).is_equal_to(32)


def test_the_and_verify_saturday_member_of_the_weekday_enum():
    """Verify Weekday.SATURDAY returns the expected properties."""
    sut_day = Weekday.SATURDAY
    assert_that(sut_day.value).is_equal_to("Saturday")
    assert_that(sut_day.hex_rep()).is_equal_to(0x40)
    assert_that(sut_day.bit_rep()).is_equal_to(64)


def test_the_and_verify_sunday_member_of_the_weekday_enum():
    """Verify Weekday.SUNDAY returns the expected properties."""
    sut_day = Weekday.SUNDAY
    assert_that(sut_day.value).is_equal_to("Sunday")
    assert_that(sut_day.hex_rep()).is_equal_to(0x80)
    assert_that(sut_day.bit_rep()).is_equal_to(128)
