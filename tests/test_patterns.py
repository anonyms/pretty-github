import pytest

import patterns


def test_known_pattern_is_returned():
    assert patterns.get_pattern("batman") is not None


def test_unknown_pattern_is_none():
    assert patterns.get_pattern("does-not-exist") is None


# parametrize runs the test once per pattern, so a failure names the broken one
@pytest.mark.parametrize("name", sorted(patterns.patterns))
def test_pattern_is_seven_rows_of_equal_width(name):
    rows = patterns.get_pattern(name)
    assert len(rows) == 7, "one row per weekday, Sunday to Saturday"
    assert len({len(row) for row in rows}) == 1, "all rows must be the same width"
    assert all(char == " " or char.isdigit() for row in rows for char in row)
