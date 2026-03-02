import argparse
from pathlib import Path
from .sub_modules import audit, pam_config, login_defs
from utils.outputs import log_output

# Get project root (2 levels up from this file)
PROJECT_ROOT = str(Path(__file__).parent.parent.parent)


def main(dry_run=False, tests=False):
    """
    Main function for password policy module.

    Args:
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

    log_output("\n=== Password Policy Module ===\n")

    # Step 1: Audit current password policy settings
    log_output("Step 1: Auditing current password policy settings...")
    policy_audit = audit.audit_password_policy()

    # Display PAM audit results
    log_output("\n  PAM Password Quality Settings:")
    pam_issues = policy_audit["pam_issues"]
    if pam_issues:
        for issue in pam_issues:
            log_output(f"    ⚠ {issue}")
    else:
        log_output("    ✓ All PAM settings are compliant")

    # Display login.defs audit results
    log_output("\n  Login.defs Password Aging Settings:")
    login_issues = policy_audit["login_defs_issues"]
    if login_issues:
        for issue in login_issues:
            log_output(f"    ⚠ {issue}")
    else:
        log_output("    ✓ All login.defs settings are compliant")

    # Step 2: Configure PAM password quality
    if pam_issues:
        log_output("\nStep 2: Configuring PAM password quality...")
        if dry_run:
            log_output("  [DRY RUN] Would update /etc/pam.d/common-password")
            log_output("  [DRY RUN] Would install libpam-pwquality if needed")
        else:
            try:
                if pam_config.configure_pam_pwquality():
                    log_output("  ✓ Successfully configured PAM password quality")
                else:
                    log_output("  ✗ Failed to configure PAM password quality")
            except Exception as e:
                log_output(f"  ✗ Error configuring PAM: {e}")
    else:
        log_output("\nStep 2: PAM password quality already configured")

    # Step 3: Configure login.defs password aging
    if login_issues:
        log_output("\nStep 3: Configuring password aging policies...")
        if dry_run:
            log_output("  [DRY RUN] Would update /etc/login.defs")
        else:
            try:
                if login_defs.configure_login_defs():
                    log_output("  ✓ Successfully configured password aging policies")
                else:
                    log_output("  ✗ Failed to configure password aging policies")
            except Exception as e:
                log_output(f"  ✗ Error configuring login.defs: {e}")
    else:
        log_output("\nStep 3: Password aging policies already configured")

    # Step 4: Verify changes
    log_output("\nStep 4: Verifying configuration...")
    if not dry_run:
        final_audit = audit.audit_password_policy()
        all_issues = final_audit["pam_issues"] + final_audit["login_defs_issues"]

        if not all_issues:
            log_output("  ✓ All password policy settings are now compliant")
        else:
            log_output("  ⚠ Some issues remain:")
            for issue in all_issues:
                log_output(f"    - {issue}")
    else:
        log_output("  [DRY RUN] Skipping verification")

    log_output("\n=== Password Policy Complete ===\n")

    if dry_run:
        log_output("Note: This was a DRY RUN. No actual changes were made.")
        log_output("Run without --dry-run to apply changes.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", "-d", action="store_true")
    parser.add_argument("--test", "-t", action="store_true")

    args = parser.parse_args()
    main(args.dry_run, args.test)

