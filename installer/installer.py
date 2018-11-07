"""
Photon installer
"""
#    Copyright (C) 2015 vmware inc.
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

import subprocess
import os
import shutil
import signal
import sys
import glob
import modules.commons
from jsonwrapper import JsonWrapper
from progressbar import ProgressBar
from window import Window
from actionresult import ActionResult

class Installer(object):
    """
    Photon installer
    """
    mount_command = "./mk-mount-disk.sh"
    prepare_command = "./mk-prepare-system.sh"
    finalize_command = "./mk-finalize-system.sh"
    chroot_command = "./mk-run-chroot.sh"
    setup_grub_command = "./mk-setup-grub.sh"
    unmount_disk_command = "./mk-unmount-disk.sh"

    def __init__(self, install_config, maxy=0, maxx=0, iso_installer=False,
                 rpm_path="../stage/RPMS", log_path="../stage/LOGS", log_level="info"):
        self.install_config = install_config
        self.install_config['iso_installer'] = iso_installer
        self.rpm_path = rpm_path
        self.log_path = log_path
        self.log_level = log_level

        if 'working_directory' in self.install_config:
            self.working_directory = self.install_config['working_directory']
        else:
            self.working_directory = "/mnt/photon-root"
        self.photon_root = self.working_directory + "/photon-chroot"
        self.rpms_tobeinstalled = None

        if self.install_config['iso_installer']:
            self.output = open(os.devnull, 'w')
            #initializing windows
            height = 10
            width = 75
            progress_padding = 5

            progress_width = width - progress_padding
            starty = (maxy - height) // 2
            startx = (maxx - width) // 2
            self.window = Window(height, width, maxy, maxx,
                                 'Installing Photon', False)
            self.progress_bar = ProgressBar(starty + 3,
                                            startx + progress_padding // 2,
                                            progress_width)

        else:
            self.output = None
        signal.signal(signal.SIGINT, self.exit_gracefully)

    def install(self, params):
        """
        Install photon system and handle exception
        """
        del params
        try:
            return self._unsafe_install()
        except Exception as inst:
            if self.install_config['iso_installer']:
                modules.commons.log(modules.commons.LOG_ERROR, repr(inst))
                self.exit_gracefully(None, None)
            else:
                raise

    def _unsafe_install(self):
        """
        Install photon system
        """
        self._setup_install_repo()
        self._initialize_system()
        self._install_packages()
        self._enable_network_in_chroot()
        self._finalize_system()

        self._disable_network_in_chroot()
        self._cleanup_and_exit()
        return ActionResult(True, None)

    def exit_gracefully(self, signal1, frame1):
        """
        This will be called if the installer interrupted by Ctrl+C, exception
        or other failures
        """
        del signal1
        del frame1
        if self.install_config['iso_installer']:
            self.progress_bar.hide()
            self.window.addstr(0, 0, 'Oops, Installer got interrupted.\n\n' +
                               'Press any key to get to the bash...')
            self.window.content_window().getch()

        modules.commons.dump(modules.commons.LOG_FILE_NAME)
        sys.exit(1)

    def _cleanup_and_exit(self):
        """
        Unmount the disk, eject cd and exit
        """
        command = [Installer.unmount_disk_command, '-w', self.photon_root]
        if not self.install_config['iso_system']:
            command.extend(self._generate_partitions_param(reverse=True))
        process = subprocess.Popen(command, stdout=self.output)
        retval = process.wait()
        if retval != 0:
            modules.commons.log(modules.commons.LOG_ERROR, "Failed to unmount disks")
        if self.install_config['iso_installer']:
            self.progress_bar.hide()
            self.window.addstr(0, 0, 'Congratulations, Photon has been installed in {0} secs.\n\n'
                               'Press any key to continue to boot...'
                               .format(self.progress_bar.time_elapsed))
            self._eject_cdrom()

    def _copy_rpms(self):
        """
        Prepare RPM list and copy rpms
        """
        # prepare the RPMs list
        json_pkg_to_rpm_map = JsonWrapper(self.install_config["pkg_to_rpm_map_file"])
        pkg_to_rpm_map = json_pkg_to_rpm_map.read()

        self.rpms_tobeinstalled = []
        selected_packages = self.install_config['packages']

        for pkg in selected_packages:
            versionindex = pkg.rfind("-")
            if versionindex == -1:
                raise Exception("Invalid pkg name: " + pkg)
            package = pkg[:versionindex]
            if pkg in pkg_to_rpm_map:
                if pkg_to_rpm_map[pkg]['rpm'] is not None:
                    name = pkg_to_rpm_map[pkg]['rpm']
                    basename = os.path.basename(name)
                    self.rpms_tobeinstalled.append({'filename': basename, 'path': name,
                                                    'package' : package})

        # Copy the rpms
        for rpm in self.rpms_tobeinstalled:
            shutil.copy(rpm['path'], self.photon_root + '/RPMS/')

    def _copy_files(self):
        """
        Copy the rpm files and instal scripts.
        """
        # Make the photon_root directory if not exits
        process = subprocess.Popen(['mkdir', '-p', self.photon_root], stdout=self.output)
        retval = process.wait()
        if retval != 0:
            modules.commons.log(modules.commons.LOG_ERROR, "Fail to create the root directory")
            self.exit_gracefully(None, None)

        # Copy the installer files
        process = subprocess.Popen(['cp', '-r', "../installer", self.photon_root],
                                   stdout=self.output)
        retval = process.wait()
        if retval != 0:
            modules.commons.log(modules.commons.LOG_ERROR, "Fail to copy install scripts")
            self.exit_gracefully(None, None)

        # Create the rpms directory
        process = subprocess.Popen(['mkdir', '-p', self.photon_root + '/RPMS'],
                                   stdout=self.output)
        retval = process.wait()
        if retval != 0:
            modules.commons.log(modules.commons.LOG_ERROR, "Fail to create the rpms directory")
            self.exit_gracefully(None, None)
        self._copy_rpms()

    def _bind_installer(self):
        """
        Make the photon_root/installer directory if not exits
        The function finalize_system will access the file /installer/mk-finalize-system.sh
        after chroot to photon_root.
        Bind the /installer folder to self.photon_root/installer, so that after chroot
        to photon_root,
        the file can still be accessed as /installer/mk-finalize-system.sh.
        """
        # Make the photon_root/installer directory if not exits
        if(subprocess.call(['mkdir', '-p',
                            os.path.join(self.photon_root, "installer")]) != 0 or
           subprocess.call(['mount', '--bind', '/installer',
                            os.path.join(self.photon_root, "installer")]) != 0):
            modules.commons.log(modules.commons.LOG_ERROR, "Fail to bind installer")
            self.exit_gracefully(None, None)
    def _unbind_installer(self):
        # unmount the installer directory
        process = subprocess.Popen(['umount', os.path.join(self.photon_root,
                                                           "installer")],
                                   stdout=self.output)
        retval = process.wait()
        if retval != 0:
            modules.commons.log(modules.commons.LOG_ERROR,
                                "Fail to unbind the installer directory")
        # remove the installer directory
        process = subprocess.Popen(['rm', '-rf', os.path.join(self.photon_root, "installer")],
                                   stdout=self.output)
        retval = process.wait()
        if retval != 0:
            modules.commons.log(modules.commons.LOG_ERROR,
                                "Fail to remove the installer directory")
    def _bind_repo_dir(self):
        """
        Bind repo dir for tdnf installation
        """
        rpm_cache_dir = self.photon_root + '/cache/tdnf/photon-iso/rpms'
        if self.rpm_path.startswith("https://") or self.rpm_path.startswith("http://"):
            return
        if (subprocess.call(['mkdir', '-p', rpm_cache_dir]) != 0 or
                subprocess.call(['mount', '--bind', self.rpm_path, rpm_cache_dir]) != 0):
            modules.commons.log(modules.commons.LOG_ERROR, "Fail to bind cache rpms")
            self.exit_gracefully(None, None)

    def _unbind_repo_dir(self):
        """
        Unbind repo dir after installation
        """
        rpm_cache_dir = self.photon_root + '/cache/tdnf/photon-iso/rpms'
        if self.rpm_path.startswith("https://") or self.rpm_path.startswith("http://"):
            return
        if (subprocess.call(['umount', rpm_cache_dir]) != 0 or
                subprocess.call(['rm', '-rf', rpm_cache_dir]) != 0):
            modules.commons.log(modules.commons.LOG_ERROR, "Fail to unbind cache rpms")
            self.exit_gracefully(None, None)

    def _update_fstab(self):
        """
        update fstab
        """
        with open(os.path.join(self.photon_root, "etc/fstab"), "w") as fstab_file:
            fstab_file.write("#system\tmnt-pt\ttype\toptions\tdump\tfsck\n")

            for partition in self.install_config['disk']['partitions']:
                options = 'defaults'
                dump = 1
                fsck = 2

                if 'mountpoint' in partition and partition['mountpoint'] == '/':
                    options = options + ',barrier,noatime,noacl,data=ordered'
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

    def _generate_partitions_param(self, reverse=False):
        """
        Generate partition param for mount command
        """
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

    def _initialize_system(self):
        """
        Prepare the system to install photon
        """
        #Setup the disk
        if not self.install_config['iso_system']:
            command = [Installer.mount_command, '-w', self.photon_root]
            command.extend(self._generate_partitions_param())
            process = subprocess.Popen(command, stdout=self.output)
            retval = process.wait()
            if retval != 0:
                modules.commons.log(modules.commons.LOG_INFO,
                                    "Failed to setup the disk for installation")
                self.exit_gracefully(None, None)

        if self.install_config['iso_installer']:
            self._bind_installer()
            self._bind_repo_dir()
            process = subprocess.Popen([Installer.prepare_command, '-w',
                                        self.photon_root, 'install'],
                                       stdout=self.output)
            retval = process.wait()
            if retval != 0:
                modules.commons.log(modules.commons.LOG_INFO,
                                    "Failed to bind the installer and repo needed by tdnf")
                self.exit_gracefully(None, None)
        else:
            self._copy_files()
            #Setup the filesystem basics
            process = subprocess.Popen([Installer.prepare_command, '-w', self.photon_root],
                                       stdout=self.output)
            retval = process.wait()
            if retval != 0:
                modules.commons.log(modules.commons.LOG_INFO,
                                    "Failed to setup the file systems basics")
                self.exit_gracefully(None, None)

    def _finalize_system(self):
        """
        Finalize the system after the installation
        """
        #Setup the disk
        process = subprocess.Popen([Installer.chroot_command, '-w', self.photon_root,
                                    Installer.finalize_command, '-w', self.photon_root],
                                   stdout=self.output)
        retval = process.wait()
        if retval != 0:
            modules.commons.log(modules.commons.LOG_ERROR,
                                "Fail to setup th target system after the installation")

        if self.install_config['iso_installer']:

            modules.commons.dump(modules.commons.LOG_FILE_NAME)
            shutil.copy(modules.commons.LOG_FILE_NAME, self.photon_root + '/var/log/')
            shutil.copy(modules.commons.TDNF_LOG_FILE_NAME, self.photon_root +
                        '/var/log/')

            self._unbind_installer()
            self._unbind_repo_dir()
            # Disable the swap file
            process = subprocess.Popen(['swapoff', '-a'], stdout=self.output)
            retval = process.wait()
            if retval != 0:
                modules.commons.log(modules.commons.LOG_ERROR,
                                    "Fail to swapoff")
            # remove the tdnf cache directory and the swapfile.
            process = subprocess.Popen(['rm', '-rf', os.path.join(self.photon_root, "cache")],
                                       stdout=self.output)
            retval = process.wait()
            if retval != 0:
                modules.commons.log(modules.commons.LOG_ERROR,
                                    "Fail to remove the cache")
        if not self.install_config['iso_system']:
            # Execute post installation modules
            self._execute_modules(modules.commons.POST_INSTALL)
            if os.path.exists(modules.commons.KS_POST_INSTALL_LOG_FILE_NAME):
                shutil.copy(modules.commons.KS_POST_INSTALL_LOG_FILE_NAME,
                            self.photon_root + '/var/log/')

            if self.install_config['iso_installer'] and os.path.isdir("/sys/firmware/efi"):
                self.install_config['boot'] = 'efi'
            # install grub
            if 'boot_partition_number' not in self.install_config['disk']:
                self.install_config['disk']['boot_partition_number'] = 1

            try:
                if self.install_config['boot'] == 'bios':
                    process = subprocess.Popen(
                        [Installer.setup_grub_command, '-w', self.photon_root,
                         "bios", self.install_config['disk']['disk'],
                         self.install_config['disk']['root'],
                         self.install_config['disk']['boot'],
                         self.install_config['disk']['bootdirectory'],
                         str(self.install_config['disk']['boot_partition_number'])],
                        stdout=self.output)
                elif self.install_config['boot'] == 'efi':
                    process = subprocess.Popen(
                        [Installer.setup_grub_command, '-w', self.photon_root,
                         "efi", self.install_config['disk']['disk'],
                         self.install_config['disk']['root'],
                         self.install_config['disk']['boot'],
                         self.install_config['disk']['bootdirectory'],
                         str(self.install_config['disk']['boot_partition_number'])],
                        stdout=self.output)
            except:
                #install bios if variable is not set.
                process = subprocess.Popen(
                    [Installer.setup_grub_command, '-w', self.photon_root,
                     "bios", self.install_config['disk']['disk'],
                     self.install_config['disk']['root'],
                     self.install_config['disk']['boot'],
                     self.install_config['disk']['bootdirectory'],
                     str(self.install_config['disk']['boot_partition_number'])],
                    stdout=self.output)
            retval = process.wait()

            self._update_fstab()

    def _execute_modules(self, phase):
        """
        Execute the scripts in the modules folder
        """
        sys.path.append("./modules")
        modules_paths = glob.glob('modules/m_*.py')
        for mod_path in modules_paths:
            module = mod_path.replace('/', '.', 1)
            module = os.path.splitext(module)[0]
            try:
                __import__(module)
                mod = sys.modules[module]
            except ImportError:
                modules.commons.log(modules.commons.LOG_ERROR,
                                    'Error importing module {}'.format(module))
                continue

            # the module default is disabled
            if not hasattr(mod, 'enabled') or mod.enabled is False:
                modules.commons.log(modules.commons.LOG_INFO,
                                    "module {} is not enabled".format(module))
                continue
            # check for the install phase
            if not hasattr(mod, 'install_phase'):
                modules.commons.log(modules.commons.LOG_ERROR,
                                    "Error: can not defind module {} phase".format(module))
                continue
            if mod.install_phase != phase:
                modules.commons.log(modules.commons.LOG_INFO,
                                    "Skipping module {0} for phase {1}".format(module, phase))
                continue
            if not hasattr(mod, 'execute'):
                modules.commons.log(modules.commons.LOG_ERROR,
                                    "Error: not able to execute module {}".format(module))
                continue

            mod.execute(self.install_config, self.photon_root)

    def _adjust_packages_for_vmware_virt(self):
        """
        Install linux_esx on Vmware virtual machine if requested
        """
        try:
            if self.install_config['install_linux_esx']:
                selected_packages = self.install_config['packages']
                try:
                    selected_packages.remove('linux')
                except ValueError:
                    pass
                try:
                    selected_packages.remove('initramfs')
                except ValueError:
                    pass
                selected_packages.append('linux-esx')
        except KeyError:
            pass

    def _setup_install_repo(self):
        """
        Setup the tdnf repo for installation
        """
        if self.install_config['iso_installer']:
            self.window.show_window()
            self.progress_bar.initialize('Initializing installation...')
            self.progress_bar.show()
            #self.rpm_path = "https://dl.bintray.com/vmware/photon_release_1.0_TP2_x86_64"
            if self.rpm_path.startswith("https://") or self.rpm_path.startswith("http://"):
                cmdoption = 's/baseurl.*/baseurl={}/g'.format(self.rpm_path.replace('/', r'\/'))
                process = subprocess.Popen(['sed', '-i', cmdoption,
                                            '/etc/yum.repos.d/photon-iso.repo'])
                retval = process.wait()
                if retval != 0:
                    modules.commons.log(modules.commons.LOG_INFO, "Failed to reset repo")
                    self.exit_gracefully(None, None)

            cmdoption = (r's/cachedir=\/var/cachedir={}/g'
                         .format(self.photon_root.replace('/', r'\/')))
            process = subprocess.Popen(['sed', '-i', cmdoption, '/etc/tdnf/tdnf.conf'])
            retval = process.wait()
            if retval != 0:
                modules.commons.log(modules.commons.LOG_INFO, "Failed to reset tdnf cachedir")
                self.exit_gracefully(None, None)

    def _install_packages(self):
        """
        Install packages using tdnf or rpm command
        """
        if self.install_config['iso_installer']:
            self._tdnf_install_packages()
        else:
            self._rpm_install_packages()

    def _tdnf_install_packages(self):
        """
        Install packages using tdnf command
        """
        self._adjust_packages_for_vmware_virt()
        selected_packages = self.install_config['packages']
        state = 0
        packages_to_install = {}
        total_size = 0
        with open(modules.commons.TDNF_CMDLINE_FILE_NAME, "w") as tdnf_cmdline_file:
            tdnf_cmdline_file.write("tdnf install --installroot {0} --nogpgcheck {1}"
                                    .format(self.photon_root, " ".join(selected_packages)))
        with open(modules.commons.TDNF_LOG_FILE_NAME, "w") as tdnf_errlog:
            process = subprocess.Popen(['tdnf', 'install'] + selected_packages +
                                       ['--installroot', self.photon_root, '--nogpgcheck',
                                        '--assumeyes'], stdout=subprocess.PIPE,
                                       stderr=tdnf_errlog)
            while True:
                output = process.stdout.readline().decode()
                if output == '':
                    retval = process.poll()
                    if retval is not None:
                        break
                if state == 0:
                    if output == 'Installing:\n':
                        state = 1
                elif state == 1: #N A EVR Size(readable) Size(in bytes)
                    if output == '\n':
                        state = 2
                        self.progress_bar.update_num_items(total_size)
                    else:
                        info = output.split()
                        package = '{0}-{1}.{2}'.format(info[0], info[2], info[1])
                        packages_to_install[package] = int(info[5])
                        total_size += int(info[5])
                elif state == 2:
                    if output == 'Downloading:\n':
                        self.progress_bar.update_message('Preparing ...')
                        state = 3
                elif state == 3:
                    self.progress_bar.update_message(output)
                    if output == 'Running transaction\n':
                        state = 4
                else:
                    modules.commons.log(modules.commons.LOG_INFO, "[tdnf] {0}".format(output))
                    prefix = 'Installing/Updating: '
                    if output.startswith(prefix):
                        package = output[len(prefix):].rstrip('\n')
                        self.progress_bar.increment(packages_to_install[package])

                    self.progress_bar.update_message(output)
            # 0 : succeed; 137 : package already installed; 65 : package not found in repo.
            if retval != 0 and retval != 137:
                modules.commons.log(modules.commons.LOG_ERROR,
                                    "Failed to install some packages, refer to {0}"
                                    .format(modules.commons.TDNF_LOG_FILE_NAME))
                self.exit_gracefully(None, None)
        self.progress_bar.show_loading('Finalizing installation')

    def _rpm_install_packages(self):
        """
        Install packages using rpm command
        """
        rpms = []
        for rpm in self.rpms_tobeinstalled:
            # We already installed the filesystem in the preparation
            if rpm['package'] == 'filesystem':
                continue
            rpms.append(rpm['filename'])
        rpms = set(rpms)
        rpm_paths = []
        for root, _, files in os.walk(self.rpm_path):
            for file in files:
                if file in rpms:
                    rpm_paths.append(os.path.join(root, file))

        # --nodeps is for hosts which do not support rich dependencies
        rpm_params = ['--nodeps', '--root', self.photon_root, '--dbpath',
                      '/var/lib/rpm']

        if (('type' in self.install_config and
             (self.install_config['type'] in ['micro', 'minimal'])) or
                self.install_config['iso_system']):
            rpm_params.append('--excludedocs')

        modules.commons.log(modules.commons.LOG_INFO,
                            "installing packages {0}, with params {1}"
                            .format(rpm_paths, rpm_params))
        process = subprocess.Popen(['rpm', '-Uvh'] + rpm_params + rpm_paths,
                                   stderr=subprocess.STDOUT)
        return_value = process.wait()
        if return_value != 0:
            self.exit_gracefully(None, None)


    def _eject_cdrom(self):
        """
        Eject the cdrom on request
        """
        eject_cdrom = True
        if 'ui_install' in self.install_config:
            self.window.content_window().getch()
        if 'eject_cdrom' in self.install_config and not self.install_config['eject_cdrom']:
            eject_cdrom = False
        if eject_cdrom:
            process = subprocess.Popen(['eject', '-r'], stdout=self.output)
            process.wait()

    def _enable_network_in_chroot(self):
        """
        Enable network in chroot
        """
        if os.path.exists("/etc/resolv.conf"):
            shutil.copy("/etc/resolv.conf", self.photon_root + '/etc/.')

    def _disable_network_in_chroot(self):
        """
        disable network in chroot
        """
        if os.path.exists(self.photon_root + '/etc/resolv.conf'):
            os.remove(self.photon_root + '/etc/resolv.conf')
