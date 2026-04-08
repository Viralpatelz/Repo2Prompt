import os
import shutil
import tempfile
import urllib.parse
from git import Repo

def is_github_url(source):
    """
    Checks if the given string is a valid GitHub URL.
    Supports https://github.com/user/repo and https://github.com/user/repo.git
    """
    parsed = urllib.parse.urlparse(source)
    if parsed.netloc in ["github.com", "www.github.com"]:
        return True
    # Basic check for git@github.com:user/repo.git form
    if source.startswith("git@github.com:"):
        return True
    return False

def clone_repo_to_temp(url):
    """
    Clones the given repository URL to a temporary directory.
    Returns the path to the temporary directory.
    Note: It is the caller's responsibility to delete this temp dir!
    """
    temp_dir = tempfile.mkdtemp(prefix="repo2prompt_")
    print(f"Cloning {url} into temporary directory...")
    # shallow clone to speed things up
    Repo.clone_from(url, temp_dir, depth=1)
    return temp_dir
