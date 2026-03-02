import pytest
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from modules.pswd_policy.sub_modules import audit, pam_config, login_defs


class TestPasswordPolicy:
    """Test password policy module functionality."""

    def test_get_current_pam_settings(self):
        """Test reading current PAM settings."""
        settings = pam_config.get_current_pam_settings()
        assert settings is not None
        assert isinstance(settings, dict)
        assert "minlen" in settings
        assert "dcredit" in settings
        assert "ucredit" in settings
        assert "lcredit" in settings
        assert "ocredit" in settings

    def test_audit_pam_pwquality(self):
        """Test PAM audit functionality."""
        issues = pam_config.audit_pam_pwquality()
        assert isinstance(issues, list)
        # Issues may or may not exist depending on system state
        print(f"\nPAM issues found: {len(issues)}")
        for issue in issues:
            print(f"  - {issue}")

    def test_get_current_login_defs(self):
        """Test reading current login.defs settings."""
        settings = login_defs.get_current_login_defs()
        assert settings is not None
        assert isinstance(settings, dict)
        assert "PASS_MAX_DAYS" in settings
        assert "PASS_MIN_DAYS" in settings
        assert "PASS_WARN_AGE" in settings

    def test_audit_login_defs(self):
        """Test login.defs audit functionality."""
        issues = login_defs.audit_login_defs()
        assert isinstance(issues, list)
        # Issues may or may not exist depending on system state
        print(f"\nlogin.defs issues found: {len(issues)}")
        for issue in issues:
            print(f"  - {issue}")

    def test_audit_password_policy(self):
        """Test comprehensive password policy audit."""
        result = audit.audit_password_policy()
        assert isinstance(result, dict)
        assert "pam_issues" in result
        assert "login_defs_issues" in result
        assert "pam_settings" in result
        assert "login_defs_settings" in result

        print(f"\nPassword Policy Audit Results:")
        print(f"  PAM issues: {len(result['pam_issues'])}")
        print(f"  login.defs issues: {len(result['login_defs_issues'])}")

        if result['pam_settings']:
            print(f"\n  Current PAM settings:")
            for key, value in result['pam_settings'].items():
                if key != 'line' and value is not None:
                    print(f"    {key}: {value}")

        if result['login_defs_settings']:
            print(f"\n  Current login.defs settings:")
            for key, value in result['login_defs_settings'].items():
                if value is not None:
                    print(f"    {key}: {value}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

