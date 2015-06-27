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
        json_wrapper_option_list = JsonWrapper("install_options.json")
        option_list_json = json_wrapper_option_list.read()
        options_sorted = sorted(option_list_json.items(), key=lambda item: item[1]['order'])

        self.package_menu_items = []

        for install_option in options_sorted:
            if install_option[1]["visible"] == True:
                json_wrapper_package_list = JsonWrapper(install_option[1]["file"])
                package_list_json = json_wrapper_package_list.read()
                self.package_menu_items.append((install_option[1]["title"], self.exit_function, [install_option[1]["type"], package_list_json["packages"]] ))

        self.package_menu = Menu(self.menu_starty,  self.maxx, self.package_menu_items)

    def exit_function(self,  selected_item_params):
        self.install_config['type'] = selected_item_params[0];
        self.install_config['packages'] = selected_item_params[1];
        return ActionResult(True, {'custom': False})

    def custom_packages(self, params):
        return ActionResult(True, {'custom': True})

    def display(self, params):
        return self.window.do_action()
