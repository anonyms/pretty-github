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


def write(folder, name, text):
    path = folder / f"{name}.txt"
    path.write_text(text, encoding="utf-8")
    return path


def test_dots_are_blanks_and_comments_are_skipped(tmp_path):
    write(tmp_path, "dot", "# one commit on Monday\n.\n1\n.\n.\n.\n.\n.\n")
    assert patterns.load_patterns(tmp_path) == {"dot": [" ", "1", " ", " ", " ", " ", " "]}


@pytest.mark.parametrize(
    "text, problem",
    [
        ("1\n1\n1\n", "7 rows"),
        ("11\n1\n1\n1\n1\n1\n1\n", "same width"),
        ("x\n1\n1\n1\n1\n1\n1\n", "digits and dots"),
        # Spaces instead of dots: trailing ones get stripped, which is why dots are used
        ("1 \n1 \n1 \n1 \n1 \n1 \n11\n", "blanks are dots"),
        ("1 1\n111\n111\n111\n111\n111\n111\n", "digits and dots"),
    ],
)
def test_malformed_file_names_the_problem(tmp_path, text, problem):
    path = write(tmp_path, "bad", text)
    with pytest.raises(ValueError, match=f"bad.txt: .*{problem}"):
        patterns.read_pattern(path)
