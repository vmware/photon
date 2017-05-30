#!/usr/bin/python2
#
#    Copyright (C) 2015 vmware inc.
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

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
import modules.commons
from jsonwrapper import JsonWrapper
from progressbar import ProgressBar
from window import Window
from actionresult import ActionResult
from __builtin__ import isinstance

class Installer(object):
    def __init__(self, install_config, maxy = 0, maxx = 0, iso_installer = False, rpm_path = "../stage/RPMS", log_path = "../stage/LOGS", ks_config = None):
        self.install_config = install_config
        self.ks_config = ks_config
        self.iso_installer = iso_installer
        self.rpm_path = rpm_path
        self.log_path = log_path
        self.mount_command = "./mk-mount-disk.sh"
        self.prepare_command = "./mk-prepare-system.sh"
        self.finalize_command = "./mk-finalize-system.sh"
        self.install_package_command = "./mk-install-package.sh"
        self.chroot_command = "./mk-run-chroot.sh"
        self.setup_grub_command = "./mk-setup-grub.sh"
        self.unmount_disk_command = "./mk-unmount-disk.sh"

        if self.iso_installer:
            self.working_directory = "/mnt/photon-root"
        elif 'working_directory' in self.install_config:
            self.working_directory = self.install_config['working_directory']
        else:
            self.working_directory = "/mnt/photon-root"
        self.photon_root = self.working_directory + "/photon-chroot";

        self.restart_command = "shutdown"

        if self.iso_installer:
            self.output = open(os.devnull, 'w')
        else:
            self.output = None

        if self.iso_installer:
            #initializing windows
            self.maxy = maxy
            self.maxx = maxx
            self.height = 10
            self.width = 75
            self.progress_padding = 5

            self.progress_width = self.width - self.progress_padding
            self.starty = (self.maxy - self.height) / 2
            self.startx = (self.maxx - self.width) / 2
            self.window = Window(self.height, self.width, self.maxy, self.maxx, 'Installing Photon', False)
            self.progress_bar = ProgressBar(self.starty + 3, self.startx + self.progress_padding / 2, self.progress_width)

        signal.signal(signal.SIGINT, self.exit_gracefully)

    # This will be called if the installer interrupted by Ctrl+C or exception
    def exit_gracefully(self, signal, frame):
        if self.iso_installer:
            self.progress_bar.hide()
            self.window.addstr(0, 0, 'Opps, Installer got interrupted.\n\nPress any key to get to the bash...')
            self.window.content_window().getch()

        modules.commons.dump(modules.commons.LOG_FILE_NAME)        
        sys.exit(1)

    def install(self, params):
        try:
            return self.unsafe_install(params)
        except Exception as inst:
            if self.iso_installer:
                modules.commons.log(modules.commons.LOG_ERROR, repr(inst))
                self.exit_gracefully(None, None)
            else:
                raise

    def unsafe_install(self, params):

        if self.iso_installer:
            self.window.show_window()
            self.progress_bar.initialize('Initializing installation...')
            self.progress_bar.show()
            #self.rpm_path = "https://dl.bintray.com/vmware/photon_release_1.0_TP2_x86_64"
            if self.rpm_path.startswith("https://") or self.rpm_path.startswith("http://"):
                cmdoption = 's/baseurl.*/baseurl={}/g'.format(self.rpm_path.replace('/','\/'))
                process = subprocess.Popen(['sed', '-i', cmdoption,'/etc/yum.repos.d/photon-iso.repo']) 
                retval = process.wait()
                if retval != 0:
                    modules.commons.log(modules.commons.LOG_INFO, "Failed to reset repo")
                    self.exit_gracefully(None, None)

            cmdoption = 's/cachedir=\/var/cachedir={}/g'.format(self.photon_root.replace('/','\/'))
            process = subprocess.Popen(['sed', '-i', cmdoption,'/etc/tdnf/tdnf.conf']) 
            retval = process.wait()
            if retval != 0:
                modules.commons.log(modules.commons.LOG_INFO, "Failed to reset tdnf cachedir")
                self.exit_gracefully(None, None)
        self.execute_modules(modules.commons.PRE_INSTALL)

        self.initialize_system()

        if self.iso_installer:
            self.get_size_of_packages()
            selected_packages = self.install_config['packages']
            for package in selected_packages:
                self.progress_bar.update_message('Installing {0}...'.format(package))
                process = subprocess.Popen(['tdnf', 'install', package, '--installroot', self.photon_root, '--nogpgcheck', '--assumeyes'], stdout=self.output, stderr=subprocess.STDOUT)
                retval = process.wait()
                # 0 : succeed; 137 : package already installed; 65 : package not found in repo.
                if retval != 0 and retval != 137:
                    modules.commons.log(modules.commons.LOG_ERROR, "Failed install: {} with error code {}".format(package, retval))
                    self.exit_gracefully(None, None)
                self.progress_bar.increment(self.size_of_packages[package])
        else:
        #install packages
            for rpm in self.rpms_tobeinstalled:
                # We already installed the filesystem in the preparation
                if rpm['package'] == 'filesystem':
                    continue
                return_value = self.install_package(rpm['filename'])
                if return_value != 0:
                    self.exit_gracefully(None, None)


        if self.iso_installer:
            self.progress_bar.show_loading('Finalizing installation')

        self.finalize_system()

        if not self.install_config['iso_system']:
            # Execute post installation modules
            self.execute_modules(modules.commons.POST_INSTALL)

            # install grub
            try:
                if self.install_config['boot'] == 'bios':
                    process = subprocess.Popen([self.setup_grub_command, '-w', self.photon_root, "bios", self.install_config['disk']['disk'], self.install_config['disk']['root'], self.install_config['disk']['boot'], self.install_config['disk']['bootdirectory']], stdout=self.output)
                elif self.install_config['boot'] == 'efi':
                    process = subprocess.Popen([self.setup_grub_command, '-w', self.photon_root, "efi", self.install_config['disk']['disk'], self.install_config['disk']['root'], self.install_config['disk']['boot'], self.install_config['disk']['bootdirectory']], stdout=self.output)
            except:
                #install bios if variable is not set.
                process = subprocess.Popen([self.setup_grub_command, '-w', self.photon_root, "bios", self.install_config['disk']['disk'], self.install_config['disk']['root'], self.install_config['disk']['boot'], self.install_config['disk']['bootdirectory']], stdout=self.output)

            retval = process.wait()

            self.update_fstab()

        command = [self.unmount_disk_command, '-w', self.photon_root]
        if not self.install_config['iso_system']:
            command.extend(self.generate_partitions_param(reverse = True))
        process = subprocess.Popen(command, stdout=self.output)
        retval = process.wait()

        if self.iso_installer:
            self.progress_bar.hide()
            self.window.addstr(0, 0, 'Congratulations, Photon has been installed in {0} secs.\n\nPress any key to continue to boot...'.format(self.progress_bar.time_elapsed))
            if self.ks_config == None:
                self.window.content_window().getch()

        return ActionResult(True, None)
        
    def copy_rpms(self):
        # prepare the RPMs list
        json_pkg_to_rpm_map = JsonWrapper(self.install_config["pkg_to_rpm_map_file"])
        pkg_to_rpm_map = json_pkg_to_rpm_map.read()

        self.rpms_tobeinstalled = []
        selected_packages = self.install_config['packages']

        for pkg in selected_packages:
            if pkg in pkg_to_rpm_map:
                if not pkg_to_rpm_map[pkg]['rpm'] is None:
                    name = pkg_to_rpm_map[pkg]['rpm']
                    basename = os.path.basename(name)
                    self.rpms_tobeinstalled.append({'filename': basename, 'path': name, 'package' : pkg})

    def copy_files(self):
        # Make the photon_root directory if not exits
        process = subprocess.Popen(['mkdir', '-p', self.photon_root], stdout=self.output)
        retval = process.wait()

        # Copy the installer files
        process = subprocess.Popen(['cp', '-r', "../installer", self.photon_root], stdout=self.output)
        retval = process.wait()

        # Create the rpms directory
        process = subprocess.Popen(['mkdir', '-p', self.photon_root + '/RPMS'], stdout=self.output)
        retval = process.wait()
        self.copy_rpms()

    def bind_installer(self):
        # Make the photon_root/installer directory if not exits
        process = subprocess.Popen(['mkdir', '-p', os.path.join(self.photon_root, "installer")], stdout=self.output)
        retval = process.wait()
        # The function finalize_system will access the file /installer/mk-finalize-system.sh after chroot to photon_root. 
        # Bind the /installer folder to self.photon_root/installer, so that after chroot to photon_root,
        # the file can still be accessed as /installer/mk-finalize-system.sh.
        process = subprocess.Popen(['mount', '--bind', '/installer', os.path.join(self.photon_root, "installer")], stdout=self.output)
        retval = process.wait()

    def update_fstab(self):
        fstab_file = open(os.path.join(self.photon_root, "etc/fstab"), "w")
        fstab_file.write("#system\tmnt-pt\ttype\toptions\tdump\tfsck\n")

        for partition in self.install_config['disk']['partitions']:
            options = 'defaults'
            dump = 1
            fsck = 2

            if 'mountpoint' in partition and partition['mountpoint'] == '/':
                fsck = 1
            
            if partition['filesystem'] == 'swap':
                mountpoint = 'swap'
                dump = 0
                fsck = 0
            else:
                mountpoint = partition['mountpoint']

            fstab_file.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(
                partition['path'],
                mountpoint,
                partition['filesystem'],
                options,
                dump,
                fsck
                ))
        # Add the cdrom entry
        fstab_file.write("/dev/cdrom\t/mnt/cdrom\tiso9660\tro,noauto\t0\t0\n")

        fstab_file.close()

    def generate_partitions_param(self, reverse = False):
        if reverse:
            step = -1
        else:
            step = 1
        params = []
        for partition in self.install_config['disk']['partitions'][::step]:
            if partition["filesystem"] == "swap":
                continue

            params.extend(['--partitionmountpoint', partition["path"], partition["mountpoint"]])
        return params

    def initialize_system(self):
        #Setup the disk
        if (not self.install_config['iso_system']):
            command = [self.mount_command, '-w', self.photon_root]
            command.extend(self.generate_partitions_param())
            process = subprocess.Popen(command, stdout=self.output)
            retval = process.wait()
        
        if self.iso_installer:
            self.bind_installer()
            process = subprocess.Popen([self.prepare_command, '-w', self.photon_root, 'install'], stdout=self.output)
            retval = process.wait()
        else:
            self.copy_files()
            #Setup the filesystem basics
            process = subprocess.Popen([self.prepare_command, '-w', self.photon_root], stdout=self.output)
            retval = process.wait()
    
    def finalize_system(self):
        #Setup the disk
        process = subprocess.Popen([self.chroot_command, '-w', self.photon_root, self.finalize_command, '-w', self.photon_root], stdout=self.output)
        retval = process.wait()
        if self.iso_installer:

            modules.commons.dump(modules.commons.LOG_FILE_NAME)
            shutil.copy(modules.commons.LOG_FILE_NAME, self.photon_root + '/var/log/')

            # unmount the installer directory
            process = subprocess.Popen(['umount', os.path.join(self.photon_root, "installer")], stdout=self.output)
            retval = process.wait()
            # remove the installer directory
            process = subprocess.Popen(['rm', '-rf', os.path.join(self.photon_root, "installer")], stdout=self.output)
            retval = process.wait()
            # Disable the swap file
            process = subprocess.Popen(['swapoff', '-a'], stdout=self.output)
            retval = process.wait()
            # remove the tdnf cache directory and the swapfile.
            process = subprocess.Popen(['rm', '-rf', os.path.join(self.photon_root, "cache")], stdout=self.output)

    def install_package(self,  package_name):
        rpm_params = ''

        os.environ["RPMROOT"] = self.rpm_path
        rpm_params = rpm_params + ' --force '
        rpm_params = rpm_params + ' --root ' + self.photon_root
        rpm_params = rpm_params + ' --dbpath /var/lib/rpm '

        if ('type' in self.install_config and (self.install_config['type'] in ['micro', 'minimal'])) or self.install_config['iso_system']:
            rpm_params = rpm_params + ' --excludedocs '

        process = subprocess.Popen([self.install_package_command, '-w', self.photon_root, package_name, rpm_params],  stdout=self.output)

        return process.wait()

    def execute_modules(self, phase):
        modules_paths = glob.glob('modules/m_*.py')
        for mod_path in modules_paths:
            module = mod_path.replace('/', '.', 1)
            module = os.path.splitext(module)[0]
            try:
                __import__(module)
                mod = sys.modules[module]
            except ImportError:
                modules.commons.log(modules.commons.LOG_ERROR, 'Error importing module {}'.format(module))
                continue
            
            # the module default is disabled
            if not hasattr(mod, 'enabled') or mod.enabled == False:
                modules.commons.log(modules.commons.LOG_INFO, "module {} is not enabled".format(module))
                continue
            # check for the install phase
            if not hasattr(mod, 'install_phase'):
                modules.commons.log(modules.commons.LOG_ERROR, "Error: can not defind module {} phase".format(module))
                continue
            if mod.install_phase != phase:
                modules.commons.log(modules.commons.LOG_INFO, "Skipping module {0} for phase {1}".format(module, phase))
                continue
            if not hasattr(mod, 'execute'):
                modules.commons.log(modules.commons.LOG_ERROR, "Error: not able to execute module {}".format(module))
                continue
            mod.execute(module, self.ks_config, self.install_config, self.photon_root)

    def get_install_size_of_a_package(self, name_size_pairs, package):
        modules.commons.log(modules.commons.LOG_INFO, "Find the install size of: {} ".format(package))
        for index, name in enumerate(name_size_pairs, start=0):
            if name[name.find(":") + 1:].strip() == package.strip():  
                item = name_size_pairs[index + 1] 
                size = item[item.find("(") + 1:item.find(")")]
                return int(size)
        raise LookupError("Cannot find package {} in the repo.".format(package))
    def get_size_of_packages(self):
        #call tdnf info to get the install size of all the packages.
        process = subprocess.Popen(['tdnf', 'info', '--installroot', self.photon_root], stdout=subprocess.PIPE)
        out,err = process.communicate()
        if err != None and err != 0:
            modules.commons.log(modules.commons.LOG_ERROR, "Failed to get infomation from : {} with error code {}".format(package, err))

        name_size_pairs = re.findall("(?:^Name.*$)|(?:^.*Install Size.*$)", out, re.M)
        selected_packages = self.install_config['packages']
        self.size_of_packages = {}
        progressbar_num_items = 0
        for package in selected_packages:
            size = self.get_install_size_of_a_package(name_size_pairs, package)
            progressbar_num_items += size;
            self.size_of_packages[package] = size;
        self.progress_bar.update_num_items(progressbar_num_items)    


    def run(self, command, comment = None):
        if comment != None:
            modules.commons.log(modules.commons.LOG_INFO, "Installer: {} ".format(comment))
            self.progress_bar.update_loading_message(comment)

        modules.commons.log(modules.commons.LOG_INFO, "Installer: {} ".format(command))
        process = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE)
        out,err = process.communicate()
        if err != None and err != 0 and "systemd-tmpfiles" not in command:
            modules.commons.log(modules.commons.LOG_ERROR, "Installer: failed in {} with error code {}".format(command, err))
            modules.commons.log(modules.commons.LOG_ERROR, out)
            self.exit_gracefully(None, None)

        return err
