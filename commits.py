"""Makes the planned commits on main and pushes them: the step behind `make commits`.

Shows the same preview as `make preview`, then asks before committing and again before
pushing. The commits are empty, so no file changes, and dated at noon UTC so the day cannot
slip in any timezone. Pushes with git's stored login; no token is asked for.
"""

import os
import subprocess
import sys
from datetime import UTC, date, datetime, time

import preview

MESSAGE = "Contribution"
NOON_UTC = time(12, tzinfo=UTC)


def git(*args: str, cwd: str | None = None, env: dict | None = None) -> str:
    """Run git and return its output; raise RuntimeError with git's message if it fails."""
    try:
        result = subprocess.run(
            ["git", *args], cwd=cwd, env=env, capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError as error:
        raise RuntimeError(error.stderr.strip() or f"git {args[0]} failed") from None
    return result.stdout.strip()


def check_ready(cwd: str | None = None) -> None:
    """Raise RuntimeError unless we are on main, with no changes, level with GitHub.

    Level with GitHub keeps the undo simple and the push a plain fast-forward.
    """
    branch = git("branch", "--show-current", cwd=cwd)
    if branch != "main":
        raise RuntimeError(f"On branch '{branch}'; switch to main first (git switch main)")
    # Untracked files don't matter: the commits are empty
    if git("status", "--porcelain", "--untracked-files=no", cwd=cwd):
        raise RuntimeError("main has uncommitted changes; commit or stash them first")
    git("fetch", "-q", "origin", cwd=cwd)
    behind = int(git("rev-list", "--count", "HEAD..origin/main", cwd=cwd))
    if behind:
        raise RuntimeError(f"main is {behind} commits behind GitHub; run git pull first")
    ahead = int(git("rev-list", "--count", "origin/main..HEAD", cwd=cwd))
    if ahead:
        raise RuntimeError(f"main has {ahead} commits not on GitHub; push or drop them first")


def make_commits(plan: list[tuple[date, int]], cwd: str | None = None) -> int:
    """Make the planned empty commits at noon UTC on each day; return how many were made."""
    total = sum(count for _, count in plan)
    made = 0
    for day, count in plan:
        stamp = datetime.combine(day, NOON_UTC).isoformat()
        # Both dates: GitHub uses the author date, git log and the web view show the committer's
        env = os.environ | {"GIT_AUTHOR_DATE": stamp, "GIT_COMMITTER_DATE": stamp}
        for _ in range(count):
            git("commit", "--allow-empty", "-q", "-m", MESSAGE, cwd=cwd, env=env)
            made += 1
            # \r returns to the start of the line, so the counter updates in place
            print(f"\r{made}/{total} commits", end="", flush=True)
    print()
    return made


def ask(question: str) -> bool:
    """True only for y or yes; anything else, or no input at all, is no."""
    try:
        return input(f"{question} [y/N] ").strip().lower() in ("y", "yes")
    except EOFError:
        return False


def main(argv: list[str]) -> None:
    name, start, plan = preview.read_args(argv, "commits")
    try:
        check_ready()
    except RuntimeError as error:
        raise SystemExit(error) from None

    preview.show(name, start, plan)
    email = git("config", "user.email")
    print(f"\nAuthor: {email}. GitHub only counts the commits if this email is verified")
    print("on your account (Settings > Emails).")

    total = sum(count for _, count in plan)
    if not ask(f"\nMake {total} commits on main?"):
        raise SystemExit("Nothing changed.")
    before = git("rev-parse", "--short", "HEAD")
    # Printed first, so it is on screen even if the run stops halfway
    print(f"To undo before pushing: git reset --keep {before}")
    make_commits(plan)

    if not ask("Push to GitHub?"):
        raise SystemExit(
            f"Not pushed. Push later with git push, or undo: git reset --keep {before}"
        )
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("Pushed. The graph on your profile can take a few minutes to update.")


if __name__ == "__main__":
    main(sys.argv[1:])
