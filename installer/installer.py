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

        modules.commons.dump(modules.commons.LOG_ERROR, modules.commons.LOG_FILE_NAME)        
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
            #self.rpm_path = "https://dl.bintray.com/vmware/photon_release_1.0_TP2_x86_64"
            if self.rpm_path.startswith("https://"):
                cmdoption = 's/baseurl.*/baseurl={}/g'.format(self.rpm_path.replace('/','\/'))
                process = subprocess.Popen(['sed', '-i', cmdoption,'/etc/yum.repos.d/photon-iso.repo']) 
                retval = process.wait()
                if retval != 0:
                    modules.commons.log(modules.commons.LOG_INFO, "Failed to reset repo")
                    self.exit_gracefully(None, None)
        self.execute_modules(modules.commons.PRE_INSTALL)

        self.initialize_system()

        if self.iso_installer:
            selected_packages = self.install_config['packages']
            self.progress_bar.update_num_items(len(selected_packages))
            for package in selected_packages:
                self.progress_bar.update_message('Installing {0}...'.format(package))
                process = subprocess.Popen(['tdnf', 'install', package, '--installroot', self.photon_root, '--nogpgcheck', '--assumeyes'], stdout=self.output, stderr=subprocess.STDOUT)
                retval = process.wait()
                # 0 : succeed; 137 : package already installed; 65 : package not found in repo.
                if retval != 0 and retval != 137:
                    modules.commons.log(modules.commons.LOG_ERROR, "Failed install: {} with error code {}".format(package, retval))
                    self.exit_gracefully(None, None)
                self.progress_bar.increment(1)
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
                modules.commons.log(modules.commons.LOG_WARNING, "Package {} not found in the repo".format(package))
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
            pattern2 = package + '-[a-z][0-9]*.rpm'
            for rpm in rpms:
                if fnmatch.fnmatch(rpm['filename'], pattern) or fnmatch.fnmatch(rpm['filename'], pattern2):
                    rpm['package'] = package
                    self.rpms_tobeinstalled.append(rpm)
                    progressbar_num_items += rpm['size'] + rpm['size'] * self.install_factor
                    break
        # Copy the rpms
        for rpm in self.rpms_tobeinstalled:
            shutil.copy(rpm['path'], self.photon_root + '/RPMS/')

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

    def bind_installer(self):
        # Make the photon_root directory if not exits
        process = subprocess.Popen(['mkdir', '-p', os.path.join(self.photon_root, "installer")], stdout=self.output)
        retval = process.wait()
        process = subprocess.Popen(['mount', '--bind', '/installer', os.path.join(self.photon_root, "installer")], stdout=self.output)
        retval = process.wait()

    def initialize_system(self):
        #Setup the disk
        if (not self.install_config['iso_system']):
            process = subprocess.Popen([self.mount_command, '-w', self.photon_root, self.install_config['disk']['root']], stdout=self.output)
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
        initrd_dir = 'boot'
        initrd_file_name = 'initrd.img-no-kmods'
        if self.iso_installer:
            # just copy the initramfs /boot -> /photon_mnt/boot
            shutil.copy(os.path.join(initrd_dir, initrd_file_name), self.photon_root + '/boot/')
            # remove the installer directory
            process = subprocess.Popen(['umount', os.path.join(self.photon_root, "installer")], stdout=self.output)
            retval = process.wait()
            process = subprocess.Popen(['rm', '-rf', os.path.join(self.photon_root, "installer")], stdout=self.output)
            retval = process.wait()
        elif not self.install_config['vmdk_install']:
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
            self.add_dracut_configuration()
            process = subprocess.Popen([self.chroot_command, '-w', self.photon_root, 'dracut', '--force', '--kver', version_string, os.path.join(initrd_dir,initrd_file_name)],  stdout=self.output, stderr=self.output)
            retval = process.wait()

    def add_dracut_configuration(self):
        if self.install_config.has_key("dracut_configuration"):
            dracut_configuration = []
            
            for key in self.install_config["dracut_configuration"].keys():
                keyValue = self.install_config["dracut_configuration"][key]
                config=key
                if isinstance(keyValue,list):
                    config=config+'+="'+" ".join(keyValue)+'"'
                else:
                    config=config+'="'+keyValue+'"'
                config=config+"\n"
                dracut_configuration.append(config)
            
            f = open(self.photon_root+"/etc/dracut.conf","a")
            f.writelines(dracut_configuration)
        

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

    def run(self, command, comment = None):
        if comment != None:
            modules.commons.log(modules.commons.LOG_INFO, "Installer: {} ".format(comment))
            self.progress_bar.update_loading_message(comment)

        modules.commons.log(modules.commons.LOG_INFO, "Installer: {} ".format(command))
        process = subprocess.Popen([command], shell=True, stdout=self.output)
        retval = process.wait()
        return retval
