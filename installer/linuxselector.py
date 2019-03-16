#
#    Copyright (C) 2017 vmware inc.
#
#    Author: Xiaolin Li <xiaolinl@vmware.com>

from menu import Menu
from window import Window
from actionresult import ActionResult

class LinuxSelector(object):
    def __init__(self, maxy, maxx, install_config):
        self.install_config = install_config
        self.maxx = maxx
        self.maxy = maxy
        self.win_width = 60
        self.win_height = 13

        self.win_starty = (self.maxy - self.win_height) // 2
        self.win_startx = (self.maxx - self.win_width) // 2

        self.menu_starty = self.win_starty + 6

        self.menu_items = []
        self.menu_items.append(("1. VMware hypervisor optimized", self.set_linux_esx_installation, True))
        self.menu_items.append(("2. Generic", self.set_linux_esx_installation, False))

        self.host_menu = Menu(self.menu_starty, self.maxx, self.menu_items,
                              default_selected=0, tab_enable=False)

        self.window = Window(self.win_height, self.win_width, self.maxy, self.maxx,
                             'Select Linux kernel to install', True, tab_enabled=False,
                             position=1, can_go_next=True)
        self.window.set_action_panel(self.host_menu)

    def set_linux_esx_installation(self, is_linux_esx):
        self.install_config['install_linux_esx'] = is_linux_esx
        return ActionResult(True, None)

    def display(self, params):
        self.window.addstr(0, 0, 'The installer has detected that you are installing')
        self.window.addstr(1, 0, 'Photon OS on a VMware hypervisor.')
        self.window.addstr(2, 0, 'Which type of Linux kernel would you like to install?')
        return self.window.do_action()
