#!/usr/bin/python3
#
#    Author: Sharath George <sharathg@vmware.com>

import json
import collections

class JsonWrapper(object):

    def __init__(self, filename):
        self.filename = filename
        self.data = None
    def read(self):
        try:
            with open(self.filename) as json_data:
                self.data = json.load(json_data, object_pairs_hook=collections.OrderedDict)
        except Exception as _:
            raise Exception("Unable to read {}".format(self.filename))
        return self.data

    def write(self, data):
        self.data = data
        try:
            with open(self.filename, 'w') as outfile:
                json.dump(data, outfile)
        except Exception as _:
            raise Exception("Unable to write {}".format(self.filename))
