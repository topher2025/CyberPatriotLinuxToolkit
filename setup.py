from pathlib import Path
from utils.scripts import run_script, run_line


def setup():
    print("Starting setup process...")

    print("Installing dependencies... ", end="")
    result = run_line("pip install -r requirements.txt")
    if result["returncode"] == 0:
        print("Done.")
    else:
        print(f"\nFailed to install dependencies. {result['stderr']}")
        return False

    print("Setting up sudo...")
    result = run_script("setup_sudo.sh", "-y", cwd=str(Path(__file__).parent))
    if result["returncode"] == 0:
        print("Done.")
    else:
        print(f"\nFailed to set up sudo: {result['stderr']}")
        return False

    return True


if __name__ == "__main__":
    if setup():
        print("Setup completed successfully.")
