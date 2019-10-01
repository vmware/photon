#
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

import os
from jsonwrapper import JsonWrapper
from menu import Menu
from window import Window
from actionresult import ActionResult

class PackageSelector(object):
    def __init__(self, maxy, maxx, install_config, options_file):
        self.install_config = install_config
        self.maxx = maxx
        self.maxy = maxy
        self.win_width = 50
        self.win_height = 13

        self.win_starty = (self.maxy - self.win_height) // 2
        self.win_startx = (self.maxx - self.win_width) // 2

        self.menu_starty = self.win_starty + 3

        self.load_package_list(options_file)

        self.window = Window(self.win_height, self.win_width, self.maxy, self.maxx,
                             'Select Installation', True, action_panel=self.package_menu,
                             can_go_next=True, position=1)

    @staticmethod
    def get_packages_to_install(option, output_data_path):
        if 'packagelist_file' in option:
            json_wrapper_package_list = JsonWrapper(os.path.join(output_data_path,
                                                option['packagelist_file']))
            package_list_json = json_wrapper_package_list.read()
            return package_list_json["packages"]
        elif 'packages' in option:
            return option["packages"]
        else:
            raise Exception("Install option '" + option['title'] + "' must have 'packagelist_file' or 'packages' property")

    def load_package_list(self, options_file):
        json_wrapper_option_list = JsonWrapper(options_file)
        option_list_json = json_wrapper_option_list.read()
        options_sorted = option_list_json.items()

        self.package_menu_items = []
        base_path = os.path.dirname(options_file)
        package_list = []

        default_selected = 0
        visible_options_cnt = 0
        for install_option in options_sorted:
            if install_option[1]["visible"] == True:
                package_list = PackageSelector.get_packages_to_install(install_option[1],
                                                                       base_path)
                self.package_menu_items.append((install_option[1]["title"],
                                                self.exit_function,
                                                [install_option[0], package_list]))
                if install_option[0] == 'minimal':
                    default_selected = visible_options_cnt
                visible_options_cnt = visible_options_cnt + 1


        self.package_menu = Menu(self.menu_starty, self.maxx, self.package_menu_items,
                                 default_selected=default_selected, tab_enable=False)

    def exit_function(self, selected_item_params):
        self.install_config['type'] = selected_item_params[0]
        self.install_config['packages'] = selected_item_params[1]
        return ActionResult(True, {'custom': False})

    def custom_packages(self):
        return ActionResult(True, {'custom': True})

    def display(self):
        return self.window.do_action()
