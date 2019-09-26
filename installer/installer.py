"""
Photon installer
"""
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

import subprocess
import os
import shutil
import signal
import sys
import glob
import re
import modules.commons
from logger import Logger
from commandutils import CommandUtils
from jsonwrapper import JsonWrapper
from progressbar import ProgressBar
from window import Window
from actionresult import ActionResult

class Installer(object):
    """
    Photon installer
    """
    mount_command = os.path.dirname(__file__)+"/mk-mount-disk.sh"
    finalize_command = "./mk-finalize-system.sh"
    chroot_command = os.path.dirname(__file__)+"/mk-run-chroot.sh"
    unmount_disk_command = os.path.dirname(__file__)+"/mk-unmount-disk.sh"
    default_partitions = [{"mountpoint": "/", "size": 0, "filesystem": "ext4"}]

    def __init__(self, install_config, maxy=0, maxx=0, iso_installer=False,
                 rpm_path=os.path.dirname(__file__)+"/../stage/RPMS", log_path=os.path.dirname(__file__)+"/../stage/LOGS", log_level="info"):
        self.exiting = False
        self.install_config = install_config
        self.install_config['iso_installer'] = iso_installer
        self.rpm_path = rpm_path
        self.logger = Logger.get_logger(log_path, log_level, not iso_installer)
        self.cmd = CommandUtils(self.logger)

        if 'working_directory' in self.install_config:
            self.working_directory = self.install_config['working_directory']
        else:
            self.working_directory = "/mnt/photon-root"

        self.cmd.run(['mkdir', '-p', self.working_directory])

        if 'prepare_script' in self.install_config:
            self.prepare_command = self.install_config['prepare_script']
        else:
            self.prepare_command = os.path.dirname(__file__)+"/mk-prepare-system.sh"

        self.photon_root = self.working_directory + "/photon-chroot"
        self.installer_path = os.path.dirname(os.path.abspath(__file__))
        self.tdnf_conf_path = self.working_directory + "/tdnf.conf"
        self.tdnf_repo_path = self.working_directory + "/photon-local.repo"
        self.rpm_cache_dir = self.photon_root + '/cache/tdnf/photon-local/rpms'
        # used by tdnf.conf as cachedir=, tdnf will append the rest
        self.rpm_cache_dir_short = self.photon_root + '/cache/tdnf'

        if 'setup_grub_script' in self.install_config:
            self.setup_grub_command = self.install_config['setup_grub_script']
        else:
            self.setup_grub_command = os.path.dirname(__file__)+"/mk-setup-grub.sh"
        self.rpms_tobeinstalled = None

        if self.install_config['iso_installer']:
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

        signal.signal(signal.SIGINT, self.exit_gracefully)

    def install(self):
        """
        Install photon system and handle exception
        """
        if self.install_config['iso_installer']:
            self.window.show_window()
            self.progress_bar.initialize('Initializing installation...')
            self.progress_bar.show()

        try:
            return self._unsafe_install()
        except Exception as inst:
            if self.install_config['iso_installer']:
                self.logger.exception(repr(inst))
                self.exit_gracefully()
            else:
                raise

    def _unsafe_install(self):
        """
        Install photon system
        """
        self._format_disk()
        self._setup_install_repo()
        self._initialize_system()
        self._install_packages()
        self._enable_network_in_chroot()
        self._finalize_system()
        self._cleanup_install_repo()
        self._execute_modules(modules.commons.POST_INSTALL)
        self._post_install()
        self._disable_network_in_chroot()
        self._cleanup_and_exit()
        return ActionResult(True, None)

    def exit_gracefully(self, signal1=None, frame1=None):
        """
        This will be called if the installer interrupted by Ctrl+C, exception
        or other failures
        """
        del signal1
        del frame1
        if not self.exiting:
            self.exiting = True
            if self.install_config['iso_installer']:
                self.progress_bar.hide()
                self.window.addstr(0, 0, 'Oops, Installer got interrupted.\n\n' +
                                   'Press any key to get to the bash...')
                self.window.content_window().getch()

            self._cleanup_install_repo()
            self._cleanup_and_exit()
        sys.exit(1)

    def _cleanup_and_exit(self):
        """
        Unmount the disk, eject cd and exit
        """
        command = [Installer.unmount_disk_command, '-w', self.photon_root]
        command.extend(self._generate_partitions_param(reverse=True))
        retval = self.cmd.run(command)
        if retval != 0:
            self.logger.error("Failed to unmount disks")
        if self.install_config['iso_installer']:
            self.progress_bar.hide()
            self.window.addstr(0, 0, 'Congratulations, Photon has been installed in {0} secs.\n\n'
                               'Press any key to continue to boot...'
                               .format(self.progress_bar.time_elapsed))
            if 'ui_install' in self.install_config:
                self.window.content_window().getch()
            self._eject_cdrom()

    def _create_installrpms_list(self):
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

    def _copy_files(self):
        """
        Copy the rpm files and instal scripts.
        """
        # Make the photon_root directory if not exits
        retval = self.cmd.run(['mkdir', '-p', self.photon_root])
        if retval != 0:
            self.logger.error("Fail to create the root directory")
            self.exit_gracefully()

        # Copy the installer files
        retval = self.cmd.run(['cp', '-r', os.path.dirname(__file__), self.photon_root])
        if retval != 0:
            self.logger.error("Fail to copy install scripts")
            self.exit_gracefully()

        self._create_installrpms_list()

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
        if(self.cmd.run(['mkdir', '-p',
                            os.path.join(self.photon_root, "installer")]) != 0 or
           self.cmd.run(['mount', '--bind', self.installer_path,
                            os.path.join(self.photon_root, "installer")]) != 0):
            self.logger.error("Fail to bind installer")
            self.exit_gracefully()

    def _unbind_installer(self):
        # unmount the installer directory
        retval = self.cmd.run(['umount', os.path.join(self.photon_root, "installer")])
        if retval != 0:
            self.logger.error("Fail to unbind the installer directory")
        # remove the installer directory
        retval = self.cmd.run(['rm', '-rf', os.path.join(self.photon_root, "installer")])
        if retval != 0:
            self.logger.error("Fail to remove the installer directory")

    def _bind_repo_dir(self):
        """
        Bind repo dir for tdnf installation
        """
        if self.rpm_path.startswith("https://") or self.rpm_path.startswith("http://"):
            return
        if (self.cmd.run(['mkdir', '-p', self.rpm_cache_dir]) != 0 or
                self.cmd.run(['mount', '--bind', self.rpm_path, self.rpm_cache_dir]) != 0):
            self.logger.error("Fail to bind cache rpms")
            self.exit_gracefully()

    def _unbind_repo_dir(self):
        """
        Unbind repo dir after installation
        """
        if self.rpm_path.startswith("https://") or self.rpm_path.startswith("http://"):
            return
        if (self.cmd.run(['umount', self.rpm_cache_dir]) != 0 or
                self.cmd.run(['rm', '-rf', self.rpm_cache_dir]) != 0):
            self.logger.error("Fail to unbind cache rpms")

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
        command = [Installer.mount_command, '-w', self.photon_root]
        command.extend(self._generate_partitions_param())
        retval = self.cmd.run(command)
        if retval != 0:
            self.logger.info("Failed to setup the disk for installation")
            self.exit_gracefully()

        if self.install_config['iso_installer']:
            self.progress_bar.update_message('Initializing system...')
            self._bind_installer()
            self._bind_repo_dir()
            retval = self.cmd.run([self.prepare_command, '-w',
                                        self.photon_root, 'install'])
            if retval != 0:
                self.logger.info("Failed to bind the installer and repo needed by tdnf")
                self.exit_gracefully()
        else:
            self._copy_files()
            #Setup the filesystem basics
            retval = self.cmd.run([self.prepare_command, '-w', self.photon_root, self.rpm_path])
            if retval != 0:
                self.logger.info("Failed to setup the file systems basics")
                self.exit_gracefully()

    def _finalize_system(self):
        """
        Finalize the system after the installation
        """
        #Setup the disk
        retval = self.cmd.run([Installer.chroot_command, '-w', self.photon_root,
                                    Installer.finalize_command, '-w', self.photon_root])
        if retval != 0:
            self.logger.error("Fail to setup the target system after the installation")

    def _cleanup_install_repo(self):
        if self.install_config['iso_installer']:
            self._unbind_installer()
            self._unbind_repo_dir()
            # Disable the swap file
            retval = self.cmd.run(['swapoff', self.photon_root+'/cache/swapfile'])
            if retval != 0:
                self.logger.error("Fail to swapoff")
            # remove the tdnf cache directory and the swapfile.
            retval = self.cmd.run(['rm', '-rf', os.path.join(self.photon_root, "cache")])
            if retval != 0:
                self.logger.error("Fail to remove the cache")

    def _post_install(self):
        # install grub
        if 'boot_partition_number' not in self.install_config['disk']:
            self.install_config['disk']['boot_partition_number'] = 1

        retval = self.cmd.run(
            [self.setup_grub_command, '-w', self.photon_root,
             self.install_config.get('boot', 'bios'),
             self.install_config['disk']['disk'],
             self.install_config['disk']['root'],
             self.install_config['disk']['boot'],
             self.install_config['disk']['bootdirectory'],
             str(self.install_config['disk']['boot_partition_number'])])

        if retval != 0:
            raise Exception("Bootloader (grub2) setup failed")

        self._update_fstab()
        if not self.install_config['iso_installer']:
            retval = self.cmd.run(['rm', '-rf', os.path.join(self.photon_root, "installer")])
            if retval != 0:
                self.logger.error("Fail to remove the installer directory")

    def _execute_modules(self, phase):
        """
        Execute the scripts in the modules folder
        """
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "modules")))
        modules_paths = glob.glob(os.path.abspath(os.path.join(os.path.dirname(__file__), 'modules')) + '/m_*.py')
        for mod_path in modules_paths:
            module = os.path.splitext(os.path.basename(mod_path))[0]
            try:
                __import__(module)
                mod = sys.modules[module]
            except ImportError:
                self.logger.error('Error importing module {}'.format(module))
                continue

            # the module default is disabled
            if not hasattr(mod, 'enabled') or mod.enabled is False:
                self.logger.info("module {} is not enabled".format(module))
                continue
            # check for the install phase
            if not hasattr(mod, 'install_phase'):
                self.logger.error("Error: can not defind module {} phase".format(module))
                continue
            if mod.install_phase != phase:
                self.logger.info("Skipping module {0} for phase {1}".format(module, phase))
                continue
            if not hasattr(mod, 'execute'):
                self.logger.error("Error: not able to execute module {}".format(module))
                continue
            self.logger.info("Executing: " + module)
            mod.execute(self)

    def _adjust_packages_for_vmware_virt(self):
        """
        Install linux_esx on Vmware virtual machine if requested
        """
        try:
            if self.install_config['install_linux_esx']:
                regex = re.compile(r'^linux-[0-9]|^initramfs-[0-9]')
                self.install_config['packages'] = [x for x in self.install_config['packages'] if not regex.search(x)]
                self.install_config['packages'].append('linux-esx')
        except KeyError:
            pass

    def _format_disk(self):
        """
        Partition and format the disk
        """
        # skip partitioning if installer was called from image
        if not self.install_config['iso_installer']:
            return

        self.progress_bar.update_message('Partitioning...')

        if 'partitions' in self.install_config:
            partitions = self.install_config['partitions']
        else:
            partitions = Installer.default_partitions

        # do partitioning
        partitions_data = self.partition_disk(self.install_config['disk'], partitions)

        if partitions_data == None:
            raise Exception("Partitioning failed.")
        self.install_config['disk'] = partitions_data


    def _setup_install_repo(self):
        """
        Setup the tdnf repo for installation
        """
        if self.install_config['iso_installer']:
            keepcache = False
            with open(self.tdnf_repo_path, "w") as repo_file:
                repo_file.write("[photon-local]\n")
                repo_file.write("name=VMWare Photon installer repo\n")
                if self.rpm_path.startswith("https://") or self.rpm_path.startswith("http://"):
                    repo_file.write("baseurl={}\n".format(self.rpm_path.replace('/', r'\/')))
                else:
                    repo_file.write("baseurl=file://{}\n".format(self.rpm_cache_dir))
                    keepcache = True
                repo_file.write("gpgcheck=0\nenabled=1\n")
            with open(self.tdnf_conf_path, "w") as conf_file:
                conf_file.writelines([
                    "[main]\n",
                    "gpgcheck=0\n",
                    "installonly_limit=3\n",
                    "clean_requirements_on_remove=true\n"])
                # baseurl and cachedir are bindmounted to rpm_path, we do not
                # want input RPMS to be removed after installation.
                if keepcache:
                    conf_file.write("keepcache=1\n")
                conf_file.write("repodir={}\n".format(self.working_directory))
                conf_file.write("cachedir={}\n".format(self.rpm_cache_dir_short))

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
        self.logger.debug("tdnf install --installroot {0} {1} -c {2}"
                           .format(self.photon_root, " ".join(selected_packages),
                                            self.tdnf_conf_path))
        process = subprocess.Popen(['tdnf', 'install'] + selected_packages +
                                   ['--installroot', self.photon_root,
                                    '--assumeyes', '-c', self.tdnf_conf_path],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
                self.logger.info("[tdnf] {0}".format(output))
                prefix = 'Installing/Updating: '
                if output.startswith(prefix):
                    package = output[len(prefix):].rstrip('\n')
                    self.progress_bar.increment(packages_to_install[package])

                self.progress_bar.update_message(output)
        # 0 : succeed; 137 : package already installed; 65 : package not found in repo.
        if retval != 0 and retval != 137:
            self.logger.error("Failed to install some packages")
            self.logger.error(process.communicate()[1].decode())
            self.exit_gracefully()
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

        if ('type' in self.install_config and
             (self.install_config['type'] in ['micro', 'minimal'])):
            rpm_params.append('--excludedocs')

        self.logger.info("installing packages {0}, with params {1}"
                            .format(rpm_paths, rpm_params))
        retval = self.cmd.run(['rpm', '-Uvh'] + rpm_params + rpm_paths)
        if retval != 0:
            self.exit_gracefully()


    def _eject_cdrom(self):
        """
        Eject the cdrom on request
        """
        eject_cdrom = True
        if 'eject_cdrom' in self.install_config and not self.install_config['eject_cdrom']:
            eject_cdrom = False
        if eject_cdrom:
            self.cmd.run(['eject', '-r'])

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

    def partition_compare(self, p):
        if 'mountpoint' in p:
            return (1, len(p['mountpoint']), p['mountpoint'])
        return (0, 0, "A")

    def partition_disk(self, disk, partitions):
        partitions_data = {}
        partitions_data['disk'] = disk
        partitions_data['partitions'] = partitions

        # Clear the disk
        retval = self.cmd.run(['sgdisk', '-o', '-g', disk])
        if retval != 0:
            self.logger.error("Failed clearing disk {0}".format(disk))
            return None
        # Partitioning the disk
        extensible_partition = None
        partitions_count = len(partitions)
        partition_number = 3
        # Add part size and grub flags

        bios_flag = ':ef02'
        part_size = '+2M'
        # Adding the bios partition
        partition_cmd = ['sgdisk', '-n 1::' + part_size]

        efi_flag = ':ef00'
        part_size = '+3M'
        # Adding the efi partition
        partition_cmd.extend(['-n 2::' + part_size])
        # Adding the known size partitions

        arch = subprocess.check_output(['uname', '-m'], universal_newlines=True)
        if "x86" not in arch:
            partition_number = 2
            # Adding the efi partition
            partition_cmd = ['sgdisk', '-n 1::' + part_size]

        for partition in partitions:
            if partition['size'] == 0:
                # Can not have more than 1 extensible partition
                if extensible_partition != None:
                    self.logger.error("Can not have more than 1 extensible partition")
                    return None
                extensible_partition = partition
            else:
                partition_cmd.extend(['-n', '{}::+{}M'.format(partition_number, partition['size'])])

            partition['partition_number'] = partition_number
            prefix = ''
            if 'nvme' in disk or 'mmcblk' in disk:
                prefix = 'p'
            partition['path'] = disk + prefix + repr(partition_number)
            partition_number = partition_number + 1

        # Adding the last extendible partition
        if extensible_partition:
            partition_cmd.extend(['-n', repr(extensible_partition['partition_number'])])

        partition_cmd.extend(['-p', disk])

        # Run the partitioning command
        retval = self.cmd.run(partition_cmd)
        if retval != 0:
            self.logger.error("Failed partition disk, command: {0}". format(partition_cmd))
            return None

        if "x86" not in arch:
            retval = self.cmd.run(['sgdisk', '-t1' + efi_flag, disk])
            if retval != 0:
                self.logger.error("Failed to setup efi partition")
                return None

        else:
            retval = self.cmd.run(['sgdisk', '-t1' + bios_flag, disk])
            if retval != 0:
                self.logger.error("Failed to setup bios partition")
                return None

            retval = self.cmd.run(['sgdisk', '-t2' + efi_flag, disk])
            if retval != 0:
                self.logger.error("Failed to setup efi partition")
                return None
        # Format the filesystem
        for partition in partitions:
            if "mountpoint" in partition:
                if partition['mountpoint'] == '/':
                    partitions_data['root'] = partition['path']
                    partitions_data['root_partition_number'] = partition['partition_number']
                elif partition['mountpoint'] == '/boot':
                    partitions_data['boot'] = partition['path']
                    partitions_data['boot_partition_number'] = partition['partition_number']
                    partitions_data['bootdirectory'] = '/'
            if partition['filesystem'] == "swap":
                retval = self.cmd.run(['mkswap', partition['path']])
                if retval != 0:
                    self.logger.error("Failed to create swap partition @ {}".format(partition['path']))
                    return None
            else:
                mkfs_cmd = ['mkfs', '-t', partition['filesystem'], partition['path']]
                retval = self.cmd.run(mkfs_cmd)
                if retval != 0:
                    self.logger.error(
                        "Failed to format {} partition @ {}".format(partition['filesystem'],
                                                                partition['path']))
                    return None

        # Check if there is no root partition
        if 'root' not in partitions_data:
            self.logger.error("There is no partition assigned to root '/'")
            return None

        if 'boot' not in partitions_data:
            partitions_data['boot'] = partitions_data['root']
            partitions_data['boot_partition_number'] = partitions_data['root_partition_number']
            partitions_data['bootdirectory'] = '/boot/'

        partitions.sort(key=lambda p: self.partition_compare(p))

        return partitions_data

