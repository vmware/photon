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
from menu import Menu

class OstreeInstaller(Installer):

    def __init__(self, install_config, maxy = 0, maxx = 0, iso_installer = False, rpm_path = "../stage/RPMS", log_path = "../stage/LOGS", ks_config = None):
        Installer.__init__(self, install_config, maxy, maxx, iso_installer, rpm_path, log_path, ks_config)
    
        self.win_height = 13
        self.win_width = 50
        self.menu_starty = self.starty + 3    
        self.ostree_host_menu_items = []
        self.ostree_host_menu_items.append(("Default RPM-OSTree Server", self.default_installation, []))
        self.ostree_host_menu_items.append(("Custom RPM-OSTree Server", self.custom_installation, []))
        self.host_menu = Menu(self.menu_starty,  self.maxx, self.ostree_host_menu_items)
        self.window = Window(self.win_height, self.win_width, self.maxy, self.maxx, 'Select OSTree Server', True, self.host_menu)
        self.default_repo = True

    def default_installation(self,  selected_item_params):
        self.default_repo = True
        return ActionResult(True, None)

    def custom_installation(self,  selected_item_params):
        self.default_repo = False
        success = False
        while not success:
            got_the_url = False
            while not got_the_url:
                ostree_url_reader = WindowStringReader(
                    self.maxy, self.maxx, 10, 70,
                    "ostree_repo_url", False,
                    "Please provide the URL of OSTree repo",
                    "OSTree Repo URL:", 2,
                    self.install_config,
                    "https://dl.bintray.com/vmware/photon/rpm-ostree/dev/x86_64/minimal")

                ret = ostree_url_reader.get_user_string(None)
                self.ostree_repo_url = ret.result
                got_the_url = ret.success

            ostree_ref_reader = WindowStringReader(self.maxy,
                self.maxx, 10, 70,
                "ostree_ref", False,
                "Please provide the Ref in OSTree repo",
                "OSTree Repo Ref:", 2,
                self.install_config,
                "dev/x86_64/minimal")

            ret = ostree_ref_reader.get_user_string(None)
            self.ostree_ref = ret.result
            success = ret.success

        return ActionResult(True, None)

    def get_ostree_repo_url(self):
        if self.ks_config != None:
            self.ostree_repo_url = self.ks_config['ostree_repo_url']
            self.ostree_ref = self.ks_config['ostree_repo_ref']
            return
        self.window.do_action()

    def deploy_ostree(self, repo_url, repo_ref):
        self.run("ostree admin --sysroot={} init-fs {}".format(self.photon_root, self.photon_root), "Initializing OSTree filesystem")
        self.run("ostree remote add --repo={}/ostree/repo --set=gpg-verify=false photon {}".format(self.photon_root, repo_url), "Adding OSTree remote")
        self.run("ostree pull --repo={}/ostree/repo photon {}".format(self.photon_root, repo_ref), "Pulling OSTree remote repo")
        self.run("ostree admin --sysroot={} os-init photon ".format(self.photon_root), "OSTree OS Initializing")
        self.run("ostree admin --sysroot={} deploy --os=photon photon/{}".format(self.photon_root, repo_ref), "Deploying")

    def do_systemd_tmpfiles_commands(self, commit_number):
        prefixes = ["/var/home",
            "/var/roothome",
            "/var/lib/rpm",
            "/var/opt",
            "/var/srv",
            "/var/userlocal",
            "/var/mnt",
            "/var/spool/mail"]

        for prefix in prefixes:
            command = "systemd-tmpfiles --create --boot --root={}/ostree/deploy/photon/deploy/{}.0 --prefix={}".format(self.photon_root, commit_number, prefix)
            self.run(command)

    def mount_devices_in_deployment(self, commit_number):
        for command in ["mount -t bind -o bind,defaults /dev  {}/ostree/deploy/photon/deploy/{}.0/dev",
            "mount -t devpts -o gid=5,mode=620 devpts  {}/ostree/deploy/photon/deploy/{}.0/dev/pts",
            "mount -t tmpfs -o defaults tmpfs  {}/ostree/deploy/photon/deploy/{}.0/dev/shm",
            "mount -t proc -o defaults proc  {}/ostree/deploy/photon/deploy/{}.0/proc",
            "mount -t bind -o bind,defaults /run  {}/ostree/deploy/photon/deploy/{}.0/run",
            "mount -t sysfs -o defaults sysfs  {}/ostree/deploy/photon/deploy/{}.0/sys" ]:
            self.run(command.format(self.photon_root, commit_number))

    def get_commit_number(self, ref):
        fileName = os.path.join(self.photon_root, "ostree/repo/refs/remotes/photon/{}".format(ref))
        commit_number = None
        with open (fileName, "r") as file:
            commit_number = file.read().replace('\n', '')
        return commit_number

    def unsafe_install(self, params):
        self.org_photon_root = self.photon_root
        sysroot_ostree = os.path.join(self.photon_root, "ostree")
        sysroot_boot = os.path.join(self.photon_root, "boot")
        loader0 = os.path.join(sysroot_boot, "loader.0")
        loader1 = os.path.join(sysroot_boot, "loader.1")

        boot0 = os.path.join(sysroot_ostree, "boot.0")
        boot1 = os.path.join(sysroot_ostree, "boot.1")

        boot01 = os.path.join(sysroot_ostree, "boot.0.1")
        boot11 = os.path.join(sysroot_ostree, "boot.1.1")

        self.get_ostree_repo_url()

        self.window.show_window()
        self.progress_bar.initialize("Initializing installation...")
        self.progress_bar.show()

        self.execute_modules(modules.commons.PRE_INSTALL)

        disk = self.install_config['disk']['disk']
        self.run("sgdisk -d 2 -n 2::+300M -n 3: -p {}".format(disk), "Updating partition table for OSTree")
        self.run("mkfs -t ext4 {}2".format(disk))
        self.run("mkfs -t ext4 {}3".format(disk))
        self.run("mount {}3 {}".format(disk, self.photon_root))
        self.run("mkdir -p {} ".format(sysroot_boot))
        self.run("mount {}2 {}".format(disk, sysroot_boot))

        self.deploy_ostree(self.ostree_repo_url, self.ostree_ref)

        commit_number = self.get_commit_number(self.ostree_ref)
        self.do_systemd_tmpfiles_commands(commit_number)

        self.mount_devices_in_deployment(commit_number)
        deployment = os.path.join(self.photon_root, "ostree/deploy/photon/deploy/" + commit_number + ".0/")

        deployment_boot = os.path.join(deployment, "boot")
        deployment_sysroot = os.path.join(deployment, "sysroot")

        self.run("mv {} {}".format(loader1, loader0))
        self.run("mv {} {}".format(boot1, boot0))
        self.run("mv {} {}".format(boot11, boot01))
        self.run("mount --bind {} {}".format(sysroot_boot, deployment_boot))
        self.run("mount --bind {} {}".format(self.photon_root, deployment_sysroot))
        self.run("chroot {} bash -c \"grub2-install /dev/sda\"".format(deployment))
        self.run("chroot {} bash -c \"grub2-mkconfig -o /boot/grub2/grub.cfg\"".format(deployment))
        self.run("mv {} {}".format(loader0, loader1))
        self.run("mv {} {}".format(boot0, boot1))
        self.run("mv {} {}".format(boot01, boot11))
        self.run("chroot {} bash -c \"ostree admin instutil set-kargs root=/dev/sda3 \"".format(deployment))
        sysroot_grub2_grub_cfg = os.path.join(self.photon_root, "boot/grub2/grub.cfg")
        self.run("ln -sf ../loader/grub.cfg {}".format(sysroot_grub2_grub_cfg))
        self.run("mv {} {}".format(loader1, loader0))
        self.run("mv {} {}".format(boot1, boot0))
        self.run("mv {} {}".format(boot11, boot01))


        deployment_fstab = os.path.join(deployment, "etc/fstab")
        self.run("echo \"/dev/sda2    /boot    ext4   defaults   1 2  \" >> {} ".format(deployment_fstab), "Adding /boot mount point in fstab")
        self.run("mount --bind {} {}".format(deployment, self.photon_root))
        self.progress_bar.show_loading("Starting post install modules")
        self.execute_modules(modules.commons.POST_INSTALL)

        self.run("{} {} {}".format(self.unmount_disk_command, '-w', self.photon_root))

        self.progress_bar.hide()
        self.window.addstr(0, 0,
            "Congratulations, Photon has been installed in {} secs.\n\nPress any key to continue to boot...".format(self.progress_bar.time_elapsed))
        if self.ks_config == None:
            self.window.content_window().getch()

        return ActionResult(True, None)

