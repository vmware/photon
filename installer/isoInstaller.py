#! /usr/bin/python2
#
#    Copyright (C) 2015 vmware inc.
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

from optparse import OptionParser
import os.path
import curses
import sys
import subprocess
import re
import requests
import json
import time
import os
import cracklib
import crypt
import string
import random
import urllib
import urllib2
import modules.commons
from diskpartitioner import DiskPartitioner
from packageselector import PackageSelector
from custompackageselector import CustomPackageSelector
from installer import Installer
from installercontainer import InstallerContainer
from ostreeinstaller import OstreeInstaller
from windowstringreader import WindowStringReader
from ostreewindowstringreader import OSTreeWindowStringReader
from jsonwrapper import JsonWrapper
from selectdisk import SelectDisk
from license import License
from ostreeserverselector import OSTreeServerSelector

class IsoInstaller(object):

    def get_config(self, path):
        if path.startswith("http://"):
            # Do 3 trials to get the kick start
            # TODO: make sure the installer run after network is up
            for x in range(0,3):
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
                time.sleep(1)


            # Something went wrong
            print "Failed to get the kickstart file at {0}, exiting the installer, check the logs for more details".format(path)
            raise Exception(err_msg)
        else:
            if path.startswith("cdrom:/"):
                self.mount_RPMS_cd()
                path = os.path.join(self.cd_path, path.replace("cdrom:/", "", 1))
            return (JsonWrapper(path)).read();

    def mount_RPMS_cd(self):
        # check if the cd is already mounted
        if self.cd_path:
            return

        # Mount the cd to get the RPMS
        process = subprocess.Popen(['mkdir', '-p', '/mnt/cdrom'])
        retval = process.wait()

        # Retry mount the CD
        for i in range(0,3):
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
        error_msg = "It should start with alpha char and ends with alpha-numeric char"
        if (hostname == None or len(hostname) == 0):
            return False, error_msg
        return (ord(hostname[0]) in self.alpha_chars) and (hostname[-1] not in ['.', '-']), error_msg

    def validate_ostree_url_input(self, text):
        status = 0
        if not text:
            return False, "Error: Invalid input"

        try:
           if text.startswith("https"):
               status = urllib2.urlopen(text,cafile="/usr/lib/python2.7/site-packages/requests/cacert.pem").getcode()
           else:
               status = urllib2.urlopen(text).getcode()

        except:
            return False , "Error: Invalid or unreachable Url"
        else:
            if status != 200:
                return False , "Error: URL not accessible"

        return True, None

    def validate_ostree_refs_input(self, text):
        return not (not text), "Error: Invalid input"

    def validate_password(self, text):
        try:
            p = cracklib.VeryFascistCheck(text)
        except ValueError, message:
            p = str(message)
        return p == text, "Error: " + p

    def generate_password_hash(self,  password):
        shadow_password = crypt.crypt(password, "$6$" + "".join([random.choice(string.ascii_letters + string.digits) for _ in range(16)]))
        return shadow_password

    def __init__(self, stdscreen, options_file):
        self.screen = stdscreen

        # Init the colors
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_WHITE)

        self.screen.bkgd(' ', curses.color_pair(1))

        self.maxy,  self.maxx = self.screen.getmaxyx()
        self.screen.addstr(self.maxy - 1, 0, '<Tab> moves; <Space> selects; <Enter> forward')

        curses.curs_set(0)

        self.cd_path = None;
        
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
            rpm_path=os.path.join(self.cd_path, "RPMS")

        # This represents the installer screen, the bool indicated if I can go back to this window or not
        items = []
        if not ks_config:
            random_id = '%12x' % random.randrange(16**12)
            random_hostname = "photon-" + random_id.strip()
            install_config = {'iso_system': False}
            license_agreement = License(self.maxy, self.maxx)
            select_disk = SelectDisk(self.maxy, self.maxx, install_config)
            package_selector = PackageSelector(self.maxy, self.maxx, install_config, options_file)

            self.alpha_chars = range(65, 91)
            self.alpha_chars.extend(range(97,123))
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
                    random_hostname)
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
            ostree_server_selector = OSTreeServerSelector(self.maxy, self.maxx, install_config)
            ostree_url_reader = OSTreeWindowStringReader(
                    self.maxy, self.maxx, 10, 80, 
                    'ostree_repo_url', 
                    None, # confirmation error msg if it's a confirmation text
                    None, # echo char
                    None, # set of accepted chars
                    self.validate_ostree_url_input, # validation function of the input
                    None, # post processing of the input field
                    'Please provide the URL of OSTree repo', 'OSTree Repo URL:', 2, install_config,
                    "http://")
            ostree_ref_reader = OSTreeWindowStringReader(
                    self.maxy, self.maxx, 10, 70, 
                    'ostree_repo_ref', 
                    None, # confirmation error msg if it's a confirmation text
                    None, # echo char
                    None, # set of accepted chars
                    self.validate_ostree_refs_input, # validation function of the input
                    None, # post processing of the input field
                    'Please provide the Ref in OSTree repo', 'OSTree Repo Ref:', 2, install_config,
                    "photon/tp2/x86_64/minimal")
            
            items = items + [
                    (license_agreement.display, False),
                    (select_disk.display, True),
                    (package_selector.display, True),
                    (hostname_reader.get_user_string, True),
                    (root_password_reader.get_user_string, True),
                    (confirm_password_reader.get_user_string, False),
                    (ostree_server_selector.display, True),
                    (ostree_url_reader.get_user_string, True),
                    (ostree_ref_reader.get_user_string, True),
                 ]
        else:
            install_config = ks_config
            install_config['iso_system'] = False

        installer = InstallerContainer(install_config, self.maxy, self.maxx, True, rpm_path=rpm_path, log_path="/var/log", ks_config=ks_config)

        items = items + [(installer.install, False)]

        index = 0
        params = None
        while True:
            result = items[index][0](params)
            if result.success:
                index += 1
                params = result.result
                if index == len(items):
                    break
            else:
                index -= 1
                while index >= 0 and items[index][1] == False:
                    index -= 1
                if index < 0:
                    index = 0

if __name__ == '__main__':
    usage = "Usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-j",  "--json-file", dest="options_file",  default="input.json")

    (options,  args) = parser.parse_args()
    curses.wrapper(IsoInstaller, options.options_file)
