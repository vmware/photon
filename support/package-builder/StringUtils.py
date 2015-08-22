import re

class StringUtils(object):

    def getStringInBrackets(self, inputstring):
        inputstring=inputstring.strip()
        m = re.search(r"^\(([A-Za-z0-9_.-]+)\)",  inputstring)
        if m is None:
            return inputstring
        return m.group(1)

    def getFileNameFromURL(self,inputstring):
        index=inputstring.rfind("/")
        return inputstring[index+1:]

    def getPackageNameFromURL(self,inputstring):
        filename=self.getFileNameFromURL(inputstring)
        m = re.search(r"(zip|mozjs|.+-)([0-9_.]+)(\.source|\.tar|-src|\.zip|\+md|\.tgz).*",  filename)
        if m is None:
            print "Unable to parse "+filename
            return inputstring
        name = m.group(1)
        if name.endswith("-"):
            name = name[:-1]
        return name

    def getPackageVersionFromURL(self,inputstring):
        filename=self.getFileNameFromURL(inputstring)
        m = re.search(r"(zip|mozjs|.*-)([0-9_.]+)(\.source|\.tar|-src|\.zip|\+md|\.tgz).*",  filename)
        if m is None:
            print "Unable to parse "+filename
            return inputstring
        name = m.group(2)
        return name.replace("_", ".")
