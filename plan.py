"""Turns a pattern and a start date into the commits to make: (day, number of commits).

The one place that knows how a pattern maps onto the contribution graph, so the preview
and the commit step can never disagree. No git and no network, so it is easy to test.
"""

from datetime import date, timedelta

# date.weekday() counts Monday as 0, so Sunday is 6
SUNDAY = 6


def check_start(start: date) -> None:
    """Raise ValueError unless start is a Sunday, the top row of the graph."""
    if start.weekday() != SUNDAY:
        raise ValueError(f"{start} is a {start:%A}; the pattern's top-left cell must be a Sunday")


def plan_commits(pattern: list[str], start: date) -> list[tuple[date, int]]:
    """List (day, commits) for every digit in the pattern, in date order."""
    check_start(start)
    plan = []
    # Each column is a week and each row a weekday (Sunday first), so walk column by
    # column to get the days in date order
    for week in range(len(pattern[0])):
        for weekday, row in enumerate(pattern):
            char = row[week]
            # A space or 0 means no commits that day
            if char.isdigit() and char != "0":
                plan.append((start + timedelta(weeks=week, days=weekday), int(char)))
    return plan
