import re


class StringUtils(object):

    # Opens conditional brackets from
    # (aaa <= 3.1 or bbb) ccc (ddd or fff > 4.5.6)
    # into
    # aaa <= 3.1 ccc ddd
    def getStringInConditionalBrackets(self, inputstring):
        inputstring = inputstring.strip()
        items = re.findall(r"([(][A-Za-z0-9 %{?}_\.\-<>=]+[)])", inputstring)
        for m in items:
            out = m[m.find("(") + 1 : m.find(" or ")].strip()
            inputstring = inputstring.replace(m, out)
        return inputstring

    def getFileNameFromURL(self, inputstring):
        index = inputstring.rfind("/")
        return inputstring[index + 1 :]

    def getPackageNameFromURL(self, inputstring):
        filename = self.getFileNameFromURL(inputstring)
        m = re.search(
            r"(zip|mozjs|.+-)([0-9_.]+)(\.source|\.tar|-src|\.zip|\+md|\.tgz).*",
            filename,
        )
        if m is None:
            print("Unable to parse " + filename)
            return inputstring
        name = m.group(1)
        if name.endswith("-"):
            name = name[:-1]
        return name

    def getPackageVersionFromURL(self, inputstring):
        filename = self.getFileNameFromURL(inputstring)
        m = re.search(
            r"(zip|mozjs|.*-)([0-9_.]+)(\.source|\.tar|-src|\.zip|\+md|\.tgz).*",
            filename,
        )
        if m is None:
            print("Unable to parse " + filename)
            return inputstring
        name = m.group(2)
        return name.replace("_", ".")

    @staticmethod
    def splitPackageNameAndVersion(pkg):
        packageVersion = pkg.rsplit("-", 1)[0]
        if not packageVersion:
            raise Exception(f"Invalid argument: {pkg}")
        packageName = packageVersion.rsplit("-", 1)[0]
        packageVersion = pkg.rsplit(packageName)[1][1:]
        return packageName, packageVersion

    @staticmethod
    def splitRPMFilename(filename):
        """splitRPMFilename splits RPM filename or RPM package name into components: name, version, release, dist tag, arch
        Examples:
        "openssl-libs-3.0.8-2.ph5.x86_64.rpm" -> { "name": "openssl-libs", "version": "3.0.8", "release": "2", "tag": "ph5", "arch": "x86_64")
        "openssl-libs-3.0.8-2.ph5" -> ("name": "openssl-libs", "version": "3.0.8", "release": "2", "tag": "ph5", "arch": "")
        :param filename: string containing filename or package name
        :return: dictionary of strings values by keys: name, version, release, tag, arch
        """
        if filename[-4:] == ".rpm":
            filename = filename[:-4]

        archIndex = filename.rfind(".")
        arch = filename[archIndex + 1 :]
        if arch not in ["noarch", "x86_64", "aarch64", "src"]:
            arch = ""
            archIndex = len(filename)

        tagIndex = filename[:archIndex].rfind(".")
        tag = filename[tagIndex + 1 : archIndex]

        relIndex = filename[:tagIndex].rfind("-")
        rel = filename[relIndex + 1 : tagIndex]

        verIndex = filename[:relIndex].rfind("-")
        ver = filename[verIndex + 1 : relIndex]

        name = filename[0:verIndex]
        return {"name": name, "version": ver, "release": rel, "tag": tag, "arch": arch}
