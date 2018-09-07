import os
import sys
import subprocess
import shlex
import re
import json
import time
import crypt
import string
import random
import requests
import cracklib
import modules.commons
from partitionISO import PartitionISO
from packageselector import PackageSelector
from windowstringreader import WindowStringReader
from jsonwrapper import JsonWrapper
from selectdisk import SelectDisk
from license import License
from linuxselector import LinuxSelector

class IsoConfig(object):
    """This class handles iso installer configuration."""
    def __init__(self):
        self.cd_mount_path = None
        self.alpha_chars = list(range(65, 91))
        self.alpha_chars.extend(range(97, 123))
        self.hostname_accepted_chars = self.alpha_chars
        # Adding the numeric chars
        self.hostname_accepted_chars.extend(range(48, 58))
        # Adding the . and -
        self.hostname_accepted_chars.extend([ord('.'), ord('-')])
        self.random_id = '%12x' % random.randrange(16**12)
        self.random_hostname = "photon-" + self.random_id.strip()

    def Configure(self, options_file, maxy, maxx):
        ks_path = None
        rpm_path = None
        ks_config = None
        cd_search = None

        with open('/proc/cmdline', 'r') as f:
            kernel_params = shlex.split(f.read().replace('\n', ''))

        for arg in kernel_params:
            if arg.startswith("ks="):
                ks_path = arg[len("ks="):]
            elif arg.startswith("repo="):
                rpm_path = arg[len("repo="):]
            elif arg.startswith("photon.media="):
                cd_search = arg[len("photon.media="):]

        if cd_search is not None:
            self.mount_cd(cd_search)

        if ks_path is not None:
            ks_config = self.get_config(ks_path)

        if rpm_path is None:
            # the rpms should be in the cd
            if self.cd_mount_path is None:
                raise Exception("Please specify RPM repo location, as no cdrom is specified. (PXE?)")
            rpm_path = os.path.join(self.cd_mount_path, "RPMS")

        if ks_config:
            install_config = self.ks_config(options_file, ks_config)
        else:
            install_config = self.ui_config(options_file, maxy, maxx)
        return rpm_path, install_config

    @staticmethod
    def is_vmware_virtualization():
        """Detect vmware vm"""
        process = subprocess.Popen(['systemd-detect-virt'], stdout=subprocess.PIPE)
        out, err = process.communicate()
        if err is not None and err != 0:
            return False
        return out.decode() == 'vmware\n'

    def get_config(self, path):
        """kick start configuration"""
        if path.startswith("http://"):
            # Do 5 trials to get the kick start
            # TODO: make sure the installer run after network is up
            ks_file_error = "Failed to get the kickstart file at {0}".format(path)
            wait = 1
            for _ in range(0, 5):
                err_msg = ""
                try:
                    response = requests.get(path, timeout=3)
                    if response.ok:
                        return json.loads(response.text)
                    err_msg = response.text
                except Exception as e:
                    err_msg = e

                modules.commons.log(modules.commons.LOG_ERROR,
                                    ks_file_error)
                modules.commons.log(modules.commons.LOG_ERROR,
                                    "error msg: {0}".format(err_msg))
                print(ks_file_error)
                print("retry in a second")
                time.sleep(wait)
                wait = wait * 2

            # Something went wrong
            print(ks_file_error)
            print("exiting the installer, check the logs for more details")
            raise Exception(err_msg)
        else:
            if path.startswith("cdrom:/"):
                if self.cd_mount_path is None:
                    raise Exception("cannot read ks config from cdrom, no cdrom specified")
                path = os.path.join(self.cd_mount_path, path.replace("cdrom:/", "", 1))
            return (JsonWrapper(path)).read()

    def mount_cd(self, cd_search):
        """Mount the cd with RPMS"""
        # check if the cd is already mounted
        if self.cd_mount_path:
            return
        mount_path = "/mnt/cdrom"

        # Mount the cd to get the RPMS
        os.makedirs(mount_path, exist_ok=True)

        # Construct mount cmdline
        cmdline = ['mount']
        if cd_search.startswith("UUID="):
            cmdline.extend(['-U', cd_search[len("UUID="):] ]);
        elif cd_search.startswith("LABEL="):
            cmdline.extend(['-L', cd_search[len("LABEL="):] ]);
        elif cd_search == "cdrom":
            cmdline.append('/dev/cdrom')
        else:
            print("Unsupported installer media, check photon.media in kernel cmdline")
            raise Exception("Can not mount the cd")

        cmdline.extend(['-o', 'ro', mount_path])

        # Retry mount the CD
        for _ in range(0, 3):
            process = subprocess.Popen(cmdline)
            retval = process.wait()
            if retval == 0:
                self.cd_mount_path = mount_path
                return
            print("Failed to mount the cd, retry in a second")
            time.sleep(1)
        print("Failed to mount the cd, exiting the installer")
        print("check the logs for more details")
        raise Exception("Can not mount the cd")

    def ks_config(self, options_file, ks_config):
        """Load configuration from file"""
        del options_file
        install_config = ks_config
        install_config['iso_system'] = False
        if self.is_vmware_virtualization() and 'install_linux_esx' not in install_config:
            install_config['install_linux_esx'] = True

        json_wrapper_option_list = JsonWrapper("build_install_options_all.json")
        option_list_json = json_wrapper_option_list.read()
        options_sorted = option_list_json.items()

        base_path = os.path.dirname("build_install_options_all.json")
        package_list = []

        package_list = PackageSelector.get_packages_to_install(options_sorted,
                                                               install_config['type'],
                                                               base_path)
        if 'additional_packages' in install_config:
            package_list.extend(install_config['additional_packages'])
        install_config['packages'] = package_list

        if 'partitions' in install_config:
            partitions = install_config['partitions']
        else:
            partitions = modules.commons.default_partitions

        install_config['disk'] = modules.commons.partition_disk(install_config['disk'], partitions)

        if "hostname" in install_config:
            evalhostname = os.popen('printf ' + install_config["hostname"].strip(" ")).readlines()
            install_config['hostname'] = evalhostname[0]
        if "hostname" not in install_config or install_config['hostname'] == "":
            install_config['hostname'] = "photon-" + self.random_id.strip()

        # crypt the password if needed
        if install_config['password']['crypted']:
            install_config['password'] = install_config['password']['text']
        else:
            install_config['password'] = crypt.crypt(
                install_config['password']['text'],
                "$6$" + "".join([random.choice(
                    string.ascii_letters + string.digits) for _ in range(16)]))
        return install_config

    @staticmethod
    def validate_hostname(hostname):
        """A valid hostname must start with a letter"""
        error_empty = "Empty hostname or domain is not allowed"
        error_dash = "Hostname or domain should not start or end with '-'"
        error_hostname = "Hostname should start with alpha char and <= 64 chars"

        if hostname is None or not hostname:
            return False, error_empty

        fields = hostname.split('.')
        for field in fields:
            if not field:
                return False, error_empty
            if field[0] == '-' or field[-1] == '-':
                return False, error_dash

        machinename = fields[0]
        return (len(machinename) <= 64 and
                machinename[0].isalpha(), error_hostname)

    @staticmethod
    def validate_password(text):
        """Validate password with cracklib"""
        try:
            password = cracklib.VeryFascistCheck(text)
        except ValueError as message:
            password = str(message)
        return password == text, "Error: " + password

    @staticmethod
    def generate_password_hash(password):
        """Generate hash for the password"""
        shadow_password = crypt.crypt(
            password, "$6$" + "".join(
                [random.choice(
                    string.ascii_letters + string.digits) for _ in range(16)]))
        return shadow_password

    def ui_config(self, options_file, maxy, maxx):
        """Configuration through UI"""
        # This represents the installer screen, the bool indicated if
        # I can go back to this window or not
        install_config = {'iso_system': False}
        install_config['ui_install'] = True
        items, select_linux_index = self.add_ui_pages(options_file, maxy, maxx,
                                                      install_config)
        index = 0
        while True:
            result = items[index][0](None)
            if result.success:
                index += 1
                if index == len(items):
                    break
                #Skip linux select screen for ostree installation.
                if index == select_linux_index:
                    if install_config['type'] == 'ostree_server':
                        index += 1
            else:
                index -= 1
                while index >= 0 and items[index][1] is False:
                    index -= 1
                if index < 0:
                    index = 0
                #Skip linux select screen for ostree installation.
                if index == select_linux_index:
                    if install_config['type'] == 'ostree_server':
                        index -= 1
        return install_config
    def add_ui_pages(self, options_file, maxy, maxx, install_config):
        items = []
        license_agreement = License(maxy, maxx)
        select_disk = SelectDisk(maxy, maxx, install_config)
        select_partition = PartitionISO(maxy, maxx, install_config)
        package_selector = PackageSelector(maxy, maxx, install_config, options_file)
        hostname_reader = WindowStringReader(
            maxy, maxx, 10, 70,
            'hostname',
            None, # confirmation error msg if it's a confirmation text
            None, # echo char
            self.hostname_accepted_chars, # set of accepted chars
            IsoConfig.validate_hostname, # validation function of the input
            None, # post processing of the input field
            'Choose the hostname for your system', 'Hostname:', 2, install_config,
            self.random_hostname,
            True)
        root_password_reader = WindowStringReader(
            maxy, maxx, 10, 70,
            'password',
            None, # confirmation error msg if it's a confirmation text
            '*', # echo char
            None, # set of accepted chars
            IsoConfig.validate_password, # validation function of the input
            None,  # post processing of the input field
            'Set up root password', 'Root password:', 2, install_config)
        confirm_password_reader = WindowStringReader(
            maxy, maxx, 10, 70,
            'password',
            # confirmation error msg if it's a confirmation text
            "Passwords don't match, please try again.",
            '*', # echo char
            None, # set of accepted chars
            None, # validation function of the input
            IsoConfig.generate_password_hash, # post processing of the input field
            'Confirm root password', 'Confirm Root password:', 2, install_config)

        items.append((license_agreement.display, False))
        items.append((select_disk.display, True))
        items.append((select_partition.display, False))
        items.append((select_disk.guided_partitions, False))
        items.append((package_selector.display, True))
        select_linux_index = -1
        if self.is_vmware_virtualization():
            linux_selector = LinuxSelector(maxy, maxx, install_config)
            items.append((linux_selector.display, True))
            select_linux_index = items.index((linux_selector.display, True))
        items.append((hostname_reader.get_user_string, True))
        items.append((root_password_reader.get_user_string, True))
        items.append((confirm_password_reader.get_user_string, False))
        return items, select_linux_index
