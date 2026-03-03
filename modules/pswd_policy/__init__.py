"""
Password policy package.

Responsible for:
- Password quality requirements (PAM pwquality)
- Password aging policies (login.defs)
- Password policy auditing

Does NOT handle:
- User password changes
- Account lockout policies
- Account lockout detection
- Password history enforcement
- Specific user password auditing
"""

from modules.pswd_policy.sub_modules.pam_config import (
    configure_pam_pwquality,
    audit_pam_pwquality,
    get_current_pam_settings,
)

from modules.pswd_policy.sub_modules.login_defs import (
    configure_login_defs,
    audit_login_defs,
    get_current_login_defs,
)

from modules.pswd_policy.sub_modules.audit import (
    audit_password_policy,
)

__all__ = [
    # PAM configuration
    "configure_pam_pwquality",
    "audit_pam_pwquality",
    "get_current_pam_settings",
    # login.defs configuration
    "configure_login_defs",
    "audit_login_defs",
    "get_current_login_defs",
    # audit
    "audit_password_policy",
]

