#!/usr/bin/python2
#
#    Copyright (C) 2015 vmware inc.
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

from windowstringreader import WindowStringReader
from actionresult import ActionResult

class OSTreeWindowStringReader(WindowStringReader):
    def __init__(self, maxy, maxx, height, width, field, confirmation_err_msg, echo_char, accepted_chars, validation_fn, conversion_fn, title, display_string, inputy, install_config, default_string = None):
        WindowStringReader.__init__(self, maxy, maxx, height, width, field, confirmation_err_msg, echo_char, accepted_chars, validation_fn, conversion_fn, title, display_string, inputy, install_config, default_string)

    def get_user_string(self):
        if self.install_config['type'] == 'ostree_host' and not self.install_config['default_repo']:
            return self.window.do_action()
        return ActionResult(True, None)
