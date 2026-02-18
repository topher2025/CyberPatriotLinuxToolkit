#!/bin/bash
# Quick setup script for passwordless sudo configuration
# Run this in WSL to configure sudo for CyberPatriot testing

echo "=========================================="
echo "CyberPatriot Sudo Configuration Setup"
echo "=========================================="
echo ""

# Get current username
USERNAME=$(whoami)
echo "Current user: $USERNAME"
echo ""

# Create sudoers file content
SUDOERS_FILE="/etc/sudoers.d/cyber-patriot"
SUDOERS_CONTENT="# Cyber Patriot - Passwordless sudo configuration
$USERNAME ALL=(ALL) NOPASSWD: /usr/sbin/useradd
$USERNAME ALL=(ALL) NOPASSWD: /usr/sbin/deluser
$USERNAME ALL=(ALL) NOPASSWD: /usr/sbin/usermod
$USERNAME ALL=(ALL) NOPASSWD: /usr/sbin/groupadd
$USERNAME ALL=(ALL) NOPASSWD: /usr/sbin/groupdel
$USERNAME ALL=(ALL) NOPASSWD: /usr/bin/gpasswd"

echo "This script will create: $SUDOERS_FILE"
echo ""
echo "With the following content:"
echo "----------------------------------------"
echo "$SUDOERS_CONTENT"
echo "----------------------------------------"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
fi

# Create the sudoers file
echo "$SUDOERS_CONTENT" | sudo tee "$SUDOERS_FILE" > /dev/null

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Sudoers file created successfully!"

    # Verify syntax
    sudo visudo -c -f "$SUDOERS_FILE"

    if [ $? -eq 0 ]; then
        echo "✓ Sudoers syntax is valid!"
        echo ""
        echo "Testing passwordless sudo..."

        # Test if it works
        if sudo -n true 2>/dev/null; then
            echo "✓ Passwordless sudo is working!"
            echo ""
            echo "=========================================="
            echo "Setup Complete!"
            echo "=========================================="
            echo ""
        else
            echo "⚠ Note: You may need to start a new shell for changes to take effect."
        fi
    else
        echo "✗ Error: Invalid sudoers syntax"
        sudo rm -f "$SUDOERS_FILE"
        exit 1
    fi
else
    echo "✗ Error: Failed to create sudoers file"
    exit 1
fi

