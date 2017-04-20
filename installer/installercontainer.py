#! /usr/bin/python2
#
#    Copyright (C) 2015 vmware inc.
#
#    Author: Touseef Liaqat <tliaqat@vmware.com>

from installer import Installer
from ostreeinstaller import OstreeInstaller
from ostreeserverinstaller import OstreeServerInstaller

class InstallerContainer(object):
    def __init__(self, install_config, maxy = 0, maxx = 0, iso_installer = False, rpm_path = "../stage/RPMS", log_path = "../stage/LOGS", ks_config = None):
        self.install_config = install_config
        self.maxy = maxy
        self.maxx = maxx
        self.ks_config = ks_config
        self.iso_installer = iso_installer
        self.rpm_path = rpm_path
        self.log_path = log_path

    def install(self, params):
        installer = None
        if self.install_config['type'] == "ostree_host":
            installer = OstreeInstaller(self.install_config, self.maxy, self.maxx, self.iso_installer, self.rpm_path, self.log_path, self.ks_config)
        elif self.install_config['type'] == "ostree_server":
            installer = OstreeServerInstaller(self.install_config, self.maxy, self.maxx, self.iso_installer, self.rpm_path, self.log_path, self.ks_config)
        else:
            installer = Installer(self.install_config, self.maxy, self.maxx, self.iso_installer, self.rpm_path, self.log_path, self.ks_config)

        return installer.install(params)