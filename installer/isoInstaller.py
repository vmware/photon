#!/usr/bin/env python3
#
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>
import os
import subprocess
import shlex
import requests
import time
import json
import base64
from argparse import ArgumentParser
from installer import Installer
from commandutils import CommandUtils
from jsonwrapper import JsonWrapper
from device import Device

class IsoInstaller(object):
    def __init__(self, options):
        install_config=None
        self.media_mount_path = None
        photon_media = None
        ks_path = options.install_config_file
        # Path to RPMS repository: local media or remote URL
        # If --repo-path= provided - use it,
        # if not provided - use kernel repo= parameter,
        # if not provided - use /RPMS path from photon_media,
        # exit otherwise.
        repo_path = options.repo_path
        insecure = False

        with open('/proc/cmdline', 'r') as f:
            kernel_params = shlex.split(f.read().replace('\n', ''))

        for arg in kernel_params:
            if arg.startswith("ks="):
                if not ks_path:
                    ks_path = arg[len("ks="):]
            elif arg.startswith("repo="):
                if not repo_path:
                    repo_path = arg[len("repo="):]
            elif arg.startswith("photon.media="):
                photon_media = arg[len("photon.media="):]
            elif arg.startswith("insecure_installation="):
                insecure = arg.split("=")[1].lower() in ["1", "true", "y", "yes"]

        if photon_media:
            self.mount_media(photon_media)

        if not repo_path:
            if self.media_mount_path:
                repo_path = self.media_mount_path + "/RPMS"
            else:
                print("Please specify RPM repo path.")
                return

        if ks_path:
            if ks_path.startswith("http://") and not insecure:
                raise Exception("Refusing to download kick start configuration from non-https URLs. \
                                \nPass insecure_installation=1 as a parameter when giving http url in ks.")
            install_config=self._load_ks_config_url(ks_path, verify=not insecure)
        else:
            install_config=self._load_ks_config_platform(verify=not insecure)

        if install_config is None:
            install_config = {}
        elif insecure:
            install_config['insecure_repo'] = True
        install_config['release_version'] = options.release_version

        if options.ui_config_file:
            ui_config = (JsonWrapper(options.ui_config_file)).read()
        else:
            ui_config={}
        ui_config['options_file'] = options.options_file

        # Run installer
        installer = Installer(rpm_path=repo_path, log_path="/var/log")

        installer.configure(install_config, ui_config)
        installer.execute()

    def _load_ks_config_http(self, url, retries=5, timeout=3, verify=True):
        # Do 5 trials to get the kick start
        # TODO: make sure the installer run after network is up
        wait = 1
        for _ in range(0, retries):
            err_msg = ""
            try:
                response = requests.get(url, timeout=timeout, verify=verify)
            except Exception as e:
                err_msg = e
            else:
                return json.loads(response.text)

            print("error msg: {0}  Retry after {1} seconds".format(err_msg, wait))
            time.sleep(wait)
            wait = wait * 2

        # Something went wrong
        print("Failed to get the kickstart file at {0}".format(url))
        raise Exception(err_msg)

    def _load_ks_config_url(self, path, verify=True):
        """kick start configuration"""
        if path.startswith("https+insecure://"):
            verify = False
            path = "https://" + path[len("https+insecure://"):]
        if path.startswith("https://") or path.startswith("http://"):
            return self._load_ks_config_http(path, verify=verify)
        else:
            if path.startswith("cdrom:/"):
                if self.media_mount_path is None:
                    raise Exception("cannot read ks config from cdrom, no cdrom specified")
                path = os.path.join(self.media_mount_path, path.replace("cdrom:/", "", 1))
            return (JsonWrapper(path)).read()

    def _load_ks_config_platform(self, verify=True):
        if CommandUtils.is_vmware_virtualization():
            return self._load_ks_config_vmware(verify=verify)
        else:
            return None

    def _load_ks_config_vmware(self, verify=True):
        result = subprocess.run(['vmtoolsd', '--cmd', 'info-get guestinfo.kickstart.data'],
                universal_newlines=True, stdout=subprocess.PIPE)
        if result.returncode == 0:
            return json.loads(base64.b64decode(result.stdout.rstrip('\n')))
        result = subprocess.run(['vmtoolsd', '--cmd', 'info-get guestinfo.kickstart.url'],
                universal_newlines=True, stdout=subprocess.PIPE)
        if result.returncode == 0:
            return self._load_ks_config_url(result.stdout.rstrip('\n'), verify=verify)
        return None

    def mount_media(self, photon_media):
        """Mount the cd with RPMS"""
        # check if the cd is already mounted
        if self.media_mount_path:
            return
        mount_path = "/mnt/media"

        # Mount the cd to get the RPMS
        os.makedirs(mount_path, exist_ok=True)

        # Construct mount cmdline
        cmdline = ['mount']
        if photon_media.startswith("UUID="):
            cmdline.extend(['-U', photon_media[len("UUID="):] ])
        elif photon_media.startswith("LABEL="):
            cmdline.extend(['-L', photon_media[len("LABEL="):] ])
        elif photon_media == "cdrom":
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
                self.media_mount_path = mount_path
                return
            print("Failed to mount the cd, retry in 5 seconds")
            Device.refresh_devices()
            time.sleep(5)
        print("Failed to mount the cd, exiting the installer")
        print("check the logs for more details")
        raise Exception("Can not mount the cd")


if __name__ == '__main__':
    usage = "Usage: %prog [options]"
    parser = ArgumentParser(usage)
    parser.add_argument("-c", "--config", dest="install_config_file")
    parser.add_argument("-u", "--ui-config", dest="ui_config_file")
    parser.add_argument("-j", "--json-file", dest="options_file", default="input.json")
    parser.add_argument("-r", "--repo-path", dest="repo_path")
    parser.add_argument("-p", "--release-version", dest="release_version")
    options = parser.parse_args()

    IsoInstaller(options)
