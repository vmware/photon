#! /usr/bin/python2
#
#    Copyright (C) 2015 vmware inc.
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>


class Action(object):

    def do_action(self, params):
        raise NameError('Abstract method, this should be implemented in the child class')
    
    def hide(self, params):
        raise NameError('Abstract method, this should be implemented in the child class')


    
    