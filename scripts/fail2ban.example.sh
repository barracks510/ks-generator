#!/bin/bash
# FAIL2BAN

yum install deltarpm -y
yum update -y
yum install epel-release -y
yum install fail2ban -y

# SET SSH JAIL
cat <<'EOF' >> /etc/fail2ban/jail.local
[sshd]
enabled = true
filter = sshd
maxretry = 10
EOF
# SET SYSTEMD UNITFILE EDIT
mkdir -p /etc/systemd/system/fail2ban.service.d/
cat <<'EOF' >> /etc/systemd/system/fail2ban.service.d/capabilities.conf
[Service]
CapabilityBoundingSet=
CapabilityBoundingSet=CAP_DAC_READ_SEARCH CAP_NET_ADMIN CAP_NET_RAW
ReadOnlyDirectories=
ReadWriteDirectories=
ReadOnlyDirectories=/
ReadWriteDirectories=/var/run/fail2ban /var/lib/fail2ban /var/spool/postfix/maildrop /tmp /var/log
EOF
yum install nginx -y
#yum install yum-cron -y
yum update -y

