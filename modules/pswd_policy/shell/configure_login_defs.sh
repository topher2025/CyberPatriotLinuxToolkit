#!/bin/bash
# Configure /etc/login.defs password aging with secure settings

LOGIN_DEFS="/etc/login.defs"
BACKUP_FILE="${LOGIN_DEFS}.backup.$(date +%Y%m%d_%H%M%S)"

# Create backup
cp "$LOGIN_DEFS" "$BACKUP_FILE"
echo "Backup created: $BACKUP_FILE"

# Configure password aging settings
# Maximum password age: 90 days
sed -i 's/^PASS_MAX_DAYS.*/PASS_MAX_DAYS   90/' "$LOGIN_DEFS"

# Minimum password age: 1 day (prevents users from immediately changing back)
sed -i 's/^PASS_MIN_DAYS.*/PASS_MIN_DAYS   1/' "$LOGIN_DEFS"

# Password warning age: 7 days before expiration
sed -i 's/^PASS_WARN_AGE.*/PASS_WARN_AGE   7/' "$LOGIN_DEFS"

echo "Password aging configured successfully in /etc/login.defs"

