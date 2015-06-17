#! /usr/bin/python2
#
#    Copyright (C) 2015 vmware inc.
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

import curses
import sys
import subprocess
import re
import requests
import json
import time
import os
from diskpartitioner import DiskPartitioner
from packageselector import PackageSelector
from custompackageselector import CustomPackageSelector
from installer import Installer
from windowstringreader import WindowStringReader
from jsonwrapper import JsonWrapper
from selectdisk import SelectDisk
from license import License

class IsoInstaller(object):

    def get_config(self, path, cd_path):
        if path.startswith("http"):
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
                print >> sys.stderr, "Failed to get the kickstart file at {0}, error msg: {1}".format(path, err_msg)
                print "Failed to get the kickstart file at {0}, retry in a second".format(path)
                time.sleep(1)


            # Something went wrong
            print "Failed to get the kickstart file at {0}, exiting the installer, check the logs for more details".format(path)
            raise Exception(err_msg)
        else:
            if path.startswith("cdrom:/"):
                path = os.path.join(cd_path, path.replace("cdrom:/", "", 1))
            return (JsonWrapper(path)).read();

    def mount_RPMS_cd(self):
        # Mount the cd to get the RPMS
        process = subprocess.Popen(['mkdir', '-p', '/mnt/cdrom'])
        retval = process.wait()

        # Retry mount the CD
        for i in range(0,3):
            process = subprocess.Popen(['mount', '/dev/cdrom', '/mnt/cdrom'])
            retval = process.wait()
            if retval == 0:
                return "/mnt/cdrom"
            print "Failed to mount the cd, retry in a second"
            time.sleep(1)
        print "Failed to mount the cd, exiting the installer, check the logs for more details"
        raise Exception("Can not mount the cd")
    
    def __init__(self, stdscreen):
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

        self.install_config = {'iso_system': False}

        # Mount the cd for the RPM, tools, and may be the ks
        cd_path = self.mount_RPMS_cd()
        
        # check the kickstart params
        ks_config = None
        kernel_params = subprocess.check_output(['cat', '/proc/cmdline'])
        m = re.match(r".*ks=(\S+)\s*.*\s*", kernel_params)
        if m != None:
            ks_config = self.get_config(m.group(1), cd_path)

        license_agreement = License(self.maxy, self.maxx)
        select_disk = SelectDisk(self.maxy, self.maxx, self.install_config)
        package_selector = PackageSelector(self.maxy, self.maxx, self.install_config)
        custom_package_selector = CustomPackageSelector(self.maxy, self.maxx, self.install_config)
        hostname_reader = WindowStringReader(self.maxy, self.maxx, 10, 70, False,  'Choose the hostname for your system',
            'Hostname:', 
            2, self.install_config)
        root_password_reader = WindowStringReader(self.maxy, self.maxx, 10, 70, True,  'Set up root password',
            'Root password:', 
            2, self.install_config)
        installer = Installer(self.install_config, self.maxy, self.maxx, True, tools_path=cd_path, rpm_path=os.path.join(cd_path, "RPMS"), log_path="/var/log", ks_config=ks_config)

        # This represents the installer screen, the bool indicated if I can go back to this window or not
        items = []
        if not ks_config:
            items = items + [
                    (license_agreement.display, False),
                    (select_disk.display, True),
                    (package_selector.display, True),
                    (custom_package_selector.display, False),
                    (hostname_reader.get_user_string, True),
                    (root_password_reader.get_user_string, True),
                 ]
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
    curses.wrapper(IsoInstaller)
