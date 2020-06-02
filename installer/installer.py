"""
Photon installer
"""
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

import subprocess
import os
import re
import shutil
import signal
import sys
import glob
import modules.commons
import random
import curses
import stat
import tempfile
from logger import Logger
from commandutils import CommandUtils
from jsonwrapper import JsonWrapper
from progressbar import ProgressBar
from window import Window
from actionresult import ActionResult
from networkmanager import NetworkManager
from enum import Enum

class PartitionType(Enum):
    SWAP = 1
    LINUX = 2
    LVM = 3
    ESP = 4
    BIOS = 5

class Installer(object):
    """
    Photon installer
    """

    # List of allowed keys in kickstart config file.
    # Please keep ks_config.txt file updated.
    known_keys = {
        'additional_files',
        'additional_packages',
        'additional_rpms_path',
        'arch',
        'autopartition',
        'bootmode',
        'disk',
        'eject_cdrom',
        'hostname',
        'install_linux_esx',
        'live',
        'log_level',
        'ostree',
        'packages',
        'packagelist_file',
        'partition_type',
        'partitions',
        'network',
        'password',
        'postinstall',
        'postinstallscripts',
        'public_key',
        'search_path',
        'setup_grub_script',
        'shadow_password',
        'type',
        'ui'
    }

    default_partitions = [{"mountpoint": "/", "size": 0, "filesystem": "ext4"}]

    def __init__(self, working_directory="/mnt/photon-root",
                 rpm_path=os.path.dirname(__file__)+"/../stage/RPMS", log_path=os.path.dirname(__file__)+"/../stage/LOGS"):
        self.exiting = False
        self.interactive = False
        self.install_config = None
        self.rpm_path = rpm_path
        self.log_path = log_path
        self.logger = None
        self.cmd = None
        self.working_directory = working_directory

        if os.path.exists(self.working_directory) and os.path.isdir(self.working_directory) and working_directory == '/mnt/photon-root':
            shutil.rmtree(self.working_directory)
        if not os.path.exists(self.working_directory):
            os.mkdir(self.working_directory)

        self.photon_root = self.working_directory + "/photon-chroot"
        self.installer_path = os.path.dirname(os.path.abspath(__file__))
        self.tdnf_conf_path = self.working_directory + "/tdnf.conf"
        self.tdnf_repo_path = self.working_directory + "/photon-local.repo"
        self.rpm_cache_dir = self.photon_root + '/cache/tdnf/photon-local/rpms'
        # used by tdnf.conf as cachedir=, tdnf will append the rest
        self.rpm_cache_dir_short = self.photon_root + '/cache/tdnf'

        self.setup_grub_command = os.path.dirname(__file__)+"/mk-setup-grub.sh"

        signal.signal(signal.SIGINT, self.exit_gracefully)
        self.lvs_to_detach = {'vgs': [], 'pvs': []}

    """
    create, append and validate configuration date - install_config
    """
    def configure(self, install_config, ui_config = None):
        # Initialize logger and cmd first
        if not install_config:
            # UI installation
            log_level = 'debug'
            console = False
        else:
            log_level = install_config.get('log_level', 'info')
            console = not install_config.get('ui', False)
        self.logger = Logger.get_logger(self.log_path, log_level, console)
        self.cmd = CommandUtils(self.logger)

        # run UI configurator iff install_config param is None
        if not install_config and ui_config:
            from iso_config import IsoConfig
            self.interactive = True
            config = IsoConfig()
            install_config = curses.wrapper(config.configure, ui_config)

        self._add_defaults(install_config)

        issue = self._check_install_config(install_config)
        if issue:
            self.logger.error(issue)
            raise Exception(issue)

        self.install_config = install_config


    def execute(self):
        if 'setup_grub_script' in self.install_config:
            self.setup_grub_command = self.install_config['setup_grub_script']

        if self.install_config['ui']:
            curses.wrapper(self._install)
        else:
            self._install()

    def _add_defaults(self, install_config):
        """
        Add default install_config settings if not specified
        """
        # set arch to host's one if not defined
        arch = subprocess.check_output(['uname', '-m'], universal_newlines=True).rstrip('\n')
        if 'arch' not in install_config:
            install_config['arch'] = arch

        # 'bootmode' mode
        if 'bootmode' not in install_config:
            if "x86_64" in arch:
                install_config['bootmode'] = 'dualboot'
            else:
                install_config['bootmode'] = 'efi'

        # extend 'packages' by 'packagelist_file' and 'additional_packages'
        packages = []
        if 'packagelist_file' in install_config:
            plf = install_config['packagelist_file']
            if not plf.startswith('/'):
                plf = os.path.join(os.path.dirname(__file__), plf)
            json_wrapper_package_list = JsonWrapper(plf)
            package_list_json = json_wrapper_package_list.read()
            packages.extend(package_list_json["packages"])

        if 'additional_packages' in install_config:
            packages.extend(install_config['additional_packages'])

        # add bootloader packages after bootmode set
        if install_config['bootmode'] in ['dualboot', 'efi']:
            packages.append('grub2-efi-image')

        if 'packages' in install_config:
            install_config['packages'] = list(set(packages + install_config['packages']))
        else:
            install_config['packages'] = packages

        # live means online system. When you create an image for
        # target system, live should be set to false.
        if 'live' not in install_config:
            install_config['live'] = 'loop' not in install_config['disk']

        # default partition
        if 'partitions' not in install_config:
            install_config['partitions'] = Installer.default_partitions

        # define 'hostname' as 'photon-<RANDOM STRING>'
        if "hostname" not in install_config or install_config['hostname'] == "":
            install_config['hostname'] = 'photon-%12x' % random.randrange(16**12)

        # Set password if needed.
        # Installer uses 'shadow_password' and optionally 'password'/'age'
        # to set aging if present. See modules/m_updaterootpassword.py
        if 'shadow_password' not in install_config:
            if 'password' not in install_config:
                install_config['password'] = {'crypted': True, 'text': '*', 'age': -1}

            if install_config['password']['crypted']:
                install_config['shadow_password'] = install_config['password']['text']
            else:
                install_config['shadow_password'] = CommandUtils.generate_password_hash(install_config['password']['text'])

        # Do not show UI progress by default
        if 'ui' not in install_config:
            install_config['ui'] = False

        # Log level
        if 'log_level' not in install_config:
            install_config['log_level'] = 'info'

        # Extend search_path by current dir and script dir
        if 'search_path' not in install_config:
            install_config['search_path'] = []
        for dirname in [os.getcwd(), os.path.abspath(os.path.dirname(__file__))]:
            if dirname not in install_config['search_path']:
                install_config['search_path'].append(dirname)

    def _check_install_config(self, install_config):
        """
        Sanity check of install_config before its execution.
        Return error string or None
        """

        unknown_keys = install_config.keys() - Installer.known_keys
        if len(unknown_keys) > 0:
            return "Unknown install_config keys: " + ", ".join(unknown_keys)

        if not 'disk' in install_config:
            return "No disk configured"

        if 'install_linux_esx' not in install_config:
            install_config['install_linux_esx'] = False

        # Perform following checks here:
        # 1) Only one extensible partition is allowed per disk
        # 2) /boot can not be LVM
        # 3) / must present
        # 4) Duplicate mountpoints should not be present
        has_extensible = {}
        has_root = False
        mountpoints = []
        default_disk = install_config['disk']
        for partition in install_config['partitions']:
            disk = partition.get('disk', default_disk)
            mntpoint = partition.get('mountpoint', '')
            if disk not in has_extensible:
                has_extensible[disk] = False
            size = partition['size']
            if size == 0:
                if has_extensible[disk]:
                    return "Disk {} has more than one extensible partition".format(disk)
                else:
                    has_extensible[disk] = True
            if mntpoint != '':
                mountpoints.append(mntpoint)
            if mntpoint == '/boot' and 'lvm' in partition:
                return "/boot on LVM is not supported"
            elif mntpoint == '/':
                has_root = True
        if not has_root:
            return "There is no partition assigned to root '/'"

        if len(mountpoints) != len(set(mountpoints)):
            return "Duplicate mountpoints exist in partition table!!"

        if install_config['arch'] not in ["aarch64", 'x86_64']:
            return "Unsupported target architecture {}".format(install_config['arch'])

        # No BIOS for aarch64
        if install_config['arch'] == 'aarch64' and install_config['bootmode'] in ['dualboot', 'bios']:
            return "Aarch64 targets do not support BIOS boot. Set 'bootmode' to 'efi'."

        if 'age' in install_config.get('password', {}):
            if install_config['password']['age'] < -1:
                return "Password age should be -1, 0 or positive"

        return None

    def _install(self, stdscreen=None):
        """
        Install photon system and handle exception
        """
        if self.install_config['ui']:
            # init the screen
            curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
            curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
            curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)
            curses.init_pair(4, curses.COLOR_RED, curses.COLOR_WHITE)
            stdscreen.bkgd(' ', curses.color_pair(1))
            maxy, maxx = stdscreen.getmaxyx()
            curses.curs_set(0)

            # initializing windows
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
            self.window.show_window()
            self.progress_bar.initialize('Initializing installation...')
            self.progress_bar.show()

        try:
            self._unsafe_install()
        except Exception as inst:
            self.logger.exception(repr(inst))
            self.exit_gracefully()

        # Congratulation screen
        if self.install_config['ui']:
            self.progress_bar.hide()
            self.window.addstr(0, 0, 'Congratulations, Photon has been installed in {0} secs.\n\n'
                               'Press any key to continue to boot...'
                               .format(self.progress_bar.time_elapsed))
            if self.interactive:
                self.window.content_window().getch()

        if self.install_config['live']:
            self._eject_cdrom()

    def _unsafe_install(self):
        """
        Install photon system
        """
        self._partition_disk()
        self._format_partitions()
        self._mount_partitions()
        if 'ostree' in self.install_config:
            from ostreeinstaller import OstreeInstaller
            ostree = OstreeInstaller(self)
            ostree.install()
        else:
            self._setup_install_repo()
            self._initialize_system()
            self._mount_special_folders()
            self._install_packages()
            self._install_additional_rpms()
            self._enable_network_in_chroot()
            self._setup_network()
            self._finalize_system()
            self._cleanup_install_repo()
            self._setup_grub()
            self._create_fstab()
        self._execute_modules(modules.commons.POST_INSTALL)
        self._disable_network_in_chroot()
        self._unmount_all()

    def exit_gracefully(self, signal1=None, frame1=None):
        """
        This will be called if the installer interrupted by Ctrl+C, exception
        or other failures
        """
        del signal1
        del frame1
        if not self.exiting and self.install_config:
            self.exiting = True
            if self.install_config['ui']:
                self.progress_bar.hide()
                self.window.addstr(0, 0, 'Oops, Installer got interrupted.\n\n' +
                                   'Press any key to get to the bash...')
                self.window.content_window().getch()

            self._cleanup_install_repo()
            self._unmount_all()
        sys.exit(1)

    def _setup_network(self):
        if 'network' not in self.install_config:
            return
        # setup network config files in chroot
        nm = NetworkManager(self.install_config, self.photon_root)
        if not nm.setup_network():
            self.logger.error("Failed to setup network!")
            self.exit_gracefully()

        # Configure network when in live mode (ISO) and when network is not
        # already configured (typically in KS flow).
        if ('live' in self.install_config and
                'conf_files' not in self.install_config['network']):
            nm = NetworkManager(self.install_config)
            if not nm.setup_network():
                self.logger.error("Failed to setup network in ISO system")
                self.exit_gracefully()
            nm.restart_networkd()

    def _unmount_all(self):
        """
        Unmount partitions and special folders
        """
        for d in ["/tmp", "/run", "/sys", "/dev/pts", "/dev", "/proc"]:
            if os.path.exists(self.photon_root + d):
                retval = self.cmd.run(['umount', '-l', self.photon_root + d])
                if retval != 0:
                    self.logger.error("Failed to unmount {}".format(d))

        for partition in self.install_config['partitions'][::-1]:
            if self._get_partition_type(partition) in [PartitionType.BIOS, PartitionType.SWAP]:
                continue
            mountpoint = self.photon_root + partition["mountpoint"]
            if os.path.exists(mountpoint):
                retval = self.cmd.run(['umount', '-l', mountpoint])
                if retval != 0:
                    self.logger.error("Failed to unmount partition {}".format(mountpoint))

        # need to call it twice, because of internal bind mounts
        if 'ostree' in self.install_config:
            if os.path.exists(self.photon_root):
                retval = self.cmd.run(['umount', '-R', self.photon_root])
                retval = self.cmd.run(['umount', '-R', self.photon_root])
                if retval != 0:
                    self.logger.error("Failed to unmount disks in photon root")

        self.cmd.run(['sync'])
        if os.path.exists(self.photon_root):
            shutil.rmtree(self.photon_root)

        # Deactivate LVM VGs
        for vg in self.lvs_to_detach['vgs']:
            retval = self.cmd.run(["vgchange", "-v", "-an", vg])
            if retval != 0:
                self.logger.error("Failed to deactivate LVM volume group: {}".format(vg))

        # Get the disks from partition table
        disks = set(partition.get('disk', self.install_config['disk']) for partition in self.install_config['partitions'])
        for disk in disks:
            if 'loop' in disk:
                # Simulate partition hot remove to notify LVM
                for pv in self.lvs_to_detach['pvs']:
                    retval = self.cmd.run(["dmsetup", "remove", pv])
                    if retval != 0:
                        self.logger.error("Failed to detach LVM physical volume: {}".format(pv))
                # Uninitialize device paritions mapping
                retval = self.cmd.run(['kpartx', '-d', disk])
                if retval != 0:
                    self.logger.error("Failed to unmap partitions of the disk image {}". format(disk))
                    return None

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
        if os.path.exists(os.path.join(self.photon_root, "installer")):
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
        if os.path.exists(self.rpm_cache_dir):
            if (self.cmd.run(['umount', self.rpm_cache_dir]) != 0 or
                    self.cmd.run(['rm', '-rf', self.rpm_cache_dir]) != 0):
                self.logger.error("Fail to unbind cache rpms")

    def _get_partuuid(self, path):
        partuuid = subprocess.check_output(['blkid', '-s', 'PARTUUID', '-o', 'value', path],
                                       universal_newlines=True).rstrip('\n')
        # Backup way to get uuid/partuuid. Leave it here for later use.
        #if partuuidval == '':
        #    sgdiskout = Utils.runshellcommand(
        #        "sgdisk -i 2 {} ".format(disk_device))
        #    partuuidval = (re.findall(r'Partition unique GUID.*',
        #                          sgdiskout))[0].split(':')[1].strip(' ').lower()
        return partuuid

    def _get_uuid(self, path):
        return subprocess.check_output(['blkid', '-s', 'UUID', '-o', 'value', path],
                                       universal_newlines=True).rstrip('\n')

    def _create_fstab(self, fstab_path = None):
        """
        update fstab
        """
        if not fstab_path:
            fstab_path = os.path.join(self.photon_root, "etc/fstab")
        with open(fstab_path, "w") as fstab_file:
            fstab_file.write("#system\tmnt-pt\ttype\toptions\tdump\tfsck\n")

            for partition in self.install_config['partitions']:
                ptype = self._get_partition_type(partition)
                if ptype == PartitionType.BIOS:
                    continue

                options = 'defaults'
                dump = 1
                fsck = 2

                if partition.get('mountpoint', '') == '/':
                    options = options + ',barrier,noatime,noacl,data=ordered'
                    fsck = 1

                if ptype == PartitionType.SWAP:
                    mountpoint = 'swap'
                    dump = 0
                    fsck = 0
                else:
                    mountpoint = partition['mountpoint']

                # Use PARTUUID/UUID instead of bare path.
                # Prefer PARTUUID over UUID as it is supported by kernel
                # and UUID only by initrd.
                path = partition['path']
                mnt_src = None
                partuuid = self._get_partuuid(path)
                if partuuid != '':
                    mnt_src = "PARTUUID={}".format(partuuid)
                else:
                    uuid = self._get_uuid(path)
                    if uuid != '':
                        mnt_src = "UUID={}".format(uuid)
                if not mnt_src:
                    raise RuntimeError("Cannot get PARTUUID/UUID of: {}".format(path))

                fstab_file.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(
                    mnt_src,
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
        for partition in self.install_config['partitions'][::step]:
            if self._get_partition_type(partition) in [PartitionType.BIOS, PartitionType.SWAP]:
                continue

            params.extend(['--partitionmountpoint', partition["path"], partition["mountpoint"]])
        return params

    def _mount_partitions(self):
        for partition in self.install_config['partitions'][::1]:
            if self._get_partition_type(partition) in [PartitionType.BIOS, PartitionType.SWAP]:
                continue
            mountpoint = self.photon_root + partition["mountpoint"]
            self.cmd.run(['mkdir', '-p', mountpoint])
            retval = self.cmd.run(['mount', '-v', partition["path"], mountpoint])
            if retval != 0:
                self.logger.error("Failed to mount partition {}".format(partition["path"]))
                self.exit_gracefully()

    def _initialize_system(self):
        """
        Prepare the system to install photon
        """
        if self.install_config['ui']:
            self.progress_bar.update_message('Initializing system...')
        self._bind_installer()
        self._bind_repo_dir()

        # Initialize rpm DB
        self.cmd.run(['mkdir', '-p', os.path.join(self.photon_root, "var/lib/rpm")])
        retval = self.cmd.run(['rpm', '--root', self.photon_root, '--initdb',
                               '--dbpath', '/var/lib/rpm'])
        if retval != 0:
            self.logger.error("Failed to initialize rpm DB")
            self.exit_gracefully()

        # Install filesystem rpm
        tdnf_cmd = "tdnf install filesystem --installroot {0} --assumeyes -c {1}".format(self.photon_root,
                        self.tdnf_conf_path)
        retval = self.cmd.run(tdnf_cmd)
        if retval != 0:
            retval = self.cmd.run(['docker', 'run',
                                   '-v', self.rpm_cache_dir+':'+self.rpm_cache_dir,
                                   '-v', self.working_directory+':'+self.working_directory,
                                   'photon:3.0', '/bin/sh', '-c', tdnf_cmd])
            if retval != 0:
                self.logger.error("Failed to install filesystem rpm")
                self.exit_gracefully()

        # Create special devices. We need it when devtpmfs is not mounted yet.
        devices = {
            'console': (600, stat.S_IFCHR, 5, 1),
            'null': (666, stat.S_IFCHR, 1, 3),
            'random': (444, stat.S_IFCHR, 1, 8),
            'urandom': (444, stat.S_IFCHR, 1, 9)
        }
        for device, (mode, dev_type, major, minor) in devices.items():
            os.mknod(os.path.join(self.photon_root, "dev", device),
                    mode | dev_type, os.makedev(major, minor))


    def _mount_special_folders(self):
        for d in ["/proc", "/dev", "/dev/pts", "/sys"]:
            retval = self.cmd.run(['mount', '-o', 'bind', d, self.photon_root + d])
            if retval != 0:
                self.logger.error("Failed to bind mount {}".format(d))
                self.exit_gracefully()

        for d in ["/tmp", "/run"]:
            retval = self.cmd.run(['mount', '-t', 'tmpfs', 'tmpfs', self.photon_root + d])
            if retval != 0:
                self.logger.error("Failed to bind mount {}".format(d))
                self.exit_gracefully()

    def _copy_additional_files(self):
        if 'additional_files' in self.install_config:
            for filetuples in self.install_config['additional_files']:
                for src, dest in filetuples.items():
                    if src.startswith('http://') or src.startswith('https://'):
                        temp_file = tempfile.mktemp()
                        result, msg = CommandUtils.wget(src, temp_file, False)
                        if result:
                            shutil.copyfile(temp_file, self.photon_root + dest)
                        else:
                            self.logger.error("Download failed URL: {} got error: {}".format(src, msg))
                    else:
                        srcpath = self.getfile(src)
                        if (os.path.isdir(srcpath)):
                            shutil.copytree(srcpath, self.photon_root + dest, True)
                        else:
                            shutil.copyfile(srcpath, self.photon_root + dest)

    def _finalize_system(self):
        """
        Finalize the system after the installation
        """
        if self.install_config['ui']:
            self.progress_bar.show_loading('Finalizing installation')

        self._copy_additional_files()

        self.cmd.run_in_chroot(self.photon_root, "/sbin/ldconfig")

        # Importing the pubkey
        self.cmd.run_in_chroot(self.photon_root, "rpm --import /etc/pki/rpm-gpg/*")

    def _cleanup_install_repo(self):
        self._unbind_installer()
        self._unbind_repo_dir()
        # remove the tdnf cache directory.
        retval = self.cmd.run(['rm', '-rf', os.path.join(self.photon_root, "cache")])
        if retval != 0:
            self.logger.error("Fail to remove the cache")
        if os.path.exists(self.tdnf_conf_path):
            os.remove(self.tdnf_conf_path)
        if os.path.exists(self.tdnf_repo_path):
            os.remove(self.tdnf_repo_path)

    def _setup_grub(self):
        bootmode = self.install_config['bootmode']

        # Setup bios grub
        if bootmode == 'dualboot' or bootmode == 'bios':
            retval = self.cmd.run('grub2-install --target=i386-pc --force --boot-directory={} {}'.format(self.photon_root + "/boot", self.install_config['disk']))
            if retval != 0:
                retval = self.cmd.run(['grub-install', '--target=i386-pc', '--force',
                                   '--boot-directory={}'.format(self.photon_root + "/boot"),
                                   self.install_config['disk']])
                if retval != 0:
                    raise Exception("Unable to setup grub")

        # Setup efi grub
        if bootmode == 'dualboot' or bootmode == 'efi':
            esp_pn = '1'
            if bootmode == 'dualboot':
                esp_pn = '2'

            self.cmd.run(['mkdir', '-p', self.photon_root + '/boot/efi/boot/grub2'])
            with open(os.path.join(self.photon_root, 'boot/efi/boot/grub2/grub.cfg'), "w") as grub_cfg:
                grub_cfg.write("search -n -u {} -s\n".format(self._get_uuid(self.install_config['partitions_data']['boot'])))
                grub_cfg.write("set prefix=($root){}grub2\n".format(self.install_config['partitions_data']['bootdirectory']))
                grub_cfg.write("configfile {}grub2/grub.cfg\n".format(self.install_config['partitions_data']['bootdirectory']))

            if self.install_config['live']:
                arch = self.install_config['arch']
                # 'x86_64' -> 'bootx64.efi', 'aarch64' -> 'bootaa64.efi'
                exe_name = 'boot'+arch[:-5]+arch[-2:]+'.efi'
                # Some platforms do not support adding boot entry. Thus, ignore failures
                self.cmd.run(['efibootmgr', '--create', '--remove-dups', '--disk', self.install_config['disk'],
                              '--part', esp_pn, '--loader', '/EFI/BOOT/' + exe_name, '--label', 'Photon'])

        # Create custom grub.cfg
        retval = self.cmd.run(
            [self.setup_grub_command, self.photon_root,
             self.install_config['partitions_data']['root'],
             self.install_config['partitions_data']['boot'],
             self.install_config['partitions_data']['bootdirectory']])

        if retval != 0:
            raise Exception("Bootloader (grub2) setup failed")

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
        if self.install_config['install_linux_esx']:
            if 'linux' in self.install_config['packages']:
                self.install_config['packages'].remove('linux')
            else:
                regex = re.compile(r'(?!linux-[0-9].*)')
                self.install_config['packages'] = list(filter(regex.match,self.install_config['packages']))
            self.install_config['packages'].append('linux-esx')
        else:
            regex = re.compile(r'(?!linux-esx-[0-9].*)')
            self.install_config['packages'] = list(filter(regex.match,self.install_config['packages']))


    def _add_packages_to_install(self, package):
        """
        Install packages on Vmware virtual machine if requested
        """
        self.install_config['packages'].append(package)

    def _setup_install_repo(self):
        """
        Setup the tdnf repo for installation
        """
        keepcache = False
        with open(self.tdnf_repo_path, "w") as repo_file:
            repo_file.write("[photon-local]\n")
            repo_file.write("name=VMWare Photon installer repo\n")
            if self.rpm_path.startswith("https://") or self.rpm_path.startswith("http://"):
                repo_file.write("baseurl={}\n".format(self.rpm_path))
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

    def _install_additional_rpms(self):
        rpms_path = self.install_config.get('additional_rpms_path', None)

        if not rpms_path or not os.path.exists(rpms_path):
            return

        if self.cmd.run([ 'rpm', '--root', self.photon_root, '-U', rpms_path + '/*.rpm' ]) != 0:
            self.logger.info('Failed to install additional_rpms from ' + rpms_path)
            self.exit_gracefully()

    def _install_packages(self):
        """
        Install packages using tdnf command
        """
        self._adjust_packages_for_vmware_virt()
        selected_packages = self.install_config['packages']
        state = 0
        packages_to_install = {}
        total_size = 0
        stderr = None
        tdnf_cmd = "tdnf install --installroot {0} --assumeyes -c {1} {2}".format(self.photon_root,
                        self.tdnf_conf_path, " ".join(selected_packages))
        self.logger.debug(tdnf_cmd)

        # run in shell to do not throw exception if tdnf not found
        process = subprocess.Popen(tdnf_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if self.install_config['ui']:
            while True:
                output = process.stdout.readline().decode()
                if output == '':
                    retval = process.poll()
                    if retval is not None:
                        stderr = process.communicate()[1]
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
        else:
            stdout,stderr = process.communicate()
            self.logger.info(stdout.decode())
            retval = process.returncode
            # image creation. host's tdnf might not be available or can be outdated (Photon 1.0)
            # retry with docker container
            if retval != 0 and retval != 137:
                self.logger.error(stderr.decode())
                stderr = None
                self.logger.info("Retry 'tdnf install' using docker image")
                retval = self.cmd.run(['docker', 'run',
                                   '-v', self.rpm_cache_dir+':'+self.rpm_cache_dir,
                                   '-v', self.working_directory+':'+self.working_directory,
                                   'photon:3.0', '/bin/sh', '-c', tdnf_cmd])

        # 0 : succeed; 137 : package already installed; 65 : package not found in repo.
        if retval != 0 and retval != 137:
            self.logger.error("Failed to install some packages")
            if stderr:
                self.logger.error(stderr.decode())
            self.exit_gracefully()

    def _eject_cdrom(self):
        """
        Eject the cdrom on request
        """
        if self.install_config.get('eject_cdrom', True):
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

    def _get_partition_path(self, disk, part_idx):
        prefix = ''
        if 'nvme' in disk or 'mmcblk' in disk or 'loop' in disk:
            prefix = 'p'

        # loop partitions device names are /dev/mapper/loopXpY instead of /dev/loopXpY
        if 'loop' in disk:
            path = '/dev/mapper' + disk[4:] + prefix + repr(part_idx)
        else:
            path = disk + prefix + repr(part_idx)

        return path

    def _get_partition_type(self, partition):
        if partition['filesystem'] == 'bios':
            return PartitionType.BIOS
        if partition['filesystem'] == 'swap':
            return PartitionType.SWAP
        if partition.get('mountpoint', '') == '/boot/efi' and partition['filesystem'] == 'vfat':
            return PartitionType.ESP
        if partition.get('lvm', None):
            return PartitionType.LVM
        return PartitionType.LINUX

    def _partition_type_to_string(self, ptype):
        if ptype == PartitionType.BIOS:
            return 'ef02'
        if ptype == PartitionType.SWAP:
            return '8200'
        if ptype == PartitionType.ESP:
            return 'ef00'
        if ptype == PartitionType.LVM:
            return '8e00'
        if ptype == PartitionType.LINUX:
            return '8300'
        raise Exception("Unknown partition type: {}".format(ptype))

    def _create_logical_volumes(self, physical_partition, vg_name, lv_partitions, extensible):
        """
        Create logical volumes
        """
        #Remove LVM logical volumes and volume groups if already exists
        #Existing lvs & vg should be removed to continue re-installation
        #else pvcreate command fails to create physical volumes even if executes forcefully
        retval = self.cmd.run(['bash', '-c', 'pvs | grep {}'. format(vg_name)])
        if retval == 0:
            #Remove LV's associated to VG and VG
            retval = self.cmd.run(["vgremove", "-f", vg_name])
            if retval != 0:
                self.logger.error("Error: Failed to remove existing vg before installation {}". format(vg_name))
        # if vg is not extensible (all lvs inside are known size) then make last lv
        # extensible, i.e. shrink it. Srinking last partition is important. We will
        # not be able to provide specified size because given physical partition is
        # also used by LVM header.
        extensible_logical_volume = None
        if not extensible:
            extensible_logical_volume = lv_partitions[-1]
            extensible_logical_volume['size'] = 0

        # create physical volume
        command = ['pvcreate', '-ff', '-y', physical_partition]
        retval = self.cmd.run(command)
        if retval != 0:
            raise Exception("Error: Failed to create physical volume, command : {}".format(command))

        # create volume group
        command = ['vgcreate', vg_name, physical_partition]
        retval = self.cmd.run(command)
        if retval != 0:
            raise Exception("Error: Failed to create volume group, command = {}".format(command))

        # create logical volumes
        for partition in lv_partitions:
            lv_cmd = ['lvcreate', '-y']
            lv_name = partition['lvm']['lv_name']
            size = partition['size']
            if partition['size'] == 0:
                # Each volume group can have only one extensible logical volume
                if not extensible_logical_volume:
                    extensible_logical_volume = partition
            else:
                lv_cmd.extend(['-L', '{}M'.format(partition['size']), '-n', lv_name, vg_name ])
                retval = self.cmd.run(lv_cmd)
                if retval != 0:
                    raise Exception("Error: Failed to create logical volumes , command: {}".format(lv_cmd))
            partition['path'] = '/dev/' + vg_name + '/' + lv_name

        # create extensible logical volume
        if not extensible_logical_volume:
            raise Exception("Can not fully partition VG: " + vg_name)

        lv_name = extensible_logical_volume['lvm']['lv_name']
        lv_cmd = ['lvcreate', '-y']
        lv_cmd.extend(['-l', '100%FREE', '-n', lv_name, vg_name ])

        retval = self.cmd.run(lv_cmd)
        if retval != 0:
            raise Exception("Error: Failed to create extensible logical volume, command = {}". format(lv_cmd))

        # remember pv/vg for detaching it later.
        self.lvs_to_detach['pvs'].append(os.path.basename(physical_partition))
        self.lvs_to_detach['vgs'].append(vg_name)

    def _get_partition_tree_view(self):
        # Tree View of partitions list, to be returned.
        # 1st level: dict of disks
        # 2nd level: list of physical partitions, with all information necessary to partition the disk
        # 3rd level: list of logical partitions (LVM) or detailed partition information needed to format partition
        ptv = {}

        # Dict of VG's per disk. Purpose of this dict is:
        # 1) to collect its LV's
        # 2) to accumulate total size
        # 3) to create physical partition representation for VG
        vg_partitions = {}

        default_disk = self.install_config['disk']
        partitions = self.install_config['partitions']
        for partition in partitions:
            disk = partition.get('disk', default_disk)
            if disk not in ptv:
                ptv[disk] = []
            if disk not in vg_partitions:
                vg_partitions[disk] = {}

            if partition.get('lvm', None):
                vg_name = partition['lvm']['vg_name']
                if vg_name not in vg_partitions[disk]:
                    vg_partitions[disk][vg_name] = {
                        'size': 0,
                        'type': self._partition_type_to_string(PartitionType.LVM),
                        'extensible': False,
                        'lvs': [],
                        'vg_name': vg_name
                    }
                vg_partitions[disk][vg_name]['lvs'].append(partition)
                if partition['size'] == 0:
                    vg_partitions[disk][vg_name]['extensible'] = True
                    vg_partitions[disk][vg_name]['size'] = 0
                else:
                    if not vg_partitions[disk][vg_name]['extensible']:
                        vg_partitions[disk][vg_name]['size'] = vg_partitions[disk][vg_name]['size'] + partition['size']
            else:
                if 'type' in partition:
                    ptype_code = partition['type']
                else:
                    ptype_code = self._partition_type_to_string(self._get_partition_type(partition))

                l2entry = {
                    'size': partition['size'],
                    'type': ptype_code,
                    'partition': partition
                }
                ptv[disk].append(l2entry)

        # Add accumulated VG partitions
        for disk, vg_list in vg_partitions.items():
                ptv[disk].extend(vg_list.values())
        return ptv

    def _insert_boot_partitions(self):
        bios_found = False
        esp_found = False
        for partition in self.install_config['partitions']:
            ptype = self._get_partition_type(partition)
            if ptype == PartitionType.BIOS:
                bios_found = True
            if ptype == PartitionType.ESP:
                esp_found = True

       # Adding boot partition required for ostree if already not present in partitions table
        if 'ostree' in self.install_config:
            mount_points = [partition['mountpoint'] for partition in self.install_config['partitions'] if 'mountpoint' in partition]
            if '/boot' not in mount_points:
                boot_partition = {'size': 300, 'filesystem': 'ext4', 'mountpoint': '/boot'}
                self.install_config['partitions'].insert(0, boot_partition)

        bootmode = self.install_config.get('bootmode', 'bios')

        # Insert efi special partition
        if not esp_found and (bootmode == 'dualboot' or bootmode == 'efi'):
            efi_partition = { 'size': 10, 'filesystem': 'vfat', 'mountpoint': '/boot/efi' }
            self.install_config['partitions'].insert(0, efi_partition)

        # Insert bios partition last to be very first
        if not bios_found and (bootmode == 'dualboot' or bootmode == 'bios'):
            bios_partition = { 'size': 4, 'filesystem': 'bios' }
            self.install_config['partitions'].insert(0, bios_partition)

    def _partition_disk(self):
        """
        Partition the disk
        """

        if self.install_config['ui']:
            self.progress_bar.update_message('Partitioning...')

        self._insert_boot_partitions()
        ptv = self._get_partition_tree_view()

        partitions = self.install_config['partitions']
        partitions_data = {}
        lvm_present = False

        # Partitioning disks
        for disk, l2entries in ptv.items():

            # Clear the disk first
            retval = self.cmd.run(['sgdisk', '-o', '-g', disk])
            if retval != 0:
                raise Exception("Failed clearing disk {0}".format(disk))

            # Build partition command and insert 'part' into 'partitions'
            partition_cmd = ['sgdisk']
            part_idx = 1
            # command option for extensible partition
            last_partition = None
            for l2 in l2entries:
                if 'lvs' in l2:
                    # will be used for _create_logical_volumes() invocation
                    l2['path'] = self._get_partition_path(disk, part_idx)
                else:
                    l2['partition']['path'] = self._get_partition_path(disk, part_idx)

                if l2['size'] == 0:
                    last_partition = []
                    last_partition.extend(['-n{}'.format(part_idx)])
                    last_partition.extend(['-t{}:{}'.format(part_idx, l2['type'])])
                else:
                    partition_cmd.extend(['-n{}::+{}M'.format(part_idx, l2['size'])])
                    partition_cmd.extend(['-t{}:{}'.format(part_idx, l2['type'])])
                part_idx = part_idx + 1
            # if extensible partition present, add it to the end of the disk
            if last_partition:
                partition_cmd.extend(last_partition)
            partition_cmd.extend(['-p', disk])

            # Run the partitioning command (all physical partitions in one shot)
            retval = self.cmd.run(partition_cmd)
            if retval != 0:
                raise Exception("Failed partition disk, command: {0}".format(partition_cmd))

            # For RPi image we used 'parted' instead of 'sgdisk':
            # parted -s $IMAGE_NAME mklabel msdos mkpart primary fat32 1M 30M mkpart primary ext4 30M 100%
            # Try to use 'sgdisk -m' to convert GPT to MBR and see whether it works.
            if self.install_config.get('partition_type', 'gpt') == 'msdos':
                # m - colon separated partitions list
                m = ":".join([str(i) for i in range(1,part_idx)])
                retval = self.cmd.run(['sgdisk', '-m', m, disk])
                if retval != 0:
                    raise Exception("Failed to setup efi partition")

            # Make loop disk partitions available
            if 'loop' in disk:
                retval = self.cmd.run(['kpartx', '-avs', disk])
                if retval != 0:
                    raise Exception("Failed to rescan partitions of the disk image {}". format(disk))

            # Go through l2 entries again and create logical partitions
            for l2 in l2entries:
                if 'lvs' not in l2:
                    continue
                lvm_present = True
                self._create_logical_volumes(l2['path'], l2['vg_name'], l2['lvs'], l2['extensible'])

        if lvm_present:
            # add lvm2 package to install list
            self._add_packages_to_install('lvm2')

        # Create partitions_data (needed for mk-setup-grub.sh)
        for partition in partitions:
            if "mountpoint" in partition:
                if partition['mountpoint'] == '/':
                    partitions_data['root'] = partition['path']
                elif partition['mountpoint'] == '/boot':
                    partitions_data['boot'] = partition['path']
                    partitions_data['bootdirectory'] = '/'

        # If no separate boot partition, then use /boot folder from root partition
        if 'boot' not in partitions_data:
            partitions_data['boot'] = partitions_data['root']
            partitions_data['bootdirectory'] = '/boot/'

        # Sort partitions by mountpoint to be able to mount and
        # unmount it in proper sequence
        partitions.sort(key=lambda p: self.partition_compare(p))

        self.install_config['partitions_data'] = partitions_data

    def _format_partitions(self):
        partitions = self.install_config['partitions']
        self.logger.info(partitions)

        # Format the filesystem
        for partition in partitions:
            ptype = self._get_partition_type(partition)
            # Do not format BIOS boot partition
            if ptype == PartitionType.BIOS:
                continue
            if ptype == PartitionType.SWAP:
                mkfs_cmd = ['mkswap']
            else:
                mkfs_cmd = ['mkfs', '-t', partition['filesystem']]

            if 'fs_options' in partition:
                options = re.sub("[^\S]", " ", partition['fs_options']).split()
                mkfs_cmd.extend(options)

            mkfs_cmd.extend([partition['path']])
            retval = self.cmd.run(mkfs_cmd)

            if retval != 0:
                raise Exception(
                    "Failed to format {} partition @ {}".format(partition['filesystem'],
                                                         partition['path']))

    def getfile(self, filename):
        """
        Returns absolute filepath by filename.
        """
        for dirname in self.install_config['search_path']:
            filepath = os.path.join(dirname, filename)
            if os.path.exists(filepath):
                return filepath
        raise Exception("File {} not found in the following directories {}".format(filename, self.install_config['search_path']))

