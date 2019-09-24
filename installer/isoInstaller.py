#! /usr/bin/python3
#
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

from argparse import ArgumentParser
import curses
from installercontainer import InstallerContainer
from iso_config import IsoConfig

class IsoInstaller(object):
    def __init__(self, stdscreen, options_file, rpms_path):
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
        config = IsoConfig()
        rpm_path, install_config = config.Configure(options_file, rpms_path, self.maxy, self.maxx)

        self.screen.erase()
        installer = InstallerContainer(
            install_config,
            self.maxy, self.maxx,
            True,
            rpm_path=rpm_path,
            log_path="/var/log")

        installer.install()

if __name__ == '__main__':
    usage = "Usage: %prog [options]"
    parser = ArgumentParser(usage)
    parser.add_argument("-j", "--json-file", dest="options_file", default="input.json")
    parser.add_argument("-r", "--rpms-path", dest="rpms_path", default="../stage/RPMS")
    options = parser.parse_args()
    curses.wrapper(IsoInstaller, options.options_file, options.rpms_path)
