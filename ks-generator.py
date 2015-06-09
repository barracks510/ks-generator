#!/usr/bin/env python2
# 
# This program creates a ks.cfg file based of the configuration options given.
# 
# Copyright (c) 2015 Dennis Chen. All rights reserved.

from crypt import crypt
import random

hosts = {
"sorin1.cnsm.csulb.edu": "134.139.127.25",
"sorin2.cnsm.csulb.edu": "134.139.127.26",
"sorin3.cnsm.csulb.edu": "134.139.127.27",
"sorin4.cnsm.csulb.edu": "134.139.127.28",
"sorin5.cnsm.csulb.edu": "134.139.127.29",
"sorin6.cnsm.csulb.edu": "134.139.127.46",
"sorin7.cnsm.csulb.edu": "134.139.127.47",
"sorin8.cnsm.csulb.edu": "134.139.127.48",
"sorin9.cnsm.csulb.edu": "134.139.127.49",
"sorin10.cnsm.csulb.edu": "134.139.127.50",
"spot.cnsm.csulb.edu": "134.139.127.18",
"banana.cnsm.csulb.edu": "134.139.127.16",
"storage1.cnsm.csulb.edu": "134.139.127.19",
"storage2.cnsm.csulb.edu": "134.139.127.20",
"folding1.cnsm.csulb.edu": "134.139.127.31",
"folding2.cnsm.csulb.edu": "134.139.127.32" }

NS = "134.139.19.5"
NM = "255.255.255.128"
GW = "134.139.127.1"
DEV = "enp5s1"

print "Copyright (c) 2015 Dennis Chen. All rights reserved."

# Open a File HOSTNAME.CFG in WRITE mode
hostname = str(raw_input("Machine Host Name: "))
ks = open(hostname.replace(".", "-") + ".cfg", "w")
ks.write("#version=RHEL\n#Created by Dennis Chen's ks-generator. \n")

# Write CFG Header
ks.write("# System authorization information\nauth --enableshadow --passalgo=sha512\n")

if raw_input("NET INSTALL? [Y/n]: ") == "n":
	ks.write(
	"# Use hard drive installation media\nharddrive --dir=None --partition=/dev/mapper/live-base\n")
else:
	ks.write(
	"# Use CentOS 7 Mirrors\nurl --mirrorlist=http://mirror.centos.org/centos/7/os/x86_64/\n")

ks.write("# Do NOT run the Setup Agent on first boot\nfirstboot --disable\n# Keyboard layouts\nkeyboard --vckeymap=us --xlayouts='us'\n# System language\nlang en_US.UTF-8\n")

# Networking setup
print "Configuring Networking..."
if raw_input("IPv6 [Y/n]: ") == "n":
	pass
if raw_input("DHCP? [Y/n]: ") == "n":
	print "Confirm the following are correct before using CFG."
	print "Hostname: %s\nIP: %s" % (hostname, hosts[hostname])
	print "NS: %s\nNetmask: %s" % (NS, NM)
	print "Gateway: %s" % (GW)
	print "Device: %s" % (DEV)
	
	ks.write("network --activate --bootproto=static --device=")
	ks.write(DEV)
	ks.write(" --gateway=")
	ks.write(GW)
	ks.write(" --ip=")
	ks.write(hosts[hostname])
	ks.write(" --nameserver=")
	ks.write(NS)
	ks.write(" --netmask=")
	ks.write(NM)
	ks.write(" --hostname=")
	ks.write(hostname)
	ks.write("\n")
else:
	ks.write("network --activate --bootproto=dhcp")

# Set system timezone and chrony
ks.write("# System services (chrony)\nservices --enabled=\"chronyd\"\n")
ks.write("# System timezone\ntimezone America/Los_Angeles --isUtc --ntpservers=0.us.pool.ntp.org,1.us.pool.ntp.org,2.us.pool.ntp.org,3.us.pool.ntp.org\n")

# User Accounts
root_password = raw_input("Root password: ")
ks.write("#User Accounts\nrootpw --iscrypted " + crypt(root_password, "$6$"+str(random.random())))

user = raw_input("Username for non-root user: ")
user_fullname = raw_input("Full name for non-root user: ")
user_password = raw_input("User Password: ")


user_flags = "user --name=" + user + " --password" + crypt(user_password, "$6$"+str(random.random())) +" --iscrypted --gecos=\"" + user_fullname + "\""

if raw_input("Give Sudoer? [Y/n]") == "n":
	ks.write(user_flags + "\n")
else:
	user_flags += " --groups=wheel\n"
	ks.write(user_flags)

# # System bootloader configuration
# bootloader --location=mbr --boot-drive=sda
# # Partition clearing information
# clearpart --all --initlabel --drives=sda
# # Disk partitioning information
# 
# 

# Write hosts to /etc/hosts
ks.write("%post\n")
ks.write("#!/bin/bash\n")
for host in hosts:
	ks.write("echo -e \"" + hosts[host] + "\\t" + host + "\" >> /etc/hosts\n")
ks.write("%end\n\n")

# Disable RedHat KDump
ks.write("%addon com_redhat_kdump --disable --reserve-mb=auto\n")
ks.write("%end\n")


ks.close()

print "Setup complete."
print "Please read the DEPLOYMENT file distributed with this program. "

