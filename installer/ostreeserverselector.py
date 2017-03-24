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

class OSTreeServerSelector(object):
    def __init__(self,  maxy, maxx, install_config):

        self.install_config = install_config
        self.maxx = maxx
        self.maxy = maxy
        self.win_width = 50
        self.win_height = 13

        self.win_starty = (self.maxy - self.win_height) / 2
        self.win_startx = (self.maxx - self.win_width) / 2

        self.menu_starty = self.win_starty + 3

        self.menu_items = []
        self.menu_items.append(("Default RPM-OSTree Server", self.set_default_repo_installation, True))
        self.menu_items.append(("Custom RPM-OSTree Server", self.set_default_repo_installation, False))

        self.host_menu = Menu(self.menu_starty, self.maxx, self.menu_items,
                              default_selected = 0, tab_enable=False)

        self.window = Window(self.win_height, self.win_width, self.maxy, self.maxx,
                             'Select OSTree Server', True, items=[], tab_enabled = False,
                             position = 1, can_go_next=True)
        self.window.set_action_panel(self.host_menu)

    def set_default_repo_installation(self,  is_default_repo ):
        self.install_config['default_repo'] = is_default_repo
        return ActionResult(True, None)

    def display(self, params):
        if self.install_config['type'] == 'ostree_host':
            return self.window.do_action()
        return ActionResult(True, None)
