"""The patterns that can be drawn, read from one text file each in the patterns/ folder.

A file is 7 lines, Sunday to Saturday: a digit is the number of commits that day, a dot is
none. Dots rather than spaces, because editors often strip trailing spaces and the rows
would no longer line up. Lines starting with # are comments.
"""

from pathlib import Path

FOLDER = Path(__file__).parent / "patterns"


def read_pattern(path: Path) -> list[str]:
    """The 7 rows of one pattern file, dots turned into spaces; ValueError if malformed."""
    lines = path.read_text(encoding="utf-8").splitlines()
    rows = [line.rstrip() for line in lines if line.strip() and not line.startswith("#")]
    if len(rows) != 7:
        raise ValueError(f"{path.name}: needs 7 rows (Sunday to Saturday), has {len(rows)}")
    if len({len(row) for row in rows}) != 1:
        raise ValueError(f"{path.name}: rows must all be the same width (blanks are dots)")
    if any(char != "." and not char.isdigit() for row in rows for char in row):
        raise ValueError(f"{path.name}: use only digits and dots")
    return [row.replace(".", " ") for row in rows]


def load_patterns(folder: Path = FOLDER) -> dict[str, list[str]]:
    """Every pattern in the folder, by file name without .txt, in alphabetical order."""
    return {path.stem: read_pattern(path) for path in sorted(folder.glob("*.txt"))}


patterns = load_patterns()


def get_pattern(name):
    return patterns.get(name)
