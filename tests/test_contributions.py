from datetime import date

from contributions import Day, parse_calendar


def answer(*days):
    """A GraphQL answer shaped like GitHub's, with one week holding these days."""
    week = {
        "contributionDays": [
            {"date": day, "contributionCount": count, "contributionLevel": level}
            for day, count, level in days
        ]
    }
    calendar = {"weeks": [week]}
    return {"data": {"user": {"contributionsCollection": {"contributionCalendar": calendar}}}}


def test_parse_calendar_reads_counts_and_levels():
    response = answer(
        ("2024-01-07", 0, "NONE"),
        ("2024-01-08", 1, "FIRST_QUARTILE"),
        ("2024-01-09", 5, "FOURTH_QUARTILE"),
    )
    assert parse_calendar(response) == {
        date(2024, 1, 7): Day(0, 0),
        date(2024, 1, 8): Day(1, 1),
        date(2024, 1, 9): Day(5, 4),
    }
