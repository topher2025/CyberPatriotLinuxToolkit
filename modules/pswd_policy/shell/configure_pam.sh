#!/bin/bash
# Configure PAM password quality with secure settings

PAM_FILE="/etc/pam.d/common-password"
BACKUP_FILE="${PAM_FILE}.backup.$(date +%Y%m%d_%H%M%S)"

# Create backup
cp "$PAM_FILE" "$BACKUP_FILE"
echo "Backup created: $BACKUP_FILE"

# Remove any existing pam_pwquality.so line
sed -i '/pam_pwquality.so/d' "$PAM_FILE"

# Add new secure configuration
# Insert after the @include common-password line or at the beginning of password section
if grep -q "password.*requisite.*pam_pwhistory.so" "$PAM_FILE"; then
    # Insert before pwhistory if it exists
    sed -i '/password.*requisite.*pam_pwhistory.so/i password requisite pam_pwquality.so retry=3 minlen=12 difok=3 ucredit=-1 lcredit=-1 dcredit=-1 ocredit=-1 maxrepeat=2 gecoscheck=1 dictcheck=1 usercheck=1 enforcing=1' "$PAM_FILE"
else
    # Insert at the first password line
        sed -i '0,/^password/{/^password/i password requisite pam_pwquality.so retry=3 minlen=12 difok=3 ucredit=-1 lcredit=-1 dcredit=-1 ocredit=-1 maxrepeat=2 gecoscheck=1 dictcheck=1 usercheck=1 enforcing=1
}' "$PAM_FILE"
fi

echo "PAM password quality configured successfully"

