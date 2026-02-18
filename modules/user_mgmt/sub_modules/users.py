from pathlib import Path
from utils.data import load_json
from utils.scripts import run_script_stdout

# Get project root (3 levels up from this file)
PROJECT_ROOT = str(Path(__file__).parent.parent.parent.parent)


def user_exists(username):
    if username in load_json("users", "data/audits"):
        return True
    else:
        return False


def create_user(username):
    try:
        run_script_stdout("modules/user_mgmt/shell/sudo/create_user.sh", username, cwd=PROJECT_ROOT, sudo=True)
        return True
    except Exception as e:
        print(f"Error creating user: {e}")
        return False


def delete_user(username):
    try:
        run_script_stdout("modules/user_mgmt/shell/sudo/delete_user.sh", username, cwd=PROJECT_ROOT, sudo=True)
        return True
    except Exception as e:
        print(f"Error deleting user: {e}")
        return False


def lock_user(username):
    try:
        run_script_stdout("modules/user_mgmt/shell/sudo/lock_user.sh", username, cwd=PROJECT_ROOT, sudo=True)
        return True
    except Exception as e:
        print(f"Error locking user: {e}")
        return False
