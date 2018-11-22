from SpecUtils import Specutils
import os
import platform
from Logger import Logger
from distutils.version import StrictVersion
import Queue
import json
import operator
from constants import constants
from distutils.version import LooseVersion
from StringUtils import StringUtils

class SpecObject(object):
    def __init__(self):
        self.listPackages=[]
        self.listRPMPackages=[]
        self.name=""
        self.version=""
        self.release=""
        self.buildRequirePackages=[]
        self.checkBuildRequirePackages=[]
        self.installRequiresAllPackages=[]
        self.installRequiresPackages={}
        self.specFile=""
        self.listSources=[]
        self.checksums={}
        self.listPatches=[]
        self.securityHardening=""
        self.url=""
        self.sourceurl=""
        self.license=""
        self.specDefs={}

class SpecObjectsUtils(object):

    def __init__(self,logPath):
        self.mapSpecObjects={}
        self.mapPackageToSpec={}
        self.logger=Logger.getLogger("Serializable Spec objects", logPath )

    def readSpecsAndConvertToSerializableObjects(self, specFilesPath):
        listSpecFiles = []
        self.getListSpecFiles(listSpecFiles,specFilesPath)
        for specFile in listSpecFiles:
            spec = Specutils(specFile)
            specName = spec.getBasePackageName()
            specObj = SpecObject()
            specObj.name=specName
            specObj.buildRequirePackages=spec.getBuildRequiresAllPackages()
            specObj.installRequiresAllPackages=spec.getRequiresAllPackages()
            specObj.checkBuildRequirePackages=spec.getCheckBuildRequiresAllPackages()
            specObj.listPackages=spec.getPackageNames()
            specObj.specFile=specFile
            specObj.version=spec.getVersion()
            specObj.release=spec.getRelease()
            specObj.listSources=spec.getSourceNames()
            specObj.checksums=spec.getChecksums()
            specObj.specDefs=spec.getDefinitions()
            specObj.listPatches=spec.getPatchNames()
            specObj.securityHardening=spec.getSecurityHardeningOption()
            specObj.isCheckAvailable=spec.isCheckAvailable()
            specObj.license=spec.getLicense()
            specObj.url=spec.getURL()
            specObj.sourceurl=spec.getSourceURL()
            for specPkg in specObj.listPackages:
                specObj.installRequiresPackages[specPkg]=spec.getRequires(specPkg)
                self.mapPackageToSpec[specPkg]=specName
                if spec.getIsRPMPackage(specPkg):
                    specObj.listRPMPackages.append(specPkg)
            if specName in self.mapSpecObjects:
                self.mapSpecObjects[specName].append(specObj)
            else:
                self.mapSpecObjects[specName]=[specObj]
        for key, value in self.mapSpecObjects.iteritems():
            if len(value) > 1:
                self.mapSpecObjects[key] = sorted(value, key=lambda x : self.compareVersions(x), reverse=True)

    def getListSpecFiles(self,listSpecFiles,path):
        for dirEntry in os.listdir(path):
            dirEntryPath = os.path.join(path, dirEntry)
            if os.path.isfile(dirEntryPath) and dirEntryPath.endswith(".spec") and os.path.basename(dirEntryPath) not in constants.skipSpecsForArch.get(platform.machine(),[]):
                listSpecFiles.append(dirEntryPath)
            elif os.path.isdir(dirEntryPath):
                self.getListSpecFiles(listSpecFiles,dirEntryPath)

    def _getProperVersion(self,depPkg):
        if (depPkg.compare == ""):
            return self.getHighestVersion(depPkg.package)
        specObjs=self.getSpecObj(depPkg.package)
        try:
            for obj in specObjs:
                verrel=obj.version+"-"+obj.release
                if depPkg.compare == "gte":
                    if LooseVersion(verrel) >= LooseVersion(depPkg.version):
                        return obj.version
                    if LooseVersion(obj.version) >= LooseVersion(depPkg.version):
                        return obj.version
                elif depPkg.compare == "lte":
                    if LooseVersion(verrel) <= LooseVersion(depPkg.version):
                        return obj.version
                    if LooseVersion(obj.version) <= LooseVersion(depPkg.version):
                        return obj.version
                elif depPkg.compare == "eq":
                    if LooseVersion(verrel) == LooseVersion(depPkg.version):
                        return obj.version
                    if LooseVersion(obj.version) == LooseVersion(depPkg.version):
                        return obj.version
                elif depPkg.compare == "lt":
                    if LooseVersion(verrel) < LooseVersion(depPkg.version):
                        return obj.version
                    if LooseVersion(obj.version) < LooseVersion(depPkg.version):
                        return obj.version
                elif depPkg.compare == "gt":
                    if LooseVersion(verrel) > LooseVersion(depPkg.version):
                        return obj.version
                    if LooseVersion(obj.version) > LooseVersion(depPkg.version):
                        return obj.version
        except Exception as e:
            self.logger.error("Exception happened while searching for: " + depPkg.package + depPkg.compare + depPkg.version)
            raise e

        # To ignore Epoch, consider the highest version of the package
        if "epoch" in depPkg.version:
            return self.getHighestVersion(depPkg.package)
        # about to throw exception
        availableVersions=""
        for obj in specObjs:
            availableVersions+=" "+obj.name+"-"+obj.version+"-"+obj.release
        raise Exception("Can not find package: " + depPkg.package + depPkg.compare + depPkg.version + " available specs:"+availableVersions)

    def _getSpecObjField(self, package, version, field):
        specName = self.getSpecName(package)
        for specObj in self.mapSpecObjects[specName]:
            if specObj.version == version:
                return field(specObj)
        self.logger.error("Could not able to find " + package +
                          "-" + version + " package from specs")
        raise Exception("Invalid package: " + package + "-" + version)

    def getBuildRequiresForPackage(self, package, version):
        buildRequiresList=[]
        buildRequiresPackages = self._getSpecObjField(package, version, field=lambda x : x.buildRequirePackages)
        for pkg in buildRequiresPackages:
            properVersion = self._getProperVersion(pkg)
            buildRequiresList.append(pkg.package+"-"+properVersion)
        return buildRequiresList

    def getBuildRequiresForPkg(self, pkg):
        package, version = StringUtils.splitPackageNameAndVersion(pkg)
        return self.getBuildRequiresForPackage(package, version)

    # Returns list of [ "pkg1-vers1", "pkg2-vers2",.. ]
    def getRequiresAllForPackage(self, package, version):
        requiresList=[]
        requiresPackages = self._getSpecObjField(package, version, field=lambda x : x.installRequiresAllPackages)
        for pkg in requiresPackages:
            properVersion = self._getProperVersion(pkg)
            requiresList.append(pkg.package+"-"+properVersion)
        return requiresList

    def getRequiresAllForPkg(self, pkg):
        package, version = StringUtils.splitPackageNameAndVersion(pkg)
        return self.getRequiresAllForPackage(package, version)

    def getRequiresForPackage(self, package, version):
        requiresList=[]
        specName = self.getSpecName(package)
        for specObj in self.mapSpecObjects[specName]:
            if specObj.version == version:
                if package in specObj.installRequiresPackages:
                    requiresPackages = specObj.installRequiresPackages[package]
                    for pkg in requiresPackages:
                        properVersion = self._getProperVersion(pkg)
                        requiresList.append(pkg.package+"-"+properVersion)
                return requiresList
        self.logger.error("Could not able to find " + package +
                          "-" + version + " package from specs")
        raise Exception("Invalid package: " + package + "-" + version)

    def getRequiresForPkg(self, pkg):
        package, version = StringUtils.splitPackageNameAndVersion(pkg)
        return self.getRequiresForPackage(package, version)

    def getCheckBuildRequiresForPackage(self, package, version):
        checkBuildRequiresList=[]
        checkBuildRequiresPackages = self._getSpecObjField(package, version, field=lambda x : x.checkBuildRequirePackages)
        for pkg in checkBuildRequiresPackages:
            properVersion = self._getProperVersion(pkg)
            checkBuildRequiresList.append(pkg.package+"-"+properVersion)
        return checkBuildRequiresList

    def getRelease(self, package, version=None):
        specName=self.getSpecName(package)
        if not version:
            return self.mapSpecObjects[specName][0].release
        for p in self.mapSpecObjects[specName]:
            if p.version == version:
                return p.release
        return None

    def getHighestVersion(self, package):
        specName = self.getSpecName(package)
        return self.mapSpecObjects[specName][0].version

    def getVersions(self, package):
        versions=[]
        specName = self.getSpecName(package)
        for specObj in self.mapSpecObjects[specName]:
            versions.append(specObj.version)
        return versions

    def getSpecFile(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x : x.specFile)

    def getPatches(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x : x.listPatches)

    def getSources(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x : x.listSources)

    def getSHA1(self, package, source, version):
        return self._getSpecObjField(package, version, field=lambda x : x.checksums.get(source))
    # returns list of package names (no versions)
    def getPackages(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x : x.listPackages)

    def getPackagesForPkg(self, pkg):
        pkgs=[]
        package, version = StringUtils.splitPackageNameAndVersion(pkg)
        for p in self.getPackages(package, version):
            pkgs.append(p+"-"+version)
        return pkgs

    def getRPMPackages(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x : x.listRPMPackages)

    @staticmethod
    def compareVersions(p):
        return (StrictVersion(p.version))

    def getSpecName(self,package):
        if package in self.mapPackageToSpec:
            specName=self.mapPackageToSpec[package]
            if specName in self.mapSpecObjects:
                return specName
        self.logger.error("Could not able to find "+package+" package from specs")
        raise Exception("Invalid package:"+package)

    def isRPMPackage(self,package):
        if package in self.mapPackageToSpec:
            specName=self.mapPackageToSpec[package]
            if specName in self.mapSpecObjects:
                return True
        return False

    def getSecurityHardeningOption(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x : x.securityHardening)

    def isCheckAvailable(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x : x.isCheckAvailable)

    def getListPackages(self):
        return self.mapSpecObjects.keys()

    def getURL(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x : x.url)

    def getSourceURL(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x : x.sourceurl)

    def getLicense(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x : x.license)

    def getNumberOfVersions(self, package):
        specName=self.getSpecName(package)
        return len(self.mapSpecObjects[specName])

    def getSpecObj(self, package):
        specName=self.getSpecName(package)
        return self.mapSpecObjects[specName]

    def getPkgNamesFromObj(self, objlist):
        listPkgName=[]
        listPkgNames=list(set(objlist))
        for name in listPkgNames:
                listPkgName.append(name.package)
        listPkgName=list(set(listPkgName))
        return listPkgName

    # Converts "glibc-devel-2.28" into "glibc-2.28"
    def getBasePkg(self, pkg):
        package, version = StringUtils.splitPackageNameAndVersion(pkg)
        return self.getSpecName(package)+"-"+version

    def printAllObjects(self):
        listSpecs=self.mapSpecObjects.keys()
        for spec in listSpecs:
            specObj=self.mapSpecObjects[spec]
            self.logger.info("-----------Spec:"+specObj.name+"--------------")
            self.logger.info("Version:"+specObj.version)
            self.logger.info("Release:"+specObj.release)
            self.logger.info("SpecFile:"+specObj.specFile)
            self.logger.info(" ")
            self.logger.info("Source Files")
            self.logger.info(specObj.listSources)
            self.logger.info(" ")
            self.logger.info("Patch Files")
            self.logger.info(specObj.listPatches)
            self.logger.info(" ")
            self.logger.info(" ")
            self.logger.info("List RPM packages")
            self.logger.info(specObj.listPackages)
            self.logger.info(" ")
            self.logger.info(" ")
            self.logger.info("Build require packages")
            self.logger.info(self.getPkgNamesFromObj(specObj.buildRequirePackages))
            self.logger.info(" ")
            self.logger.info(" ")
            self.logger.info("install require packages")
            self.logger.info(self.getPkgNamesFromObj(specObj.installRequiresAllPackages))
            self.logger.info(" ")
            self.logger.info(specObj.installRequiresPackages)
            self.logger.info("security_hardening: " + specObj.securityHardening)
            self.logger.info("------------------------------------------------")

