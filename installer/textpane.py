#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>
import curses
from actionresult import ActionResult
from action import Action

class TextPane(Action):
    def __init__(self, starty, maxx, width, text_file_path, height,
                 menu_items, partition=False, popupWindow=False,
                 install_config={}, text_items=[], table_space=0,
                 default_start=0, info=[], size_left=[]):
        self.head_position = 0  #This is the start of showing
        self.menu_position = default_start
        self.lines = []
        self.menu_items = menu_items
        self.text_items = text_items
        self.table_space = table_space
        self.info = info
        self.size_left = size_left

        self.width = width

        if partition == False:
            self.read_file(text_file_path, self.width - 3)
        else:
            self.install_config = install_config
            self.partition()

        self.num_items = len(self.lines)
        if self.info:
            self.text_height = height - 4
        else:
            self.text_height = height - 2

        # Check if we need to add a scroll bar
        if self.num_items > self.text_height:
            self.show_scroll = True
        else:
            self.show_scroll = False

        # Some calculation to detitmine the size of the scroll filled portion
        if self.num_items == 0:
            self.filled = 0
        else:
            self.filled = int(round(self.text_height * self.text_height / float(self.num_items)))
        if self.filled == 0:
            self.filled += 1
        for i in [1, 2]:
            if ((self.num_items - self.text_height) >= i and
                    (self.text_height - self.filled) == (i - 1)):
                self.filled -= 1

        self.window = curses.newwin(height, self.width)
        self.window.bkgd(' ', curses.color_pair(2))
        self.popupWindow = popupWindow

        self.window.keypad(1)
        self.panel = curses.panel.new_panel(self.window)

        self.panel.move(starty, (maxx - self.width) // 2)
        self.panel.hide()
        curses.panel.update_panels()

    def partition(self):
        if self.install_config == {}:
            return

        tstring = ''
        #calculate the start index for each item and draw the title
        for index, item in enumerate(self.text_items):
            tstring = tstring + item[0] + ' '*(item[1] - len(item[0])) + ' '*self.table_space

        self.lines.append(tstring)
        #draw the table
        for i in range(int(self.install_config['partitionsnumber'])):
            pdisk = self.install_config['partition_disk']
            if len(pdisk) > self.text_items[0][1]:
                pdisk = pdisk[-self.text_items[0][1]:]
            psize = self.install_config[str(i)+'partition_info'+str(0)]
            if len(psize) > self.text_items[1][1]:
                psize = psize[-self.text_items[1][1]:]
            if len(psize) == 0:
                psize = '<' + self.size_left + '>'
            ptype = self.install_config[str(i) + 'partition_info' + str(1)]
            if len(ptype) > self.text_items[2][1]:
                ptype = ptype[-self.text_items[2][1]:]
            pmountpoint = self.install_config[str(i) + 'partition_info' + str(2)]
            if len(pmountpoint) > self.text_items[3][1]:
                pmountpoint = pmountpoint[-self.text_items[3][1]:]
            pstring = (pdisk + ' '*(self.text_items[0][1] - len(pdisk)) +
                       ' ' * self.table_space + psize +
                       ' '*(self.text_items[1][1] - len(psize)) +
                       ' ' * self.table_space + ptype +
                       ' '*(self.text_items[2][1] - len(ptype) +
                            self.table_space) + pmountpoint)
            self.lines.append(pstring)

    def read_file(self, text_file_path, line_width):
        with open(text_file_path, "rb") as f:
            for line in f:
                # expand tab to 8 spaces.
                try:
                    line = line.decode(encoding='latin1')
                except UnicodeDecodeError:
                    pass
                line = line.expandtabs()
                indent = len(line) - len(line.lstrip())
                actual_line_width = line_width - indent
                line = line.strip()
                # Adjust the words on the lines
                while len(line) > actual_line_width:
                    sep_index = actual_line_width

                    while sep_index > 0 and line[sep_index-1] != ' ' and line[sep_index] != ' ':
                        sep_index = sep_index - 1

                    current_line_width = sep_index
                    if sep_index == 0:
                        current_line_width = actual_line_width
                    currLine = line[:current_line_width]
                    line = line[current_line_width:]
                    line = line.strip()

                    # Lengthen the line with spaces
                    self.lines.append(' ' * indent + currLine +
                                      ' ' *(actual_line_width - len(currLine)))

                # lengthen the line with spaces
                self.lines.append(' ' * indent + line + ' ' *(actual_line_width - len(line)))

    def navigate(self, n):
        if self.show_scroll:
            self.head_position += n
            if self.head_position < 0:
                self.head_position = 0
            elif self.head_position > (len(self.lines) - self.text_height + 1):
                self.head_position = len(self.lines) - self.text_height + 1

    def navigate_menu(self, n):
        self.menu_position += n
        if self.menu_position < 0:
            self.menu_position = 0
        elif self.menu_position >= len(self.menu_items):
            self.menu_position = len(self.menu_items) - 1


    def render_scroll_bar(self):
        if self.show_scroll:
            remaining_above = self.head_position
            remaining_down = self.num_items - self.text_height - self.head_position#

            up = int(round(remaining_above * self.text_height / float(self.num_items)))
            down = self.text_height - up - self.filled

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

    def refresh(self):
        self.window.clear()
        for index, line in enumerate(self.lines):
            if index < self.head_position:
                continue
            elif index > self.head_position + self.text_height - 1:
                continue

            x = 0
            y = index - self.head_position
            if len(line) > 0:
                self.window.addstr(y, x, line)

        xpos = self.width
        for index, item in enumerate(self.menu_items):
            if index == self.menu_position:
                mode = curses.color_pair(3)
            else:
                mode = curses.color_pair(2)
            if self.info:
                self.window.addstr(self.text_height + 3, xpos - len(item[0]) - 4, item[0], mode)
            else:
                self.window.addstr(self.text_height + 1, xpos - len(item[0]) - 4, item[0], mode)
            xpos = xpos - len(item[0]) - 4

        if self.info:
            self.window.addstr(self.text_height+1, 5, self.info)


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
                self.hide()
                return self.menu_items[self.menu_position][1]()
            if key == curses.KEY_UP:
                self.navigate(-1)
            elif key == curses.KEY_DOWN:
                self.navigate(1)

            elif key == curses.KEY_LEFT:
                self.navigate_menu(1)
            elif key == curses.KEY_RIGHT:
                self.navigate_menu(-1)

            elif key == curses.KEY_NPAGE:
                self.navigate(self.text_height)
            elif key == curses.KEY_PPAGE:
                self.navigate(-self.text_height)

            elif key == curses.KEY_HOME:
                self.head_position = 0
