check() {
  local check_name="$1"
  local check_command="$2"
  local points="$3"

  MAX_SCORE=$((MAX_SCORE + points))

  if eval "$check_command"; then
    SCORE=$((SCORE + points))
    echo "[+] $check_name (+$points)" >> $LOG
    CHECKS_HTML+="<div class=\"check-item passed\"><span class=\"check-icon\">✓</span><span class=\"check-text\">$check_name</span><span class=\"check-points\">+$points</span></div>"
  else
    echo "[-] $check_name" >> $LOG
    CHECKS_HTML+="<div class=\"check-item failed\"><span class=\"check-icon\">✗</span><span class=\"check-text\">$check_name</span><span class=\"check-points\">0/$points</span></div>"
  fi
}

check "UFW Enabled" "ufw status | grep -q active" 5
check "Root SSH Disabled" "! grep -q 'PermitRootLogin yes' /etc/ssh/sshd_config" 5
check "No unauthorized users" "! id hacker &>/dev/null" 10
check "Telnet removed" "! systemctl is-active telnet" 5
check "vsftpd removed" "! systemctl is-active vsftpd" 5
check "Password policy enforced" "grep -q 'minlen=12' /etc/pam.d/common-password" 5
check "SSH Protocol 2 only" "! grep -q 'Protocol.*1' /etc/ssh/sshd_config" 5
check "Empty passwords disabled" "! grep -q 'PermitEmptyPasswords yes' /etc/ssh/sshd_config" 5
check "Apache hardened" "! grep -q 'ServerTokens Full' /etc/apache2/conf-enabled/security.conf" 5
check "Samba share secured" "! grep -q 'guest ok = yes' /etc/samba/smb.conf" 5
