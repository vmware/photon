#! /usr/bin/python2
#
#    Copyright (C) 2015 vmware inc.
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

import curses
import crypt
import string
import random
import cracklib
import sys
from actionresult import ActionResult
from action import Action
from confirmwindow import ConfirmWindow

class ReadText(Action):
    def __init__(self, maxy, maxx, textwin, y, install_config, field, confirm_pass, default_string = None):
        self.textwin = textwin
        self.maxy = maxy
        self.maxx = maxx
        self.y = y
        self.install_config = install_config
        self.field = field
        self.confirm_pass = confirm_pass;
        self.default_string = default_string
        self.textwin_width = self.textwin.getmaxyx()[1] - 1
        self.visible_text_width = self.textwin_width - 1

        self.init_text()
        self.maxlength = 255

        #initialize the accepted characters
        if self.field == "password":
            # Adding all the letters
            self.accepted_chars = range(33, 127)
        elif self.field == "hostname":

            self.alpha_chars = range(65, 91)
            self.alpha_chars.extend(range(97,123))
            
            self.accepted_chars = list(self.alpha_chars)
            # Adding the numeric chars
            self.accepted_chars.extend(range(48, 58))
            # Adding the . and -
            self.accepted_chars.extend([ord('.'), ord('-')])
        else:
            self.accepted_chars = range(33, 127)

    def hide(self):
        return
    
    def init_text(self):
        self.x = 0;
        #initialize the ----
        dashes = '_' * self.textwin_width
        self.textwin.addstr(self.y, 0, dashes)
        self.str = ''

        #remove the error messages
        spaces = ' ' * self.textwin_width
        self.textwin.addstr(self.y + 2, 0, spaces)

    def do_action(self):
        self.init_text()
        curses.curs_set(1)

        if self.default_string != None:
            self.textwin.addstr(self.y, 0, self.default_string)
            self.str = self.default_string

        while True:
            if len(self.str) > self.visible_text_width:
                curs_loc = self.visible_text_width
            else:
                curs_loc = len(self.str)
            ch = self.textwin.getch(self.y, curs_loc)

            if ch in [curses.KEY_ENTER, ord('\n')]:
                if self.confirm_pass:
                    if self.str != self.install_config['password']:
                        curses.curs_set(0)
                        conf_message_height = 8
                        conf_message_width = 40
                        conf_message_button_y = (self.maxy - conf_message_height) / 2 + 5
                        confrim_window = ConfirmWindow(conf_message_height, conf_message_width, self.maxy, self.maxx, conf_message_button_y, "passwords don't match, please try again.", True)
                        confrim_window.do_action()
                        return ActionResult(False, {'goBack': True})
                    self.install_config['password'] = self.generate_password_hash(self.str)
                elif self.field == "password":
                    err = self.validate_password(self.str)
                    if err != self.str:
                        self.init_text()
                        self.textwin.addstr(self.y + 2, 0, "Error: " + err, curses.color_pair(4))
                        continue
                    self.install_config['password'] = self.str;
                elif self.field == "hostname":
                    if not self.validate_hostname(self.str):
                        self.textwin.addstr(self.y + 2, 0, "It should start with alpha char and ends with alpha-numeric char", curses.color_pair(4))
                        continue
                    self.install_config['hostname'] = self.str
                else:
                    self.install_config[self.field] = self.str
                    return ActionResult(True, self.str)
                curses.curs_set(0)
                return ActionResult(True, None)
            elif ch in [ord('\t')]:
                curses.curs_set(0)
                return ActionResult(False, None)
            elif ch == 127:
                # Handle the backspace case
                self.str = self.str[:len(self.str) - 1]

                update_text = True

            elif len(self.str) < self.maxlength and ch in self.accepted_chars:
                self.str += chr(ch)
                update_text = True

            if update_text:
                if len(self.str) > self.visible_text_width:
                    text = self.str[-self.visible_text_width:]
                else:
                    text = self.str
                if self.field == "password":
                    text = '*' * len(text)
                # Add the dashes
                text = text + '_' * (self.visible_text_width - len(self.str))
                self.textwin.addstr(self.y, 0, text)

    def validate_hostname(self, hostname):
        if (hostname == None or len(hostname) == 0):
            return False;
        return (ord(hostname[0]) in self.alpha_chars) and (hostname[-1] not in ['.', '-'])

    def validate_password(self, text):
        try:
            p = cracklib.VeryFascistCheck(text)
        except ValueError, message:
            p = str(message)
        return p

    def generate_password_hash(self,  password):
        shadow_password = crypt.crypt(password, "$6$" + "".join([random.choice(string.ascii_letters + string.digits) for _ in range(16)]))
        return shadow_password
