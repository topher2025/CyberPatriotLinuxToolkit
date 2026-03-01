#!/bin/bash

echo "=========================================="
echo "Provisioning Ubuntu Practice VM"
echo "=========================================="

# Update system
apt update -y
DEBIAN_FRONTEND=noninteractive apt upgrade -y

# Install Ubuntu desktop environment
echo "Installing Ubuntu desktop environment..."
DEBIAN_FRONTEND=noninteractive apt install -y ubuntu-desktop

# Configure auto-login for vagrant user
mkdir -p /etc/gdm3
cat > /etc/gdm3/custom.conf << EOF
[daemon]
AutomaticLoginEnable=true
AutomaticLogin=vagrant
EOF

systemctl set-default graphical.target

# Create authorized administrators (should have sudo)
useradd -m -s /bin/bash mwheeler
useradd -m -s /bin/bash dhenderson
useradd -m -s /bin/bash lsinclair
useradd -m -s /bin/bash nwheeler
useradd -m -s /bin/bash sharrington

# Set admin passwords (some weak, some strong)
echo "mwheeler:p4Lac|In11" | chpasswd
echo "dhenderson:w@teRG/\t3" | chpasswd
echo "lsinclair:ne\/er3ND5try" | chpasswd
echo "nwheeler:inn3r5tRE|\|gth" | chpasswd
echo "sharrington:ahoy" | chpasswd

# VULNERABILITY 1: Not all admins are in sudo group - dhenderson and sharrington missing
usermod -aG sudo mwheeler
usermod -aG sudo lsinclair
usermod -aG sudo nwheeler

# Create authorized regular users
useradd -m -s /bin/bash jhopper
useradd -m -s /bin/bash jbyers
useradd -m -s /bin/bash kwheeler
useradd -m -s /bin/bash mbrenner
useradd -m -s /bin/bash wbyers
useradd -m -s /bin/bash mmayfield
useradd -m -s /bin/bash bhargrove
useradd -m -s /bin/bash bnewby
useradd -m -s /bin/bash sowens
useradd -m -s /bin/bash rbuckley
useradd -m -s /bin/bash mbauman
useradd -m -s /bin/bash argyle
useradd -m -s /bin/bash emunson
useradd -m -s /bin/bash gareth
useradd -m -s /bin/bash jeff
useradd -m -s /bin/bash cpowell
useradd -m -s /bin/bash hwheeler
useradd -m -s /bin/bash ocallahan
useradd -m -s /bin/bash sbingham
useradd -m -s /bin/bash dantonov
useradd -m -s /bin/bash alexei

# VULNERABILITY 2: Unauthorized users present
useradd -m -s /bin/bash hacker
useradd -m -s /bin/bash guest
useradd -m -s /bin/bash backdoor

# VULNERABILITY 3: Unauthorized user has sudo access
echo "hacker:hacker123" | chpasswd
usermod -aG sudo hacker

# VULNERABILITY 4: Some users have no passwords
# jhopper, kwheeler, mbrenner left without passwords

# VULNERABILITY 5: Some users have weak passwords
echo "jbyers:password" | chpasswd
echo "wbyers:123456" | chpasswd
echo "bhargrove:qwerty" | chpasswd
echo "rbuckley:ubuntu" | chpasswd
echo "guest:guest" | chpasswd
echo "backdoor:backdoor" | chpasswd

# Set remaining user passwords
echo "mmayfield:Str0ng!Pass#22" | chpasswd
echo "bnewby:Complex@Pass99" | chpasswd
echo "sowens:SecureP@ssw0rd!" | chpasswd
echo "mbauman:MyP@ss2024!" | chpasswd
echo "argyle:S3cur3*Pass!" | chpasswd
echo "emunson:Dragonfire#2024" | chpasswd
echo "gareth:Knight!Quest99" | chpasswd
echo "jeff:P@ladin2024!" | chpasswd
echo "cpowell:Str0ngPwd#22" | chpasswd
echo "hwheeler:Secure*Pass88" | chpasswd
echo "ocallahan:Complex@99!" | chpasswd
echo "sbingham:MySecret#2024" | chpasswd
echo "dantonov:Rus5ian!Pass" | chpasswd
echo "alexei:Stranger#Thing5" | chpasswd

# VULNERABILITY 6: User wrongly given admin privileges
usermod -aG sudo jbyers

