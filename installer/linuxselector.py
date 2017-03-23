#!/usr/bin/python2
#
#    Copyright (C) 2015 vmware inc.
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

import json
import os
import curses
from sets import Set
from jsonwrapper import JsonWrapper
from menu import Menu
from window import Window
from actionresult import ActionResult

class LinuxSelector(object):
    def __init__(self,  maxy, maxx, install_config):
        self.install_config = install_config
        self.maxx = maxx
        self.maxy = maxy
        self.win_width = 50
        self.win_height = 13

        self.win_starty = (self.maxy - self.win_height) / 2
        self.win_startx = (self.maxx - self.win_width) / 2

        self.menu_starty = self.win_starty + 3

        menu_items = []
        menu_items.append(("Linux generic", self.set_linux_esx_installation, False))
        menu_items.append(("Linux esx", self.set_linux_esx_installation, True))

        host_menu = Menu(self.menu_starty, self.maxx, menu_items, default_selected = 0, tab_enable=False)

        self.window = Window(self.win_height, self.win_width, self.maxy, self.maxx,
                             'Select Linux', True, items=[], tab_enabled = False,
                             position = 1, can_go_next=True)
        self.window.set_action_panel(host_menu)

    def set_linux_esx_installation(self, is_linux_esx):
        self.install_config['install_linux_esx'] = is_linux_esx
        return ActionResult(True, None)

    def display(self, params):
        if (self.install_config['type'] == 'ostree_host' or
            self.install_config['type'] == 'ostree_server'):
            return ActionResult(True, None)
        return self.window.do_action()

