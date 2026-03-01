import argparse
from pathlib import Path
from .sub_modules import audit, groups, users
from utils.data import load_json_file
from utils.outputs import log_output

# Get project root (2 levels up from this file)
PROJECT_ROOT = str(Path(__file__).parent.parent.parent)


def main(datapath="data/parsed.json", dry_run=False, tests=False):
    """
    Main function for user management module.

    Args:
        datapath (str): Path to parsed JSON configuration file
        dry_run (bool): Preview changes without applying them
        tests (bool): Run in test mode
    """
    if tests:
        # Run tests
        import subprocess
        import sys
        test_file = Path(__file__).parent / "tests" / "tests.py"
        log_output(f"Running tests from {test_file}")
        result = subprocess.run([sys.executable, "-m", "pytest", str(test_file), "-v"])
        sys.exit(result.returncode)

    # Load parsed data
    log_output(f"Loading configuration from {datapath}")

    # Construct full path from PROJECT_ROOT
    # Handle both paths with and without leading slash
    if datapath.startswith("/"):
        datapath = datapath.lstrip("/")

    full_path = str(Path(PROJECT_ROOT) / datapath)
    log_output(f"Resolved path: {full_path}")

    # Load the JSON file
    data = load_json_file(full_path)

    if not data:
        log_output(f"ERROR: Failed to load {full_path} or file is empty")
        return

    # Extract expected data
    expected_users = data.get("users", [])
    expected_admins = data.get("admins", [])
    add_users = data.get("add_users", [])
    add_groups = data.get("add_groups", {})

    # Combine users and admins for comprehensive audit
    all_expected_users = list(set(expected_users + expected_admins + add_users))

    log_output("\n=== User Management Module ===\n")

    # Step 1: Audit existing users
    log_output("Step 1: Auditing users...")
    user_audit = audit.audit_users(all_expected_users)

    log_output(f"  Found users: {len(user_audit['found_users'])}")
    log_output(f"  Missing users: {len(user_audit['missing_users'])}")
    log_output(f"  Unexpected users: {len(user_audit['unexpected_users'])}")

    if user_audit['missing_users']:
        log_output(f"  Missing: {', '.join(user_audit['missing_users'])}")
    if user_audit['unexpected_users']:
        log_output(f"  Unexpected: {', '.join(user_audit['unexpected_users'])}")

    # Step 2: Audit existing groups
    log_output("\nStep 2: Auditing groups...")
    expected_groups = list(add_groups.keys())
    group_audit = audit.audit_groups(expected_groups)

    log_output(f"  Found groups: {len(group_audit['found_groups'])}")
    log_output(f"  Missing groups: {len(group_audit['missing_groups'])}")
    log_output(f"  Unexpected groups: {len(group_audit['unexpected_groups'])}")

    if group_audit['missing_groups']:
        log_output(f"  Missing: {', '.join(group_audit['missing_groups'])}")

    # Step 3: Create missing users
    if user_audit['missing_users']:
        log_output("\nStep 3: Creating missing users...")
        for username in user_audit['missing_users']:
            if dry_run:
                log_output(f"  [DRY RUN] Would create user: {username}")
            else:
                log_output(f"  Creating user: {username}")
                if users.create_user(username):
                    log_output(f"    ✓ Successfully created user: {username}")
                else:
                    log_output(f"    ✗ Failed to create user: {username}")
    else:
        log_output("\nStep 3: No missing users to create")

    # Step 4: Create missing groups
    if group_audit['missing_groups']:
        log_output("\nStep 4: Creating missing groups...")
        for group_name in group_audit['missing_groups']:
            if dry_run:
                log_output(f"  [DRY RUN] Would create group: {group_name}")
            else:
                log_output(f"  Creating group: {group_name}")
                if groups.create_group(group_name):
                    log_output(f"    ✓ Successfully created group: {group_name}")
                else:
                    log_output(f"    ✗ Failed to create group: {group_name}")
    else:
        log_output("\nStep 4: No missing groups to create")

    # Step 5: Manage group memberships
    if add_groups:
        log_output("\nStep 5: Managing group memberships...")
        for group_name, members in add_groups.items():
            log_output(f"  Processing group: {group_name}")
            for username in members:
                if dry_run:
                    log_output(f"    [DRY RUN] Would add {username} to {group_name}")
                else:
                    log_output(f"    Adding {username} to {group_name}")
                    if groups.add_user_to_group(username, group_name):
                        log_output(f"      ✓ Successfully added {username} to {group_name}")
                    else:
                        log_output(f"      ✗ Failed to add {username} to {group_name}")
    else:
        log_output("\nStep 5: No group memberships to manage")

    # Step 6: Handle admin privileges
    if expected_admins:
        log_output("\nStep 6: Managing admin privileges (sudo group)...")
        for admin in expected_admins:
            if dry_run:
                log_output(f"  [DRY RUN] Would add {admin} to sudo group")
            else:
                log_output(f"  Adding {admin} to sudo group")
                if groups.add_user_to_group(admin, "sudo"):
                    log_output(f"    ✓ Successfully added {admin} to sudo group")
                else:
                    log_output(f"    ✗ Failed to add {admin} to sudo group")
    else:
        log_output("\nStep 6: No admins to configure")

    # Step 7: Handle unexpected users (optional - lock them)
    if user_audit['unexpected_users']:
        log_output("\nStep 7: Handling unexpected users...")
        log_output(f"  Found {len(user_audit['unexpected_users'])} unexpected users")
        log_output("  Note: Consider locking or removing these users manually:")
        for username in user_audit['unexpected_users']:
            log_output(f"    - {username}")
    else:
        log_output("\nStep 7: No unexpected users found")

    log_output("\n=== User Management Complete ===\n")

    if dry_run:
        log_output("Note: This was a DRY RUN. No actual changes were made.")
        log_output("Run without --dry-run to apply changes.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-path", "-p", default="/data/parsed.json")
    parser.add_argument("--dry-run", "-d", action="store_true")
    parser.add_argument("--test", "-t", action="store_true")

    args = parser.parse_args()
    main(args.data_path, args.dry_run, args.test)

