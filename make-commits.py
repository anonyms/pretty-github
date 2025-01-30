import os
import subprocess
from datetime import datetime, timedelta

# Define the pattern for a smiley face
pattern = [
    "  121  ",
    " 1   1 ",
    "1  2  1",
    "1     1",
    " 1   1 ",
    "  121  "
]

FILENAME = "contributions.txt"

def ensure_file_exists():
    """Create the file if it doesn't exist."""
    if not os.path.exists(FILENAME):
        with open(FILENAME, 'w') as f:
            f.write("GitHub Contribution Log\n")

def create_commit(date, count):
    """Modify the file and commit the change multiple times."""
    for _ in range(count):  # Repeat based on commit count
        # Append a new entry to the file
        with open(FILENAME, 'a') as f:
            f.write(f"Commit on {date.strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Stage the file
        subprocess.run(["git", "add", FILENAME], check=True)

        # Commit the file
        subprocess.run(["git", "commit", "--date", date.isoformat(), "-m", "Contribution"], check=True)


def update_contributions(start_date,github_username, github_url):
    ensure_file_exists()
    current_date = start_date
    
    for row in pattern:
        for char in row:
            if char.isdigit():  # Check if it's a number
                commit_count = int(char)
                create_commit(current_date, commit_count)
            current_date += timedelta(days=1)

    # Push the commits to the repository
    # Create the URL with the token embedded

    token = input("Enter GitHub Token: ")
    repo_with_token_url = f"https://{github_username}:{token}@{github_url[8:]}"  # Removes "https://"

    # Run the git push command with the updated URL
    subprocess.run(["git", "push", repo_with_token_url], check=True)

if __name__ == "__main__":
    # Get start date from the user
    start_date_str = input("Enter the start date (YYYY-MM-DD): ")
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")

    github_username = input("GitHub User Name: ")
    github_repo = input("Enter GitHub Repo for this user name: ")
    github_url = "https://github.com/"+github_username+"/"+github_repo+".git"

    # Initialize the git repository if it doesn't exist
    if not os.path.exists(".git"):
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "remote", "add", "origin", "https://github.com/"+github_username+"/"+github_repo+".git"], check=True)

    update_contributions(start_date, github_username, github_url)