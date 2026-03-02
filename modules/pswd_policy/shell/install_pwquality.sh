#!/bin/bash
# Install libpam-pwquality if not already installed

if ! dpkg -l | grep -q libpam-pwquality; then
    echo "Installing libpam-pwquality..."
    apt-get update -qq
    apt-get install -y libpam-pwquality
    echo "libpam-pwquality installed successfully"
else
    echo "libpam-pwquality is already installed"
fi

