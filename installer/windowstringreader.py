#
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

from window import Window
from readtext import ReadText

class WindowStringReader(object):
    def __init__(self, maxy, maxx, height, width, field, confirmation_err_msg,
                 echo_char, accepted_chars, validation_fn, conversion_fn, title,
                 display_string, inputy, install_config, default_string=None,
                 tab_enabled=False):
        self.title = title
        self.display_string = display_string
        self.install_config = install_config
        self.inputy = inputy

        self.width = width
        self.height = height
        self.maxx = maxx
        self.maxy = maxy

        self.startx = (self.maxx - self.width) // 2
        self.starty = (self.maxy - self.height) // 2
        self.tab_enabled = False
        self.can_go_next = True

        self.window = Window(self.height, self.width, self.maxy, self.maxx, self.title,
                             True, tab_enabled=self.tab_enabled,
                             position=1, can_go_next=self.can_go_next, read_text=self.can_go_next)
        self.read_text = ReadText(maxy, maxx, self.window.content_window(), self.inputy,
                                  install_config,
                                  field, confirmation_err_msg, echo_char, accepted_chars,
                                  validation_fn,
                                  conversion_fn, default_string, tab_enabled=self.tab_enabled)
        self.window.set_action_panel(self.read_text)
        self.window.addstr(0, 0, self.display_string)

    def get_user_string(self, params):
        return self.window.do_action()
