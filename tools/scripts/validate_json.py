#!/usr/bin/python3

import json
import sys


def main():
    arglen = len(sys.argv)

    if arglen <= 1:
        return

    for arg in range(1, arglen):
        try:
            json.load(open(sys.argv[arg]))
        except ValueError as e:
            print("Check: " + sys.argv[arg] + " for syntax errors")
            raise Exception(e)


if __name__ == "__main__":
    main()
