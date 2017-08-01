#! /usr/bin/python2
#
#    Copyright (C) 2017 vmware inc.
#
#    Author: Rui Gu <ruig@vmware.com>
from constants import constants
from optparse import OptionParser
import os
import sys

def main():
    usage = os.path.basename(__file__) + "--pkg=[pkg_name]"
    parser = OptionParser(usage)
    parser.add_option("-p", "--pkg", dest="pkg")
    (options,  args) = parser.parse_args() 

    if options.pkg in constants.listCoreToolChainPackages:
        sys.exit(0)
    elif options.pkg in constants.listToolChainPackages:
        sys.exit(0)

    sys.exit(1)

if __name__=="__main__":
    main()
