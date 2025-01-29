import os
import subprocess
from datetime import datetime, timedelta

# Define the pattern for a smiley face
pattern = [
    "     000      ",
    "   0     0    ",
    " 0         0  ",
    "0           0 ",
    "0  0000000  0 ",
    "0  0     0  0 ",
    " 0         0  ",
    "   0     0    ",
    "     000      "
]

def create_commit(date):
    # Create a new file with a random name
    filename = f"file_{date.strftime('%Y%m%d%H%M%S')}.txt"
    with open(filename, 'w') as f:
        f.write(f"This is a file created on {date}")

    # Stage the file
    subprocess.run(["git", "add", filename], check=True)

    # Commit the file
    subprocess.run(["git", "commit", "--date", date.isoformat(), "-m", "Contribution"], check=True)

    # Remove the file
    os.remove(filename)

def update_contributions(start_date):
    current_date = start_date
    for row in pattern:
        for char in row:
            if char == '0':
                create_commit(current_date)
            current_date += timedelta(days=1)
        current_date += timedelta(days=1)  # Move to the next row

    # Push the commits to the repository
    subprocess.run(["git", "push"], check=True)

if __name__ == "__main__":
    # Get start date from the user
    start_date_str = input("Enter the start date (YYYY-MM-DD): ")
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")

    github_username = input("GitHub User Name")
    github_repo = input("Enter GitHub Repo for this user name ")

    # Initialize the git repository if it doesn't exist
    if not os.path.exists(".git"):
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "remote", "add", "origin", "https://github.com/"+github_username+"/"+github_repo+".git"], check=True)

    update_contributions(start_date)