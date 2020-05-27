import platform

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
        if macro.macroName == "%postun":
            self.postunMacro = macro
        if macro.macroName == "%files":
            self.filesMacro = macro
        if macro.macroName == "%description":
            self.descriptionMacro = macro

class SpecObject(object):
    def __init__(self):
        self.name = ""
        self.version = ""
        self.release = ""
        # map subpackage name to its buildarch
        self.buildarch = {}
        # list of subpackage names
        self.listPackages = []
        # list of subpackage names that have %files section
        self.listRPMPackages = []

        # Next four lists store dependentPackageData objects
        self.buildRequires = []
        self.installRequires = []
        self.checkBuildRequires = []
        self.extraBuildRequires = []
        # map subpackage name to list of install requires
        # dependentPackageData objects
        self.installRequiresPackages = {}

        # full spec file name
        self.specFile = ""
        self.listSources = []
        self.checksums = {}
        self.listPatches = []
        self.securityHardening = ""
        self.url = ""
        self.sourceurl = ""
        self.license = ""
