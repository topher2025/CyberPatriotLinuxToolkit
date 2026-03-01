from pathlib import Path
from utils.scripts import run_script_stdout
from utils.data import dump_json

# Get project root (3 levels up from this file)
PROJECT_ROOT = str(Path(__file__).parent.parent.parent.parent)


def audit_users(expected_users):
    audit = run_script_stdout("modules/user_mgmt/shell/list_users.sh", cwd=PROJECT_ROOT)
    struct = {"found_users": [], "missing_users": [], "unexpected_users": []}
    for line in audit.splitlines():
        username = line.strip()
        if username in expected_users:
            struct["found_users"].append(username)
        else:
            struct["unexpected_users"].append(username)
    for user in expected_users:
        if user not in struct["found_users"]:
            struct["missing_users"].append(user)
    dump_json(struct, "data/audits/users.json")
    return struct


def audit_groups(expected_groups):
    audit = run_script_stdout(
        "modules/user_mgmt/shell/list_groups.sh", cwd=PROJECT_ROOT
    )
    struct = {"found_groups": [], "missing_groups": [], "unexpected_groups": []}
    for line in audit.splitlines():
        group_name = line.strip()
        if group_name in expected_groups:
            struct["found_groups"].append(group_name)
        else:
            struct["unexpected_groups"].append(group_name)
    for group in expected_groups:
        if group not in struct["found_groups"]:
            struct["missing_groups"].append(group)

    dump_json(struct, "data/audits/groups.json")
    return struct
