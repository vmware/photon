#
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

from window import Window
from actionresult import ActionResult
from textpane import TextPane

class License(object):
    def __init__(self, maxy, maxx):
        self.maxx = maxx
        self.maxy = maxy
        self.win_width = maxx - 4
        self.win_height = maxy - 4

        self.win_starty = (self.maxy - self.win_height) // 2
        self.win_startx = (self.maxx - self.win_width) // 2

        self.text_starty = self.win_starty + 4
        self.text_height = self.win_height - 6
        self.text_width = self.win_width - 6

        self.window = Window(self.win_height, self.win_width, self.maxy, self.maxx,
                             'Welcome to the Photon installer', False)

    def display(self, params):
        accept_decline_items = [('<Accept>', self.accept_function),
                                ('<Cancel>', self.exit_function)]

        title = 'VMWARE 3.0 LICENSE AGREEMENT'
        self.window.addstr(0, (self.win_width - len(title)) // 2, title)
        self.text_pane = TextPane(self.text_starty, self.maxx, self.text_width,
                                  "EULA.txt", self.text_height, accept_decline_items)

        self.window.set_action_panel(self.text_pane)

        return self.window.do_action()


    def accept_function(self):
        return ActionResult(True, None)

    def exit_function(self):
        exit(0)
