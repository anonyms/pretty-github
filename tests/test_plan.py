from datetime import date

import pytest

import patterns
from plan import plan_commits

SUNDAY = date(2024, 1, 7)


def test_rows_are_weekdays_from_sunday():
    pattern = ["1", "2", "3", "4", "5", "6", "7"]
    assert plan_commits(pattern, SUNDAY) == [
        (date(2024, 1, 7), 1),  # Sunday
        (date(2024, 1, 8), 2),
        (date(2024, 1, 9), 3),
        (date(2024, 1, 10), 4),
        (date(2024, 1, 11), 5),
        (date(2024, 1, 12), 6),
        (date(2024, 1, 13), 7),  # Saturday
    ]


def test_columns_are_weeks_and_blanks_are_skipped():
    pattern = ["1 2", "   ", "   ", "   ", "   ", "   ", "  3"]
    assert plan_commits(pattern, SUNDAY) == [
        (date(2024, 1, 7), 1),
        (date(2024, 1, 21), 2),  # third column = two weeks later
        (date(2024, 1, 27), 3),  # its Saturday
    ]


def test_zero_means_no_commits():
    pattern = ["0", " ", " ", " ", " ", " ", " "]
    assert plan_commits(pattern, SUNDAY) == []


def test_start_must_be_a_sunday():
    with pytest.raises(ValueError, match="Sunday"):
        plan_commits(patterns.get_pattern("heart"), date(2024, 1, 8))


@pytest.mark.parametrize("name", sorted(patterns.patterns))
def test_every_digit_of_every_pattern_is_planned(name):
    pattern = patterns.get_pattern(name)
    total = sum(int(char) for row in pattern for char in row if char.isdigit())
    assert sum(count for _, count in plan_commits(pattern, SUNDAY)) == total
