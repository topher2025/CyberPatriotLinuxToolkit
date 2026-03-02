# Password Policy Module

## Overview

The password policy module is responsible for configuring and auditing password quality and aging policies on Linux systems. This module helps ensure compliance with CyberPatriot security requirements.

## Quick Reference

### Common Commands
```bash
# Basic usage - configure password policy
python3 main.py --password-policy              # or -p

# Preview changes without applying
python3 main.py --password-policy --dry-run    # or -p -d

# Run module tests
python3 main.py --password-policy --test

# Combine with other modules
python3 main.py -R -P -u -p                    # README parsing + user mgmt + password policy
python3 main.py --all                           # Run all security tasks
```

### What Gets Checked
- ✅ Password length (12+ characters)
- ✅ Character complexity (uppercase, lowercase, digits, special chars)
- ✅ Password aging policies (max 90 days, min 1 day, warning 7 days)
- ✅ Dictionary and username checks
- ✅ Maximum repeated characters

### Files Modified
- `/etc/pam.d/common-password` (with timestamped backup)
- `/etc/login.defs` (with timestamped backup)

### Requirements
- Sudo/root privileges
- Ubuntu/Debian-based system
- `libpam-pwquality` (auto-installed if needed)

## Features

### Password Quality (PAM pwquality)
- Minimum password length enforcement
- Character complexity requirements (digits, uppercase, lowercase, special characters)
- Password difference requirements from previous passwords
- Dictionary and username checking
- Configurable retry limits

### Password Aging (login.defs)
- Maximum password age (expiration)
- Minimum password age (prevents immediate changes)
- Password expiration warning period

## Usage

### From Main Script
```bash
# Audit and configure password policy
python3 main.py --password-policy

# Dry run (preview changes)
python3 main.py --password-policy --dry-run

# Run tests
python3 main.py --password-policy --test
```

### Standalone
```bash
cd modules/pswd_policy
python3 main.py
python3 main.py --dry-run
python3 main.py --test
```

## Configuration Standards

### PAM Password Quality Settings
- **minlen**: 12 characters minimum
- **dcredit**: -1 (at least 1 digit required)
- **ucredit**: -1 (at least 1 uppercase required)
- **lcredit**: -1 (at least 1 lowercase required)
- **ocredit**: -1 (at least 1 special character required)
- **difok**: 3 (at least 3 characters different from old password)
- **retry**: 3 attempts maximum
- **maxrepeat**: 2 (max consecutive identical characters)
- **gecoscheck**: 1 (check against user's GECOS info)
- **dictcheck**: 1 (check against dictionary)
- **usercheck**: 1 (check if password contains username)
- **enforcing**: 1 (enforce all checks)

### Password Aging Settings
- **PASS_MAX_DAYS**: 90 days (password expires after 90 days)
- **PASS_MIN_DAYS**: 1 day (password can't be changed for 1 day after setting)
- **PASS_WARN_AGE**: 7 days (warn user 7 days before expiration)

## Files Modified

### PAM Configuration
- `/etc/pam.d/common-password` - Password quality requirements
- Backups created as `/etc/pam.d/common-password.backup.YYYYMMDD_HHMMSS`

### Login Definitions
- `/etc/login.defs` - Password aging policies
- Backups created as `/etc/login.defs.backup.YYYYMMDD_HHMMSS`

## Module Structure

```
pswd_policy/
├── __init__.py           # Module exports
├── main.py               # Main entry point
├── README.md             # This file
├── shell/                # Shell scripts
│   ├── install_pwquality.sh
│   ├── configure_pam.sh
│   └── configure_login_defs.sh
├── sub_modules/          # Python modules
│   ├── audit.py          # Comprehensive auditing
│   ├── pam_config.py     # PAM configuration
│   └── login_defs.py     # login.defs configuration
└── tests/                # Unit tests
    └── tests.py
```

## Dependencies

- `libpam-pwquality` - PAM module for password quality checking
  - Automatically installed by the module if missing

## Security Notes

1. **Backup Policy**: All configuration changes create timestamped backups
2. **Root Required**: This module requires sudo/root privileges
3. **Existing Users**: Password aging changes only affect new passwords
4. **Competition Safe**: All changes are reversible and logged

## CyberPatriot Compliance

This module addresses common vulnerabilities found in CyberPatriot competitions:
- ✓ Weak password policies
- ✓ Disabled password aging
- ✓ Excessive password age limits
- ✓ Missing password complexity requirements
- ✓ Insufficient password length requirements

## Testing

Run the test suite to verify functionality:
```bash
python3 main.py --test
```

Tests verify:
- Reading current PAM settings
- Reading current login.defs settings
- Auditing password policies
- Detecting policy violations

## Troubleshooting

### libpam-pwquality not found
The module will automatically install it. If manual installation is needed:
```bash
sudo apt-get update
sudo apt-get install libpam-pwquality
```

### Changes not taking effect
- Ensure scripts are run with sudo privileges
- Check `/var/log/auth.log` for PAM errors
- Verify backup files were created

### Password changes rejected
After tightening password policies, existing weak passwords won't immediately fail, but new password changes must comply with the new rules.

## Related Modules

- **user_mgmt**: User and group management
- **audit_policy**: System auditing configuration
- **security_hardening**: Additional system hardening

## Author

Christopher Lewis, 2026

