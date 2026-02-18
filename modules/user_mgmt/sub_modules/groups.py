from pathlib import Path
from utils.data import load_json
from utils.scripts import run_script_stdout

# Get project root (3 levels up from this file)
PROJECT_ROOT = str(Path(__file__).parent.parent.parent.parent)


def group_exists(group_name):
    if group_name in load_json("groups", "data/audits"):
        return True
    else:
        return False


def create_group(group_name):
    try:
        run_script_stdout("modules/user_mgmt/shell/sudo/create_group.sh", group_name, cwd=PROJECT_ROOT, sudo=True)
        return True
    except Exception as e:
        print(f"Error creating group: {e}")
        return False


def delete_group(group_name):
    try:
        run_script_stdout("modules/user_mgmt/shell/sudo/delete_group.sh", group_name, cwd=PROJECT_ROOT, sudo=True)
        return True
    except Exception as e:
        print(f"Error deleting group: {e}")
        return False


def add_user_to_group(username, group_name):
    try:
        run_script_stdout(
            "modules/user_mgmt/shell/sudo/add_user_to_group.sh", username, group_name, cwd=PROJECT_ROOT, sudo=True
        )
        return True
    except Exception as e:
        print(f"Error adding user to group: {e}")
        return False


def remove_user_from_group(username, group_name):
    try:
        run_script_stdout(
            "modules/user_mgmt/shell/sudo/remove_user_from_group.sh", username, group_name, cwd=PROJECT_ROOT, sudo=True
        )
        return True
    except Exception as e:
        print(f"Error removing user from group: {e}")
        return False
