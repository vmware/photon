#!/usr/bin/python2
#
#    Copyright (C) 2015 vmware inc.
#
#    Author: Touseef Liaqat <tliaqat@vmware.com>

import subprocess
import curses
import os
import crypt
import re
import random
import string
import shutil
import fnmatch
import signal
import sys
import glob
import urllib
import modules.commons
from jsonwrapper import JsonWrapper
from progressbar import ProgressBar
from windowstringreader import WindowStringReader
from window import Window
from actionresult import ActionResult
from installer import Installer

class OstreeServerInstaller(Installer):

    def __init__(self, install_config, maxy = 0, maxx = 0, iso_installer = False, rpm_path = "../stage/RPMS", log_path = "../stage/LOGS"):
        Installer.__init__(self, install_config, maxy, maxx, iso_installer, rpm_path, log_path)

    def finalize_system(self):
        Installer.finalize_system(self)

        self.run("mkdir -p {}/srv/rpm-ostree/repo".format(self.photon_root))
        self.run("cp ./photon-base.json {}/srv/rpm-ostree/".format(self.photon_root))
        self.run("cp ./photon-minimal.json {}/srv/rpm-ostree/".format(self.photon_root))
        self.run("cp ./photon-full.json {}/srv/rpm-ostree/".format(self.photon_root))
        self.run("ln -s /etc/yum.repos.d/photon.repo {}/srv/rpm-ostree/photon-ostree.repo".format(self.photon_root))
        self.run("ln -s /etc/yum.repos.d/photon-iso.repo {}/srv/rpm-ostree/photon-iso-ostree.repo".format(self.photon_root))
        self.run("ln -s /etc/yum.repos.d/photon-updates.repo {}/srv/rpm-ostree/photon-updates-ostree.repo".format(self.photon_root))
        self.run("ln -s /etc/yum.repos.d/photon-extras.repo {}/srv/rpm-ostree/photon-extras-ostree.repo".format(self.photon_root))
        self.run("cp ./ostree-httpd.conf {}/srv/rpm-ostree/".format(self.photon_root))
        # Use a custom httpd service file for ostree server
        self.run("mkdir {}/etc/systemd/system/httpd.service.d".format(self.photon_root))
        self.run("cp ./10-httpd-service.conf {}/etc/systemd/system/httpd.service.d/".format(self.photon_root))
        self.run("cp ./get-ip-address.sh {}/usr/bin/".format(self.photon_root))
        self.run("cp ./ostree-server-greeting.txt {}/etc/issue".format(self.photon_root))
        self.run("ln -s /usr/lib/systemd/system/httpd.service {}/usr/lib/systemd/system/multi-user.target.wants/httpd.service".format(self.photon_root))
        self.run("tar -xf /mnt/cdrom/ostree-repo.tar.gz -C {}/srv/rpm-ostree/repo".format(self.photon_root))
        self.run("sed -i \"\\$i iptables -A INPUT -m state --state NEW,ESTABLISHED -p tcp --dport 80 -j ACCEPT\" {}/etc/systemd/scripts/iptables".format(self.photon_root))
        self.run("sed -i \"\\$i iptables -A INPUT -m state --state NEW,ESTABLISHED -p tcp --dport 443 -j ACCEPT\" {}/etc/systemd/scripts/iptables".format(self.photon_root))
        self.run("sed -i \"s/umask[ \t]\+[0-9]\+/umask 022/g\" {}/etc/profile".format(self.photon_root))


