#
#    Copyright (C) 2015 vmware inc.
#
#    Author: Touseef Liaqat <tliaqat@vmware.com>

from installer import Installer

class InstallerContainer(object):
    def __init__(self, install_config, maxy=0, maxx=0,
                 iso_installer=False, rpm_path="../stage/RPMS",
                 log_path="../stage/LOGS", log_level="info"):

        self.install_config = install_config
        self.maxy = maxy
        self.maxx = maxx
        self.iso_installer = iso_installer
        self.rpm_path = rpm_path
        self.log_path = log_path
        self.log_level = log_level

    def install(self, params):
        installer = None
        installer = Installer(self.install_config, self.maxy, self.maxx,
                              self.iso_installer, self.rpm_path, self.log_path, self.log_level)

        return installer.install(params)
