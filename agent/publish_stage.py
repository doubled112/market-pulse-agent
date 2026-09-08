"""
Stage 3: Publish Agent
Job: take processed data and make it available to the dashboard (docs/data.json),
then commit and push so GitHub Pages picks up the update.
Does NOT fetch or calculate anything itself.
"""

import shutil
import subprocess
from pathlib import Path

# Resolve paths relative to the project root, not the current working directory,
# so this script works no matter which folder it's run from.
ROOT = Path(__file__).resolve().parent.parent
PROCESSED_PATH = ROOT / "data" / "processed_prices.json"
PUBLISH_PATH = ROOT / "docs" / "data.json"

def publish():
    shutil.copyfile(PROCESSED_PATH, PUBLISH_PATH)
    print(f"Copied {PROCESSED_PATH} -> {PUBLISH_PATH}")

def git_commit_and_push():
    subprocess.run(["git", "add", "docs/data.json"], check=True, cwd=ROOT)
    result = subprocess.run(
        ["git", "commit", "-m", "Automated market data update"],
        capture_output=True, text=True, cwd=ROOT
    )
    output = result.stdout + result.stderr
    print(output)

    if "nothing to commit" in output or "nothing added to commit" in output:
        print("No changes to commit.")
        return

    subprocess.run(["git", "push"], check=True, cwd=ROOT)
    print("Pushed update to GitHub.")

if __name__ == "__main__":
    publish()
    git_commit_and_push()