#!/usr/bin/env python3
"""Verify that the shell scripts have been fixed."""

import os
import sys

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

files = [
    'modules/pswd_policy/shell/install_pwquality.sh',
    'modules/pswd_policy/shell/configure_login_defs.sh',
    'modules/pswd_policy/shell/configure_pam.sh'
]

print("=" * 70)
print("VERIFICATION: Shell Script Line Endings")
print("=" * 70)

all_good = True
for filepath in files:
    filename = os.path.basename(filepath)
    try:
        with open(filepath, 'rb') as f:
            content = f.read()

        has_crlf = b'\r\n' in content
        has_content = len(content) > 0
        has_newlines = b'\n' in content

        if not has_content:
            status = "[X] EMPTY FILE"
            all_good = False
        elif has_crlf:
            status = "[X] CRLF (Windows) - WILL FAIL ON LINUX"
            all_good = False
        elif has_newlines:
            status = "[OK] LF (Unix) - CORRECT"
        else:
            status = "[!] No newlines found"
            all_good = False

        print(f"{filename:30s} {status}")
    except Exception as e:
        print(f"{filename:30s} [X] ERROR: {e}")
        all_good = False

print("=" * 70)

if all_good:
    print("[OK] All shell scripts are properly configured!")
    print("\nThe password policy module should now work correctly on Linux.")
    print("\nNext steps:")
    print("1. Transfer/sync the fixed files to your Linux VM")
    print("2. Run the password policy module again")
    print("3. The scripts should execute without '$\\r' errors")
else:
    print("[X] Some issues remain. Please review the files above.")

print("\nNote: Make sure to use the .gitattributes file to prevent future issues.")


