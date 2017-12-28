from window import Window
from windowstringreader import WindowStringReader
from textpane import TextPane
from readmultext import ReadMulText
from confirmwindow import ConfirmWindow
from actionresult import ActionResult
from device import Device

class PartitionISO(object):
    def __init__(self, maxy, maxx, install_config):
        self.maxx = maxx
        self.maxy = maxy
        self.win_width = maxx - 4
        self.win_height = maxy - 4
        self.install_config = install_config
        self.path_checker = []

        self.win_starty = (self.maxy - self.win_height) // 2
        self.win_startx = (self.maxx - self.win_width) // 2

        self.text_starty = self.win_starty + 4
        self.text_height = self.win_height - 6
        self.text_width = self.win_width - 6
        self.install_config['partitionsnumber'] = 0
        self.devices = Device.refresh_devices_bytes()
        self.has_slash = False
        self.has_remain = False
        self.has_empty = False

        self.disk_size = []
        for index, device in enumerate(self.devices):
            self.disk_size.append((device.path, int(device.size) / 1048576))

        self.window = Window(self.win_height, self.win_width, self.maxy, self.maxx,
                             'Welcome to the Photon installer', False, can_go_next=False)
        Device.refresh_devices()

    def display(self, params):
        if 'skipPrevs' in self.install_config and self.install_config['skipPrevs'] == True:
            self.delete()
            return ActionResult(False, {'goBack':True})
        if 'autopartition' in self.install_config and self.install_config['autopartition'] == True:
            return ActionResult(True, None)
        if ('delete_partition' in self.install_config and
                self.install_config['delete_partition'] == True):
            self.delete()
            self.install_config['delete_partition'] = False

        self.device_index = self.install_config['diskindex']

        self.disk_buttom_items = []
        self.disk_buttom_items.append(('<Next>', self.next))
        self.disk_buttom_items.append(('<Create New>', self.create_function))
        self.disk_buttom_items.append(('<Delete All>', self.delete_function))
        self.disk_buttom_items.append(('<Go Back>', self.go_back))

        self.text_items = []
        self.text_items.append(('Disk', 20))
        self.text_items.append(('Size', 5))
        self.text_items.append(('Type', 5))
        self.text_items.append(('Mountpoint', 20))
        self.table_space = 5

        title = 'Current partitions:\n'
        self.window.addstr(0, (self.win_width - len(title)) // 2, title)

        info = ("Unpartitioned space: " +
                str(self.disk_size[self.device_index][1])+
                " MB, Total size: "+
                str(int(self.devices[self.device_index].size)/ 1048576) + " MB")

        self.text_pane = TextPane(self.text_starty, self.maxx, self.text_width,
                                  "EULA.txt", self.text_height, self.disk_buttom_items,
                                  partition=True, popupWindow=True,
                                  install_config=self.install_config,
                                  text_items=self.text_items, table_space=self.table_space,
                                  default_start=1, info=info,
                                  size_left=str(self.disk_size[self.device_index][1]))

        self.window.set_action_panel(self.text_pane)

        return self.window.do_action()

    def validate_partition(self, pstr):
        if not pstr:
            return ActionResult(False, None)
        sizedata = pstr[0]
        mtdata = pstr[2]
        typedata = pstr[1]
        devicedata = self.devices[self.device_index].path

        #no empty fields unless swap
        if (typedata == 'swap' and
                (len(mtdata) != 0 or len(typedata) == 0 or len(devicedata) == 0)):
            return False, "invalid swap data "

        if (typedata != 'swap' and
                (len(sizedata) == 0 or
                 len(mtdata) == 0 or
                 len(typedata) == 0 or
                 len(devicedata) == 0)):
            if not self.has_empty and mtdata and typedata and devicedata:
                self.has_empty = True
            else:
                return False, "Input cannot be empty"

        if typedata != 'swap' and typedata != 'ext3' and typedata != 'ext4':
            return False, "Invalid type"

        if len(mtdata) != 0 and mtdata[0] != '/':
            return False, "Invalid path"

        if mtdata in self.path_checker:
            return False, "Path already existed"
        #validate disk: must be one of the existing disks
        i = self.device_index

        #valid size: must not exceed memory limit
        curr_size = self.disk_size[i][1]
        if len(sizedata) != 0:
            try:
                int(sizedata)
            except ValueError:
                return False, "invalid device size"

            if int(curr_size) - int(sizedata) < 0:
                return False, "invalid device size"
            #if valid, update the size and return true
            new_size = (self.disk_size[i][0], int(curr_size)- int(sizedata))
            self.disk_size[i] = new_size

        if mtdata == "/":
            self.has_slash = True

        self.path_checker.append(mtdata)
        return True, None

    def create_function(self):
        self.window.hide_window()

        self.install_config['partition_disk'] = self.devices[self.device_index].path
        self.partition_items = []
        self.partition_items.append(('Size in MB: ' +
                                     str(self.disk_size[self.device_index][1]) +
                                     ' available'))
        self.partition_items.append(('Type: (ext3, ext4, swap)'))
        self.partition_items.append(('Mountpoint:'))
        self.create_window = ReadMulText(
            self.maxy, self.maxx, 0,
            self.install_config,
            str(self.install_config['partitionsnumber']) + 'partition_info',
            self.partition_items,
            None,
            None,
            None,
            self.validate_partition,   #validation function of the input
            None,
            True,
            )
        result = self.create_window.do_action()
        if result.success:
            self.install_config['partitionsnumber'] = self.install_config['partitionsnumber'] + 1

        #parse the input in install config
        return self.display(False)

    def delete_function(self):
        self.delete()
        return self.display(False)

    def go_back(self):
        self.delete()
        self.window.hide_window()
        self.text_pane.hide()
        return ActionResult(False, {'goBack':True})

    def next(self):
        if self.install_config['partitionsnumber'] == 0:
            window_height = 9
            window_width = 40
            window_starty = (self.maxy-window_height) // 2 + 5
            confirm_window = ConfirmWindow(window_height, window_width, self.maxy,
                                           self.maxx, window_starty,
                                           'Partition information cannot be empty',
                                           info=True)
            confirm_window.do_action()
            return self.display(False)
        #must have /
        if not self.has_slash:
            window_height = 9
            window_width = 40
            window_starty = (self.maxy - window_height) // 2 + 5
            confirm_window = ConfirmWindow(window_height, window_width, self.maxy,
                                           self.maxx, window_starty, 'Missing /',
                                           info=True)
            confirm_window.do_action()
            return self.display(False)

        self.window.hide_window()
        self.text_pane.hide()
        return ActionResult(True, {'goNext':True})

    def delete(self):
        for i in range(int(self.install_config['partitionsnumber'])):
            self.install_config[str(i)+'partition_info'+str(0)] = ''
            self.install_config[str(i)+'partition_info'+str(1)] = ''
            self.install_config[str(i)+'partition_info'+str(2)] = ''
            self.install_config[str(i)+'partition_info'+str(3)] = ''
        del self.disk_size[:]
        for index, device in enumerate(self.devices):
            self.disk_size.append((device.path, int(device.size) / 1048576))
        del self.path_checker[:]
        self.has_slash = False
        self.has_remain = False
        self.has_empty = False
        self.install_config['partitionsnumber'] = 0
