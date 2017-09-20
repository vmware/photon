#!/usr/bin/python2
#
#    Copyright (C) 2015 vmware inc.
#
#    Author: Sharath George <sharathg@vmware.com>


import json
import collections

class JsonWrapper(object):

    def __init__(self,  filename):
        self.filename = filename

    def read(self):
        json_data = open(self.filename)
        self.data = json.load(json_data, object_pairs_hook=collections.OrderedDict)
        json_data.close()
        return self.data

    def write(self,  data):
        self.data = data
        outfile = open(self.filename,  'wb')
        json.dump(data,  outfile)
