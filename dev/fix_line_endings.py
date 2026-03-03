#!/usr/bin/env python3
"""
Fix line endings in shell scripts to use Unix LF instead of Windows CRLF.
This prevents the '$\\r': command not found' error when running scripts on Linux.
"""

import os
import glob

def convert_to_lf(file_path):
    """Convert a file from CRLF to LF line endings."""
    try:
        with open(file_path, 'rb') as f:
            content = f.read()

        # Check if file has CRLF
        if b'\r\n' in content:
            # Convert CRLF to LF
            content = content.replace(b'\r\n', b'\n')
            with open(file_path, 'wb') as f:
                f.write(content)
            print(f"✓ Converted: {file_path}")
            return True
        else:
            print(f"  Skipped (already LF): {file_path}")
            return False
    except Exception as e:
        print(f"✗ Error converting {file_path}: {e}")
        return False

def main():
    """Find and convert all shell scripts in the project."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Find all .sh files
    shell_files = glob.glob(os.path.join(base_dir, '**', '*.sh'), recursive=True)

    print(f"Found {len(shell_files)} shell script(s)")
    print("-" * 60)

    converted = 0
    for file_path in shell_files:
        if convert_to_lf(file_path):
            converted += 1

    print("-" * 60)
    print(f"\nConverted {converted} file(s) from CRLF to LF")

if __name__ == "__main__":
    main()

