import os
import requests
import json
import subprocess

# Replace these with your details
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')  # GitHub Personal Access Token
REPO_OWNER = "sydneylin12"                # GitHub username or organization
REPO_NAME = "pull-shark"                  # Repository name
BASE_BRANCH = "main"                      # Target branch (e.g., 'main' or 'master')
HEAD_BRANCH = "feature"            # Feature branch name
PR_TITLE = "Auto-generated Pull Request" 
PR_BODY = "This pull request was created and merged automatically."

# Function to create a new pull request
def create_pull_request():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
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
        return pr_data['number']  # PR number for merging
    else:
        print(f"Failed to create pull request: {response.status_code} {response.text}")
        return None

# Function to merge the pull request
def merge_pull_request(pr_number):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls/{pr_number}/merge"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    payload = {"commit_title": "Auto-merged PR"}

    response = requests.put(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        print(f"Pull request merged successfully: {response.json()['sha']}")
    else:
        print(f"Failed to merge pull request: {response.status_code} {response.text}")

# Push the feature branch (if needed)
def push_branch():
    subprocess.run(["git", "checkout", HEAD_BRANCH])
    subprocess.run(["git", "push", "origin", HEAD_BRANCH])

# Main flow
def main():
    push_branch()  # Push the branch to remote (if needed)
    pr_number = create_pull_request()
    if pr_number:
        merge_pull_request(pr_number)

if __name__ == "__main__":
    main()
