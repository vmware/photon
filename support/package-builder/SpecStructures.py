import platform

class rpmMacro(object):

    def __init__(self):
        self.macroName = ""
        self.macroFlag = ""
        self.content = ""
        self.position = -1
        self.endposition = -1

    def setName(self, name):
        self.macroName = name

    def displayMacro(self):
        print("Macro:")
        print(self.macroName + " {}".format(self.macroFlag)
              + " {}".format(self.position)
              + " {}".format(self.endposition))
        print(self.content)

class dependentPackageData(object):

    def __init__(self):
        self.package = ""
        self.version = ""
        self.compare = ""

class Package(object):
    def __init__(self, basePkg=None):
        self.summary = ""
        self.name = ""
        self.group = ""
        self.license = ""
        self.version = ""
        self.release = ""
        self.buildarch = platform.machine()
        self.distribution = "Photon"
        self.basePkgName = ""
        self.URL = ""

        self.sources = []
        self.checksums = {}
        self.patches = []
        self.buildrequires = []
        self.buildprovides = []
        self.checkbuildrequires = []
        self.extrabuildrequires = []

        self.requires = []
        self.provides = []
        self.obsoletes = []
        self.conflicts = []

        self.descriptionMacro = None
        self.postMacro = None
        self.postunMacro = None
        self.filesMacro = None
        self.packageMacro = None

        if basePkg is not None:
            self.basePkgName = basePkg.name
            self.group = basePkg.group
            self.license = basePkg.license
            self.version = basePkg.version
            self.buildarch = basePkg.buildarch
            self.release = basePkg.release
            self.distribution = basePkg.distribution

    def updatePackageMacro(self, macro):
        if macro.macroName == "%post":
            self.postMacro = macro
            return True
        if macro.macroName == "%postun":
            self.postunMacro = macro
            return True
        if macro.macroName == "%files":
            self.filesMacro = macro
            return True
        if macro.macroName == "%description":
            self.descriptionMacro = macro
            return True
        return False
