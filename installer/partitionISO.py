from window import Window 
from windowstringreader import WindowStringReader
from textpane import TextPane
from readmultext import ReadMulText
from actionresult import ActionResult
from device import Device

class PartitionISO(object):
    def __init__(self, maxy, maxx, install_config):
        self.maxx = maxx
        self.maxy = maxy
        self.win_width = maxx - 4
        self.win_height = maxy - 4
        self.install_config = install_config

        self.win_starty = (self.maxy - self.win_height) / 2
        self.win_startx = (self.maxx - self.win_width) / 2

        self.text_starty = self.win_starty + 4
        self.text_height = self.win_height - 6
        self.text_width = self.win_width - 6
        self.install_config['partitionsnumber'] = 0

        self.partition_items = []
        self.partition_items.append(('Disk:'))
        self.partition_items.append(('Size:'))
        self.partition_items.append(('Type:'))
        self.partition_items.append(('Mountpoint:'))
        self.devices = Device.refresh_devices_bytes()

        self.disk_size = []
        for index, device in enumerate(self.devices):
            self.disk_size.append((device.path, int(device.size) / 1048576))     

        self.window = Window(self.win_height, self.win_width, self.maxy, self.maxx, 'Welcome to the Photon installer', False)
        Device.refresh_devices()


    def display(self, params):
        if 'autopartition' in self.install_config and self.install_config['autopartition'] == True:
            return ActionResult(True, None)

        self.disk_buttom_items = []
        self.disk_buttom_items.append(('<Create New>', self.create_function))
        self.disk_buttom_items.append(('<Delete All>', self.delete_function))
        self.disk_buttom_items.append(('<Go Back>', self.go_back))
        self.disk_buttom_items.append(('<Next>', self.next))

        self.text_items = []
        self.text_items.append(('Disk', 20))
        self.text_items.append(('Size', 5))
        self.text_items.append(('Type', 5))
        self.text_items.append(('Mountpoint', 20))
        self.table_space = 5


        title = 'Current partitions:\n'
        self.window.addstr(0, (self.win_width - len(title)) / 2, title)

        self.text_pane = TextPane(self.text_starty, self.maxx, self.text_width, 
            "EULA.txt", self.text_height, self.disk_buttom_items, 
            partition = True, popupWindow = True, install_config = self.install_config, 
            text_items = self.text_items, table_space=self.table_space)

        self.window.set_action_panel(self.text_pane)

        return self.window.do_action()

    def validate_partition(self, pstr):
        if not pstr:
            return ActionResult(False, None)
        sizedata = pstr[1]
        mtdata = pstr[3]
        typedata = pstr[2]
        devicedata = pstr[0]

        #no empty fields unless swap
        if typedata == 'swap' and (len(mtdata)!=0 or len(typedata) == 0 or len(devicedata) == 0):
            return False, "invalid swap data "

        if typedata != 'swap' and (len(sizedata) == 0 or len(mtdata) == 0 or len(typedata) == 0 or len(devicedata) == 0):
            return False, "Input cannot be empty"

        #validate disk: must be one of the existing disks
        valid_disk = False
        i = 0
        for index, device in enumerate(self.disk_size):
            if devicedata == self.disk_size[i][0]:
                valid_disk = True
                break
            i = i+1

        if not valid_disk:
            return False, "invald device path "

        #valid size: must not exceed memory limit
        curr_size = self.disk_size[i][1]
        try:
            int(sizedata)
        except ValueError:
            return False, "invalid device size"

        if int(curr_size) - int(sizedata) <= 0:
            return False, "invalid device size"
        #if valid, update the size and return true
        new_size = (self.disk_size[i][0], int(curr_size)- int(sizedata))
        self.disk_size[i] =new_size
        return True, None

    def create_function(self):

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
                )
        result = self.create_window.do_action()
        if result.success:
            self.install_config['partitionsnumber'] = self.install_config['partitionsnumber'] + 1

        #parse the input in install config
        return self.display(False)

    def delete_function(self):
        for i in range(int(self.install_config['partitionsnumber'])):
            self.install_config[str(i)+'partition_info'+str(0)] = ''
            self.install_config[str(i)+'partition_info'+str(1)] = ''
            self.install_config[str(i)+'partition_info'+str(2)] = ''
            self.install_config[str(i)+'partition_info'+str(3)] = ''

        del self.disk_size[:]
        for index, device in enumerate(self.devices):
            self.disk_size.append((device.path, int(device.size) / 1048576))  

        self.install_config['partitionsnumber'] = 0

        return self.display(False)

    def go_back(self):
        self.window.hide_window()
        self.text_pane.hide()
        return ActionResult(False, {'goBack':True})

    def next(self):
        self.window.hide_window()
        self.text_pane.hide()        
        return ActionResult(True, None)
