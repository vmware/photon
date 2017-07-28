from SpecParser import SpecParser
from StringUtils import StringUtils
import os

class Specutils(object):
    
    def __init__(self,specfile):
        self.specfile=""
        self.spec = SpecParser()
        if self.isSpecFile(specfile):
            self.specfile=specfile
            self.spec.parseSpecFile(self.specfile)
    
    def isSpecFile(self,specfile):
        if os.path.isfile(specfile) and specfile[-5:] == ".spec":
            return True
        return False
    
    def getSourceNames(self):
        sourceNames=[]
        strUtils = StringUtils()
        pkg = self.spec.packages.get('default')
        if pkg is None:
            return None
        for source in pkg.sources:
            sourceName=strUtils.getFileNameFromURL(source)
            sourceNames.append(sourceName)
        return sourceNames
    
    def getSourceURLs(self):
        sourceNames=[]
        strUtils = StringUtils()
        pkg = self.spec.packages.get('default')
        if pkg is None:
            return None
        for source in pkg.sources:
            sourceNames.append(source)
        return sourceNames

    def getPatchNames(self):
        patchNames=[]
        strUtils = StringUtils()
        pkg = self.spec.packages.get('default')
        if pkg is None:
            return None
        for patch in pkg.patches:
            patchName=strUtils.getFileNameFromURL(patch)
            patchNames.append(patchName)
        return patchNames
    
    def getPackageNames(self):
        packageNames=[]
        for key in self.spec.packages.keys():
            pkg = self.spec.packages.get(key)
            packageNames.append(pkg.name)
        return packageNames
    
    def getRPMNames(self):
        rpmNames=[]
        for key in self.spec.packages.keys():
            pkg = self.spec.packages.get(key)
            rpmName=pkg.name+"-"+pkg.version+"-"+pkg.release
            rpmNames.append(rpmName)
        return rpmNames

    def getRPMName(self, pkgName):
        rpmName=None
        for key in self.spec.packages.keys():
            pkg = self.spec.packages.get(key)
            if pkg.name == pkgName:
                rpmName=pkg.name+"-"+pkg.version+"-"+pkg.release
                break
        return rpmName

    def getDebuginfoRPMName(self, pkgName):
        rpmName=None
        for key in self.spec.packages.keys():
            pkg = self.spec.packages.get(key)
            if pkg.name == pkgName:
                if pkg.basePkgName:
                    rpmName=pkg.basePkgName+"-debuginfo-"+pkg.version+"-"+pkg.release
                    break
                else:
                    rpmName=pkg.name+"-debuginfo-"+pkg.version+"-"+pkg.release
                    break
        return rpmName

    def getRPMVersion(self, pkgName):
        version=None
        for key in self.spec.packages.keys():
            pkg = self.spec.packages.get(key)
            if pkg.name == pkgName:
                version=pkg.version
                break
        return version

    def getRPMRelease(self, pkgName):
        release=None
        for key in self.spec.packages.keys():
            pkg = self.spec.packages.get(key)
            if pkg.name == pkgName:
                release=pkg.release
                break
        return release

    def getLicense(self, pkgName):
        licenseInfo=None
        for key in self.spec.packages.keys():
            pkg = self.spec.packages.get(key)
            if pkg.name == pkgName:
                licenseInfo=pkg.license
                break
        return licenseInfo

    def getURL(self, pkgName):
        url=None
        for key in self.spec.packages.keys():
            pkg = self.spec.packages.get(key)
            if pkg.name == pkgName:
                url=pkg.URL
                break
        return url

    def getBuildArch(self, pkgName):
        buildArch="x86_64"
        for key in self.spec.packages.keys():
            pkg = self.spec.packages.get(key)
            if pkg.name == pkgName:
                buildArch=pkg.buildarch
                break
        return buildArch
    
    def getRequiresAllPackages(self):
        depedentPackages=[]
        for key in self.spec.packages.keys():
            pkg = self.spec.packages.get(key)
            for dpkg in pkg.requires:
                depedentPackages.append(dpkg.package)
        depedentPackages=list(set(depedentPackages))
        packageNames=self.getPackageNames()
        for pkgName in packageNames:
            if pkgName in depedentPackages:
                depedentPackages.remove(pkgName)
        return depedentPackages
        
    def getRequiresAllPackagesForGiven(self, pkgName):
        dependentPackages=[]
        for key in self.spec.packages.keys():
            pkg = self.spec.packages.get(key)
            if pkg.name == pkgName:
                for dpkg in pkg.requires:
                    dependentPackages.append(dpkg.package)
        #if (pkgName == "mono-extras"):
    #    print "4given packages:", self.spec.packages
        #    print "4given dep packages: ", dependentPackages
        return dependentPackages
    
    def getBuildRequiresAllPackages(self):
        depedentPackages=[]
        for key in self.spec.packages.keys():
            pkg = self.spec.packages.get(key)
            #if(pkg.name == "mono"):
                #print "build dendent packages len 4 mono-devel:", len(pkg.buildrequires)
            for dpkg in pkg.buildrequires:
                depedentPackages.append(dpkg.package)
        depedentPackages=list(set(depedentPackages))
        packageNames=self.getPackageNames()
        for pkgName in packageNames:
            if pkgName in depedentPackages:
                depedentPackages.remove(pkgName)
        return depedentPackages
        
    
    def getRequires(self,pkgName):
        dependentPackages=[]
        #if( pkgName == "mono-devel"):
            #print "packages:", self.spec.packages
        for key in self.spec.packages.keys():
            pkg = self.spec.packages.get(key)
            if pkg.name == pkgName:
                #if( pkgName == "mono-devel"):
                    #print "dendent packages len 4 mono-devel:", len(pkg.requires), pkg.requires[0].package
                for dpkg in pkg.requires:
                    dependentPackages.append(dpkg.package)
        return dependentPackages

    def getBuildRequires(self,pkgName):
        dependentPackages=[]
        for key in self.spec.packages.keys():
            pkg = self.spec.packages.get(key)
            if pkg.name == pkgName:
                #if( pkgName == "mono-devel"):
                    #print "build dendent packages len 4 mono-devel:", len(pkg.buildrequires), pkg.buildrequires[0].package
                for dpkg in pkg.buildrequires:
                    dependentPackages.append(dpkg.package)
        return dependentPackages
        
    def getProvides(self,packageName):
        depedentPackages=[]
        defaultPkgName=self.spec.packages['default'].name
        pkg = None
        if self.spec.packages.has_key(packageName):
            pkg = self.spec.packages.get(packageName)
        if defaultPkgName == packageName:
            pkg=self.spec.packages['default']
        if pkg is not None:
            for dpkg in pkg.provides:
                depedentPackages.append(dpkg.package)
        else:
            print "package not found"
        return depedentPackages
    
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

def main():
    spec = Specutils("/workspace1/myrepos/photon/SPECS/docker/docker.spec")
    print "packages",spec.getPackageNames()
    print "packages",spec.getRPMNames()
    print "sources",spec.getSourceNames()
    print "patches",spec.getPatchNames()  
    print "requires",spec.getRequires('libltdl-devel')
    print "requires",spec.getRequires('libtool')
    
    print "provides",spec.getProvides('libtool')  
    print "all-requires",spec.getRequiresAllPackages()
    print "all-build-requires",spec.getBuildRequiresAllPackages()
    
if __name__ == '__main__':
    main()
    
