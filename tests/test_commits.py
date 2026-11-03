"""Runs against throwaway git repos in pytest's tmp_path, never this repo."""

import subprocess
from datetime import date

import pytest

from commits import check_ready, git, make_commits


def run(*args, cwd):
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)


@pytest.fixture
def repo(tmp_path):
    """A clone on main, level with its own bare 'GitHub' repo next to it."""
    origin, work = tmp_path / "origin.git", tmp_path / "work"
    run("init", "-q", "--bare", "-b", "main", str(origin), cwd=tmp_path)
    run("clone", "-q", str(origin), str(work), cwd=tmp_path)
    for key, value in [
        ("user.name", "Test"),
        ("user.email", "test@example.com"),
        ("commit.gpgsign", "false"),
    ]:
        run("config", key, value, cwd=work)
    run("switch", "-q", "-c", "main", cwd=work)
    run("commit", "-q", "--allow-empty", "-m", "start", cwd=work)
    run("push", "-q", "-u", "origin", "main", cwd=work)
    return str(work)


def test_commits_are_empty_and_dated_noon_utc(repo):
    plan = [(date(2024, 3, 4), 2), (date(2024, 3, 5), 1)]
    assert make_commits(plan, cwd=repo) == 3
    # A fixed date format, since git versions differ in how they print UTC
    stamp = "%Y-%m-%d %H:%M %z"
    log = git("log", "-3", f"--date=format:{stamp}", "--format=%s %ad / %cd", cwd=repo)
    assert log.splitlines() == [
        "Contribution 2024-03-05 12:00 +0000 / 2024-03-05 12:00 +0000",
        "Contribution 2024-03-04 12:00 +0000 / 2024-03-04 12:00 +0000",
        "Contribution 2024-03-04 12:00 +0000 / 2024-03-04 12:00 +0000",
    ]
    # Empty: no file changed in any of them
    assert git("diff", "--stat", "HEAD~3", "HEAD", cwd=repo) == ""


def test_ready_when_on_main_and_level(repo):
    check_ready(cwd=repo)


def test_not_ready_on_another_branch(repo):
    run("switch", "-q", "-c", "feature", cwd=repo)
    with pytest.raises(RuntimeError, match="switch to main"):
        check_ready(cwd=repo)


def test_not_ready_with_uncommitted_changes(repo, tmp_path):
    (tmp_path / "work" / "file.txt").write_text("x")
    run("add", "file.txt", cwd=repo)
    with pytest.raises(RuntimeError, match="uncommitted"):
        check_ready(cwd=repo)


def test_untracked_files_are_fine(repo, tmp_path):
    (tmp_path / "work" / "notes.txt").write_text("x")
    check_ready(cwd=repo)


def test_not_ready_with_unpushed_commits(repo):
    run("commit", "-q", "--allow-empty", "-m", "local", cwd=repo)
    with pytest.raises(RuntimeError, match="1 commits not on GitHub"):
        check_ready(cwd=repo)


def test_not_ready_when_behind(repo, tmp_path):
    other = tmp_path / "other"
    run("clone", "-q", str(tmp_path / "origin.git"), str(other), cwd=tmp_path)
    run("-c", "user.name=T", "-c", "user.email=t@e", "commit", "-q", "--allow-empty", "-m", "x",
        cwd=other)  # fmt: skip
    run("push", "-q", "origin", "main", cwd=other)
    with pytest.raises(RuntimeError, match="behind"):
        check_ready(cwd=repo)
