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

class Installer(object):
    def __init__(self, install_config, maxy = 0, maxx = 0, iso_installer = False, tools_path = "../stage", rpm_path = "../stage/RPMS", log_path = "../stage/LOGS", ks_config = None):
        self.install_config = install_config
        self.ks_config = ks_config
        self.iso_installer = iso_installer
        self.tools_path = tools_path
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

        self.install_factor = 3
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
            self.window.addstr(0, 0, 'Opps, Installer got inturrupted.\n\nPress any key to get to the bash...')
            self.window.content_window().getch()
        
        sys.exit(1)

    def install(self, params):
        try:
            return self.unsafe_install(params)
        except:
            if self.iso_installer:
                self.exit_gracefully(None, None)
            else:
                raise

    def unsafe_install(self, params):

        if self.iso_installer:
            self.window.show_window()
            self.progress_bar.initialize('Initializing installation...')
            self.progress_bar.show()

        self.execute_modules(modules.commons.PRE_INSTALL)

        self.initialize_system()

        #install packages
        for rpm in self.rpms_tobeinstalled:
            # We already installed the filesystem in the preparation
            if rpm['package'] == 'filesystem':
                continue
            if self.iso_installer:
                self.progress_bar.update_message('Installing {0}...'.format(rpm['package']))
            return_value = self.install_package(rpm['package'])
            if return_value != 0:
                self.exit_gracefully(None, None)
            if self.iso_installer:
                self.progress_bar.increment(rpm['size'] * self.install_factor)

        if self.iso_installer:
            self.progress_bar.show_loading('Finalizing installation')

        self.finalize_system()

        if not self.install_config['iso_system']:
            # Execute post installation modules
            self.execute_modules(modules.commons.POST_INSTALL)

            # install grub
            process = subprocess.Popen([self.setup_grub_command, '-w', self.photon_root, self.install_config['disk']['disk'], self.install_config['disk']['root']], stdout=self.output)
            retval = process.wait()

        process = subprocess.Popen([self.unmount_disk_command, '-w', self.photon_root], stdout=self.output)
        retval = process.wait()

        if self.iso_installer:
            self.progress_bar.hide()
            self.window.addstr(0, 0, 'Congratulations, Photon has been installed in {0} secs.\n\nPress any key to continue to boot...'.format(self.progress_bar.time_elapsed))
            if self.ks_config == None:
                self.window.content_window().getch()

        return ActionResult(True, None)

    def copy_rpms(self):
        # prepare the RPMs list
        rpms = []
        for root, dirs, files in os.walk(self.rpm_path):
            for name in files:
                file = os.path.join(root, name)
                size = os.path.getsize(file)
                rpms.append({'name': name, 'path': file, 'size': size})

        progressbar_num_items = 0
        self.rpms_tobeinstalled = []
        selected_packages = self.install_config['packages']
        for package in selected_packages:
            pattern = package + '-[0-9]*.rpm'
            for rpm in rpms:
                if fnmatch.fnmatch(rpm['name'], pattern):
                    rpm['package'] = package
                    self.rpms_tobeinstalled.append(rpm)
                    progressbar_num_items += rpm['size'] + rpm['size'] * self.install_factor
                    break

        process = subprocess.Popen(['mkdir', '-p', self.photon_root + '/RPMS'], stdout=self.output)
        retval = process.wait()

        if self.iso_installer:
            self.progress_bar.update_num_items(progressbar_num_items)

        # Copy the rpms
        for rpm in self.rpms_tobeinstalled:
            shutil.copy(rpm['path'], self.photon_root + '/RPMS/')
            if self.iso_installer:
                self.progress_bar.increment(rpm['size'])

    def copy_files(self):
        # Make the photon_root directory if not exits
        process = subprocess.Popen(['mkdir', '-p', self.photon_root], stdout=self.output)
        retval = process.wait()

        # Copy the installer files
        process = subprocess.Popen(['cp', '-r', "../installer", self.photon_root], stdout=self.output)
        retval = process.wait()

        self.copy_rpms()

    def initialize_system(self):
        #Setup the disk
        if (not self.install_config['iso_system']):
            process = subprocess.Popen([self.mount_command, '-w', self.photon_root, self.install_config['disk']['root']], stdout=self.output)
            retval = process.wait()
        
        self.copy_files()
        
        #Setup the filesystem basics
        process = subprocess.Popen([self.prepare_command, '-w', self.photon_root, self.tools_path], stdout=self.output)
        retval = process.wait()

    def finalize_system(self):
        #Setup the disk
        process = subprocess.Popen([self.chroot_command, '-w', self.photon_root, self.finalize_command, '-w', self.photon_root], stdout=self.output)
        retval = process.wait()
        if self.iso_installer:
            # just copy the initramfs /boot -> /photon_mnt/boot
            shutil.copy('/boot/initrd.img-no-kmods', self.photon_root + '/boot/')
        else:
            #Build the initramfs
            process = subprocess.Popen([self.chroot_command, '-w', self.photon_root, './mkinitramfs', '-n', '/boot/initrd.img-no-kmods'],  stdout=self.output)
            retval = process.wait()


    def install_package(self,  package_name):
        rpm_params = ''
        
        if ('type' in self.install_config and (self.install_config['type'] in ['micro', 'minimal'])) or self.install_config['iso_system']:
            rpm_params = rpm_params + ' --excludedocs '

        process = subprocess.Popen([self.chroot_command, '-w', self.photon_root, self.install_package_command, '-w', self.photon_root, package_name, rpm_params],  stdout=self.output)
        return process.wait()

    def execute_modules(self, phase):
        modules = glob.glob('modules/m_*.py')
        for mod_path in modules:
            module = mod_path.replace('/', '.', 1)
            module = os.path.splitext(module)[0]
            try:
                __import__(module)
                mod = sys.modules[module]
            except ImportError:
                print >> sys.stderr,  'Error importing module %s' % module
                continue
            
            # the module default is disabled
            if not hasattr(mod, 'enabled') or mod.enabled == False:
                print >> sys.stderr,  "module %s is not enabled" % module
                continue
            # check for the install phase
            if not hasattr(mod, 'install_phase'):
                print >> sys.stderr,  "Error: can not defind module %s phase" % module
                continue
            if mod.install_phase != phase:
                print >> sys.stderr,  "Skipping module %s for phase %s" % (module, phase)
                continue
            if not hasattr(mod, 'execute'):
                print >> sys.stderr,  "Error: not able to execute module %s" % module
                continue
            mod.execute(module, self.ks_config, self.install_config, self.photon_root)
