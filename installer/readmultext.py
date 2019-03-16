#
#
#    Author: Yang Yao <yaoyang@vmware.com>

import curses
import sys
from actionresult import ActionResult
from action import Action
from window import Window
from confirmwindow import ConfirmWindow

class ReadMulText(Action):
    def __init__(self, maxy, maxx, y, install_config, field,
                 display_string, confirmation_error_msg,
                 echo_char, accepted_chars, validation_fn, conversion_fn,
                 can_cancel, default_string=None):
        self.maxy = maxy
        self.maxx = maxx
        self.y = y
        self.install_config = install_config
        self.field = field
        self.horizontal_padding = 10
        self.confirmation_error_msg = confirmation_error_msg
        self.echo_char = echo_char
        self.accepted_chars = accepted_chars
        self.validation_fn = validation_fn
        self.conversion_fn = conversion_fn
        self.default_string = default_string
        self.display_string = display_string
        self.textwin_width = maxx - self.horizontal_padding -2
        self.textwin_width = self.textwin_width* 2 // 3
        self.visible_text_width = self.textwin_width - 1
        self.position = 0
        self.height = len(self.display_string) * 4 + 2
        self.menu_pos = 0
        #self.textwin_width)
        self.textwin = curses.newwin(self.height, self.textwin_width + 2)
        self.textwin.bkgd(' ', curses.color_pair(2))
        self.textwin.keypad(1)

        self.shadowwin = curses.newwin(self.height, self.textwin_width + 2)
        self.shadowwin.bkgd(' ', curses.color_pair(0)) #Default shadow color

        self.panel = curses.panel.new_panel(self.textwin)
        self.panel.move((maxy-self.height) // 2, (maxx - self.textwin_width) // 2 -1)
        self.panel.hide()
        self.shadowpanel = curses.panel.new_panel(self.shadowwin)
        self.shadowpanel.move((maxy-self.height) // 2 + 1, (maxx - self.textwin_width) // 2)
        self.shadowpanel.hide()
        curses.panel.update_panels()

        self.init_text()
        self.textwin.box()
        self.maxlength = 255

        #initialize the accepted characters
        if accepted_chars:
            self.accepted_chars = accepted_chars
        else:
            self.accepted_chars = range(32, 127)

    def hide(self):
        return

    def init_text(self):
        self.shadowpanel.show()
        curses.panel.update_panels()

        self.x = 0
        #initialize the ----
        dashes = '_' * self.textwin_width
        cury = self.y + 1
        self.str = []

        for string in self.display_string:
            self.textwin.addstr(cury, 1, string)
            self.textwin.addstr(cury + 1, 1, dashes)
            cury = cury + 4
            self.str.append('')

        #remove the error messages
        spaces = ' ' * self.textwin_width
        #self.textwin.addstr(self.y + 2, 0, spaces)
        self.update_menu()

    def do_action(self):
        self.init_text()
        curses.curs_set(1)

        if self.default_string != None:
            self.textwin.addstr(self.y, 0, self.default_string)
            self.str = self.default_string

        while True:
            if len(self.str[self.position]) > self.visible_text_width:
                curs_loc = self.visible_text_width + 1
            else:
                curs_loc = len(self.str[self.position]) +1
            ch = self.textwin.getch(self.y + 2 + self.position * 4, curs_loc)

            update_text = False
            if ch in [curses.KEY_ENTER, ord('\n')]:
                if self.menu_pos == 1:
                    curses.curs_set(0)
                    self.shadowpanel.hide()
                    return ActionResult(False, None)
                if self.confirmation_error_msg:
                    if self.str != self.install_config[self.field]:
                        curses.curs_set(0)
                        conf_message_height = 8
                        conf_message_width = 48
                        conf_message_button_y = (self.maxy - conf_message_height) // 2 + 5
                        confrim_window = ConfirmWindow(conf_message_height, conf_message_width,
                                                       self.maxy, self.maxx, conf_message_button_y,
                                                       self.confirmation_error_msg, True)
                        confrim_window.do_action()
                        return ActionResult(False, {'goBack': True})
                    self.set_field()
                else:
                    if not self.validate_input():
                        continue
                    self.set_field()
                curses.curs_set(0)
                self.shadowpanel.hide()
                return ActionResult(True, None)
            elif ch == curses.KEY_UP:
                self.refresh(-1)

            elif ch == curses.KEY_DOWN:
                self.refresh(1)

            elif ch in [ord('\t')]:
                self.refresh(1, reset=True)

            elif ch == curses.KEY_LEFT:
                self.menu_refresh(1)

            elif ch == curses.KEY_RIGHT:
                self.menu_refresh(-1)

            elif ch == curses.KEY_BACKSPACE:
                # Handle the backspace case
                self.str[self.position] = self.str[self.position][:len(self.str[self.position]) - 1]
                update_text = True

            elif len(self.str[self.position]) < self.maxlength and ch in self.accepted_chars:
                self.str[self.position] += chr(ch)
                update_text = True

            if update_text:
                self.update_text()

    def menu_refresh(self, n):
        self.menu_pos += n
        if self.menu_pos < 0:
            self.menu_pos = 0
        elif self.menu_pos >= 1:
            self.menu_pos = 1
        self.update_menu()

    def update_menu(self):
        if self.menu_pos == 1:
            self.textwin.addstr(self.height-2, 5, '<Cancel>', curses.color_pair(3))
        else:
            self.textwin.addstr(self.height-2, 5, '<Cancel>')
        if self.menu_pos == 0:
            self.textwin.addstr(self.height-2, self.textwin_width-len('<OK>')-5, '<OK>',
                                curses.color_pair(3))
        else:
            self.textwin.addstr(self.height-2, self.textwin_width-len('<OK>')-5,
                                '<OK>')



    def update_text(self):
        if len(self.str[self.position]) > self.visible_text_width:
            text = self.str[self.position][-self.visible_text_width:]
        else:
            text = self.str[self.position]
        if self.echo_char:
            text = self.echo_char * len(text)

        text = text + '_' * (self.visible_text_width - len(self.str[self.position]))
        self.textwin.addstr(self.y + 2 + self.position * 4, 1, text)

    def refresh(self, n, reset=False):
        self.position += n
        if self.position < 0:
            self.position = 0
        elif self.position >= len(self.display_string):
            if reset:
                self.position = 0
            else:
                self.position = len(self.display_string)-1

    def set_field(self):
        i = 0
        for string in self.display_string:
            if self.conversion_fn:
                self.install_config[self.field+str(i)] = self.conversion_fn(self.str[i])
            else:
                self.install_config[self.field+str(i)] = self.str[i]
            i = i + 1

    def validate_input(self):
        if self.validation_fn:
            success, err = self.validation_fn(self.str)
            if not success:
                spaces = ' ' * (int(self.textwin_width) - len(self.display_string[0]))
                self.textwin.addstr(self.y + 1, len(self.display_string[0]), spaces)
                self.textwin.addstr(self.y + 1, len(self.display_string[0]), err,
                                    curses.color_pair(4))
            return success
        else:
            return True
