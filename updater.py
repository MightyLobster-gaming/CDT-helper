import os
import subprocess
import requests

# GitHub settings
GITHUB_REPO = "https://raw.githubusercontent.com/MightyLobster-gaming/CDT-helper/main/"
VERSION_FILE = "version.txt"

def get_local_version():
    try:
        with open(VERSION_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "0.0.0"

def get_remote_version():
    url = GITHUB_REPO+VERSION_FILE
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.strip()
    else:
        print("Error checking remote version.")
        return None

def update_project():
    print("Updating the project...")
    subprocess.run(["git", "pull"], check=True)
    print("Update complete. Restarting...")
    os.execv(__file__, ["python"] + os.sys.argv)

def check_for_update():
    local_version = get_local_version()
    remote_version = get_remote_version()

    print(f"Local version: {local_version}")
    print(f"Remote version: {remote_version}")

    if local_version != remote_version:
        print("New version available! Updating...")
        update_project()
    else:
        print("Already up-to-date.")

if __name__ == "__main__":
    check_for_update()
