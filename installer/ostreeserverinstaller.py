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
import xml.etree.ElementTree as ET
from jsonwrapper import JsonWrapper
from progressbar import ProgressBar
from windowstringreader import WindowStringReader
from window import Window
from actionresult import ActionResult
from installer import Installer

class OstreeServerInstaller(Installer):

    def __init__(self, install_config, maxy = 0, maxx = 0, iso_installer = False, rpm_path = "../stage/RPMS", log_path = "../stage/LOGS", ks_config = None):
        Installer.__init__(self, install_config, maxy, maxx, iso_installer, rpm_path, log_path, ks_config)

    def unsafe_install(self, params):
        rpmrepo_url_reader = WindowStringReader(
            self.maxy, self.maxx, 10, 70,
            "rpm_repo_url", False,
            "Please provide the URL of RPM repo",
            "RPM Repo URL:", 2,
            self.install_config,
            "https://dl.bintray.com/vmware/photon/rpms/dev/")

        ret = rpmrepo_url_reader.get_user_string(None)
        self.rpm_repo_url = ret.result
        return Installer.unsafe_install(self, params)

    def finalize_system(self):
        Installer.finalize_system(self)

        self.run("mkdir -p {}/srv/rpm-ostree/".format(self.photon_root))
        self.run("cp *.inc {}/srv/rpm-ostree/".format(self.photon_root))
        self.run("cp ./mk-ostree-server.sh {}/srv/rpm-ostree/".format(self.photon_root))
        self.run("cp ./photon-base.json {}/srv/rpm-ostree/".format(self.photon_root))
        self.run("cp ./photon-ostree.repo {}/srv/rpm-ostree/".format(self.photon_root))
        with open("{}/srv/rpm-ostree/photon-ostree.repo".format(self.photon_root), "a") as myfile:
            myfile.write("baseurl={}".format(self.rpm_repo_url))

        self.run("mv {}/etc/resolv.conf {}/etc/resolv.conf.bak".format(self.photon_root, self.photon_root))
        self.run("cp /etc/resolv.conf {}/etc/resolv.conf".format(self.photon_root, self.photon_root))

        self.run("mount /dev/cdrom {}/mnt/cdrom".format(self.photon_root))
        self.run("chroot {} bash -c \"cd /srv/rpm-ostree; ./mk-ostree-server.sh /\"".format(self.photon_root))

        # Restore resolv.conf
        self.run("mv {}/etc/resolv.conf.bak {}/etc/resolv.conf".format(self.photon_root, self.photon_root))
