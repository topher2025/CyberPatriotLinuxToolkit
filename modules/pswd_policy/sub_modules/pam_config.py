from pathlib import Path
from utils.scripts import run_script_stdout, run_line
from typing import Dict, Optional, List, Any
import re

# Get project root (3 levels up from this file)
PROJECT_ROOT = str(Path(__file__).parent.parent.parent.parent)


def get_current_pam_settings() -> Optional[Dict[str, Any]]:
    """
    Get current PAM password quality settings from /etc/pam.d/common-password.

    Returns:
        dict: Current PAM settings
    """
    try:
        result = run_line("grep 'pam_pwquality.so' /etc/pam.d/common-password", sudo=True)

        settings: Dict[str, Any] = {
            "minlen": None,
            "dcredit": None,
            "ucredit": None,
            "lcredit": None,
            "ocredit": None,
            "difok": None,
            "retry": None,
            "line": result["stdout"] if result["returncode"] == 0 else None
        }

        if result["returncode"] == 0 and result["stdout"]:
            line = result["stdout"]

            # Extract settings using regex
            minlen_match = re.search(r'minlen=(\d+)', line)
            dcredit_match = re.search(r'dcredit=(-?\d+)', line)
            ucredit_match = re.search(r'ucredit=(-?\d+)', line)
            lcredit_match = re.search(r'lcredit=(-?\d+)', line)
            ocredit_match = re.search(r'ocredit=(-?\d+)', line)
            difok_match = re.search(r'difok=(\d+)', line)
            retry_match = re.search(r'retry=(\d+)', line)

            if minlen_match:
                settings["minlen"] = int(minlen_match.group(1))
            if dcredit_match:
                settings["dcredit"] = int(dcredit_match.group(1))
            if ucredit_match:
                settings["ucredit"] = int(ucredit_match.group(1))
            if lcredit_match:
                settings["lcredit"] = int(lcredit_match.group(1))
            if ocredit_match:
                settings["ocredit"] = int(ocredit_match.group(1))
            if difok_match:
                settings["difok"] = int(difok_match.group(1))
            if retry_match:
                settings["retry"] = int(retry_match.group(1))

        return settings
    except Exception as e:
        print(f"Error reading PAM settings: {e}")
        return None


def audit_pam_pwquality() -> List[str]:
    """
    Audit PAM password quality settings against security best practices.

    Returns:
        list: List of issues found
    """
    issues: List[str] = []
    settings = get_current_pam_settings()

    if not settings or settings["line"] is None:
        issues.append("pam_pwquality.so not configured in /etc/pam.d/common-password")
        return issues

    # Check minimum length (should be at least 12)
    if settings["minlen"] is None or settings["minlen"] < 12:
        issues.append(f"Password minimum length is {settings['minlen']} (should be >= 12)")

    # Check digit requirement (negative means minimum required)
    if settings["dcredit"] is None or settings["dcredit"] > -1:
        issues.append(f"Digit requirement is {settings['dcredit']} (should be <= -1)")

    # Check uppercase requirement
    if settings["ucredit"] is None or settings["ucredit"] > -1:
        issues.append(f"Uppercase requirement is {settings['ucredit']} (should be <= -1)")

    # Check lowercase requirement
    if settings["lcredit"] is None or settings["lcredit"] > -1:
        issues.append(f"Lowercase requirement is {settings['lcredit']} (should be <= -1)")

    # Check other characters requirement
    if settings["ocredit"] is None or settings["ocredit"] > -1:
        issues.append(f"Special character requirement is {settings['ocredit']} (should be <= -1)")

    # Check difok (different characters from old password)
    if settings["difok"] is None or settings["difok"] < 3:
        issues.append(f"Different characters requirement is {settings['difok']} (should be >= 3)")

    # Check retry limit
    if settings["retry"] is None or settings["retry"] > 3:
        issues.append(f"Retry limit is {settings['retry']} (should be <= 3)")

    return issues


def configure_pam_pwquality():
    """
    Configure PAM password quality settings to secure defaults.

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # First, ensure libpam-pwquality is installed
        run_script_stdout(
            "modules/pswd_policy/shell/install_pwquality.sh",
            cwd=PROJECT_ROOT,
            sudo=True,
        )

        # Configure PAM with secure settings
        run_script_stdout(
            "modules/pswd_policy/shell/configure_pam.sh",
            cwd=PROJECT_ROOT,
            sudo=True,
        )

        return True
    except Exception as e:
        print(f"Error configuring PAM: {e}")
        return False



