"""Shows a plan as the contribution graph in the terminal, before anything is committed.

Run with `make preview PATTERN=heart START=2024-01-07`. Uses plan_commits, so it shows
exactly the days and counts the commit step would make. Shows the real graph now (GitHub's
own shades) and after the commits (shades estimated: GitHub's rule is not documented).
"""

import math
import os
import sys
from datetime import date, datetime, timedelta

import patterns
from contributions import Day, fetch_calendar
from plan import plan_commits

# GitHub's dark-theme greens, from level 0 (no commits) to 4 (busiest)
COLOURS = ["#2d333b", "#0e4429", "#006d32", "#26a641", "#39d353"]
WEEKDAY_LABELS = ["", "Mon", "", "Wed", "", "Fri", ""]

# A grid is 7 rows (Sunday first) of weeks; None is a day outside the year shown
Grid = list[list[int | None]]


def year_grid(
    plan: list[tuple[date, int]], year: int, last_day: date | None = None
) -> tuple[date, Grid]:
    """Values per day for the year, as the graph lays it out, plus the first column's Sunday.

    Runs past 31 December if the plan does, so a drawing is never cut off. Passing last_day
    fixes the end instead, so the grids of the real graph line up with the pattern's.
    """
    first_day = date(year, 1, 1)
    if last_day is None:
        last_day = max([date(year, 12, 31)] + [day for day, _ in plan])
    # isoweekday() is 7 for Sunday, so % 7 gives days since the last Sunday
    first_sunday = first_day - timedelta(days=first_day.isoweekday() % 7)
    weeks = (last_day - first_sunday).days // 7 + 1

    counts = dict(plan)
    grid: Grid = [[None] * weeks for _ in range(7)]
    for week in range(weeks):
        for weekday in range(7):
            day = first_sunday + timedelta(weeks=week, days=weekday)
            if first_day <= day <= last_day:
                grid[weekday][week] = counts.get(day, 0)
    return first_sunday, grid


def combine(plan: list[tuple[date, int]], real: dict[date, Day]) -> list[tuple[date, int]]:
    """Contributions per day once the plan is committed: the real counts plus the plan."""
    totals = {day: real_day.count for day, real_day in real.items()}
    for day, count in plan:
        totals[day] = totals.get(day, 0) + count
    return sorted(totals.items())


def levels(grid: Grid) -> Grid:
    """Turn commit counts into shades 0-4, relative to the busiest day, as GitHub does."""
    busiest = max((count for row in grid for count in row if count), default=0)
    return [
        [None if count is None else math.ceil(4 * count / busiest) if count else 0 for count in row]
        for row in grid
    ]


def month_header(first_sunday: date, grid: Grid) -> str:
    """Month names above the column where each month starts, like the real graph."""
    weeks = len(grid[0])
    header = [" "] * (2 * weeks)
    previous = None
    for week in range(weeks):
        # A month starts in the first column whose last shown day is in it
        last_shown = max(weekday for weekday in range(7) if grid[weekday][week] is not None)
        month = (first_sunday + timedelta(weeks=week, days=last_shown)).month
        # Skip a label that would overwrite the one before it
        if month != previous and header[2 * week] == " ":
            header[2 * week : 2 * week + 3] = f"{date(2000, month, 1):%b}"
        previous = month
    return "    " + "".join(header).rstrip()


def cell(level: int | None, colour: bool) -> str:
    if level is None:
        return "  "
    if not colour:
        return ("." if level == 0 else str(level)) + " "
    red, green, blue = (int(COLOURS[level][i : i + 2], 16) for i in (1, 3, 5))
    # ANSI escape: draw the square in this RGB colour, then reset
    return f"\x1b[38;2;{red};{green};{blue}m■\x1b[0m "


def render(first_sunday: date, shades: Grid, colour: bool = True) -> str:
    """The graph as text: month header, then one line per weekday."""
    lines = [month_header(first_sunday, shades)]
    for label, row in zip(WEEKDAY_LABELS, shades, strict=True):
        lines.append(f"{label:<4}" + "".join(cell(level, colour) for level in row).rstrip())
    legend = "".join(cell(level, colour) for level in range(5))
    lines.append(f"\n    Less {legend}More")
    return "\n".join(lines)


def read_args(argv: list[str], command: str) -> tuple[str, date, list[tuple[date, int]]]:
    """Pattern name, start date and plan from PATTERN and START; exits with a message if wrong.

    Shared with `make commits`, so both refuse the same input.
    """
    if len(argv) != 2:
        raise SystemExit(f"Usage: make {command} PATTERN=heart START=2024-01-07")
    name, start_text = argv
    pattern = patterns.get_pattern(name)
    if pattern is None:
        raise SystemExit(f"Pattern '{name}' not found. Known: {', '.join(patterns.patterns)}")
    start = datetime.strptime(start_text, "%Y-%m-%d").date()
    try:
        plan = plan_commits(pattern, start)
    except ValueError as error:
        raise SystemExit(error) from None
    return name, start, plan


def show(name: str, start: date, plan: list[tuple[date, int]]) -> None:
    """Print the graph now and after the plan, or the pattern alone if gh is not available."""
    last_day = max(date(start.year, 12, 31), plan[-1][0])
    try:
        real = fetch_calendar(range(start.year, last_day.year + 1))
    except RuntimeError as error:
        print(f"Could not read your graph from GitHub ({error}); showing the pattern alone.\n")
        real = None

    # Windows may default to cp1252, which has no ■; an empty os.system call switches on
    # colour codes in the old Windows console
    sys.stdout.reconfigure(encoding="utf-8")
    if os.name == "nt":
        os.system("")
    colour = sys.stdout.isatty()

    if real is None:
        first_sunday, grid = year_grid(plan, start.year, last_day)
        print(render(first_sunday, levels(grid), colour))
    else:
        real_levels = [(day, real_day.level) for day, real_day in real.items()]
        first_sunday, now = year_grid(real_levels, start.year, last_day)
        _, after = year_grid(combine(plan, real), start.year, last_day)
        print("Now, with GitHub's own shades")
        print(render(first_sunday, now, colour))
        print("\nAfter the commits, shades estimated (GitHub may differ)")
        print(render(first_sunday, levels(after), colour))
        busy = [day for day, _ in plan if day in real and real[day].count]
        if busy:
            print(f"\nLands on {len(busy)} days that already have contributions, first {busy[0]}")
        else:
            print("\nNo overlap with existing contributions")
    total = sum(count for _, count in plan)
    print(f"\n{name}: {total} commits on {len(plan)} days, {plan[0][0]} to {plan[-1][0]}")


def main(argv: list[str]) -> None:
    show(*read_args(argv, "preview"))


if __name__ == "__main__":
    main(sys.argv[1:])
