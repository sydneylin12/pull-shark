import os
import requests
import json
import subprocess
from datetime import datetime

# Achievement target count
ITERATIONS = 48

# Replace these with your details
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
SECOND_GITHUB_TOKEN = os.getenv('SECOND_GITHUB_TOKEN')
REPO_OWNER = "sydneylin12"
SECOND_REPO_OWNER = "sydneylin3"
REPO_NAME = "pull-shark"
SECOND_REPO_NAME = "sydneylin3"

# Creates an issue from account 2
def create_pull_request():
    url = f"https://api.github.com/repos/{SECOND_REPO_OWNER}/{REPO_NAME}/issues"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    payload = {
        "title": "Automated issue created at: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "body": "Created at: " +datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 201:
        issue_data = response.json()
        print(f"Issue created: {issue_data['url']}")
        return issue_data['url']
    else:
        print(f"Failed to create pull request: {response.status_code} {response.text}")
        return None

# Main flow
def main():
    create_pull_request

# Do this auto commit 1024 times for the achievement
if __name__ == "__main__":
    for i in range (1, 1024):
        main()
