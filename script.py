# Acknowledgements:
## https://stackoverflow.com/questions/76082808/how-to-get-github-repo-latest-release-in-python
from github import Github
import sys

token = None # Put your GitHub API token here if you want to access a private repo.
repo_path = "MayKB/devops-hands-on-project-hivebox"

if __name__ == "__main__":
    g = Github(token)
    repo = g.get_repo(repo_path)
    latest = repo.get_latest_release()
    print(latest.name)
    sys.exit(0)