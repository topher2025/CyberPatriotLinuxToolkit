#!/bin/bash
# Configure /etc/login.defs password aging with secure settings

LOGIN_DEFS="/etc/login.defs"
BACKUP_FILE="${LOGIN_DEFS}.backup.$(date +%Y%m%d_%H%M%S)"

# Create backup
cp "$LOGIN_DEFS" "$BACKUP_FILE"
echo "Backup created: $BACKUP_FILE"

# Configure password aging settings
# Maximum password age: 90 days
if grep -qE '^[#[:space:]]*PASS_MAX_DAYS' "$LOGIN_DEFS"; then
    sed -i 's/^[#[:space:]]*PASS_MAX_DAYS.*/PASS_MAX_DAYS   90/' "$LOGIN_DEFS"
else
    echo 'PASS_MAX_DAYS   90' >> "$LOGIN_DEFS"
fi

# Minimum password age: 1 day (prevents users from immediately changing back)
if grep -qE '^[#[:space:]]*PASS_MIN_DAYS' "$LOGIN_DEFS"; then
    sed -i 's/^[#[:space:]]*PASS_MIN_DAYS.*/PASS_MIN_DAYS   1/' "$LOGIN_DEFS"
else
    echo 'PASS_MIN_DAYS   1' >> "$LOGIN_DEFS"
fi

# Password warning age: 7 days before expiration
if grep -qE '^[#[:space:]]*PASS_WARN_AGE' "$LOGIN_DEFS"; then
    sed -i 's/^[#[:space:]]*PASS_WARN_AGE.*/PASS_WARN_AGE   7/' "$LOGIN_DEFS"
else
    echo 'PASS_WARN_AGE   7' >> "$LOGIN_DEFS"
fi

echo "Password aging configured successfully in /etc/login.defs"