class SPECS(object):
    __instance = None
    specData = None

    @staticmethod
    def getData():
        """ Static access method. """
        if SPECS.__instance == None:
            SPECS()
        return SPECS.__instance.specData

    def __init__(self):
        """ Virtually private constructor. """
        if SPECS.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            SPECS.__instance = self
        self.initialize()

    def initialize(self):
        # Preparse some files
        #adding openjre8 version rpm macro
        if (platform.machine() == "x86_64"):
            spec = Specutils(constants.specPath + "/openjdk8/openjdk8.spec")
            java8version = spec.getVersion()
            constants.addMacro("JAVA8_VERSION",java8version)


        #adding openjre9 version rpm macro
        if (platform.machine() == "x86_64"):
            spec = Specutils(constants.specPath + "/openjdk9/openjdk9.spec")
            java9version = spec.getVersion()
            constants.addMacro("JAVA9_VERSION",java9version)


        #adding openjre10 version rpm macro
        if (platform.machine() == "x86_64"):
            spec = Specutils(constants.specPath + "/openjdk10/openjdk10.spec")
            java10version = spec.getVersion()
            constants.addMacro("JAVA10_VERSION",java10version)

        #adding kernelversion rpm macro
        spec = Specutils(constants.specPath + "/linux/linux.spec")
        kernelversion = spec.getVersion()
        constants.addMacro("KERNEL_VERSION",kernelversion)

        #adding kernelrelease rpm macro
        kernelrelease = spec.getRelease()
        constants.addMacro("KERNEL_RELEASE",kernelrelease)

        #adding kernelsubrelease rpm macro
        a,b,c = kernelversion.split(".")
        kernelsubrelease = '%02d%02d%03d%03d' % (int(a),int(b),int(c),int(kernelrelease.split('.')[0]))
        if kernelsubrelease:
            kernelsubrelease = "."+kernelsubrelease
            constants.addMacro("kernelsubrelease",kernelsubrelease)

        # Full parsing
        self.specData = SpecObjectsUtils(constants.logPath)
        self.specData.readSpecsAndConvertToSerializableObjects(constants.specPath)
