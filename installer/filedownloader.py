#
#            © 2019 VMware Inc.,
#
#     Date: Tue Oct 15 14:17:13 IST 2019
#   Author: Siddharth Chandrasekaran <csiddharth@vmware.com>

import os
import tempfile
from commandutils import CommandUtils
from window import Window
from windowstringreader import WindowStringReader
from actionresult import ActionResult
from networkmanager import NetworkManager
from confirmwindow import ConfirmWindow

class FileDownloader(object):

    def __init__(self, maxy, maxx, install_config, title, intro, dest, setup_network=False):
        self.install_config = install_config
        self.maxy = maxy
        self.maxx = maxx
        self.title = title
        self.intro = intro
        self.netmgr = None
        self.dest = dest
        self.setup_network = setup_network
        if self.setup_network:
            self.netmgr = NetworkManager(install_config)

    def ask_proceed_unsafe_download(self, fingerprint):
        msg = ('This server could not prove its authenticity. Its '
                'fingerprint is:\n\n' + fingerprint +
                '\n\nDo you wish to proceed?\n')
        conf_message_height = 12
        conf_message_width = 80
        conf_message_button_y = (self.maxy - conf_message_height) // 2 + 8
        r = ConfirmWindow(conf_message_height, conf_message_width, self.maxy, self.maxx,
                          conf_message_button_y, msg).do_action()
        if not r.success or not r.result.get('yes', False):
            return False
        return True

    def do_setup_network(self):
        if not self.netmgr.setup_network():
            msg = 'Failed to setup network configuration!'
            conf_message_height = 12
            conf_message_width = 80
            conf_message_button_y = (self.maxy - conf_message_height) // 2 + 8
            ConfirmWindow(conf_message_height, conf_message_width, self.maxy, self.maxx,
                          conf_message_button_y, msg, True).do_action()
            return False
        self.netmgr.restart_networkd()
        return True

    def display(self):
        if self.setup_network and not self.do_setup_network():
            return ActionResult(False, {'goBack': True})

        file_source = {}
        accepted_chars = list(range(ord('a'), ord('z')+1))
        accepted_chars.extend(range(ord('A'), ord('Z')+1))
        accepted_chars.extend(range(ord('0'), ord('9')+1))
        accepted_chars.extend([ ord('-'), ord('_'), ord('.'), ord('~'), ord(':'), ord('/') ])
        result = WindowStringReader(self.maxy, self.maxx, 18, 78, 'url',
                                    None, None, accepted_chars, None, None,
                                    self.title, self.intro, 10, file_source, 'https://',
                                    True).get_user_string(None)
        if not result.success:
            return result

        status_window = Window(10,70, self.maxy, self.maxx, 'Installing Photon', False)
        status_window.addstr(1, 0, 'Downloading file...')
        status_window.show_window()

        fd, temp_file = tempfile.mkstemp()
        result, msg = CommandUtils.wget(file_source['url'], temp_file,
                                        ask_fn=self.ask_proceed_unsafe_download)
        os.close(fd)
        if not result:
            status_window.adderror('Error: ' + msg + ' Press any key to go back...')
            status_window.content_window().getch()
            status_window.clearerror()
            status_window.hide_window()
            return ActionResult(False, {'goBack': True})

        if 'additional_files' not in self.install_config:
            self.install_config['additional_files'] = []
        copy = { temp_file: self.dest }
        self.install_config['additional_files'].append(copy)

        return ActionResult(True, None)
