#! /usr/bin/python2
#
#    Copyright (C) 2015 vmware inc.
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

import subprocess
import os

class Device(object):
    def __init__(self, model, path, size):
        self.model = model
        self.path = path
        self.size = size

    @staticmethod
    def refresh_devices():
        devices_list = subprocess.check_output(['lsblk', '-S', '-I', '8', '-n', '--output', 'NAME,SIZE,MODEL'], stderr=open(os.devnull, 'w'))
        return Device.wrap_devices_from_list(devices_list)

    @staticmethod
    def wrap_devices_from_list(list):
        devices = []
        deviceslines = list.splitlines()
        for deviceline in deviceslines:
            cols = deviceline.split(None, 2)
            devices.append(
                    Device(cols[2] #Model
                        , '/dev/' + cols[0] #Path
                        , cols[1] #size
                        ))

        return devices