#
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

import curses
from actionresult import ActionResult
from action import Action

class Window(Action):

    def __init__(self, height, width, maxy, maxx, title, can_go_back,
                 action_panel=None, items=None, menu_helper=None, position=0,
                 tab_enabled=True, can_go_next=False, read_text=False):
        self.can_go_back = can_go_back
        self.can_go_next = can_go_next
        self.height = height
        self.width = width
        self.y = (maxy - height) // 2
        self.x = (maxx - width) // 2
        title = ' ' + title + ' '

        self.contentwin = curses.newwin(height - 1, width -1)
        self.contentwin.bkgd(' ', curses.color_pair(2)) #Default Window color
        self.contentwin.erase()
        self.contentwin.box()
        self.tab_enabled = tab_enabled
        self.read_text = read_text

        self.position = position
        if items:
            self.items = items
        else:
            self.items = []
        self.menu_helper = menu_helper
        self.contentwin.addstr(0, (width - 1 - len(title)) // 2, title)#
        newy = 5

        if self.can_go_back:
            self.contentwin.addstr(height - 3, 5, '<Go Back>')
        if self.can_go_next and self.can_go_back:
            self.update_next_item()

        self.dist = 0

        if len(self.items) > 0:
        #To select items, we need to identify up left right keys

            self.dist = self.width-11
            self.dist -= len('<Go Back>')
            count = 0
            for item in self.items:
                self.dist -= len(item[0])
                count += 1
            self.dist = self.dist // count
            self.contentwin.keypad(1)
            newy += len('<Go Back>')
            newy += self.dist
            for item in self.items:
                self.contentwin.addstr(height - 3, newy, item[0])
                newy += len(item[0])
                newy += self.dist

        self.textwin = curses.newwin(height - 5, width - 5)
        self.textwin.bkgd(' ', curses.color_pair(2)) #Default Window color

        self.shadowwin = curses.newwin(height - 1, width - 1)
        self.shadowwin.bkgd(' ', curses.color_pair(0)) #Default shadow color

        self.contentpanel = curses.panel.new_panel(self.contentwin)
        self.textpanel = curses.panel.new_panel(self.textwin)
        self.shadowpanel = curses.panel.new_panel(self.shadowwin)

        self.action_panel = action_panel
        self.refresh(0, True)
        self.hide_window()

    def update_next_item(self):
        self.position = 1
        self.items.append(('<Next>', self.next_function, False))
        self.tab_enabled = False


    def next_function(self, params):
        return ActionResult(True, None)

    def set_action_panel(self, action_panel):
        self.action_panel = action_panel

    def update_menu(self, action_result):
        if (action_result.result and
                'goNext' in action_result.result and
                action_result.result['goNext']):
            return ActionResult(True, None)
        if self.position == 0:
            self.contentwin.addstr(self.height - 3, 5, '<Go Back>')
            self.contentwin.refresh()
            self.hide_window()
            self.action_panel.hide()
            return ActionResult(False, None)
        else:
            if (action_result.result != None and
                    'diskIndex' in action_result.result):
                params = action_result.result['diskIndex']
                if self.menu_helper:
                    self.menu_helper(params)

            result = self.items[self.position-1][1](None)
            if result.success:
                self.hide_window()
                self.action_panel.hide()
                return result
            else:
                if 'goBack' in result.result and result.result['goBack']:
                    self.contentwin.refresh()
                    self.hide_window()
                    self.action_panel.hide()
                    return ActionResult(False, None)

    def do_action(self):
        self.show_window()
        if self.tab_enabled:
            self.refresh(0, False)
        else:
            self.refresh(0, True)
        action_result = self.action_panel.do_action()

        if action_result.success:
            if (action_result.result and
                    'goNext' in action_result.result and
                    action_result.result['goNext']):
                return ActionResult(True, None)
            if self.position != 0:    #saving the disk index
                self.items[self.position-1][1](None)
            if self.items:
                return self.update_menu(action_result)
            self.hide_window()
            return action_result
        else:
            if (not self.tab_enabled and
                    action_result.result != None and
                    'direction' in action_result.result):
                self.refresh(action_result.result['direction'], True)
            if (action_result.result != None and
                    'goBack' in action_result.result
                    and action_result.result['goBack']):
                self.hide_window()
                self.action_panel.hide()
                return action_result
            else:
                #highlight the GoBack and keep going
                self.refresh(0, True)

        while action_result.success == False:
            if self.read_text:
                is_go_back = self.position == 0
                action_result = self.action_panel.do_action(returned=True, go_back=is_go_back)
                if action_result.success:
                    if self.items:
                        return self.update_menu(action_result)
                    self.hide_window()
                    return action_result
                else:
                    if (action_result.result != None and
                            'goBack' in action_result.result and
                            action_result.result['goBack']):
                        self.hide_window()
                        self.action_panel.hide()
                        return action_result
                    if action_result.result and 'direction' in action_result.result:
                        self.refresh(action_result.result['direction'], True)
            else:
                key = self.contentwin.getch()
                if key in [curses.KEY_ENTER, ord('\n')]:
                    #remove highlight from Go Back
                    if self.position == 0:
                        self.contentwin.addstr(self.height - 3, 5, '<Go Back>')
                        self.contentwin.refresh()
                        self.hide_window()
                        self.action_panel.hide()
                        return ActionResult(False, None)
                    else:
                        if (action_result.result != None and
                                'diskIndex' in action_result.result):
                            params = action_result.result['diskIndex']
                            if self.menu_helper:
                                self.menu_helper(params)
                        result = self.items[self.position-1][1](None)
                        if result.success:
                            self.hide_window()
                            self.action_panel.hide()
                            return result
                        else:
                            if 'goBack' in result.result and result.result['goBack']:
                                self.contentwin.refresh()
                                self.hide_window()
                                self.action_panel.hide()
                                return ActionResult(False, None)
                elif key in [ord('\t')]:
                    if not self.tab_enabled:
                        continue
                    #remove highlight from Go Back
                    self.refresh(0, False)
                    # go do the action inside the panel
                    action_result = self.action_panel.do_action()
                    if action_result.success:
                        self.hide_window()
                        return action_result
                    else:
                        #highlight the GoBack and keep going
                        self.refresh(0, True)
                elif key == curses.KEY_UP or key == curses.KEY_LEFT:
                    if key == curses.KEY_UP and self.tab_enabled == False:
                        self.action_panel.navigate(-1)
                        action_result = self.action_panel.do_action()
                        if action_result.success:
                            if self.items:
                                return self.update_menu(action_result)
                            self.hide_window()
                            return action_result
                        else:
                            if 'direction' in action_result.result:
                            #highlight the GoBack and keep going
                                self.refresh(action_result.result['direction'], True)
                    else:
                        self.refresh(-1, True)

                elif key == curses.KEY_DOWN or key == curses.KEY_RIGHT:
                    if key == curses.KEY_DOWN and self.tab_enabled == False:
                        self.action_panel.navigate(1)
                        action_result = self.action_panel.do_action()
                        if action_result.success:
                            if self.items:
                                return self.update_menu(action_result)
                            self.hide_window()
                            return action_result
                        else:
                            if 'direction' in action_result.result:
                            #highlight the GoBack and keep going
                                self.refresh(action_result.result['direction'], True)
                    else:
                        self.refresh(1, True)


    def refresh(self, n, select):
        if not self.can_go_back:
            return
        self.position += n
        if self.position < 0:
            self.position = 0
        elif self.items and self.position > len(self.items):  #add 1 for the <go back>
            self.position = len(self.items)

        if not self.items and not self.can_go_next:
            self.position = 0
        #add the highlight
        newy = 5
        if self.position == 0:   #go back
            if select:
                self.contentwin.addstr(self.height - 3, 5, '<Go Back>', curses.color_pair(3))
            elif self.items: #show user the last selected items
                self.contentwin.addstr(self.height - 3, 5, '<Go Back>', curses.color_pair(1))
            else: #if Go back is the only one shown, do not highlight at all
                self.contentwin.addstr(self.height - 3, 5, '<Go Back>')

            newy += len('<Go Back>')
            newy += self.dist

            if self.items:
                for item in self.items:
                    self.contentwin.addstr(self.height - 3, newy, item[0])
                    newy += len(item[0])
                    newy += self.dist

        else:
            self.contentwin.addstr(self.height - 3, 5, '<Go Back>')
            newy += len('<Go Back>')
            newy += self.dist
            index = 1
            for item in self.items:
                if index == self.position:
                    if select:
                        self.contentwin.addstr(self.height - 3, newy, item[0], curses.color_pair(3))
                    else:
                        self.contentwin.addstr(self.height - 3, newy, item[0], curses.color_pair(1))

                else:
                    self.contentwin.addstr(self.height - 3, newy, item[0])
                newy += len(item[0])
                newy += self.dist
                index += 1

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

        if self.can_go_next:
            self.position = 1

    def hide_window(self):
        self.shadowpanel.hide()
        self.contentpanel.hide()
        self.textpanel.hide()
        curses.panel.update_panels()
        curses.doupdate()

    def addstr(self, y, x, str, mode=0):
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
