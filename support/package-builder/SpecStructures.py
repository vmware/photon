#!/usr/bin/env python3


class dependentPackageData(object):
    def __init__(self):
        self.package = ""
        self.version = ""
        self.compare = ""


class Package(object):
    def __init__(self, buildarch, basePkg=None):
        self.summary = ""
        self.name = ""
        self.group = ""
        self.license = ""
        self.summary = ""
        self.description = ""
        self.version = ""
        self.release = ""
        self.buildarch = buildarch
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
        self.buildrequiresnative = []

        self.requires = []
        self.provides = []
        self.obsoletes = []
        self.conflicts = []

        self.filesMacro = None

        if basePkg:
            self.basePkgName = basePkg.name
            self.group = basePkg.group
            self.license = basePkg.license
            self.summary = basePkg.summary
            self.version = basePkg.version
            self.buildarch = basePkg.buildarch
            self.release = basePkg.release
            self.distribution = basePkg.distribution

    def updatePackageMacro(self, macro):
        if macro.macroName == "%files":
            self.filesMacro = macro


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

        # Next five lists store dependentPackageData objects
        self.buildRequires = []
        self.installRequires = []
        self.checkBuildRequires = []
        self.extraBuildRequires = []
        self.buildRequiresNative = []

        """
        map subpackage name to list of install requires
        dependentPackageData objects
        """
        self.installRequiresPackages = {}

        # full spec file name
        self.specFile = ""
        self.listSources = []
        self.checksums = {}
        self.listPatches = []
        self.securityHardening = ""
        self.networkRequired = False
        self.url = ""
        self.sourceurl = ""
        self.license = ""
        self.summary = ""
        # map subpackage name to its description string
        self.descriptions = {}
