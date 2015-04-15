#!/usr/bin/python2
#
#    Copyright (C) 2015 vmware inc.
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

import json
import curses
from sets import Set
from jsonwrapper import JsonWrapper
from menu import Menu
from window import Window
from actionresult import ActionResult

class PackageSelector(object):
    def __init__(self,  maxy, maxx, install_config):
        self.install_config = install_config
        self.maxx = maxx
        self.maxy = maxy
        self.win_width = 50
        self.win_height = 10

        self.win_starty = (self.maxy - self.win_height) / 2
        self.win_startx = (self.maxx - self.win_width) / 2

        self.menu_starty = self.win_starty + 3

        self.load_package_list()

        self.window = Window(self.win_height, self.win_width, self.maxy, self.maxx, 'Select Installation', True, self.package_menu)

    def load_package_list(self):
        json_wrapper_package_list = JsonWrapper("package_list.json");
        self.package_list_json = json_wrapper_package_list.read()

        self.package_menu_items =   [
                                        ('1. Photon OS (Micro)', self.exit_function, ['micro', self.package_list_json["micro_packages"]]),
                                        ('2. Photon Container OS (Minimal)', self.exit_function, ['minimal', self.package_list_json["minimal_packages"]]),
                                        ('3. Photon Full OS (All)', self.exit_function, ['full', self.package_list_json["minimal_packages"] + self.package_list_json["optional_packages"]]),
                                        ('4. Photon Custom OS', self.custom_packages, ['custom', None])
                                    ]
        self.package_menu = Menu(self.menu_starty,  self.maxx, self.package_menu_items)

    def exit_function(self,  selected_item_params):
        self.install_config['type'] = selected_item_params[0];
        self.install_config['packages'] = selected_item_params[1];
        return ActionResult(True, {'custom': False})

    def custom_packages(self, params):
        return ActionResult(True, {'custom': True})

    def display(self, params):
        return self.window.do_action()
