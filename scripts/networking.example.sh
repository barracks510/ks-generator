#!/bin/bash
# NETWORKING
cat <<'EOF' >> /etc/hosts.allow
sshd:134.139.127.16     # banana
sshd:134.139.127.17     # perutz
sshd:134.139.127.18
sshd:134.139.127.19

sshd:134.139.127.31     # FOLDING1
sshd:134.139.127.32     # FOLDING2
sshd:134.139.127.33     # COLLECTION1
sshd:134.139.127.34     # COLLECTION2
sshd:134.139.127.35
sshd:134.139.127.36

sshd:134.139.127.38     # Eric S.
sshd:134.139.127.39     # Eric S.
sshd:134.139.127.40     # Eric S.
sshd:134.139.127.41     # Eric S.

sshd:134.139.127.56
EOF

cat <<'EOF' >> /etc/hosts.deny
ALL:ALL
EOF
