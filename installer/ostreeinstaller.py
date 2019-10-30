#!/usr/bin/python2
#
#    Copyright (C) 2015 vmware inc.
#
#    Author: Touseef Liaqat <tliaqat@vmware.com>

import subprocess
import os
import re
import glob
import modules.commons
from installer import Installer
from commandutils import CommandUtils

class OstreeInstaller(object):

    def __init__(self, installer):
        self.repo_config = {}
        self.repo_read_conf()

        # simulate inheritance
        self.install_config = installer.install_config
        self.logger = installer.logger
        if self.install_config['ui']:
            self.progress_bar = installer.progress_bar
        self.photon_root = installer.photon_root
        self.installer_path = installer.installer_path
        self._create_fstab = installer._create_fstab
        self.exit_gracefully = installer.exit_gracefully
        self._get_uuid = installer._get_uuid
        self.cmd = CommandUtils(self.logger)

    def get_ostree_repo_url(self):
        self.default_repo = self.install_config['ostree'].get('default_repo', False);
        if not self.default_repo:
            self.ostree_repo_url = self.install_config['ostree']['repo_url']
            self.ostree_ref = self.install_config['ostree']['repo_ref']

    def repo_read_conf(self):
        with open("ostree-release-repo.conf") as repo_conf:
            for line in repo_conf:
                name, value = line.partition("=")[::2]
                self.repo_config[name] = value.strip(' \n\t\r')

    def pull_repo(self, repo_url, repo_ref):
        self.run([['ostree', 'remote', 'add', '--repo={}/ostree/repo'.format(self.photon_root), '--set=gpg-verify=false', 'photon', '{}'.format(repo_url)]], "Adding OSTree remote")
        if self.default_repo:
            self.run([['ostree', 'pull-local', '--repo={}/ostree/repo'.format(self.photon_root), '{}'.format(self.local_repo_path)]], "Pulling OSTree repo")
            cmd = []
            cmd.append(['mv', '{}/ostree/repo/refs/heads'.format(self.photon_root), '{}/ostree/repo/refs/remotes/photon'.format(self.photon_root)])
            cmd.append(['mkdir', '-p', '{}/ostree/repo/refs/heads'.format(self.photon_root)])
            self.run(cmd)
        else:
            self.run([['ostree', 'pull', '--repo={}/ostree/repo'.format(self.photon_root), 'photon', '{}'.format(repo_ref)]], "Pulling OSTree remote repo")

    def deploy_ostree(self, repo_url, repo_ref):
        self.run([['ostree', 'admin', '--sysroot={}'.format(self.photon_root), 'init-fs', '{}'.format(self.photon_root)]], "Initializing OSTree filesystem")
        self.pull_repo(repo_url, repo_ref)
        self.run([['ostree', 'admin', '--sysroot={}'.format(self.photon_root), 'os-init', 'photon']], "OSTree OS Initializing")
        self.run([['ostree', 'admin', '--sysroot={}'.format(self.photon_root), 'deploy', '--os=photon', 'photon:{}'.format(repo_ref)]], "Deploying")


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
            command = ['systemd-tmpfiles', '--create', '--boot', '--root={}/ostree/deploy/photon/deploy/{}.0'.format(self.photon_root, commit_number), '--prefix={}'.format(prefix)]
            self.run([command], "systemd-tmpfiles command done")

    def create_symlink_directory(self, deployment):
        command = []
        command.append(['mkdir', '-p', '{}/sysroot/tmp'.format(deployment)])
        command.append(['mkdir', '-p', '{}/sysroot/ostree'.format(deployment)])
        command.append(['mkdir', '-p', '{}/run/media'.format(deployment)])
        self.run(command, "symlink directory created")

    def mount_devices_in_deployment(self, commit_number):
        command = []
        command.append(['mount', '-t', 'bind', '-o', 'bind,defaults', '/dev', '{}/ostree/deploy/photon/deploy/{}.0/dev'.format(self.photon_root, commit_number)])
        command.append(['mount', '-t', 'devpts', '-o', 'gid=5,mode=620', 'devpts', '{}/ostree/deploy/photon/deploy/{}.0/dev/pts'.format(self.photon_root, commit_number)])
        command.append(['mount', '-t', 'tmpfs', '-o', 'defaults', 'tmpfs', '{}/ostree/deploy/photon/deploy/{}.0/dev/shm'.format(self.photon_root, commit_number)])
        command.append(['mount', '-t', 'proc', '-o', 'defaults', 'proc', '{}/ostree/deploy/photon/deploy/{}.0/proc'.format(self.photon_root, commit_number)])
        command.append(['mount', '-t', 'bind', '-o', 'bind,defaults', '/run',  '{}/ostree/deploy/photon/deploy/{}.0/run'.format(self.photon_root, commit_number)])
        command.append(['mount', '-t', 'sysfs', '-o', 'defaults', 'sysfs',  '{}/ostree/deploy/photon/deploy/{}.0/sys'.format(self.photon_root, commit_number)])
        self.run(command, "mounting done")

    def get_commit_number(self, ref):
        fileName = os.path.join(self.photon_root, "ostree/repo/refs/remotes/photon/{}".format(ref))
        commit_number = None
        with open (fileName, "r") as file:
            commit_number = file.read().replace('\n', '')
        return commit_number

    def install(self):
        """
        Ostree Installer  Main
        """
        sysroot_boot = self.photon_root
        sysroot_bootefi = self.photon_root
        for partition in self.install_config['partitions']:
            if partition.get('mountpoint', '') == '/':
                root_partition = partition
            if partition.get('mountpoint', '') == '/boot':
                boot_partition = partition
                sysroot_boot = sysroot_boot + partition['mountpoint']
            if partition.get('mountpoint', '') == '/boot/efi' and partition['filesystem'] == 'vfat':
                sysroot_bootefi = sysroot_bootefi + partition['mountpoint']

        sysroot_ostree = os.path.join(self.photon_root, "ostree")
        loader0 = os.path.join(sysroot_boot, "loader.0")
        loader1 = os.path.join(sysroot_boot, "loader.1")

        boot0 = os.path.join(sysroot_ostree, "boot.0")
        boot1 = os.path.join(sysroot_ostree, "boot.1")

        boot01 = os.path.join(sysroot_ostree, "boot.0.1")
        boot11 = os.path.join(sysroot_ostree, "boot.1.1")

        self.get_ostree_repo_url()

        bootmode = self.install_config['bootmode']
        if bootmode == 'dualboot' or bootmode == 'efi':
            mount_efi = []
            mount_efi.append(['mkdir', '-p', '{}/EFI/Boot'.format(sysroot_bootefi)])
            mount_efi.append(['mkdir', '-p', '{}/boot/grub2/fonts'.format(sysroot_bootefi)])
            mount_efi.append(['cp', '-r', '{}/boot/.'.format(self.installer_path), '{}/boot/grub2/fonts/'.format(sysroot_bootefi)])
            self.run(mount_efi, "Mount and setup efi partition")

        if self.default_repo:
            self.run([['mkdir', '-p', '{}/repo'.format(self.photon_root)]])
            if self.install_config['ui']:
                self.progress_bar.show_loading("Unpacking local OSTree repo")
            self.run([['tar', '--warning=none', '-xf', '/mnt/cdrom/ostree-repo.tar.gz', '-C' '{}/repo'.format(self.photon_root)]])
            self.local_repo_path = "{}/repo".format(self.photon_root)
            self.ostree_repo_url = self.repo_config['OSTREEREPOURL']
            self.ostree_ref = self.repo_config['OSTREEREFS']
            if self.install_config['ui']:
                self.progress_bar.update_loading_message("Unpacking done")

        self.deploy_ostree(self.ostree_repo_url, self.ostree_ref)

        commit_number = self.get_commit_number(self.ostree_ref)
        self.do_systemd_tmpfiles_commands(commit_number)

        self.mount_devices_in_deployment(commit_number)
        deployment = os.path.join(self.photon_root, "ostree/deploy/photon/deploy/" + commit_number + ".0/")
        self.create_symlink_directory(deployment)

        deployment_boot = os.path.join(deployment, "boot")
        deployment_sysroot = os.path.join(deployment, "sysroot")

        if os.path.exists(loader1):
            cmd = []
            cmd.append(['mv', '{}'.format(loader1), '{}'.format(loader0)])
            cmd.append(['mv', '{}'.format(boot1), '{}'.format(boot0)])
            cmd.append(['mv', '{}'.format(boot11), '{}'.format(boot01)])
            self.run(cmd)
        mount_bind = []
        mount_bind.append(['mount', '--bind', '{}'.format(sysroot_boot), '{}'.format(deployment_boot)])
        mount_bind.append(['mount', '--bind', '{}'.format(self.photon_root), '{}'.format(deployment_sysroot)])
        self.run(mount_bind)
        if bootmode == 'dualboot' or bootmode == 'bios':
            self.run([['chroot', '{}'.format(deployment), 'bash', '-c', 'grub2-install --target=i386-pc --force --boot-directory=/boot {};'.format(self.install_config['disk'])]], "Generating Grub binaries for BIOS mode")
        if bootmode == 'dualboot' or bootmode == 'efi':
            self.run([['cp', '-r', '{}/EFI_x86_64/BOOT/.'.format(self.installer_path), '{}/EFI/Boot/'.format(sysroot_bootefi)]], "Generating grub.cfg for efi boot")
            with open(os.path.join(sysroot_bootefi, 'boot/grub2/grub.cfg'), "w") as grub_cfg:
                grub_cfg.write("search -n -u {} -s\n".format(self._get_uuid(boot_partition['path'])))
                grub_cfg.write("configfile /grub2/grub.cfg\n")
            self.run([['chroot', '{}'.format(deployment), 'bash', '-c', 'mkdir -p /boot/grub2;']])

        self.run([['chroot', '{}'.format(deployment), 'bash', '-c', 'grub2-mkconfig -o /boot/grub2/grub.cfg;']])
        if os.path.exists(loader0):
            cmd = []
            cmd.append(['mv', '{}'.format(loader0), '{}'.format(loader1)])
            cmd.append(['mv', '{}'.format(boot0), '{}'.format(boot1)])
            cmd.append(['mv', '{}'.format(boot01), '{}'.format(boot11)])
            self.run(cmd)
        self.run([['chroot', '{}'.format(deployment), 'bash', '-c', "ostree admin instutil set-kargs '$photon_cmdline' '$systemd_cmdline' root={};".format(root_partition['path'])]], "Add ostree  menu entry in grub.cfg")
        sysroot_grub2_grub_cfg = os.path.join(self.photon_root, "boot/grub2/grub.cfg")
        self.run([['ln', '-sf', '../loader/grub.cfg', '{}'.format(sysroot_grub2_grub_cfg)]])
        if os.path.exists(loader1):
            cmd = []
            cmd.append(['mv', '{}'.format(loader1), '{}'.format(loader0)])
            cmd.append(['mv', '{}'.format(boot1), '{}'.format(boot0)])
            cmd.append(['mv', '{}'.format(boot11), '{}'.format(boot01)])
            self.run(cmd)

        deployment_fstab = os.path.join(deployment, "etc/fstab")
        self._create_fstab(deployment_fstab)

        self.run([['mount', '--bind', '{}'.format(deployment), '{}'.format(self.photon_root)]], "Bind deployment to photon root")

    def run(self, commands, comment = None):
        if comment != None:
            self.logger.info("Installer: {} ".format(comment))
            if self.install_config['ui']:
                self.progress_bar.update_loading_message(comment)

        for command in commands:
            retval = self.cmd.run(command)
            if retval != 0 and "systemd-tmpfiles" not in command:
                self.logger.error("Installer: failed in {} with error code {}".format(command, retval))
                self.exit_gracefully()
        return retval
