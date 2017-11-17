import os.path
import subprocess
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
    def Configure(self,options_file, maxy, maxx):
        self.cd_path = None

        kernel_params = subprocess.check_output(['cat', '/proc/cmdline'])

        # check for the repo param
        m = re.match(r".*repo=(\S+)\s*.*\s*", kernel_params.decode())
        if m != None:
            rpm_path = m.group(1)
        else:
            # the rpms should be in the cd
            self.mount_RPMS_cd()
            rpm_path = os.path.join(self.cd_path, "RPMS")

        # check the kickstart param
        ks_config = None
        m = re.match(r".*ks=(\S+)\s*.*\s*", kernel_params.decode())
        if m != None:
            ks_config = self.get_config(m.group(1))

        install_config = None
        if ks_config:
            install_config = self.ks_config(options_file, ks_config)
        else:
            install_config = self.ui_config(options_file, maxy, maxx)
        return rpm_path, install_config

    def is_vmware_virtualization(self):
        process = subprocess.Popen(['systemd-detect-virt'], stdout=subprocess.PIPE)
        out, err = process.communicate()
        if err is not None and err != 0:
            return False
        else:
            return out == 'vmware\n'

    def get_config(self, path):
        if path.startswith("http://"):
            # Do 5 trials to get the kick start
            # TODO: make sure the installer run after network is up
            ks_file_error = "Failed to get the kickstart file at {0}".format(path)
            wait = 1
            for x in range(0, 5):
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
                self.mount_RPMS_cd()
                path = os.path.join(self.cd_path, path.replace("cdrom:/", "", 1))
            return (JsonWrapper(path)).read()

    def mount_RPMS_cd(self):
        # check if the cd is already mounted
        if self.cd_path:
            return

        # Mount the cd to get the RPMS
        process = subprocess.Popen(['mkdir', '-p', '/mnt/cdrom'])
        retval = process.wait()

        # Retry mount the CD
        for i in range(0, 3):
            process = subprocess.Popen(['mount', '/dev/cdrom', '/mnt/cdrom'])
            retval = process.wait()
            if retval == 0:
                self.cd_path = "/mnt/cdrom"
                return
            print("Failed to mount the cd, retry in a second")
            time.sleep(1)
        print("Failed to mount the cd, exiting the installer")
        print("check the logs for more details")
        raise Exception("Can not mount the cd")

    def ks_config(self, options_file, ks_config):
        install_config = ks_config
        install_config['iso_system'] = False
        if self.is_vmware_virtualization() and 'install_linux_esx' not in install_config:
            install_config['install_linux_esx'] = True

        json_wrapper_option_list = JsonWrapper("build_install_options_all.json")
        option_list_json = json_wrapper_option_list.read()
        options_sorted = option_list_json.items()

        base_path = os.path.dirname("build_install_options_all.json")
        package_list = []

        package_list = PackageSelector.get_packages_to_install(options_sorted, install_config['type'], base_path)
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
            random_id = '%12x' % random.randrange(16**12)
            install_config['hostname'] = "photon-" + random_id.strip()

        # crypt the password if needed
        if install_config['password']['crypted']:
            install_config['password'] = install_config['password']['text']
        else:
            install_config['password'] = crypt.crypt(install_config['password']['text'],
                "$6$" + "".join([random.choice(string.ascii_letters + string.digits) for _ in range(16)]))
        return install_config

    def validate_hostname(self, hostname):
        error_empty = "Empty hostname or domain is not allowed"
        error_dash = "Hostname or domain should not start or end with '-'"
        error_hostname = "Hostname should start with alpha char and <= 64 chars"

        if hostname is None or len(hostname) == 0:
            return False, error_empty

        fields = hostname.split('.')
        for field in fields:
            if len(field) == 0:
                return False, error_empty
            if field[0] == '-' or field[-1] == '-':
                return False, error_dash

        machinename = fields[0]
        return (len(machinename) <= 64) and (ord(machinename[0]) in self.alpha_chars), error_hostname

    @staticmethod
    def validate_password(text):
        try:
            p = cracklib.VeryFascistCheck(text)
        except ValueError as message:
            p = str(message)
        return p == text, "Error: " + p

    @staticmethod
    def generate_password_hash(password):
        shadow_password = crypt.crypt(password, "$6$" + "".join([random.choice(string.ascii_letters + string.digits) for _ in range(16)]))
        return shadow_password

    def ui_config(self, options_file, maxy, maxx):
        # This represents the installer screen, the bool indicated if I can go back to this window or not
        items = []
        random_id = '%12x' % random.randrange(16**12)
        random_hostname = "photon-" + random_id.strip()
        install_config = {'iso_system': False}
        install_config['ui_install'] = True
        license_agreement = License(maxy, maxx)
        select_disk = SelectDisk(maxy, maxx, install_config)
        select_partition = PartitionISO(maxy, maxx, install_config)
        package_selector = PackageSelector(maxy, maxx, install_config, options_file)
        self.alpha_chars = list(range(65, 91))
        self.alpha_chars.extend(range(97, 123))
        hostname_accepted_chars = self.alpha_chars
        # Adding the numeric chars
        hostname_accepted_chars.extend(range(48, 58))
        # Adding the . and -
        hostname_accepted_chars.extend([ord('.'), ord('-')])

        hostname_reader = WindowStringReader(
            maxy, maxx, 10, 70,
            'hostname',
            None, # confirmation error msg if it's a confirmation text
            None, # echo char
            hostname_accepted_chars, # set of accepted chars
            self.validate_hostname, # validation function of the input
            None, # post processing of the input field
            'Choose the hostname for your system', 'Hostname:', 2, install_config,
            random_hostname,
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
            "Passwords don't match, please try again.", # confirmation error msg if it's a confirmation text
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
        index = 0
        params = None
        while True:
            result = items[index][0](params)
            if result.success:
                index += 1
                params = result.result
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
