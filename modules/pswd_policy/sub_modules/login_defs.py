from pathlib import Path
from utils.scripts import run_line
from typing import Dict, Optional, List
import re

# Get project root (3 levels up from this file)
PROJECT_ROOT = str(Path(__file__).parent.parent.parent.parent)


def get_current_login_defs() -> Optional[Dict[str, Optional[int]]]:
    """
    Get current login.defs password aging settings.

    Returns:
        dict: Current login.defs settings
    """
    try:
        settings: Dict[str, Optional[int]] = {
            "PASS_MAX_DAYS": None,
            "PASS_MIN_DAYS": None,
            "PASS_WARN_AGE": None,
        }

        # Read PASS_MAX_DAYS
        result = run_line("grep '^PASS_MAX_DAYS' /etc/login.defs", sudo=True)
        if result["returncode"] == 0 and result["stdout"]:
            match = re.search(r'PASS_MAX_DAYS\s+(\d+)', result["stdout"])
            if match:
                settings["PASS_MAX_DAYS"] = int(match.group(1))

        # Read PASS_MIN_DAYS
        result = run_line("grep '^PASS_MIN_DAYS' /etc/login.defs", sudo=True)
        if result["returncode"] == 0 and result["stdout"]:
            match = re.search(r'PASS_MIN_DAYS\s+(\d+)', result["stdout"])
            if match:
                settings["PASS_MIN_DAYS"] = int(match.group(1))

        # Read PASS_WARN_AGE
        result = run_line("grep '^PASS_WARN_AGE' /etc/login.defs", sudo=True)
        if result["returncode"] == 0 and result["stdout"]:
            match = re.search(r'PASS_WARN_AGE\s+(\d+)', result["stdout"])
            if match:
                settings["PASS_WARN_AGE"] = int(match.group(1))

        return settings
    except Exception as e:
        print(f"Error reading login.defs settings: {e}")
        return None


def audit_login_defs() -> List[str]:
    """
    Audit login.defs password aging settings against security best practices.

    Returns:
        list: List of issues found
    """
    issues: List[str] = []
    settings = get_current_login_defs()

    if not settings:
        issues.append("Failed to read /etc/login.defs")
        return issues

    # Check PASS_MAX_DAYS (should be <= 90 days)
    if settings["PASS_MAX_DAYS"] is None:
        issues.append("PASS_MAX_DAYS not set in /etc/login.defs")
    elif settings["PASS_MAX_DAYS"] > 90:
        issues.append(f"Maximum password age is {settings['PASS_MAX_DAYS']} days (should be <= 90)")

    # Check PASS_MIN_DAYS (should be >= 1 day)
    if settings["PASS_MIN_DAYS"] is None:
        issues.append("PASS_MIN_DAYS not set in /etc/login.defs")
    elif settings["PASS_MIN_DAYS"] < 1:
        issues.append(f"Minimum password age is {settings['PASS_MIN_DAYS']} days (should be >= 1)")

    # Check PASS_WARN_AGE (should be >= 7 days)
    if settings["PASS_WARN_AGE"] is None:
        issues.append("PASS_WARN_AGE not set in /etc/login.defs")
    elif settings["PASS_WARN_AGE"] < 7:
        issues.append(f"Password warning age is {settings['PASS_WARN_AGE']} days (should be >= 7)")

    return issues


def configure_login_defs():
    """
    Configure login.defs password aging settings to secure defaults.

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        from utils.scripts import run_script_stdout

        # Configure login.defs with secure settings
        run_script_stdout(
            "modules/pswd_policy/shell/configure_login_defs.sh",
            cwd=PROJECT_ROOT,
            sudo=True,
        )

        return True
    except Exception as e:
        print(f"Error configuring login.defs: {e}")
        return False



