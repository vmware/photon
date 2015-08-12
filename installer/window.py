#!/usr/bin/python2
#
#    Copyright (C) 2015 vmware inc.
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

import curses
from actionresult import ActionResult
from action import Action

class Window(Action):

    def __init__(self, height, width, maxy, maxx, title, can_go_back, action_panel = None):
        self.can_go_back = can_go_back
        self.height = height
        self.width = width;
        self.y = (maxy - height) / 2
        self.x = (maxx - width ) / 2
        title = ' ' + title + ' '

        self.contentwin = curses.newwin(height - 1, width -1)
        self.contentwin.bkgd(' ', curses.color_pair(2)) #Default Window color
        self.contentwin.erase()
        self.contentwin.box()
        self.contentwin.addstr(0, (width - 1 - len(title)) / 2 , title)#
        if self.can_go_back:
            self.contentwin.addstr(height - 3, 5, '<Go Back>')

        self.textwin = curses.newwin(height - 5, width - 5)
        self.textwin.bkgd(' ', curses.color_pair(2)) #Default Window color

        self.shadowwin = curses.newwin(height - 1, width - 1)
        self.shadowwin.bkgd(' ', curses.color_pair(0)) #Default shadow color

        self.contentpanel = curses.panel.new_panel(self.contentwin)
        self.textpanel = curses.panel.new_panel(self.textwin)
        self.shadowpanel = curses.panel.new_panel(self.shadowwin)

        self.action_panel = action_panel

        self.hide_window()

    def set_action_panel(self, action_panel):
        self.action_panel = action_panel

    def do_action(self):
        self.show_window()
        action_result = self.action_panel.do_action()

        if action_result.success:
            self.hide_window()
            return action_result
        else:
            if (action_result.result != None and 'goBack' in action_result.result and action_result.result['goBack']):
                self.hide_window()
                self.action_panel.hide()
                return action_result
            else:
                #highlight the GoBack and keep going
                self.contentwin.addstr(self.height - 3, 5, '<Go Back>', curses.color_pair(3))
                self.contentwin.refresh()

        while action_result.success == False:
            key = self.contentwin.getch()
            if key in [curses.KEY_ENTER, ord('\n')]:
                #remove highlight from Go Back
                self.contentwin.addstr(self.height - 3, 5, '<Go Back>')
                self.contentwin.refresh()
                self.hide_window()
                self.action_panel.hide()
                return ActionResult(False, None)
            elif key in [ord('\t')]:
                #remove highlight from Go Back
                self.contentwin.addstr(self.height - 3, 5, '<Go Back>')
                self.contentwin.refresh()
                # go do the action inside the panel
                action_result = self.action_panel.do_action()
                if action_result.success:
                    self.hide_window()
                    return action_result
                else:
                    #highlight the GoBack and keep going
                    self.contentwin.addstr(self.height - 3, 5, '<Go Back>', curses.color_pair(3))
                    self.contentwin.refresh()

    def show_window(self):
        y = self.y
        x = self.x
        self.shadowpanel.top()
        self.contentpanel.top()
        self.textpanel.top()

        self.shadowpanel.move(y + 1, x + 1)
        self.contentpanel.move(y, x)
        self.textpanel.move(y + 2, x + 2)

        self.shadowpanel.show()
        self.contentpanel.show()
        self.textpanel.show()

        curses.panel.update_panels()
        curses.doupdate()

    def hide_window(self):
        self.shadowpanel.hide()
        self.contentpanel.hide()
        self.textpanel.hide()
        curses.panel.update_panels()
        curses.doupdate()

    def addstr(self, y, x, str, mode = 0):
        self.textwin.addstr(y, x, str, mode)

    def adderror(self, str):
        self.textwin.addstr(self.height - 7, 0, str, curses.color_pair(4))
        self.textwin.refresh()

    def clearerror(self):
        spaces = ' ' * (self.width - 6)
        self.textwin.addstr(self.height - 7, 0, spaces)
        self.textwin.refresh()

    def content_window(self):
        return self.textwin

