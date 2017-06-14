#! /usr/bin/python2
#
#    Copyright (C) 2015 vmware inc.
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

from argparse import ArgumentParser
import os.path
import curses
import subprocess
import re
import json
import time
import crypt
import string
import random
import urllib2
import requests
import cracklib
import modules.commons
from partitionISO import PartitionISO
from packageselector import PackageSelector
from installer import Installer
from installercontainer import InstallerContainer
from windowstringreader import WindowStringReader
from jsonwrapper import JsonWrapper
from selectdisk import SelectDisk
from license import License
from linuxselector import LinuxSelector

class IsoInstaller(object):

    def get_config(self, path):
        if path.startswith("http://"):
            # Do 5 trials to get the kick start
            # TODO: make sure the installer run after network is up
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
                modules.commons.log(modules.commons.LOG_ERROR, "Failed to get the kickstart file at {0}, error msg: {1}".format(path, err_msg))
                print "Failed to get the kickstart file at {0}, retry in a second".format(path)
                time.sleep(wait)
                wait = wait * 2


            # Something went wrong
            print "Failed to get the kickstart file at {0}, exiting the installer, check the logs for more details".format(path)
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
            print "Failed to mount the cd, retry in a second"
            time.sleep(1)
        print "Failed to mount the cd, exiting the installer, check the logs for more details"
        raise Exception("Can not mount the cd")

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

    def validate_password(self, text):
        try:
            p = cracklib.VeryFascistCheck(text)
        except ValueError, message:
            p = str(message)
        return p == text, "Error: " + p

    def generate_password_hash(self, password):
        shadow_password = crypt.crypt(password, "$6$" + "".join([random.choice(string.ascii_letters + string.digits) for _ in range(16)]))
        return shadow_password

    def validate_http_response(self, url, checks, exception_text, error_text):
        try:
            if url.startswith("https"):
                response = urllib2.urlopen(url, cafile="/usr/lib/python2.7/site-packages/requests/cacert.pem")
            else:
                response = urllib2.urlopen(url)

        except:
            return exception_text
        else:
            if response.getcode() != 200:
                return error_text

        html = response.read()

        for pattern, count, failed_check_text in checks:
            match = re.findall(pattern, html)
            if len(match) != count:
                return failed_check_text

        return ""
    def ui_install(self, options_file, rpm_path):
        # This represents the installer screen, the bool indicated if I can go back to this window or not
        items = []
        random_id = '%12x' % random.randrange(16**12)
        random_hostname = "photon-" + random_id.strip()
        install_config = {'iso_system': False}
        license_agreement = License(self.maxy, self.maxx)
        select_disk = SelectDisk(self.maxy, self.maxx, install_config)
        select_partition = PartitionISO(self.maxy, self.maxx, install_config)
        package_selector = PackageSelector(self.maxy, self.maxx, install_config, options_file)
        self.alpha_chars = range(65, 91)
        self.alpha_chars.extend(range(97, 123))
        hostname_accepted_chars = list(self.alpha_chars)
        # Adding the numeric chars
        hostname_accepted_chars.extend(range(48, 58))
        # Adding the . and -
        hostname_accepted_chars.extend([ord('.'), ord('-')])

        hostname_reader = WindowStringReader(
            self.maxy, self.maxx, 10, 70,
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
            self.maxy, self.maxx, 10, 70,
            'password',
            None, # confirmation error msg if it's a confirmation text
            '*', # echo char
            None, # set of accepted chars
            self.validate_password, # validation function of the input
            None,  # post processing of the input field
            'Set up root password', 'Root password:', 2, install_config)
        confirm_password_reader = WindowStringReader(
            self.maxy, self.maxx, 10, 70,
            'password',
            "Passwords don't match, please try again.", # confirmation error msg if it's a confirmation text
            '*', # echo char
            None, # set of accepted chars
            None, # validation function of the input
            self.generate_password_hash, # post processing of the input field
            'Confirm root password', 'Confirm Root password:', 2, install_config)

        items.append((license_agreement.display, False))
        items.append((select_disk.display, True))
        items.append((select_partition.display, False))
        items.append((select_disk.guided_partitions, False))
        items.append((package_selector.display, True))
        select_linux_index = -1
        if self.is_vmware_virtualization():
            linux_selector = LinuxSelector(self.maxy, self.maxx, install_config)
            items.append((linux_selector.display, True))
            select_linux_index = items.index((linux_selector.display, True))
        items.append((hostname_reader.get_user_string, True))
        items.append((root_password_reader.get_user_string, True))
        items.append((confirm_password_reader.get_user_string, False))
        installer = InstallerContainer(
            install_config,
            self.maxy,
            self.maxx,
            True,
            rpm_path=rpm_path,
            log_path="/var/log")

        items = items + [(installer.install, False)]

        index = 0
        params = None
        while True:
            result = items[index][0](params)
            if result.success:
                index += 1
                params = result.result
                if index == len(items) - 1:
                    self.screen.clear()
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


    def is_vmware_virtualization(self):
        process = subprocess.Popen(['systemd-detect-virt'], stdout=subprocess.PIPE)
        out, err = process.communicate()
        if err is not None and err != 0:
            return False
        else:
            return out == 'vmware\n'

    def __init__(self, stdscreen, options_file):
        self.screen = stdscreen

        # Init the colors
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_WHITE)

        self.screen.bkgd(' ', curses.color_pair(1))

        self.maxy, self.maxx = self.screen.getmaxyx()
        self.screen.addstr(self.maxy - 1, 0, '  Arrow keys make selections; <Enter> activates.')
        curses.curs_set(0)

        self.cd_path = None

        kernel_params = subprocess.check_output(['cat', '/proc/cmdline'])

        # check the kickstart param
        ks_config = None
        m = re.match(r".*ks=(\S+)\s*.*\s*", kernel_params)
        if m != None:
            ks_config = self.get_config(m.group(1))

        # check for the repo param
        m = re.match(r".*repo=(\S+)\s*.*\s*", kernel_params)
        if m != None:
            rpm_path = m.group(1)
        else:
            # the rpms should be in the cd
            self.mount_RPMS_cd()
            rpm_path = os.path.join(self.cd_path, "RPMS")

        if not ks_config:
            self.ui_install(options_file, rpm_path)
        else:
            install_config = ks_config
            install_config['iso_system'] = False
            if self.is_vmware_virtualization() and 'install_linux_esx' not in install_config:
                install_config['install_linux_esx'] = True
            installer = InstallerContainer(
                install_config,
                self.maxy, self.maxx,
                True,
                rpm_path=rpm_path,
                log_path="/var/log",
                ks_config=ks_config)

            installer.install(None)

if __name__ == '__main__':
    usage = "Usage: %prog [options]"
    parser = ArgumentParser(usage)
    parser.add_argument("-j", "--json-file", dest="options_file", default="input.json")

    options = parser.parse_args()
    curses.wrapper(IsoInstaller, options.options_file)
