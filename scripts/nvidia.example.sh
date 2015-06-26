#!/bin/bash
#
# This script searches for the appropriate PROPRIETARY NVIDIA driver for use in
# CentOS 7 and installs it. The developers of KS-GENERATOR do not endorse the
# proprietary driver, however it is here for your convience as an example of a
# setup script you may use with the program.

rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org
yum install http://www.elrepo.org/elrepo-release-7.0-2.el7.elrepo.noarch.rpm -y

# Enable if using Secure Boot.
#
# cat <<'EOF' > mokutil --import /etc/pki/elrepo/SECURE-BOOT-KEY-elrepo.org.der
# uefisecurebootpasswordplaceholder
# uefisecurebootpasswordplaceholder
# EOF

yum install nvidia-detect -y
yum remove xorg-x11-glamor -y

kmod_vers=$(nvidia-detect)
yum install $kmod_vers -y
yum install nvidia-x11-drv${kmod_vers#kmod_nvidia}-32bit

