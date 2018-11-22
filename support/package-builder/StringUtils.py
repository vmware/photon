import re

class StringUtils(object):

    # Opens conditional brackets from
    # (aaa <= 3.1 or bbb) ccc (ddd or fff > 4.5.6)
    # into
    # aaa <= 3.1 ccc ddd
    def getStringInConditionalBrackets(self,inputstring):
        inputstring=inputstring.strip()
        items = re.findall(r"([(][A-Za-z0-9 %{?}_\.\-<>=]+[)])",  inputstring)
        for m in items:
            out = m[m.find("(")+1 : m.find(" or ")].strip()
            inputstring = inputstring.replace(m, out);
        return inputstring

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

    @staticmethod
    def splitPackageNameAndVersion(pkg):
        versionindex = pkg.rfind("-")
        if versionindex == -1:
            raise Exception("Invalid argument")
        packageName = pkg[:versionindex]
        packageVersion = pkg[versionindex+1:]
        return packageName, packageVersion
