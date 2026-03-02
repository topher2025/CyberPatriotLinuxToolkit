from .pam_config import audit_pam_pwquality, get_current_pam_settings
from .login_defs import audit_login_defs, get_current_login_defs
from typing import Dict, List, Any, Optional


def audit_password_policy() -> Dict[str, Any]:
    """
    Perform a comprehensive audit of password policy settings.

    Returns:
        dict: Audit results with issues found
    """
    result: Dict[str, Any] = {
        "pam_issues": [],
        "login_defs_issues": [],
        "pam_settings": None,
        "login_defs_settings": None,
    }

    # Audit PAM password quality
    result["pam_issues"] = audit_pam_pwquality()
    result["pam_settings"] = get_current_pam_settings()

    # Audit login.defs password aging
    result["login_defs_issues"] = audit_login_defs()
    result["login_defs_settings"] = get_current_login_defs()

    return result


