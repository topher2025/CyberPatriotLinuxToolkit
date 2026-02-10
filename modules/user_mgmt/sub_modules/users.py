from utils.data import load_json
from utils.scripts import run_script_stdout

def user_exists(username):
    if username in load_json("users", "data/audits"):
        return True
    else:
        return False


def create_user(username):
    try:
        run_script_stdout("shell/sudo/create_user.sh", username, sudo=True)
        return True
    except Exception as e:
        return False


def delete_user(username):
    try:
        run_script_stdout("shell/sudo/delete_user.sh", username, sudo=True)
        return True
    except Exception as e:
        return False



def lock_user(username):
    try:
        run_script_stdout("shell/sudo/lock_user.sh", username, sudo=True)
        return True
    except Exception as e:
        return False
