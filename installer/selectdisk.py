#
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

from device import Device
from window import Window
from actionresult import ActionResult
from menu import Menu

class SelectDisk(object):
    def __init__(self, maxy, maxx, install_config):
        self.install_config = install_config
        self.menu_items = []

        self.maxx = maxx
        self.maxy = maxy
        self.win_width = 70
        self.win_height = 16

        self.win_starty = (self.maxy - self.win_height) // 2
        self.win_startx = (self.maxx - self.win_width) // 2

        self.menu_starty = self.win_starty + 6
        self.menu_height = 5

        self.disk_buttom_items = []
        self.disk_buttom_items.append(('<Custom>', self.custom_function, False))
        self.disk_buttom_items.append(('<Auto>', self.auto_function, False))

        self.window = Window(self.win_height, self.win_width, self.maxy, self.maxx,
                             'Select a disk', True,
                             items=self.disk_buttom_items, menu_helper=self.save_index,
                             position=2, tab_enabled=False)
        self.devices = Device.refresh_devices()

    def display(self):
        self.window.addstr(0, 0, 'Please select a disk and a method how to partition it:\n' +
                           'Auto - single partition for /, no swap partition.\n' +
                           'Custom - for customized partitioning')

        self.disk_menu_items = []

        # Fill in the menu items
        for index, device in enumerate(self.devices):
            #if index > 0:
            self.disk_menu_items.append(
                (
                    '{2} - {1} @ {0}'.format(device.path, device.size, device.model),
                    self.save_index,
                    index
                ))

        self.disk_menu = Menu(self.menu_starty, self.maxx, self.disk_menu_items,
                              self.menu_height, tab_enable=False)
        self.disk_menu.can_save_sel(True)

        self.window.set_action_panel(self.disk_menu)
        return self.window.do_action()

    def save_index(self, device_index):
        self.install_config['diskindex'] = device_index
        self.install_config['disk'] = self.devices[device_index].path
        return ActionResult(True, None)

    def auto_function(self):    #default is no partition
        self.install_config['autopartition'] = True
        self.install_config['partitionsnumber'] = 0
        return ActionResult(True, None)

    def custom_function(self):  #custom minimize partition number is 1
        self.install_config['autopartition'] = False
        return ActionResult(True, None)
