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

class CustomPackageSelector(object):
    def __init__(self,  maxy, maxx, install_config):
        self.install_config = install_config
        self.menu_items = []

        self.maxx = maxx
        self.maxy = maxy
        self.win_width = 60
        self.win_height = 23

        self.win_starty = (self.maxy - self.win_height) / 2
        self.win_startx = (self.maxx - self.win_width) / 2

        self.menu_starty = self.win_starty + 3
        self.selected_packages = Set([])

        self.load_package_list()

        self.window = Window(self.win_height, self.win_width, self.maxy, self.maxx, 'Select your Packages', True, self.package_menu)

    def load_package_list(self):
        json_wrapper_package_list = JsonWrapper("packages_full.json");
        package_list_json = json_wrapper_package_list.read()

        for package in package_list_json["packages"]:
            self.menu_items.append((package, self.exit_function))
        self.package_menu = Menu(self.menu_starty,  self.maxx, self.menu_items, height = 18, selector_menu = True)


    def exit_function(self,  selected_indexes):
        json_wrapper_package_list = JsonWrapper("packages_minimal.json");
        package_list_json = json_wrapper_package_list.read()
        selected_items = []
        for index in selected_indexes:
            selected_items.append(self.menu_items[index][0])

        self.install_config['packages'] = package_list_json["packages"] + selected_items
        return ActionResult(True, None)

    def display(self, params):
        if (params['custom']):
            return self.window.do_action()
        else:
            return ActionResult(True, None)
