#
#    Copyright (C) 2015 VMware, Inc. All rights reserved.

def constant(f):
    def fset(self, value):
        raise SyntaxError
    def fget(self):
        return f()
    return property(fget, fset)


class publishConst:
    @constant
    def new():
        return "new"
    @constant
    def updates():
        return "updates"
    @constant
    def obsoletes():
        return "obsoletes"
    @constant
    def verified():
        return "verified"
#pkg attribs
    @constant
    def path():
        return "path"
    @constant
    def published():
        return "published"
    @constant
    def name():
        return "name"
    @constant
    def sha1():
        return "sha1"
#other
    @constant
    def sha1allfilename():
        return 'sha1-all'
