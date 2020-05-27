#
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

import curses
import threading
import math
from curses import panel

class ProgressBar(object):
    def __init__(self, starty, startx, width, new_win=False):
        self.timer = None
        self.loadding_timer = None
        self.timer_lock = threading.Lock()
        self.loadding_timer_lock = threading.Lock()

        self.loading_interval = 0.4
        self.loading_chars = ['    ', '.   ', '..  ', '... ', '....']
        self.loading_count = 0

        self.width = width - 1

        self.window = curses.newwin(5, width)
        self.window.bkgd(' ', curses.color_pair(2)) #defaultbackground color
        self.progress = 0

        self.new_win = new_win
        self.x = startx
        self.y = starty

        if new_win:
            self.contentwin = curses.newwin(7, width + 2)
            self.contentwin.bkgd(' ', curses.color_pair(2)) #Default Window color
            self.contentwin.erase()
            self.contentwin.box()
            self.contentpanel = curses.panel.new_panel(self.contentwin)
            self.contentpanel.move(starty-1, startx-1)
            self.contentpanel.hide()


        self.panel = panel.new_panel(self.window)
        self.panel.move(starty, startx)
        self.panel.hide()
        panel.update_panels()

    def initialize(self, init_message):
        self.num_items = 0
        self.message = init_message
        self.time_elapsed = 0
        self.time_remaining = 60
        self.timer = threading.Timer(1, self.update_time)
        self.timer.start()

    def update_num_items(self, num_items):
        self.num_items = num_items

    def update_message(self, message):
        self.message = message
        self.render_message()

    def increment(self, step=1):
        self.progress += step
        self.render_progress()

    def update_time(self):
        with self.timer_lock:
            if self.timer != None:
                self.timer = threading.Timer(1, self.update_time)
                self.timer.start()

        self.time_elapsed += 1
        if self.progress == 0:
            self.time_remaining = 60
        else:
            self.time_remaining = (int(math.ceil(self.time_elapsed *
                                                 self.num_items / float(self.progress))) -
                                   self.time_elapsed)
        self.render_time()

    def render_message(self):
        text = self.message + (' ' * (self.width - len(self.message)))
        self.window.addstr(2, 0, text)
        self.window.refresh()

    def render_progress(self):
        if self.num_items == 0:
            return
        completed = self.progress * 100 // self.num_items
        completed_width = completed * self.width // 100
        completed_str, remaining_str = self.get_spaces(completed_width, self.width, completed)

        self.window.addstr(0, 0, completed_str, curses.color_pair(3))
        self.window.addstr(0, completed_width, remaining_str, curses.color_pair(1))
        self.window.refresh()

    def render_time(self):
        timemessage = 'Elapsed time: {0} secs'.format(self.time_elapsed)
        #timemessage += ', remaining time: {0} secs'.format(self.time_remaining)
        text = timemessage + (' ' * (self.width - len(timemessage)))
        self.window.addstr(4, 0, text)
        self.window.refresh()

    def refresh(self):
        self.window.clear()
        self.render_message()
        self.render_time()
        self.render_progress()

    def show(self):
        if self.new_win:
            self.contentpanel.top()
            self.contentpanel.move(self.y-1, self.x-1)
            self.contentpanel.show()

        self.refresh()
        self.panel.top()
        self.panel.show()
        panel.update_panels()
        curses.doupdate()

    def update_loading_symbol(self):
        with self.loadding_timer_lock:
            if self.loadding_timer != None:
                self.loadding_timer = threading.Timer(self.loading_interval,
                                                      self.update_loading_symbol)
                self.loadding_timer.start()

        self.loading_count += 1
        self.render_loading()

    def render_loading(self):
        self.window.addstr(0, self.message_len + 1,
                           self.loading_chars[self.loading_count % len(self.loading_chars)])
        self.window.refresh()

    def show_loading(self, message):
        self.loadding_timer = threading.Timer(self.loading_interval,
                                              self.update_loading_symbol)
        self.loadding_timer.start()
        self.update_loading_message(message)

    def update_loading_message(self, message):
        self.message_len = len(message)
        spaces = ' ' * self.width
        self.update_message(' ')
        self.window.addstr(0, 0, spaces)
        self.window.addstr(0, 0, message)
        self.render_loading()

    def hide(self):
        with self.timer_lock:
            if self.timer != None:
                self.timer.cancel()
                self.timer = None
        with self.loadding_timer_lock:
            if self.loadding_timer != None:
                self.loadding_timer.cancel()
                self.loadding_timer = None

        if self.new_win:
            self.contentpanel.hide()
        self.panel.hide()
        panel.update_panels()

    def get_spaces(self, completed_width, total_width, per):
        per = str(per) + '%'

        start = (total_width + 2 - len(per)) // 2
        end = start + len(per)

        index = 0

        completed_spaces = ''
        remaining_spaces = ''
        for i in range(completed_width):
            if i in range(start, end):
                completed_spaces += per[index]
                index += 1
            else:
                completed_spaces += ' '

        for i in range(completed_width, total_width):
            if i in range(start, end):
                remaining_spaces += per[index]
                index += 1
            else:
                remaining_spaces += ' '

        return completed_spaces, remaining_spaces
