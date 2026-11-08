"""Draws the pictures in the README from the pattern files: `make gallery`.

docs/gallery.svg shows every pattern, docs/example.svg a year of the graph with a few
patterns on it. Both are made with the same functions as the preview, so they show what
the preview and the commits would. A test fails when they are out of date.
"""

from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

import patterns
from plan import plan_commits
from preview import COLOURS, levels, year_grid

DOCS = Path(__file__).parent / "docs"
BACKGROUND = "#0d1117"  # GitHub's dark page
TEXT = "#c9d1d9"
CELL, GAP = 10, 3  # square size and spacing, in pixels, as on the real graph
STEP = CELL + GAP
FONT = 'font-family="-apple-system, Segoe UI, Helvetica, Arial, sans-serif" font-size="12"'

# The example: a year, and which patterns go on which week column
EXAMPLE_YEAR = 2022
EXAMPLE = [("star", 3), ("space-invader", 14), ("pacman", 29)]


def squares(shades: list[list[int | None]], left: int, top: int) -> list[str]:
    """One <rect> per shown day; None (outside the year) is left out."""
    return [
        f'<rect x="{left + week * STEP}" y="{top + weekday * STEP}" width="{CELL}" '
        f'height="{CELL}" rx="2" fill="{COLOURS[level]}"/>'
        for weekday, row in enumerate(shades)
        for week, level in enumerate(row)
        if level is not None
    ]


def svg(width: int, height: int, body: list[str]) -> str:
    return "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}">',
            f'<rect width="{width}" height="{height}" rx="6" fill="{BACKGROUND}"/>',
            *body,
            "</svg>\n",
        ]
    )


def gallery_svg(all_patterns: dict[str, list[str]], width: int = 820) -> str:
    """Every pattern as a tile with its name, laid out left to right in rows."""
    margin, spacing, label = 16, 28, 20
    tile_height = 7 * STEP + label
    body, x, y = [], margin, margin
    for name, rows in all_patterns.items():
        # Digits as counts, spaces as 0, shaded relative to the pattern's busiest day
        counts = [[int(char) if char.strip() else 0 for char in row] for row in rows]
        tile_width = max(len(rows[0]) * STEP, len(name) * 7)
        if x + tile_width > width - margin:
            x, y = margin, y + tile_height + spacing
        body += squares(levels(counts), x, y)
        body.append(
            f'<text x="{x}" y="{y + 7 * STEP + 13}" fill="{TEXT}" {FONT}>{escape(name)}</text>'
        )
        x += tile_width + spacing
    return svg(width, y + tile_height + margin, body)


def example_svg(all_patterns: dict[str, list[str]]) -> str:
    """A year of the graph with the EXAMPLE patterns on it, with month names."""
    first_day = date(EXAMPLE_YEAR, 1, 1)
    first_sunday = date.fromordinal(first_day.toordinal() - first_day.isoweekday() % 7)
    plan = []
    for name, week in EXAMPLE:
        start = date.fromordinal(first_sunday.toordinal() + 7 * week)
        plan += plan_commits(all_patterns[name], start)
    _, grid = year_grid(plan, EXAMPLE_YEAR)
    shades = levels(grid)

    left, top, margin = 40, 34, 16
    body = []
    previous = None
    for week in range(len(grid[0])):
        # Label a month at the first column whose Saturday is in it, like the real graph
        saturday = date.fromordinal(first_sunday.toordinal() + 7 * week + 6)
        if saturday.month != previous and saturday.year == EXAMPLE_YEAR:
            x = left + week * STEP
            body.append(f'<text x="{x}" y="{top - 8}" fill="{TEXT}" {FONT}>{saturday:%b}</text>')
        previous = saturday.month
    for weekday, label in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        y = top + weekday * STEP + CELL - 1
        body.append(f'<text x="{margin}" y="{y}" fill="{TEXT}" {FONT}>{label}</text>')
    body += squares(shades, left, top)
    width = left + len(grid[0]) * STEP + margin
    return svg(width, top + 7 * STEP + margin, body)


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    # newline="\n" keeps LF on Windows too
    (DOCS / "gallery.svg").write_text(gallery_svg(patterns.patterns), "utf-8", newline="\n")
    (DOCS / "example.svg").write_text(example_svg(patterns.patterns), "utf-8", newline="\n")
    print(f"Wrote {DOCS / 'gallery.svg'} and {DOCS / 'example.svg'}")


if __name__ == "__main__":
    main()
