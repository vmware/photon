#
#    Copyright (C) 2017 vmware inc.
#
#    Author: Xiaolin Li <xiaolinl@vmware.com>

from menu import Menu
from window import Window
from actionresult import ActionResult
from commandutils import CommandUtils

class LinuxSelector(object):
    def __init__(self, maxy, maxx, install_config):
        self.install_config = install_config
        self.maxx = maxx
        self.maxy = maxy
        self.win_width = 60
        self.win_height = 16

        self.win_starty = (self.maxy - self.win_height) // 2
        self.win_startx = (self.maxx - self.win_width) // 2

        self.menu_starty = self.win_starty + 6

    def set_linux_esx_installation(self, is_linux_esx):
        self.install_config['install_linux_esx'] = is_linux_esx
        return ActionResult(True, None)

    def set_linux_installation(self, selected_linux_package):
        self.install_config['linux_flavor'] = selected_linux_package
        return ActionResult(True, None)

    def create_available_linux_menu(self):
        linux_flavors = {"linux":"Generic", "linux-esx":"VMware hypervisor optimized", "linux-aws":"AWS optimized", "linux-secure":"Security hardened", "linux-rt":"Real Time"}

        self.menu_items = []
        for flavor,menu_entry in linux_flavors.items():
            if flavor in self.install_config['packages']:
                if flavor == "linux-esx" and not CommandUtils.is_vmware_virtualization():
                    continue
                self.menu_items.append((menu_entry, self.set_linux_installation, flavor))

        if len(self.menu_items) == 1:
            self.install_config['linux_flavor'] = self.menu_items[0][2]

        self.host_menu = Menu(self.menu_starty, self.maxx, self.menu_items,
                              default_selected=0, tab_enable=False)

        self.window = Window(self.win_height, self.win_width, self.maxy, self.maxx,
                             'Select Linux kernel to install', True, tab_enabled=False,
                             position=1, can_go_next=True)
        self.window.set_action_panel(self.host_menu)

    def display(self):
        if 'ostree' in self.install_config:
            return ActionResult(None, {"inactive_screen": True})

        self.create_available_linux_menu()
        if len(self.menu_items) < 2:
            return ActionResult(None, {"inactive_screen": True})

        self.window.addstr(0, 0, 'Which type of Linux kernel would you like to install?')
        return self.window.do_action()
