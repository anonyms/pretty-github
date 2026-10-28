from datetime import date

import patterns
from contributions import Day
from plan import plan_commits
from preview import combine, levels, month_header, render, year_grid


def test_year_starts_on_the_sunday_before_new_year():
    # 1 January 2024 is a Monday, so the first column starts on Sunday 31 December 2023
    first_sunday, grid = year_grid([], 2024)
    assert first_sunday == date(2023, 12, 31)
    assert grid[0][0] is None  # 31 December 2023 is not shown
    assert grid[1][0] == 0  # 1 January 2024 is
    assert len(grid[0]) == 53


def test_plan_counts_land_on_their_day():
    plan = plan_commits(patterns.get_pattern("heart"), date(2024, 1, 7))
    first_sunday, grid = year_grid(plan, 2024)
    for day, count in plan:
        week, weekday = divmod((day - first_sunday).days, 7)
        assert grid[weekday][week] == count
    assert sum(count for row in grid for count in row if count) == 24


def test_grid_runs_past_new_year_when_the_plan_does():
    plan = plan_commits(patterns.get_pattern("batman"), date(2024, 12, 1))
    first_sunday, grid = year_grid(plan, 2024)
    last_day, _ = plan[-1]
    assert last_day.year == 2025
    week, weekday = divmod((last_day - first_sunday).days, 7)
    assert grid[weekday][week] == 4


def test_levels_are_relative_to_the_busiest_day():
    grid = [[None, 0, 1, 2, 5]] + [[0] * 5 for _ in range(6)]
    assert levels(grid)[0] == [None, 0, 1, 2, 4]


def test_month_labels_sit_where_the_month_starts():
    first_sunday, grid = year_grid([], 2024)
    header = month_header(first_sunday, grid)
    assert header.startswith("    Jan")
    # February 2024 starts on a Thursday, in the column of Sunday 28 January (week 4)
    assert header.index("Feb") == 4 + 2 * 4
    # The last column holds 29-31 December only, so no January label at the end
    assert header.rstrip().endswith("Dec")


def test_render_without_colour():
    shades = [[1, 0]] + [[0, 0] for _ in range(5)] + [[None, 4]]
    lines = render(date(2024, 1, 7), shades, colour=False).splitlines()
    assert lines[1] == "    1 ."
    assert lines[2] == "Mon . ."
    assert lines[7] == "      4"


def test_combine_adds_the_plan_to_the_real_counts():
    real = {date(2024, 1, 8): Day(2, 2), date(2024, 1, 9): Day(0, 0)}
    plan = [(date(2024, 1, 8), 1), (date(2024, 1, 10), 3)]
    assert combine(plan, real) == [
        (date(2024, 1, 8), 3),
        (date(2024, 1, 9), 0),
        (date(2024, 1, 10), 3),
    ]


def test_last_day_fixes_the_end_of_the_grid():
    # Real data for a whole second year must not widen the grid past the pattern's end
    real = [(date(2025, 12, 31), 4)]
    _, grid = year_grid(real, 2024, last_day=date(2024, 12, 31))
    assert len(grid[0]) == 53
