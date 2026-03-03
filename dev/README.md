# Development Tools

This folder contains development utilities and documentation that are not required during runtime.

## Files

### Line Ending Tools

These tools fix Windows/Linux line ending compatibility issues:

- **`fix_line_endings.py`** - Converts all shell scripts from CRLF to LF line endings
  ```bash
  python dev/fix_line_endings.py
  ```

- **`verify_fix.py`** - Verifies password policy shell scripts have correct line endings
  ```bash
  python dev/check_line_endings.py
  ```


### Documentation

- **`LINE_ENDINGS.md`** - Complete guide to line ending issues and solutions
- **`FIX_SUMMARY.md`** - Summary of the line ending fix applied to password policy module

## When to Use These Tools

### Before Deploying to Linux

If you've been editing files on Windows and encounter errors like:
```
$'\r': command not found
syntax error: unexpected end of file
```

Run the fix script:
```bash
python dev/fix_line_endings.py
```

### After Editing Shell Scripts

If you manually edit any `.sh` files in your IDE, verify they have correct line endings:
```bash
python dev/check_line_endings.py
```

## Prevention

The `.gitattributes` file in the project root automatically ensures shell scripts use LF line endings. Configure your IDE:

- **PyCharm**: Bottom status bar → Click "CRLF" → Select "LF"
- **VS Code**: Bottom-right → Click "CRLF" → Select "LF"

## Note

These tools are for development only and are not needed when running the main application (`main.py`).

