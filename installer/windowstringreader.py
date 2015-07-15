#!/usr/bin/python2
#
#    Copyright (C) 2015 vmware inc.
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

import curses
from window import Window
from readtext import ReadText

class WindowStringReader(object):
    def __init__(self, maxy, maxx, height, width, ispassword, confirm_password, title, display_string, inputy, install_config):
        self.title = title
        self.display_string = display_string
        self.inputy = inputy

        self.width = width
        self.height = height
        self.maxx = maxx
        self.maxy = maxy

        self.startx = (self.maxx - self.width) / 2
        self.starty = (self.maxy - self.height) / 2

        self.window = Window(self.height, self.width, self.maxy, self.maxx, self.title, True)
        self.read_text = ReadText(maxy, maxx, self.window.content_window(), self.inputy, install_config, ispassword, confirm_password)
        self.window.set_action_panel(self.read_text)
        self.window.addstr(0, 0, self.display_string)

    def get_user_string(self, params):
        return self.window.do_action()