# Little bit of duplication
# Used by SpecVerify and SpecDeps only
class SerializedSpecObjects(object):

    def __init__(self, inputDataDir, stageDir):
        self.mapSpecObjects={}
        self.mapPackageToSpec={}
        self.jsonFilesOutPath = stageDir + "/common/data/"
        self.inputDataDir = inputDataDir

    def _getProperVersion(self,depPkg):
        if (depPkg.compare == ""):
            return self.getHighestVersion(depPkg.package)
        specObjs=self.getSpecObj(depPkg.package)
        try:
            for obj in specObjs:
                verrel=obj.version+"-"+obj.release
                if depPkg.compare == "gte":
                    if LooseVersion(verrel) >= LooseVersion(depPkg.version):
                        return obj.version
                    if LooseVersion(obj.version) >= LooseVersion(depPkg.version):
                        return obj.version
                elif depPkg.compare == "lte":
                    if LooseVersion(verrel) <= LooseVersion(depPkg.version):
                        return obj.version
                    if LooseVersion(obj.version) <= LooseVersion(depPkg.version):
                        return obj.version
                elif depPkg.compare == "eq":
                    if LooseVersion(verrel) == LooseVersion(depPkg.version):
                        return obj.version
                    if LooseVersion(obj.version) == LooseVersion(depPkg.version):
                        return obj.version
                elif depPkg.compare == "lt":
                    if LooseVersion(verrel) < LooseVersion(depPkg.version):
                        return obj.version
                    if LooseVersion(obj.version) < LooseVersion(depPkg.version):
                        return obj.version
                elif depPkg.compare == "gt":
                    if LooseVersion(verrel) > LooseVersion(depPkg.version):
                        return obj.version
                    if LooseVersion(obj.version) > LooseVersion(depPkg.version):
                        return obj.version
        except Exception as e:
            self.logger.error("Exception happened while searching for: " + depPkg.package + depPkg.compare + depPkg.version)
            raise e

        # about to throw exception
        availableVersions=""
        for obj in specObjs:
            availableVersions+=" "+obj.name+"-"+obj.version+"-"+obj.release
        raise Exception("Can not find package: " + depPkg.package + depPkg.compare + depPkg.version + " available specs:"+availableVersions)


    def findTotalRequires(self, allDeps, depQue, parent, displayOption):
        while not depQue.empty():
            pkg = depQue.get()
            for depPkg in self.getRequiresForPkg(pkg):
                if True == allDeps.has_key(depPkg):
                    if(allDeps[depPkg] < allDeps[pkg] + 1):
                        allDeps[depPkg] = allDeps[pkg] + 1
                        parent[depPkg] = pkg
                        self.updateLevels(allDeps, depPkg, parent, allDeps[depPkg])
                else:
                    allDeps[depPkg] = allDeps[pkg] + 1
                    parent[depPkg] = pkg
                    depQue.put(depPkg)

    def findTotalWhoNeedsToBuild(self, depQue, whoBuildDeps, whoBuildDepSet, displayOption):
        while not depQue.empty():
            pkg = depQue.get()
            package, version = StringUtils.splitPackageNameAndVersion(pkg)
            specName = self.getSpecName(package)
            spec=Specutils(self.getSpecFile(package, version))
            RPMName=spec.getRPMName(package)
            debuginfoRPMName=spec.getDebuginfoRPMName(package)
            whoBuildDepSet.add(RPMName)
            whoBuildDepSet.add(debuginfoRPMName)
            if specName is None:
                print(package+"-"+version+" is missing")
            if not whoBuildDeps.has_key(pkg):
                continue
            for depPkg in whoBuildDeps[pkg]:
                depQue.put(depPkg)

    def printTree(self, allDeps, children, curParent , depth):
        if (children.has_key(curParent)):
            for child in children[curParent]:
                print "\t" * depth, child
                self.printTree(allDeps, children, child, depth+1)

    def get_all_package_names(self, jsonFilePath):
        base_path = os.path.dirname(jsonFilePath)
        jsonData = open(jsonFilePath)
        option_list_json = json.load(jsonData)
        jsonData.close()
        packages = option_list_json["packages"]
        return packages

    def updateLevels(self, allDeps, inPkg, parent, level):
        p, version = StringUtils.splitPackageNameAndVersion(inPkg)
        specName = self.getSpecName(p)
        for depPkg in self.getRequiresForPkg(inPkg):
            dp, dv = StringUtils.splitPackageNameAndVersion(depPkg)
            depSpecName = self.getSpecName(dp)
            # ignore circular deps within single spec file
            if (self.getRequiresForPkg(depPkg) is not None and inPkg in self.getRequiresForPkg(depPkg) and depSpecName == specName):
                continue
            if (allDeps.has_key(depPkg) and allDeps[depPkg] < level + 1):
                allDeps[depPkg] = level + 1
                parent[depPkg] = inPkg
                self.updateLevels(allDeps, depPkg, parent, allDeps[depPkg])

    def readSpecsAndConvertToSerializableObjects(self, specFilesPath, inputType, inputValue, displayOption):
        children = {}
        listSpecFiles=[]
        whoNeedsList=[]
        whoBuildDepSet= set()
        independentRPMS=[] # list of all RPMS not built from photon and that must be blindly copied.
        whoBuildDeps = {}
        allDeps={}
        parent={}
        depQue = Queue.Queue()
        packageFound = False
        self.getListSpecFiles(listSpecFiles,specFilesPath)
        for specFile in listSpecFiles:
            spec=Specutils(specFile)
            specName=spec.getBasePackageName()
            specObj=SpecObject()
            specObj.name=specName
            specObj.buildRequirePackages=spec.getBuildRequiresAllPackages()
            specObj.installRequiresAllPackages=spec.getRequiresAllPackages()
            specObj.listPackages=spec.getPackageNames()
            specObj.specFile=specFile
            specObj.version=spec.getVersion()
            specObj.release=spec.getRelease()
            specObj.listSources=spec.getSourceNames()
            specObj.listPatches=spec.getPatchNames()
            specObj.securityHardening=spec.getSecurityHardeningOption()
            for specPkg in specObj.listPackages:
                specObj.installRequiresPackages[specPkg]=spec.getRequires(specPkg)
                if (inputType == "pkg" and inputValue == specPkg): # all the first level dependencies to a dictionary and queue
                    packageFound = True
                    for version in self.getVersions(specPkg):
                        pkg = specPkg+"-"+version
                        for depPkg in self.getRequiresForPkg(pkg):
                            if depPkg not in allDeps:
                                allDeps[depPkg] = 0
                                parent[depPkg] = ""
                                depQue.put(depPkg)
                elif (inputType == "who-needs"):
                    pkg=inputValue+"-"+self.getHighestVersion(inputValue)
                    for version in self.getVersions(specPkg):
                        depPkg = specPkg+"-"+version
                        self.logger.info(depPkg)
                        if pkg in self.getRequiresForPkg(depPkg):
                            whoNeedsList.append(depPkg)
                elif (inputType == "who-needs-build"):
                    pkg=inputValue+"-"+self.getHighestVersion(inputValue)
                    for version in self.getVersions(specPkg):
                        depPkg = specPkg+"-"+version
                        self.logger.info(depPkg)
                        for bdrq in self.getBuildRequiresForPkg(pkg):
                            basePkg = self.getBasePkg(bdrq)
                            if (whoBuildDeps.has_key(basePkg)):
                                whoBuildDeps[basePkg].add(depPkg)
                            else:
                                whoBuildDeps[basePkg] = set()
                                whoBuildDeps[basePkg].add(depPkg)
                    if(inputValue == specPkg):
                        packageFound = True
                        for depPkg in specObj.listPackages:
                            for version in self.getVersions(depPkg):
                                pkg = depPkg+"-"+version
                                depQue.put(pkg)

                self.mapPackageToSpec[specPkg]=specName
                if spec.getIsRPMPackage(specPkg):
                    specObj.listRPMPackages.append(specPkg)
            if specName in self.mapSpecObjects:
                self.mapSpecObjects[specName].append(specObj)
            else:
                self.mapSpecObjects[specName]=[specObj]

        # Generate dependencies for individual packages
        if (inputType == "pkg"):
            if (packageFound == True):
                self.findTotalRequires(allDeps, depQue, parent, displayOption)
            else:
                print "No spec file builds a package named",inputValue
                return

        # Generate dependencies for all packages in the given JSON input file
        elif (inputType == "json"):
            listData = []
            filePath = self.inputDataDir +"/"+ inputValue
            data = self.get_all_package_names(filePath)
            for pkgInData in data:
                for version in self.getVersions(pkgInData):
                    listData.append(pkgInData+"-"+version)
            for pkg in listData:
                if False == allDeps.has_key(pkg):
                    p, version = StringUtils.splitPackageNameAndVersion(pkg)
                    spName = self.getSpecName(p)
                    if(spName != None):
                        allDeps[pkg] = 0
                        parent[pkg] = ""
                        depQue.put(pkg)
                        self.findTotalRequires(allDeps, depQue, parent, displayOption)
                    else:
                        independentRPMS.append(pkg);

        #Generating the list of packages that requires the given input package at install time
        elif (inputType == "who-needs"):
            print whoNeedsList
            return

        #Generating the list of packages that the modified package will affect at build time
        elif (inputType == "who-needs-build"):
            if (packageFound == True):
                self.findTotalWhoNeedsToBuild(depQue, whoBuildDeps, whoBuildDepSet, displayOption)
                print whoBuildDepSet
            else:
                print "No spec file builds a package named", inputValue
            return

        # construct the sorted list of all packages (sorted by dependency)
        sortedList = []
        for elem in sorted(allDeps.items(), key=operator.itemgetter(1), reverse=True):
            sortedList.append(elem[0])
        sortedList.extend(independentRPMS)

        # construct all children nodes
        if (displayOption == "tree"):
            for k, v in parent.iteritems():
                children.setdefault(v, []).append(k)
            if(inputType == "json"):
                print "Dependency Mappings for", inputValue, ":", "\n----------------------------------------------------",children
                print "----------------------------------------------------"
            if (children.has_key("")):
                for child in children[""]:
                    print child
                    self.printTree(allDeps, children, child, 1)
                for pkg in independentRPMS:
                    print pkg
                print "******************",len(sortedList), "packages in total ******************"
            else:
                if (inputType == "pkg" and len(children) > 0):
                    print "cyclic dependency detected, mappings: \n",children

        # To display a flat list of all packages
        elif(displayOption == "list"):
            print sortedList

        # To generate a new JSON file based on given input json file
        elif(displayOption == "json" and inputType == "json"):
            d = {}
            d['packages'] = sortedList
            outFilePath = self.jsonFilesOutPath + inputValue
            with open(outFilePath, 'wb') as outfile:
                json.dump(d, outfile)
        return sortedList

    def getSpecObj(self, package):
        specName=self.getSpecName(package)
        return self.mapSpecObjects[specName]

    def _getSpecObjField(self, package, version, field):
        specName = self.getSpecName(package)
        for specObj in self.mapSpecObjects[specName]:
            if specObj.version == version:
                return field(specObj)
        self.logger.error("Could not able to find " + package +
                          "-" + version + " package from specs")
        raise Exception("Invalid package: " + package + "-" + version)

    def getListSpecFiles(self,listSpecFiles,path):
        for dirEntry in os.listdir(path):
            dirEntryPath = os.path.join(path, dirEntry)
            if os.path.isfile(dirEntryPath) and dirEntryPath.endswith(".spec") and os.path.basename(dirEntryPath) not in constants.skipSpecsForArch.get(platform.machine(),[]):
                listSpecFiles.append(dirEntryPath)
            elif os.path.isdir(dirEntryPath):
                self.getListSpecFiles(listSpecFiles,dirEntryPath)

    def getBuildRequiresForPackage(self, package, version):
        buildRequiresList=[]
        buildRequiresPackages = self._getSpecObjField(package, version, field=lambda x : x.buildRequirePackages)
        for pkg in buildRequiresPackages:
            properVersion = self._getProperVersion(pkg)
            buildRequiresList.append(pkg.package+"-"+properVersion)
        return buildRequiresList

    def getBuildRequiresForPkg(self, pkg):
        package, version = StringUtils.splitPackageNameAndVersion(pkg)
        return self.getBuildRequiresForPackage(package, version)

    # Returns list of [ "pkg1-vers1", "pkg2-vers2",.. ]
    def getRequiresAllForPackage(self, package, version):
        requiresList=[]
        requiresPackages = self._getSpecObjField(package, version, field=lambda x : x.installRequiresAllPackages)
        for pkg in requiresPackages:
            properVersion = self._getProperVersion(pkg)
            requiresList.append(pkg.package+"-"+properVersion)
        return requiresList

    def getRequiresAllForPkg(self, pkg):
        package, version = StringUtils.splitPackageNameAndVersion(pkg)
        return self.getRequiresAllForPackage(package, version)

    def getRequiresForPackage(self, package, version):
        requiresList=[]
        specName = self.getSpecName(package)
        for specObj in self.mapSpecObjects[specName]:
            if specObj.version == version:
                if package in specObj.installRequiresPackages:
                    requiresPackages = specObj.installRequiresPackages[package]
                    for pkg in requiresPackages:
                        properVersion = self._getProperVersion(pkg)
                        requiresList.append(pkg.package+"-"+properVersion)
                return requiresList
        self.logger.error("Could not able to find " + package +
                          "-" + version + " package from specs")
        raise Exception("Invalid package: " + package + "-" + version)

    def getRequiresForPkg(self, pkg):
        package, version = StringUtils.splitPackageNameAndVersion(pkg)
        return self.getRequiresForPackage(package, version)

    def getRelease(self, package, version=None):
        specName=self.getSpecName(package)
        if not version:
            return self.mapSpecObjects[specName][0].release
        for p in self.mapSpecObjects[specName]:
            if p.version == version:
                return p.release
        return None

    def getVersions(self, package):
        versions=[]
        specName = self.getSpecName(package)
        for specObj in self.mapSpecObjects[specName]:
            versions.append(specObj.version)
        return versions

    def getHighestVersion(self, package):
        specName = self.getSpecName(package)
        return self.mapSpecObjects[specName][0].version

    def getSpecFile(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x : x.specFile)

    def getPatches(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x : x.listPatches)

    def getSources(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x : x.listSources)

    def getPackages(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x : x.listPackages)

    def getSpecName(self,package):
        if package in self.mapPackageToSpec:
            specName=self.mapPackageToSpec[package]
            if specName in self.mapSpecObjects:
                return specName
            else:
                print "SpecDeps: Could not able to find " + package + " package from specs"
                raise Exception("Invalid package:" + package)
        else:
            return None

    def isRPMPackage(self,package):
        if self.mapPackageToSpec.has_key(package):
            specName=self.mapPackageToSpec[package]
        if self.mapSpecObjects.has_key(specName):
            return True
        return False

    def getBasePkg(self, pkg):
        package, version = StringUtils.splitPackageNameAndVersion(pkg)
        return self.getSpecName(package)+"-"+version

    def getSecurityHardeningOption(self, package, version):
        return self._getSpecObjField(package, version, field=lambda x : x.securityHardening)

    def getSpecDetails(self, name):
        print self.getPkgNamesFromObj(self.mapSpecObjects[name].installRequiresAllPackages)

