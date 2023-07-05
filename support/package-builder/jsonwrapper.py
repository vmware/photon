#!/usr/bin/env python3

import json
import collections


class JsonWrapper(object):
    def __init__(self, filename):
        self.filename = filename
        self.data = None

    def read(self):
        try:
            with open(self.filename) as json_data:
                self.data = json.load(
                    json_data, object_pairs_hook=collections.OrderedDict
                )
        except Exception:
            raise Exception(f"Unable to read {self.filename}")
        return self.data

    def write(self, data):
        self.data = data
        try:
            with open(self.filename, "w") as outfile:
                json.dump(data, outfile)
        except Exception:
            raise Exception(f"Unable to write {self.filename}")
