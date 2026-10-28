import os
import subprocess
from datetime import datetime, time

import patterns
from plan import check_start, plan_commits

FILENAME = "contributions.txt"


def ensure_file_exists():
    """Create the file if it doesn't exist."""
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w") as f:
            f.write("GitHub Contribution Log\n")


def create_commit(date, count):
    """Modify the file and commit the change multiple times."""
    for _ in range(count):  # Repeat based on commit count
        # Append a new entry to the file
        with open(FILENAME, "a") as f:
            f.write(f"Commit on {date.strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Stage the file
        subprocess.run(["git", "add", FILENAME], check=True)

        # Commit the file
        subprocess.run(
            ["git", "commit", "--date", date.isoformat(), "-m", "Contribution"], check=True
        )


def update_contributions(start_date, github_username, github_url):
    ensure_file_exists()

    # Built from patterns.py, so a new pattern shows up here without editing this line
    names = ", ".join(patterns.patterns)
    pattern_name = input(f"Enter the pattern name ({names}): ").strip().lower()
    pattern = patterns.get_pattern(pattern_name)

    if not pattern:
        print(f"Pattern '{pattern_name}' not found!")
        return

    for day, count in plan_commits(pattern, start_date.date()):
        # Commit at midnight, as version 1 did
        create_commit(datetime.combine(day, time()), count)

    # Push the commits to the repository
    # Create the URL with the token embedded

    token = input("Enter GitHub Token: ")
    repo_with_token_url = (
        f"https://{github_username}:{token}@{github_url[8:]}"  # Removes "https://"
    )

    # Run the git push command with the updated URL
    subprocess.run(["git", "push", repo_with_token_url], check=True)


if __name__ == "__main__":
    # Get start date from the user
    start_date_str = input("Enter the start date (YYYY-MM-DD): ")
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    # Stop before asking anything else if the date is not a Sunday
    try:
        check_start(start_date.date())
    except ValueError as error:
        raise SystemExit(error) from None

    ##github_username = input("GitHub User Name: ")
    # Get the GIT_USER environment variable
    github_username = os.environ.get("GIT_USER")

    if github_username:
        print(f"The Git user passed from Docker is: {github_username}")
        # You can now use the 'git_user' variable in your script's logic
    else:
        print("GIT_USER environment variable not set.")

    github_repo = input("Enter GitHub Repo for this user name: ")
    github_url = "https://github.com/" + github_username + "/" + github_repo + ".git"

    # Initialize the git repository if it doesn't exist
    if not os.path.exists(".git"):
        subprocess.run(["git", "init"], check=True)
        subprocess.run(
            [
                "git",
                "remote",
                "add",
                "origin",
                "https://github.com/" + github_username + "/" + github_repo + ".git",
            ],
            check=True,
        )

    update_contributions(start_date, github_username, github_url)
