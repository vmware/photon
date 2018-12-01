#
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

from device import Device
from window import Window
from actionresult import ActionResult
from menu import Menu
from confirmwindow import ConfirmWindow
import modules.commons
from progressbar import ProgressBar
import subprocess

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
        self.progress_padding = 5
        self.progress_width = self.win_width - self.progress_padding
        self.progress_bar = ProgressBar(self.win_starty + 6,
                                        self.win_startx + (self.progress_padding // 2),
                                        self.progress_width, new_win=True)

        self.disk_buttom_items = []
        self.disk_buttom_items.append(('<Custom>', self.custom_function, False))
        self.disk_buttom_items.append(('<Auto>', self.auto_function, False))

        self.window = Window(self.win_height, self.win_width, self.maxy, self.maxx,
                             'Select a disk', True,
                             items=self.disk_buttom_items, menu_helper=self.save_index,
                             position=2, tab_enabled=False)
        self.partition_window = Window(self.win_height, self.win_width, self.maxy,
                                       self.maxx, 'Partition', True)
        self.devices = Device.refresh_devices()

    def guided_partitions(self, params):
        if not 'diskindex' in self.install_config:
            return ActionResult(False, None)

        device_index = self.install_config['diskindex']

        menu_height = 9
        menu_width = 40
        menu_starty = (self.maxy - menu_height) // 2 + 5
        self.install_config['delete_partition'] = True
        confrim_window = ConfirmWindow(menu_height, menu_width, self.maxy,
                                       self.maxx, menu_starty,
                                       'This will erase the disk.\nAre you sure?')
        confirmed = confrim_window.do_action().result['yes']

        if confirmed == False:
            self.install_config['skipPrevs'] = True
            return ActionResult(False, {'goBack':True})

        self.install_config['skipPrevs'] = False
        self.progress_bar.initialize('Partitioning...')
        self.progress_bar.show()
        self.progress_bar.show_loading('Partitioning')

        # Do the partitioning
        if 'partitionsnumber' in self.install_config:
            if int(self.install_config['partitionsnumber']) == 0:
                partitions_data = modules.commons.partition_disk(
                    self.devices[device_index].path, modules.commons.default_partitions)
            else:
                partitions = []
                for i in range(int(self.install_config['partitionsnumber'])):
                    if len(self.install_config[str(i)+'partition_info'+str(0)]) == 0:
                        sizedata = 0
                    else:
                        sizedata = int(self.install_config[str(i) + 'partition_info' + str(0)])
                    mtdata = self.install_config[str(i) + 'partition_info' + str(2)]
                    typedata = self.install_config[str(i) + 'partition_info'+str(1)]

                    partitions = partitions + [{"mountpoint": mtdata,
                                                "size": sizedata,
                                                "filesystem": typedata},]
                partitions_data = modules.commons.partition_disk(
                    self.devices[device_index].path, partitions)
        else:
            partitions_data = modules.commons.partition_disk(
                self.devices[device_index].path, modules.commons.default_partitions)

        if partitions_data == None:
            self.partition_window.adderror('Partitioning failed, you may try again')
        else:
            self.install_config['disk'] = partitions_data
            arch = subprocess.check_output(['uname', '-m'], universal_newlines=True)
            if "x86" in arch:
                self.install_config['boot'] = 'dualboot'
            else:
                self.install_config['boot'] = 'efi'

        self.progress_bar.hide()
        return ActionResult(partitions_data != None, None)

    def display(self, params):
        if 'skipPrevs' in self.install_config:
            self.install_config['skipPrevs'] = False
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
        return ActionResult(True, None)

    def auto_function(self, params):    #default is no partition
        self.install_config['autopartition'] = True
        self.install_config['partitionsnumber'] = 0
        return ActionResult(True, None)

    def custom_function(self, params):  #custom minimize partition number is 1
        self.install_config['autopartition'] = False
        return ActionResult(True, None)
