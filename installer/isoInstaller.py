#! /usr/bin/python3
#
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

import shlex
import curses
from argparse import ArgumentParser
from installer import Installer
from commandutils import CommandUtils

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

        install_config=None
        self.cd_mount_path = None
        ks_path = None
        cd_search = None

        with open('/proc/cmdline', 'r') as f:
            kernel_params = shlex.split(f.read().replace('\n', ''))

        for arg in kernel_params:
            if arg.startswith("ks="):
                ks_path = arg[len("ks="):]
            elif arg.startswith("repo="):
                rpms_path = arg[len("repo="):]
            elif arg.startswith("photon.media="):
                cd_search = arg[len("photon.media="):]

        if cd_search is not None:
            self.mount_cd(cd_search)

        if ks_path is not None:
            install_config=self.get_ks_config(ks_path)

        # Run installer
        installer = Installer(
            maxy=self.maxy,
            maxx=self.maxx,
            iso_installer=True,
            rpm_path=rpms_path,
            log_path="/var/log",
            log_level="debug")

        ui_config={}
        ui_config['options_file'] = options_file

        installer.configure(install_config, ui_config)
        self.screen.erase()
        installer.execute()

    def _load_ks_config(self, path):
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

                self.logger.warning(ks_file_error)
                self.logger.warning("error msg: {0}".format(err_msg))
                self.logger.warning("retry in a second")
                time.sleep(wait)
                wait = wait * 2

            # Something went wrong
            self.logger.error(ks_file_error)
            raise Exception(err_msg)
        else:
            if path.startswith("cdrom:/"):
                if self.cd_mount_path is None:
                    raise Exception("cannot read ks config from cdrom, no cdrom specified")
                path = os.path.join(self.cd_mount_path, path.replace("cdrom:/", "", 1))
            return (JsonWrapper(path)).read()

    def get_ks_config(self, ks_path):
        """Load configuration from kick start file"""
        install_config = self._load_ks_config(ks_path)

        if 'install_linux_esx' not in install_config and CommandUtils.is_vmware_virtualization():
            install_config['install_linux_esx'] = True

        return install_config

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
            self.logger.error("Unsupported installer media, check photon.media in kernel cmdline")
            raise Exception("Can not mount the cd")

        cmdline.extend(['-o', 'ro', mount_path])

        # Retry mount the CD
        for _ in range(0, 3):
            process = subprocess.Popen(cmdline)
            retval = process.wait()
            if retval == 0:
                self.cd_mount_path = mount_path
                return
            self.logger.error("Failed to mount the cd, retry in a second")
            time.sleep(1)
        self.logger.error("Failed to mount the cd, exiting the installer")
        self.logger.error("check the logs for more details")
        raise Exception("Can not mount the cd")


if __name__ == '__main__':
    usage = "Usage: %prog [options]"
    parser = ArgumentParser(usage)
    parser.add_argument("-j", "--json-file", dest="options_file", default="input.json")
    parser.add_argument("-r", "--rpms-path", dest="rpms_path", default="../stage/RPMS")
    options = parser.parse_args()
    curses.wrapper(IsoInstaller, options.options_file, options.rpms_path)
