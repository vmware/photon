#! /usr/bin/python2
#
#    Copyright (C) 2015 vmware inc.
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

from device import Device
from window import Window
from actionresult import ActionResult
from menu import Menu
from confirmwindow import ConfirmWindow
import modules.commons
from progressbar import ProgressBar

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
        self.progress_padding = 5
        self.progress_width = self.win_width - self.progress_padding
        self.progress_bar = ProgressBar(self.win_starty + 6, self.win_startx + self.progress_padding / 2, self.progress_width)

        self.window = Window(self.win_height, self.win_width, self.maxy, self.maxx, 'Setup your disk', True)
        self.devices = Device.refresh_devices()

    def guided_partitions(self, device_index):
        menu_height = 9
        menu_width = 40
        menu_starty = (self.maxy - menu_height) / 2 + 5
        confrim_window = ConfirmWindow(menu_height, menu_width, self.maxy, self.maxx, menu_starty, 'This will erase the disk.\nAre you sure?')
        confirmed = confrim_window.do_action().result['yes']

        if not confirmed:
            return ActionResult(confirmed, None)

        self.progress_bar.initialize('Partitioning...')
        self.progress_bar.show()
        self.progress_bar.show_loading('Partitioning')

        # Do the partitioning
        self.window.clearerror()
        partitions_data = modules.commons.partition_disk(self.devices[device_index].path)
        if partitions_data == None:
            self.window.adderror('Partitioning failed, you may try again')
        else:
            self.install_config['disk'] = partitions_data

        self.progress_bar.hide()
        return ActionResult(partitions_data != None, None)

    def display(self, params):
        self.window.addstr(0, 0, 'First, we will setup your disks.\n\nWe have detected {0} disks, choose disk to be auto-partitioned:'.format(len(self.devices)))

        self.disk_menu_items = []

        # Fill in the menu items
        for index, device in enumerate(self.devices):
            #if index > 0:
                self.disk_menu_items.append(
                        (
                            '{2} - {1} @ {0}'.format(device.path, device.size, device.model), 
                            self.guided_partitions, 
                            index
                        )
                    )

        self.disk_menu = Menu(self.menu_starty,  self.maxx, self.disk_menu_items, self.menu_height)

        self.window.set_action_panel(self.disk_menu)
        return self.window.do_action()



