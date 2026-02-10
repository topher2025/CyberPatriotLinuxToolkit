from utils.data import load_json
from utils.scripts import run_script_stdout


def group_exists(group_name):
    if group_name in load_json("groups", "data/audits"):
        return True
    else:
        return False




def create_group(group_name):
    try:
        run_script_stdout("shell/sudo/create_group.sh", group_name, sudo=True)
        return True
    except Exception as e:
        return False


def delete_group(group_name):
    try:
        run_script_stdout("shell/sudo/delete_group.sh", group_name, sudo=True)
        return True
    except Exception as e:
        return False


def add_user_to_group(username, group_name):
    try:
        run_script_stdout("shell/sudo/add_user_to_group.sh", username, group_name, sudo=True)
        return True
    except Exception as e:
        return False


def remove_user_from_group(username, group_name):
    try:
        run_script_stdout("shell/sudo/remove_user_from_group.sh", username, group_name, sudo=True)
        return True
    except Exception as e:
        return False

