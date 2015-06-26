#!/bin/bash
yum install dnf -y
yum install dnf-automatic -y
dnf remove yum -y
dnf install dnf-yum -y
dnf update -y