# VULNERABILITY 7: Password policy extremely weak
sed -i 's/pam_pwquality.so/pam_pwquality.so retry=10 minlen=1 difok=1/' /etc/pam.d/common-password

# VULNERABILITY 8: Maximum password age set too high
sed -i 's/^PASS_MAX_DAYS.*/PASS_MAX_DAYS 99999/' /etc/login.defs

# VULNERABILITY 9: Minimum password age set to 0
sed -i 's/^PASS_MIN_DAYS.*/PASS_MIN_DAYS 0/' /etc/login.defs

# VULNERABILITY 10: SSH installed and root login enabled
apt install -y openssh-server
sed -i 's/#PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config
echo "PermitEmptyPasswords yes" >> /etc/ssh/sshd_config

# VULNERABILITY 11: Insecure services installed
apt install -y vsftpd telnetd rsh-server

# VULNERABILITY 12: FTP anonymous login enabled
sed -i 's/anonymous_enable=NO/anonymous_enable=YES/' /etc/vsftpd.conf
sed -i 's/write_enable=NO/write_enable=YES/' /etc/vsftpd.conf

# VULNERABILITY 13: Firewall disabled
ufw disable

# VULNERABILITY 14: Services enabled that shouldn't be
systemctl enable vsftpd
systemctl enable ssh
systemctl enable telnet

# VULNERABILITY 15: Cron backdoor
echo "* * * * * root nc -lvp 4444 -e /bin/bash" > /etc/cron.d/backdoor
chmod 644 /etc/cron.d/backdoor

# VULNERABILITY 16: World writable sensitive files
chmod 777 /etc/passwd
chmod 666 /etc/shadow

# VULNERABILITY 17: Sudo no password for unauthorized user
echo "hacker ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
echo "guest ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# VULNERABILITY 18: Sensitive files with wrong permissions
echo "FLAG{ubuntu_passwords_leaked}" > /home/hacker/passwords.txt
chmod 777 /home/hacker/passwords.txt
echo "admin:P@ssw0rd123" > /home/guest/credentials.txt
chmod 644 /home/guest/credentials.txt

# VULNERABILITY 19: Prohibited media files
mkdir -p /home/hacker/media
wget -q -O /home/hacker/media/movie.mp4 https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-mp4-file.mp4 || echo "dummy video" > /home/hacker/media/movie.mp4
wget -q -O /home/jbyers/music.mp3 https://www.learningcontainer.com/wp-content/uploads/2020/02/Kalimba.mp3 || echo "dummy audio" > /home/jbyers/music.mp3
chown -R hacker:hacker /home/hacker/media

# VULNERABILITY 20: Hacking tools installed
apt install -y nmap netcat hydra john wireshark tcpdump

# Create the dragonfire group (but don't add users - that's part of the task)
groupadd dragonfire

# Install scoring
mkdir -p /opt/scoring
cp -r /home/vagrant/Desktop/scoring/* /opt/scoring/ 2>/dev/null || true
chmod +x /opt/scoring/score.sh 2>/dev/null || true
ln -sf /opt/scoring/score.sh /usr/local/bin/score 2>/dev/null || true

# Restart services
systemctl restart ssh 2>/dev/null || true
systemctl restart vsftpd 2>/dev/null || true

# Set file permissions - make dev directory read-only except for logs/ and data/
echo "Setting file permissions on dev directory..."
DEV_DIR="/home/vagrant/Desktop/dev"

# Remove write permissions from all directories recursively
find "$DEV_DIR" -type d -exec chmod u-w,g-w,o-w {} \;
find "$DEV_DIR" -type f -exec chmod u-w,g-w,o-w {} \;

# Grant write permissions to logs/ and data/ directories and their contents
if [ -d "$DEV_DIR/logs" ]; then
    find "$DEV_DIR/logs" -type d -exec chmod u+w,g+w,o+w {} \;
    find "$DEV_DIR/logs" -type f -exec chmod u+w,g+w,o+w {} \;
fi

if [ -d "$DEV_DIR/data" ]; then
    find "$DEV_DIR/data" -type d -exec chmod u+w,g+w,o+w {} \;
    find "$DEV_DIR/data" -type f -exec chmod u+w,g+w,o+w {} \;
fi

echo "File permissions configured successfully."

