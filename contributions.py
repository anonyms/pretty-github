"""Reads the maintainer's real contribution graph from GitHub, for the preview.

Uses the gh CLI, so the login comes from `gh auth` and no token passes through this code.
Read only. parse_calendar is separate from the gh call so the tests need no network.
"""

import json
import subprocess
from dataclasses import dataclass
from datetime import date

QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        weeks { contributionDays { date contributionCount contributionLevel } }
      }
    }
  }
}
"""

# GitHub's names for the five shades, as levels 0-4
LEVELS = {
    "NONE": 0,
    "FIRST_QUARTILE": 1,
    "SECOND_QUARTILE": 2,
    "THIRD_QUARTILE": 3,
    "FOURTH_QUARTILE": 4,
}


# @dataclass writes __init__, == and repr from the fields; frozen=True makes it read only
@dataclass(frozen=True)
class Day:
    """One day on the real graph: how many contributions, and the shade GitHub gives it."""

    count: int
    level: int


def parse_calendar(response: dict) -> dict[date, Day]:
    """Turn the GraphQL answer into {day: Day}."""
    calendar = response["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    return {
        date.fromisoformat(day["date"]): Day(
            day["contributionCount"], LEVELS[day["contributionLevel"]]
        )
        for week in calendar["weeks"]
        for day in week["contributionDays"]
    }


def gh(*args: str) -> str:
    """Run gh and return its output; raise RuntimeError with gh's message if it fails."""
    try:
        result = subprocess.run(["gh", *args], capture_output=True, text=True, check=True)
    except FileNotFoundError:
        raise RuntimeError("gh is not installed") from None
    except subprocess.CalledProcessError as error:
        raise RuntimeError(error.stderr.strip() or f"gh {args[0]} failed") from None
    return result.stdout


def fetch_calendar(years: range) -> dict[date, Day]:
    """The real graph for these calendar years, for the account gh is logged in as."""
    login = gh("api", "user", "--jq", ".login").strip()
    days = {}
    # GitHub answers at most one year per query
    for year in years:
        answer = gh(
            "api", "graphql",
            "-F", f"login={login}",
            "-F", f"from={year}-01-01T00:00:00Z",
            "-F", f"to={year}-12-31T23:59:59Z",
            "-f", f"query={QUERY}",
        )  # fmt: skip
        days |= parse_calendar(json.loads(answer))
    return days
