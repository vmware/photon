#!/usr/bin/python2
#
#    Copyright (C) 2015 vmware inc.
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

from windowstringreader import WindowStringReader
from actionresult import ActionResult

class OSTreeWindowStringReader():
    def __init__(self, maxy, maxx, height, width, field, confirmation_err_msg, echo_char, accepted_chars, validation_fn, conversion_fn, title, display_string, inputy, install_config, default_string = None):
        self.config = {}
        self.field = field
        self.wsr = WindowStringReader(maxy, maxx, height, width, field, confirmation_err_msg, echo_char, accepted_chars, validation_fn, conversion_fn, title, display_string, inputy, self.config, default_string)
        self.install_config = install_config

    def get_user_string(self):
        result = ActionResult(True, None)
        if 'ostree' in self.install_config and not self.install_config['ostree']['default_repo']:
            result = self.wsr.window.do_action()
            if result.success:
                self.install_config['ostree'][self.field] = self.config[self.field]
        return result
