#! /usr/bin/python2
#
#    Copyright (C) 2015 vmware inc.
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

import curses
import subprocess
import os
import json
from partition import Partition

class Device(object):
    def __init__(self, model, path, size, partitions):
        self.model = model
        self.path = path
        self.size = size
        self.partitions = partitions

    @staticmethod
    def refresh_devices():
        devices_json = subprocess.check_output(['gpartedbin', 'getdevices'], stderr=open(os.devnull, 'w'))
        devices = Device.wrap_devices_from_dict(json.loads(devices_json))
        return devices

    @staticmethod
    def wrap_devices_from_dict(dct):
        if dct['success'] == False:
            return [];

        devices = []
        for device in dct['devices']:
            devices.append(
                    Device(device['model'], device['path'], device['size'], Partition.wrap_partitions_from_dict_arr(device['partitions'])))

        return devices