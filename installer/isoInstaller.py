#! /usr/bin/python2
#
#    Copyright (C) 2015 vmware inc.
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

import curses
import sys
from diskpartitioner import DiskPartitioner
from packageselector import PackageSelector
from custompackageselector import CustomPackageSelector
from installer import Installer
from windowstringreader import WindowStringReader
from jsonwrapper import JsonWrapper
from selectdisk import SelectDisk
from license import License

class IsoInstaller(object):

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

        self.install_config = {}

        license_agreement = License(self.maxy, self.maxx)

        self.install_config['iso_system'] = False
        select_disk = SelectDisk(self.maxy, self.maxx, self.install_config)

        package_selector = PackageSelector(self.maxy, self.maxx, self.install_config)
        custom_package_selector = CustomPackageSelector(self.maxy, self.maxx, self.install_config)
        hostname_reader = WindowStringReader(self.maxy, self.maxx, 10, 70, False,  'Choose the hostname for your system',
            'Hostname:', 
            2, self.install_config)
        root_password_reader = WindowStringReader(self.maxy, self.maxx, 10, 70, True,  'Set up root password',
            'Root password:', 
            2, self.install_config)
        installer = Installer(self.install_config, self.maxy, self.maxx, True, tools_path=None, rpm_path='cdrom', log_path="/var/log")

        # This represents the installer screen, the bool indicated if I can go back to this window or not
        items = [
                    (license_agreement.display, False),
                    (select_disk.display, True),
                    (package_selector.display, True),
                    (custom_package_selector.display, False),
                    (hostname_reader.get_user_string, True),
                    (root_password_reader.get_user_string, True),
                    (installer.install, False)
                ]

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
