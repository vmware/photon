#! /usr/bin/python2
#
#    Copyright (C) 2015 vmware inc.
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

import subprocess
import os
import json
from device import Device
from menu import Menu
from window import Window
from actionresult import ActionResult

class DiskPartitioner(object):
    def __init__(self,  maxy, maxx):
        self.menu_items = []

        self.maxx = maxx
        self.maxy = maxy
        self.win_width = 70
        self.win_height = 17

        self.win_starty = (self.maxy - self.win_height) / 2
        self.win_startx = (self.maxx - self.win_width) / 2

        self.menu_starty = self.win_starty + 10

        # initialize the devices
        self.devices = Device.refresh_devices()

        self.items =   [
                            ('Auto-partitioning - use entire disk',  self.guided_partitions, None),
                            ('Manual - not implemented!',  self.manual_partitions, None),
                        ]
        self.menu = Menu(self.menu_starty,  self.maxx, self.items)

        self.window = Window(self.win_height, self.win_width, self.maxy, self.maxx, 'Welcome to the Photon installer', True, self.menu)
        self.window.addstr(0, 0, 'First, we will setup your disks. \n\nYou can: \n\na) use auto-partitioning or\nb) you can do it manually.')

    def guided_partitions(self, params):
        return ActionResult(True, {'guided': True, 'devices': self.devices})

    def manual_partitions(self, params):
        raise NameError('Manual partitioning not implemented')

    def display(self, params):
        return self.window.do_action()



