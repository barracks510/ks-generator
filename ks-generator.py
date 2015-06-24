#!/usr/bin/env python3
#
# This program creates a ks.cfg file based of the configuration options given.
#
# Copyright (C) 2015 Dennis Chen <barracks510@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#

from crypt import crypt
from random import random
from subprocess import check_output
import groups

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
    "folding2.cnsm.csulb.edu": "134.139.127.32"}

NS = "134.139.19.5"
NM = "255.255.255.128"
GW = "134.139.127.1"
DEV = "enp5s1"

print("KS-GENERATOR Copyright (C) 2015 Dennis Chen <barracks510@gmail.com>")
print("This program comes with ABSOLUTELY NO WARRANTY. This is free software,")
print("and you are welcome to redistribute it under certain conditions. \n\n")

# Open a File HOSTNAME.CFG in WRITE mode
hostname = str(input("Machine Host Name: "))
ks = open(hostname.replace(".", "-") + ".cfg", "w")
ks.write("#version=RHEL\n#Created by Dennis Chen's ks-generator. \n")

# Write CFG Header
ks.write("# System authorization information\n")
ks.write("auth --enableshadow --passalgo=sha512\n")

if input("NET INSTALL? [Y/n]: ").lower() == "n":
    ks.write("# Use hard drive installation media\n")
    ks.write("harddrive --dir=None --partition=/dev/mapper/live-base\n")
else:
    ks.write("# Use CentOS 7 Mirrors\n")
    ks.write("url --url=http://mirrors.kernel.org/centos/7/os/x86_64/\n")

ks.write("# Do NOT run the Setup Agent on first boot\n")
ks.write("firstboot --disable\n")
ks.write("# Keyboard layouts\nkeyboard --vckeymap=us --xlayouts='us'\n")
ks.write("# System language\nlang en_US.UTF-8\n")

# Networking setup
print("Configuring Networking...")
if input("DHCP? [Y/n]: ").lower() == "n":
    print("Confirm the following are correct before using CFG.")
    print("Hostname: %s\nIP: %s" % (hostname, hosts[hostname]))
    print("NS: %s\nNetmask: %s" % (NS, NM))
    print("Gateway: %s" % (GW))
    print("Device: %s" % (DEV))

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
    if input("IPv6 [Y/n]: ").lower() == "n":
        ks.write(" --noipv6\n")
    else:
        ks.write("\n")
else:
    ks.write("network --activate --bootproto=dhcp")
    if input("IPv6 [Y/n]: ").lower() == "n":
        ks.write(" --noipv6\n")
    else:
        ks.write("\n")

# Set system timezone and chrony
ks.write("# System services (chrony)\nservices --enabled=\"chronyd\"\n")
ks.write("# System timezone\n")
ks.write("timezone America/Los_Angeles --isUtc --ntpservers=0.us.pool.ntp.org")
ks.write(",1.us.pool.ntp.org,2.us.pool.ntp.org,3.us.pool.ntp.org\n")

# User Accounts
root_pass = input("Root password: ")
ks.write("#User Accounts\n")
ks.write("rootpw --iscrypted " +
         crypt(root_pass, "$6$" + str(random())) + "\n")

user = input("Username for non-root user: ")
user_fullname = input("Full name for non-root user: ")
user_password = input("User Password: ")


user_flags = "user --name=" + user + " --password=" + \
    crypt(user_password, "$6$" + str(random())) + \
    " --iscrypted --gecos=\"" + user_fullname + "\""

if input("Give Sudoer? [Y/n]") == "n":
    ks.write(user_flags + "\n")
else:
    user_flags += " --groups=wheel\n"
    ks.write(user_flags + "\n")

# Setup GRUB Bootloader
grub_flags = "bootloader --location=mbr --boot-drive=sda --timeout=1"

print("RedHat recommends setting up a boot loader password on every system.")
print("An unprotected boot loader can allow a potential attacker to modify a")
print("system's boot options and gain unauthorized root access to a system. ")

ks.write("# GRUB Bootloader Options\n")

if input("Set GRUB Password? [Y/n]: ").lower() == "n":
    ks.write(grub_flags + "\n")
else:
    try:
        from passlib.hash import grub_pbkdf2_sha512 as grub_sha
        grub_password = input("GRUB Password: ")

        grub_crypt = grub_sha.encrypt(grub_password, rounds=10000)
        if len(grub_crypt) != 282:
            print("GRUB password could not be encrypted. ")
            print("Password will not be installed. ")
            ks.write(grub_flags + "\n")
        else:
            grub_flags += " --iscrypted --password=" + grub_crypt
            ks.write(grub_flags + "\n")
    except ImportError:
        print("GRUB password could not be encrypted. ")
        print("Do you have python-passlib installed?")
        print("Password will not be installed. ")
        ks.write(grub_flags + "\n")

# READ supplied DISK layout and WRITE changes
disk_location = input("DISK layout CONFIGURATION location: ")
if disk_location:
    try:
        disk = open(disk_location, "r")
    except IOError:
        print("Configuration doesn't exist at specified location.")
        print("Using AutoPartitioning.")
        ks.write("autopart\n")
    else:
        disk_layout = disk.read()
        disk.close()
        ks.write(disk_layout + "\n")
else:
    print("Using AutoPartitioning.")
    ks.write("autopart\n")

# Install CORE, BASE and NTP Packages
meta = groups.create_groups()
satisfied_list = {}

satisfied = False

print("The following are the Computing Environments avaliabled for EL7")
for environment in meta["environments"]:
    print(" - ", environment.name)
while not satisfied:
    environment_choice = input("What environment would you like?").lower()
    environment_choice = environment_choice.replace("_", " ")
    environment_choice = environment_choice.replace("-", " ")
    bad_count = 0
    for environment in meta["environments"]:
        if environment_choice[:4] in environment.abbrev:
            print("You selected", environment.name)
            satisfied_list["environment"] = environment.abbrev
            satisfied = True
            break
        elif bad_count == len(meta["environments"]):
            print("Your environment choice was not found. ")
            print("Please enter it again. ")
            break
        else:
            bad_count += 1

ks.write("%packages\n")
ks.write("@" + satisfied_list["environment"] + "\n")
ks.write("policycoreutils\n")
ks.write("policycoreutils-python\n")
ks.write("selinux-policy\n")
ks.write("selinux-policy-targeted\n")
ks.write("libselinux-utils\n")
ks.write("setroubleshoot-server\n")
ks.write("setools\n")
ks.write("setools-console\n")
ks.write("mcstrans\n")
ks.write("%end\n")

# Write hosts to /etc/hosts
ks.write("%post --interpreter=/usr/bin/bash \n")
ks.write("#!/bin/bash\n")
for host in hosts:
    ks.write("echo -e \"" + hosts[host] + "\\t" + host + "\" >> /etc/hosts\n")
try:
    script = open("./scripts/script.sh", "r")
    ks.write(script.read())
    script.close()
except IOError:
    print("No script in the scripts directory!")
ks.write("%end\n\n")

# Disable RedHat KDump
ks.write("%addon com_redhat_kdump --disable --reserve-mb=auto\n")
ks.write("%end\n\n")

# Reboot after finished installation
ks.write("shutdown\n")

ks.close()

print("Setup complete.")
print("Please read the DEPLOYMENT file distributed with this program. ")
