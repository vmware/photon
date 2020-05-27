#
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

import curses
from window import Window
from menu import Menu
from actionresult import ActionResult

class ConfirmWindow(Window):

    def __init__(self, height, width, maxy, maxx, menu_starty, message, info=False):
        if info:
            items = [('OK', self.exit_function, True)]
        else:
            items = [
                ('Yes', self.exit_function, True),
                ('No', self.exit_function, False)
                ]
        self.menu = Menu(menu_starty, maxx, items, can_navigate_outside=False, horizontal=True)
        super(ConfirmWindow, self).__init__(height, width, maxy, maxx, 'Confirm', False, self.menu)
        self.addstr(0, 0, message)

    def exit_function(self, yes):
        return ActionResult(True, {'yes': yes})
