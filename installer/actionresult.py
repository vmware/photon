#
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

# ActionResult is returned for any action
# result is a dictionary that decribes the return value
class ActionResult(object):
    def __init__(self, success, result):
        self.success = success
        self.result = result
