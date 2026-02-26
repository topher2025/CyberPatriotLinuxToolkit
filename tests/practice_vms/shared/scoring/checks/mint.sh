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

check "Apache hardened" "! grep -q 'Indexes' /etc/apache2/apache2.conf" 5
check "Samba secured" "! grep -q 'public=yes' /etc/samba/smb.conf" 5
check "Firewall active" "iptables -L | grep -q DROP" 5
check "Unauthorized users removed" "! id guest1 &>/dev/null" 5
check "Root SSH disabled" "! grep -q 'PermitRootLogin yes' /etc/ssh/sshd_config" 5
check "RSH Server removed" "! systemctl is-active rsh.socket" 5
check "Telnet removed" "! command -v telnetd &>/dev/null" 5
check "Hacking tools removed" "! command -v nmap &>/dev/null" 5
check "Password policy enforced" "grep -q 'minlen=12' /etc/pam.d/common-password" 5
check "Cron backdoor removed" "! [ -f /etc/cron.d/system_update ]" 5
