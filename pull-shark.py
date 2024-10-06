import os
import requests
import json
import subprocess
from datetime import datetime

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_OWNER = "sydneylin12"
REPO_NAME = "pull-shark"
BASE_BRANCH = "main"
HEAD_BRANCH = "feature"
LOG_FILE = "commit_log.txt"

# PR metadata
PR_TITLE = "Auto-generated Pull Request" 
PR_BODY = "This pull request was created and merged automatically."

# API request headers
headers = {"Authorization": f"token {GITHUB_TOKEN}"}

# Function to log the current date and time
def log_commit():
    subprocess.run(["git", "checkout", HEAD_BRANCH])

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"Commit pushed at {current_time}\n")

    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "save"])
    subprocess.run(["git", "push", "origin", HEAD_BRANCH])

    print(f"Logged commit at {current_time}")

# Function to create a new pull request
def create_pull_request():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls"
    payload = {
        "title": PR_TITLE,
        "body": PR_BODY,
        "head": HEAD_BRANCH,
        "base": BASE_BRANCH
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 201:
        pr_data = response.json()
        print(f"Pull request created: {pr_data['html_url']}")
        return pr_data['number']
    else:
        print(f"Failed to create pull request: {response.status_code} {response.text}")

# Function to merge the pull request
def merge_pull_request(pr_number):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls/{pr_number}/merge"
    payload = {"commit_title": "Auto-merged PR"}

    response = requests.put(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        print(f"Pull request merged successfully: {response.json()['sha']}")
    else:
        print(f"Failed to merge pull request: {response.status_code} {response.text}")

# Main flow
def main():
    log_commit()
    pr_number = create_pull_request()
    if pr_number:
        merge_pull_request(pr_number)

# Do this auto commit 1024 times for the achievement
if __name__ == "__main__":
    for i in range (1, 1024):
        main()
