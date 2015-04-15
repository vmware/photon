#! /usr/bin/python2
#
#    Copyright (C) 2015 vmware inc.
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

import subprocess
import os
import json
from device import Device
from window import Window
from actionresult import ActionResult
from menu import Menu
from confirmwindow import ConfirmWindow

class SelectDisk(object):
    def __init__(self,  maxy, maxx, install_config):
        self.install_config = install_config
        self.menu_items = []

        self.maxx = maxx
        self.maxy = maxy
        self.win_width = 70
        self.win_height = 16

        self.win_starty = (self.maxy - self.win_height) / 2
        self.win_startx = (self.maxx - self.win_width) / 2

        self.menu_starty = self.win_starty + 6
        self.menu_height = 5

        self.window = Window(self.win_height, self.win_width, self.maxy, self.maxx, 'Welcome to the Photon installer', True)
        self.devices = Device.refresh_devices()

    def guided_partitions(self, device_index):
        menu_height = 9
        menu_width = 40
        menu_starty = (self.maxy - menu_height) / 2 + 5
        confrim_window = ConfirmWindow(menu_height, menu_width, self.maxy, self.maxx, menu_starty, 'This will erase the disk.\nAre you sure?')
        confirmed = confrim_window.do_action().result['yes']
        
        if not confirmed:
            return ActionResult(confirmed, None)
        
        #self.install_config['disk'] = self.devices[device_index].path
        #return ActionResult(True, None)
        
        # Do the partitioning
        self.window.clearerror()
        json_ret = subprocess.check_output(['gpartedbin', 'defaultpartitions', self.devices[device_index].path], stderr=open(os.devnull, 'w'))
        json_dct = json.loads(json_ret)
        if json_dct['success']:
            self.install_config['disk'] = json_dct['data']
        else:
            self.window.adderror('Partitioning failed, you may try again')
        return ActionResult(json_dct['success'], None)

    def display(self, params):
        self.window.addstr(0, 0, 'First, we will setup your disks.\n\nWe have detected {0} disks, choose disk to be auto-partitioned:'.format(len(self.devices)))

        self.disk_menu_items = []

        # Fill in the menu items
        for index, device in enumerate(self.devices):
            #if index > 0:
                self.disk_menu_items.append(
                        (
                            '{2} - {1} MB @ {0}'.format(device.path, device.size, device.model), 
                            self.guided_partitions, 
                            index
                        )
                    )

        self.disk_menu = Menu(self.menu_starty,  self.maxx, self.disk_menu_items, self.menu_height)

        self.window.set_action_panel(self.disk_menu)

        return self.window.do_action()



