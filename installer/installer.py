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
import urllib
import modules.commons
import xml.etree.ElementTree as ET
from jsonwrapper import JsonWrapper
from progressbar import ProgressBar
from window import Window
from actionresult import ActionResult

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
            return_value = self.install_package(rpm['filename'])
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
            try:
                if self.install_config['boot'] == 'bios':
                    process = subprocess.Popen([self.setup_grub_command, '-w', self.photon_root, "bios", self.install_config['disk']['disk'], self.install_config['disk']['root']], stdout=self.output)
                elif self.install_config['boot'] == 'efi':
                    process = subprocess.Popen([self.setup_grub_command, '-w', self.photon_root, "efi", self.install_config['disk']['disk'], self.install_config['disk']['root']], stdout=self.output)
            except:
                #install bios if variable is not set.
                process = subprocess.Popen([self.setup_grub_command, '-w', self.photon_root, "bios", self.install_config['disk']['disk'], self.install_config['disk']['root']], stdout=self.output)

            retval = process.wait()

        process = subprocess.Popen([self.unmount_disk_command, '-w', self.photon_root], stdout=self.output)
        retval = process.wait()

        if self.iso_installer:
            self.progress_bar.hide()
            self.window.addstr(0, 0, 'Congratulations, Photon has been installed in {0} secs.\n\nPress any key to continue to boot...'.format(self.progress_bar.time_elapsed))
            if self.ks_config == None:
                self.window.content_window().getch()

        return ActionResult(True, None)

    def download_file(self, url, directory):
        # TODO: Add errors handling
        urlopener = urllib.URLopener()
        urlopener.retrieve(url, os.path.join(directory, os.path.basename(url)))

    def download_rpms(self):
        repodata_dir = os.path.join(self.photon_root, 'RPMS/repodata')
        process = subprocess.Popen(['mkdir', '-p', repodata_dir], stdout=self.output)
        retval = process.wait()

        import hawkey
        self.install_factor = 1
        # Load the repo data
        sack = hawkey.Sack()
        
        repomd_filename = "repomd.xml"
        repomd_url = os.path.join(self.rpm_path, "repodata/repomd.xml")

        self.download_file(repomd_url, repodata_dir)

        # parse to the xml to get the primary and files list
        tree = ET.parse(os.path.join(repodata_dir, repomd_filename))
        # TODO: Get the namespace dynamically from the xml file
        ns = {'ns': 'http://linux.duke.edu/metadata/repo'}

        primary_location = tree.find("./ns:data[@type='primary']/ns:location", ns).get("href");
        filelists_location = tree.find("./ns:data[@type='filelists']/ns:location", ns).get("href");
        primary_filename = os.path.basename(primary_location);
        filelists_filename = os.path.basename(filelists_location);

        self.download_file(os.path.join(self.rpm_path, primary_location), repodata_dir)
        self.download_file(os.path.join(self.rpm_path, filelists_location), repodata_dir)
        
        repo = hawkey.Repo("installrepo")
        repo.repomd_fn = os.path.join(repodata_dir, repomd_filename)
        repo.primary_fn = os.path.join(repodata_dir, primary_filename)
        repo.filelists_fn = os.path.join(repodata_dir, filelists_filename)
        
        sack.load_yum_repo(repo, load_filelists=True)

        progressbar_num_items = 0
        self.rpms_tobeinstalled = []
        selected_packages = self.install_config['packages']
        for package in selected_packages:
            # Locate the package
            q = hawkey.Query(sack).filter(name=package)
            if (len(q) > 0):
                progressbar_num_items +=  q[0].size + q[0].size * self.install_factor
                self.rpms_tobeinstalled.append({'package': package, 'size': q[0].size, 'location': q[0].location, 'filename': os.path.basename(q[0].location)})
            else:
                print >> sys.stderr, "Package %s not found in the repo" % package
                #self.exit_gracefully(None, None)

        self.progress_bar.update_num_items(progressbar_num_items)

        # Download the rpms
        for rpm in self.rpms_tobeinstalled:
            message = 'Downloading {0}...'.format(rpm['filename'])
            self.progress_bar.update_message(message)
            self.download_file(os.path.join(self.rpm_path, rpm['location']), os.path.join(self.photon_root, "RPMS"))
            self.progress_bar.increment(rpm['size'])
        
        # update the rpms path
        self.rpm_path = os.path.join(self.photon_root, "RPMS")

    def copy_rpms(self):
        # prepare the RPMs list
        self.install_factor = 3
        rpms = []
        for root, dirs, files in os.walk(self.rpm_path):
            for name in files:
                file = os.path.join(root, name)
                size = os.path.getsize(file)
                rpms.append({'filename': name, 'path': file, 'size': size})

        progressbar_num_items = 0
        self.rpms_tobeinstalled = []
        selected_packages = self.install_config['packages']
        for package in selected_packages:
            pattern = package + '-[0-9]*.rpm'
            for rpm in rpms:
                if fnmatch.fnmatch(rpm['filename'], pattern):
                    rpm['package'] = package
                    self.rpms_tobeinstalled.append(rpm)
                    progressbar_num_items += rpm['size'] + rpm['size'] * self.install_factor
                    break

        if self.iso_installer:
            self.progress_bar.update_num_items(progressbar_num_items)

        # Copy the rpms
        for rpm in self.rpms_tobeinstalled:
            if self.iso_installer:
                message = 'Copying {0}...'.format(rpm['filename'])
                self.progress_bar.update_message(message)
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

        # Create the rpms directory
        process = subprocess.Popen(['mkdir', '-p', self.photon_root + '/RPMS'], stdout=self.output)
        retval = process.wait()

        if self.rpm_path.startswith("http://"):
            self.download_rpms()
        else:
            self.copy_rpms()

    def initialize_system(self):
        #Setup the disk
        if (not self.install_config['iso_system']):
            process = subprocess.Popen([self.mount_command, '-w', self.photon_root, self.install_config['disk']['root']], stdout=self.output)
            retval = process.wait()
        
        self.copy_files()
        
        #Setup the filesystem basics
        process = subprocess.Popen([self.prepare_command, '-w', self.photon_root], stdout=self.output)
        retval = process.wait()

    def finalize_system(self):
        #Setup the disk
        process = subprocess.Popen([self.chroot_command, '-w', self.photon_root, self.finalize_command, '-w', self.photon_root], stdout=self.output)
        retval = process.wait()
        initrd_dir = 'boot'
        initrd_file_name = 'initrd.img-no-kmods'
        if self.iso_installer:
            # just copy the initramfs /boot -> /photon_mnt/boot
            shutil.copy(os.path.join(initrd_dir, initrd_file_name), self.photon_root + '/boot/')
            # remove the installer directory
            process = subprocess.Popen(['rm', '-rf', os.path.join(self.photon_root, "installer")], stdout=self.output)
            retval = process.wait()
        else:
            #Build the initramfs by passing in the kernel version
            version_string = ''	
            for root, dirs, files in os.walk(self.rpm_path):
                for name in files:
                    if fnmatch.fnmatch(name, 'linux-[0-9]*.rpm'):
                        version_array = name.split('-')
                        if len(version_array) > 2:
                            version_string = version_array[1]

            if 'initrd_dir' in self.install_config:
                initrd_dir = self.install_config['initrd_dir']
            process = subprocess.Popen([self.chroot_command, '-w', self.photon_root, './mkinitramfs', '-n', os.path.join(initrd_dir, initrd_file_name), '-k', version_string],  stdout=self.output)
            retval = process.wait()


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

    def run(self, command, comment = None):
        if comment != None:
            print >> sys.stderr, "Installer: {} ".format(comment)
            self.progress_bar.update_loading_message(comment)

        print >> sys.stderr, "Installer: {} ".format(command)
        process = subprocess.Popen([command], shell=True, stdout=self.output)
        retval = process.wait()
        return retval