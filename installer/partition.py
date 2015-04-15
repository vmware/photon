#! /usr/bin/python2
#
#    Copyright (C) 2015 vmware inc.
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

class Partition(object):
    def __init__(self, path, size, filesystem):
        self.path = path
        self.size = size
        self.filesystem = filesystem
        self.unallocated = (path == 'unallocated')

    @staticmethod
    def wrap_partitions_from_dict_arr(arr):
    	partitions = []
        for partition in arr:
            partitions.append(Partition(partition['path'], partition['size'], partition['filesystem']))

        return partitions

