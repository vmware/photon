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
from actionresult import ActionResult
from action import Action

class ReadText(Action):
    def __init__(self, textwin, y, install_config, ispassword):
        self.textwin = textwin
        self.y = y
        self.install_config = install_config
        self.ispassword = ispassword
        self.x = 0

        #initialize the ----
        dashes = '_' * (self.textwin.getmaxyx()[1] - 1)
        self.textwin.addstr(self.y, 0, dashes)
        self.str = ''

        #initialize the accepted characters
        if self.ispassword:
            self.maxlength = self.textwin.getmaxyx()[1] - 2
            # Adding all the letters
            self.accepted_chars = range(33, 127)
        else:
            self.maxlength = 255

            self.alpha_chars = range(65, 91)
            self.alpha_chars.extend(range(97,123))

            self.accepted_chars = list(self.alpha_chars)
            # Adding the numeric chars
            self.accepted_chars.extend(range(48, 58))
            # Adding the . and -
            self.accepted_chars.extend([ord('.'), ord('-')])


    def hide(self):
        return

    def do_action(self):
        curses.curs_set(1)

        while True:
            ch = self.textwin.getch(self.y, self.x)

            if ch in [curses.KEY_ENTER, ord('\n')]:
                if self.ispassword:
                    err = self.validate_password(self.str)
                    if err != self.str:
                        spaces = ' ' * (self.textwin.getmaxyx()[1] - 1)
                        self.textwin.addstr(self.y + 2, 0, spaces)
                        self.textwin.addstr(self.y + 2, 0, "Error: " + err, curses.color_pair(4))
                        continue
                    self.install_config['password'] = self.generate_password_hash(self.str);
                else:
                    if not self.validate_hostname(self.str):
                        self.textwin.addstr(self.y + 2, 0, "It should start with alpha char and ends with alpha-numeric char", curses.color_pair(4))
                        continue
                    self.install_config['hostname'] = self.str
                curses.curs_set(0)
                return ActionResult(True, None)
            elif ch in [ord('\t')]:
                curses.curs_set(0)
                return ActionResult(False, None)
            elif ch == 127:
                # Handle the backspace case
                self.x -= 1
                if self.x < 0:
                    self.x = 0
                self.textwin.addch(self.y, self.x, ord('_'))
                self.str = self.str[:len(self.str) - 1]
            elif self.x < self.maxlength and ch in self.accepted_chars:
                if (self.ispassword):
                    self.textwin.echochar(ord('*'))
                else:
                    self.textwin.echochar(ch)
                self.str += chr(ch)
                self.x += 1

    def validate_hostname(self, hostname):
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
