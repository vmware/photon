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
        
    def getSpecNameFromPackageName(self, pkgName):
        id = pkgName.rfind("-")
        if (id != -1):
            return pkgName[0:id];
        else:
            return pkgName;
