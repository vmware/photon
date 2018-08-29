# pylint: disable=invalid-name,missing-docstring
import os
from SpecParser import SpecParser
from StringUtils import StringUtils

class Specutils(object):

    def __init__(self, specfile):
        self.specfile = ""
        self.spec = SpecParser()
        if Specutils._isSpecFile(specfile):
            self.specfile = specfile
            self.spec.parseSpecFile(self.specfile)

    @staticmethod
    def _isSpecFile(specfile):
        if os.path.isfile(specfile) and specfile.endswith(".spec"):
            return True
        return False

    def getSourceNames(self):
        sourceNames = []
        strUtils = StringUtils()
        pkg = self.spec.packages.get('default')
        if pkg is None:
            return None
        for source in pkg.sources:
            sourceName = strUtils.getFileNameFromURL(source)
            sourceNames.append(sourceName)
        return sourceNames

    def getChecksums(self):
        pkg = self.spec.packages.get('default')
        return pkg.checksums

    def getPatchNames(self):
        patchNames = []
        strUtils = StringUtils()
        pkg = self.spec.packages.get('default')
        if pkg is None:
            return None
        for patch in pkg.patches:
            patchName = strUtils.getFileNameFromURL(patch)
            patchNames.append(patchName)
        return patchNames

    def getPackageNames(self):
        packageNames = []
        for pkg in self.spec.packages.values():
            packageNames.append(pkg.name)
        return packageNames

    def getIsRPMPackage(self, pkgName):
        defaultPkgName = self.spec.packages['default'].name
        if pkgName == defaultPkgName:
            pkgName = "default"
        if pkgName in self.spec.packages.keys():
            pkg = self.spec.packages.get(pkgName)
            if pkg.filesMacro is not None:
                return True
        return False

    def getRPMNames(self):
        rpmNames = []
        for pkg in self.spec.packages.values():
            rpmName = pkg.name + "-" + pkg.version + "-" + pkg.release
            rpmNames.append(rpmName)
        return rpmNames

    def getLicense(self):
        pkg = self.spec.packages.get('default')
        if pkg is None:
            return None
        return pkg.license

    def getBuildArch(self, pkgName):
        for pkg in self.spec.packages.values():
            if pkg.name == pkgName:
                return pkg.buildarch
        pkg = self.spec.packages.get('default')
        return pkg.buildarch

    def getURL(self):
        pkg = self.spec.packages.get('default')
        if pkg is None:
            return None
        return pkg.URL

    def getSourceURL(self):
        pkg = self.spec.packages.get('default')
        if pkg is None:
            return None
        if not pkg.sources:
            return None
        sourceURL = pkg.sources[0]
        if sourceURL.startswith("http") or sourceURL.startswith("ftp"):
            return sourceURL
        return None

    def getRequiresAllPackages(self):
        dependentPackages = []
        for pkg in self.spec.packages.values():
            for dpkg in pkg.requires:
                dependentPackages.append(dpkg)
        listDependentPackages = list(set(dependentPackages))
        packageNames = self.getPackageNames()
        for pkgName in packageNames:
            for objName in listDependentPackages:
                if objName.package == pkgName:
                        dependentPackages.remove(objName)
        dependentPackages = list(set(dependentPackages))
        return dependentPackages

    def getBuildRequiresAllPackages(self):
        dependentPackages = []
        for pkg in self.spec.packages.values():
            for dpkg in pkg.buildrequires:
                dependentPackages.append(dpkg)
        listDependentPackages = list(set(dependentPackages))
        packageNames = self.getPackageNames()
        for pkgName in packageNames:
            for objName in listDependentPackages:
                if objName.package == pkgName:
                        dependentPackages.remove(objName)
        dependentPackages = list(set(dependentPackages))
        return dependentPackages

    def getCheckBuildRequiresAllPackages(self):
        dependentPackages = []
        for pkg in self.spec.packages.values():
            for dpkg in pkg.checkbuildrequires:
                dependentPackages.append(dpkg)
        dependentPackages = list(set(dependentPackages))
        return dependentPackages

    def getRequires(self, pkgName):
        dependentPackages = []
        for pkg in self.spec.packages.values():
            if pkg.name == pkgName:
                for dpkg in pkg.requires:
                    dependentPackages.append(dpkg.package)
        return dependentPackages

    def getProvides(self, packageName):
        dependentPackages = []
        defaultPkgName = self.spec.packages['default'].name
        pkg = None
        if packageName in self.spec.packages:
            pkg = self.spec.packages.get(packageName)
        if defaultPkgName == packageName:
            pkg = self.spec.packages['default']
        if pkg is not None:
            for dpkg in pkg.provides:
                dependentPackages.append(dpkg.package)
        else:
            print("package not found")
        return dependentPackages

    def getVersion(self):
        pkg = self.spec.packages.get('default')
        return pkg.version

    def getRelease(self):
        pkg = self.spec.packages.get('default')
        return pkg.release

    def getBasePackageName(self):
        pkg = self.spec.packages.get('default')
        return pkg.name

    def getSecurityHardeningOption(self):
        return self.spec.globalSecurityHardening

    def isCheckAvailable(self):
        check = False
        if self.spec.checkMacro is not None:
            check = True
        return check

    def getDefinitions(self):
        return self.spec.defs

def main():
    spec = Specutils("/workspace1/myrepos/photon/SPECS/docker/docker.spec")
    print("packages {}".format(spec.getPackageNames()))
    print("packages {}".format(spec.getRPMNames()))
    print("sources {}".format(spec.getSourceNames()))
    print("patches {}".format(spec.getPatchNames()))
    print("requires {}".format(spec.getRequires('libltdl-devel')))
    print("requires {}".format(spec.getRequires('libtool')))

    print("provides {}".format(spec.getProvides('libtool')))
    print("all-requires {}".format(spec.getPkgNamesFromObj(spec.getRequiresAllPackages())))
    print("all-build-requires {}".format(spec.getPkgNamesFromObj(spec.getBuildRequiresAllPackages())))

if __name__ == '__main__':
    main()
