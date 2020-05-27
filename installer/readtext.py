#
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

import curses
import sys
from actionresult import ActionResult
from action import Action
from confirmwindow import ConfirmWindow

class ReadText(Action):
    def __init__(self, maxy, maxx, textwin, y, install_config, field,
                 confirmation_error_msg, echo_char, accepted_chars, validation_fn,
                 conversion_fn, default_string=None, tab_enabled=True):
        self.textwin = textwin
        self.maxy = maxy
        self.maxx = maxx
        self.y = y
        self.install_config = install_config
        self.field = field
        self.confirmation_error_msg = confirmation_error_msg
        self.echo_char = echo_char
        self.accepted_chars = accepted_chars
        self.validation_fn = validation_fn
        self.conversion_fn = conversion_fn
        self.default_string = default_string
        self.textwin_width = self.textwin.getmaxyx()[1] - 1
        self.visible_text_width = self.textwin_width - 1
        self.tab_enabled = tab_enabled

        self.init_text()
        self.maxlength = 255

        if not tab_enabled:
            self.textwin.keypad(1)

        #initialize the accepted characters
        if accepted_chars:
            self.accepted_chars = accepted_chars
        else:
            self.accepted_chars = range(32, 127)

    def hide(self):
        return

    def init_text(self):
        self.x = 0
        #initialize the ----
        dashes = '_' * self.textwin_width
        self.textwin.addstr(self.y, 0, dashes)
        self.str = ''

        #remove the error messages
        spaces = ' ' * self.textwin_width
        self.textwin.addstr(self.y + 2, 0, spaces)

    def do_action(self, returned=False, go_back=False):
        if returned:
            if len(self.str) > self.visible_text_width:
                text = self.str[-self.visible_text_width:]
            else:
                text = self.str
            if self.echo_char:
                text = self.echo_char * len(text)
            # Add the dashes
            text = text + '_' * (self.visible_text_width - len(self.str))
            self.textwin.addstr(self.y, 0, text)
        if not returned:
            curses.curs_set(1)
            self.init_text()
            if self.default_string != None:
                self.textwin.addstr(self.y, 0, self.default_string)
                self.str = self.default_string

        while True:
            if len(self.str) > self.visible_text_width:
                curs_loc = self.visible_text_width
            else:
                curs_loc = len(self.str)
            ch = self.textwin.getch(self.y, curs_loc)

            update_text = False
            if ch in [curses.KEY_ENTER, ord('\n')]:
                curses.curs_set(0)
                if go_back:
                    return ActionResult(False, {'goBack': True})
                if self.confirmation_error_msg:
                    if self.str != self.install_config[self.field]:
                        conf_message_height = 8
                        conf_message_width = 48
                        conf_message_button_y = (self.maxy - conf_message_height) // 2 + 5
                        confrim_window = ConfirmWindow(conf_message_height, conf_message_width,
                                                       self.maxy,
                                                       self.maxx, conf_message_button_y,
                                                       self.confirmation_error_msg, True)
                        confrim_window.do_action()
                        return ActionResult(False, {'goBack': True})
                    self.set_field()
                else:
                    if not self.validate_input():
                        continue
                    self.set_field()
                curses.curs_set(0)
                return ActionResult(True, None)
            elif ch == curses.KEY_LEFT and not self.tab_enabled:
                return ActionResult(False, {'direction': -1})
            elif ch == curses.KEY_RIGHT and not self.tab_enabled:
                return ActionResult(False, {'direction': 1})
            elif ch in [ord('\t')]:
                curses.curs_set(0)
                return ActionResult(False, None)
            elif ch == curses.KEY_BACKSPACE: #originally ==127
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
                if self.echo_char:
                    text = self.echo_char * len(text)
                # Add the dashes
                text = text + '_' * (self.visible_text_width - len(self.str))
                self.textwin.addstr(self.y, 0, text)

    def set_field(self):
        if self.conversion_fn:
            self.install_config[self.field] = self.conversion_fn(self.str)
        else:
            self.install_config[self.field] = self.str

    def validate_input(self):
        if self.validation_fn:
            success, err = self.validation_fn(self.str)
            if not success:
                spaces = ' ' * self.textwin_width
                self.textwin.addstr(self.y + 2, 0, spaces)
                self.textwin.addstr(self.y + 2, 0, err, curses.color_pair(4))
            return success
        else:
            return True
