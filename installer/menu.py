#
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

import curses
from actionresult import ActionResult
from action import Action

class Menu(Action):
    def __init__(self, starty, maxx, items, height=0, selector_menu=False,
                 can_navigate_outside=True, horizontal=False, default_selected=0,
                 save_sel=False, tab_enable=True):
        self.can_navigate_outside = can_navigate_outside
        self.horizontal = horizontal
        self.horizontal_padding = 10
        self.position = default_selected
        self.head_position = 0  #This is the start of showing
        self.items = items
        self.items_strings = []
        self.width = self.lengthen_items()
        self.num_items = len(self.items)
        self.save_sel = save_sel
        self.tab_enable = tab_enable
        if height == 0 or height > self.num_items:
            self.height = self.num_items
        else:
            self.height = height

        # Check if we need to add a scroll bar
        if self.num_items > self.height:
            self.show_scroll = True
            self.width += 2
        else:
            self.show_scroll = False

        # Some calculation to detitmine the size of the scroll filled portion
        self.filled = int(round(self.height * self.height / float(self.num_items)))
        if self.filled == 0:
            self.filled += 1
        for i in [1, 2]:
            if (self.num_items - self.height) >= i and (self.height - self.filled) == (i - 1):
                self.filled -= 1

        # increment the width if it's a selector menu
        self.selector_menu = selector_menu
        if self.selector_menu:
            self.width += 4
            self.selected_items = set([])

        if self.horizontal:
            menu_win_width = (self.width + self.horizontal_padding) * self.num_items
        else:
            menu_win_width = self.width

        self.window = curses.newwin(self.height, menu_win_width)
        self.window.bkgd(' ', curses.color_pair(2))

        self.window.keypad(1)
        self.panel = curses.panel.new_panel(self.window)

        self.panel.move(starty, (maxx - menu_win_width) // 2)
        self.panel.hide()
        curses.panel.update_panels()

    def can_save_sel(self, can_save_sel):
        self.save_sel = can_save_sel

    def lengthen_items(self):
        width = 0
        for item in self.items:
            if len(item[0]) > width:
                width = len(item[0])

        for item in self.items:
            spaces = ''
            for i in range(width - len(item[0])):
                spaces += ' '
            self.items_strings.append(item[0] + spaces)
        return width + 1


    def navigate(self, n):
        self.position += n
        if self.position < 0:
            self.position = 0
        elif self.position >= len(self.items):
            self.position = len(self.items)-1

        if self.position >= self.head_position + self.height:
            self.head_position = self.position - self.height + 1
        if self.position < self.head_position:
            self.head_position = self.position


    def render_scroll_bar(self):
        if self.show_scroll:
            remaining_above = self.head_position
            remaining_down = self.num_items - self.height - self.head_position#

            up = int(round(remaining_above * self.height / float(self.num_items)))
            down = self.height - up - self.filled

            if up == 0 and remaining_above > 0:
                up += 1
                down -= 1
            if down == 0 and remaining_down > 0:
                up -= 1
                down += 1
            if remaining_down == 0 and down != 0:
                up += down
                down = 0


            for index in range(up):
                self.window.addch(index, self.width - 2, curses.ACS_CKBOARD)

            for index in range(self.filled):
                self.window.addstr(index + up, self.width - 2, ' ', curses.A_REVERSE)

            for index in range(down):
                self.window.addch(index + up + self.filled, self.width - 2, curses.ACS_CKBOARD)

    def refresh(self, highligh=True):
        self.window.clear()
        for index, item in enumerate(self.items_strings):
            if index < self.head_position:
                continue
            elif index > self.head_position + self.height - 1:
                continue
            elif index == self.position:
                if highligh:
                    mode = curses.color_pair(3)
                else:
                    mode = curses.color_pair(1)
            else:
                mode = curses.color_pair(2)

            if self.selector_menu:
                if index in self.selected_items:
                    item = '[x] ' + item
                else:
                    item = '[ ] ' + item
            if self.horizontal:
                x = self.horizontal_padding // 2 + index * self.horizontal_padding
                y = 0
            else:
                x = 0
                y = index - self.head_position
            self.window.addstr(y, x, item, mode)

        self.render_scroll_bar()

        self.window.refresh()
        self.panel.top()
        self.panel.show()
        curses.panel.update_panels()
        curses.doupdate()

    def hide(self):
        self.panel.hide()
        curses.panel.update_panels()
        curses.doupdate()

    def do_action(self):
        while True:
            self.refresh()

            key = self.window.getch()

            if key in [curses.KEY_ENTER, ord('\n')]:
                if self.selector_menu:
                    # send the selected indexes
                    result = self.items[self.position][1](self.selected_items)
                else:
                    result = self.items[self.position][1](self.items[self.position][2])
                if result.success:
                    self.hide()
                    return result

            if key in [ord(' ')] and self.selector_menu:
                if self.position in self.selected_items:
                    self.selected_items.remove(self.position)
                else:
                    self.selected_items.add(self.position)
            elif key in [ord('\t')] and self.can_navigate_outside:
                if not self.tab_enable:
                    continue
                self.refresh(False)
                if self.save_sel:
                    return ActionResult(False, {'diskIndex': self.position})
                else:
                    return ActionResult(False, None)

            elif key == curses.KEY_UP or key == curses.KEY_LEFT:
                if not self.tab_enable and key == curses.KEY_LEFT:
                    if self.save_sel:
                        return ActionResult(False, {'diskIndex': self.position, 'direction':-1})
                    elif self.selector_menu:
                        result = self.items[self.position][1](self.selected_items)
                    else:
                        result = self.items[self.position][1](self.items[self.position][2])
                    return ActionResult(False, {'direction': -1})
                self.navigate(-1)

            elif key == curses.KEY_DOWN or key == curses.KEY_RIGHT:
                if not self.tab_enable and key == curses.KEY_RIGHT:
                    if self.save_sel:
                        return ActionResult(False, {'diskIndex': self.position, 'direction':1})
                    else:
                        return ActionResult(False, {'direction': 1})
                self.navigate(1)

            elif key == curses.KEY_NPAGE:
                self.navigate(self.height)

            elif key == curses.KEY_PPAGE:
                self.navigate(-self.height)

            elif key == curses.KEY_HOME:
                self.navigate(-self.position)
