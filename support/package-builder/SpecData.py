from SpecUtils import Specutils
import os
import platform
from Logger import Logger
from distutils.version import StrictVersion
import Queue
import json
import operator
from constants import constants

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

    def getBuildRequiresForPackage(self, package, index=0):
        specName=self.getSpecName(package)
        return self.mapSpecObjects[specName][index].buildRequirePackages

    def getRequiresAllForPackage(self, package, index=0):
        specName=self.getSpecName(package)
        return self.mapSpecObjects[specName][index].installRequiresAllPackages

    def getRequiresForPackage(self, package, index=0):
        specName=self.getSpecName(package)
        if self.mapSpecObjects[specName][index].installRequiresPackages.has_key(package):
            return self.mapSpecObjects[specName][index].installRequiresPackages[package]
        return None

    def getCheckBuildRequiresForPackage(self, package, index=0):
        specName=self.getSpecName(package)
        return self.mapSpecObjects[specName][index].checkBuildRequirePackages

    def getRelease(self, package, version=None):
        specName=self.getSpecName(package)
        if not version:
            return self.mapSpecObjects[specName][0].release
        for p in self.mapSpecObjects[specName]:
            if p.version == version:
                return p.release
        return None

    def getVersion(self, package, index=0):
        specName=self.getSpecName(package)
        return self.mapSpecObjects[specName][index].version

    def getSpecFile(self, package, index=0):
        specName=self.getSpecName(package)
        return self.mapSpecObjects[specName][index].specFile

    def getPatches(self, package, index=0):
        specName=self.getSpecName(package)
        return self.mapSpecObjects[specName][index].listPatches

    def getSources(self, package, index=0):
        specName=self.getSpecName(package)
        return self.mapSpecObjects[specName][index].listSources

    def getSHA1(self, package, source, index=0):
        specName=self.getSpecName(package)
        return self.mapSpecObjects[specName][index].checksums.get(source)

    def getPackages(self, package, index=0):
        specName=self.getSpecName(package)
        return self.mapSpecObjects[specName][index].listPackages

    def getRPMPackages(self, package, index=0):
        specName=self.getSpecName(package)
        return self.mapSpecObjects[specName][index].listRPMPackages

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

    def isRPMPackage(self,package, index=0):
        if package in self.mapPackageToSpec:
            specName=self.mapPackageToSpec[package]
            if specName in self.mapSpecObjects:
                return True
        return False

    def getSecurityHardeningOption(self, package, index=0):
        specName=self.getSpecName(package)
        return self.mapSpecObjects[specName][index].securityHardening

    def isCheckAvailable(self, package, index=0):
        specName=self.getSpecName(package)
        return self.mapSpecObjects[specName][index].isCheckAvailable

    def getListPackages(self):
        return self.mapSpecObjects.keys()

    def getURL(self, package, index=0):
        specName=self.getSpecName(package)
        return self.mapSpecObjects[specName][index].url

    def getSourceURL(self, package, index=0):
        specName=self.getSpecName(package)
        return self.mapSpecObjects[specName][index].sourceurl

    def getLicense(self, package, index=0):
        specName=self.getSpecName(package)
        return self.mapSpecObjects[specName][index].license

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

    def findTotalRequires(self, allDeps, depQue, parent, displayOption):
        while not depQue.empty():
            specPkg = depQue.get()
            specName = self.getSpecName(specPkg)
            if specName is None:
                print specPkg + " is missing"
            specObj = self.mapSpecObjects[specName]
            for depPkg in specObj.installRequiresPackages[specPkg]:
                if True == allDeps.has_key(depPkg):
                    if(allDeps[depPkg] < allDeps[specPkg] + 1):
                        allDeps[depPkg] = allDeps[specPkg] + 1
                        parent[depPkg] = specPkg
                        self.updateLevels(allDeps, depPkg, parent, allDeps[depPkg])
                else:
                    allDeps[depPkg] = allDeps[specPkg] + 1
                    parent[depPkg] = specPkg
                    depQue.put(depPkg)

    def findTotalWhoNeedsToBuild(self, depQue, whoBuildDeps, whoBuildDepSet, displayOption):
        while not depQue.empty():
            specPkg = depQue.get()
            specName = self.getSpecName(specPkg)
            spec=Specutils(self.getSpecFile(specPkg))
            RPMName=spec.getRPMName(specPkg)
            debuginfoRPMName=spec.getDebuginfoRPMName(specPkg)
            whoBuildDepSet.add(RPMName)
            whoBuildDepSet.add(debuginfoRPMName)
            if specName is None:
                print specPkg + " is missing"
            if not whoBuildDeps.has_key(specPkg):
                continue
            for depPkg in whoBuildDeps[specPkg]:
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
        specName = self.getSpecName(inPkg)
        specObj = self.mapSpecObjects[specName]
        for depPkg in specObj.installRequiresPackages[inPkg]:
            # ignore circular deps within single spec file
            if (specObj.installRequiresPackages.has_key(depPkg) and inPkg in specObj.installRequiresPackages[depPkg] and self.getSpecName(depPkg) == specName):
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
                    for depPkg in specObj.installRequiresPackages[specPkg]:
                        if False == allDeps.has_key(depPkg):
                            allDeps[depPkg] = 0
                            parent[depPkg] = ""
                            depQue.put(depPkg)
                elif (inputType == "who-needs" and (inputValue in specObj.installRequiresPackages[specPkg])):
                    whoNeedsList.append(specPkg)
                elif (inputType == "who-needs-build"):
                    for bdrq in specObj.buildRequirePackages:
                        if (whoBuildDeps.has_key(bdrq.package)):
                            whoBuildDeps[bdrq.package].add(specPkg)
                        else:
                            whoBuildDeps[bdrq.package] = set()
                            whoBuildDeps[bdrq.package].add(specPkg)
                    if(inputValue == specPkg):
                        packageFound = True
                        for depPkg in specObj.listPackages:
                            depQue.put(depPkg)

                self.mapPackageToSpec[specPkg]=specName
            self.mapSpecObjects[specName]=specObj

        # Generate dependencies for individual packages
        if (inputType == "pkg"):
            if (packageFound == True):
                self.findTotalRequires(allDeps, depQue, parent, displayOption)
            else:
                print "No spec file builds a package named",inputValue
                return

        # Generate dependencies for all packages in the given JSON input file
        elif (inputType == "json"):
            filePath = self.inputDataDir +"/"+ inputValue
            data = self.get_all_package_names(filePath)
            for pkg in data:
                if False == allDeps.has_key(pkg):
                    spName = self.getSpecName(pkg)
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

    def getListSpecFiles(self,listSpecFiles,path):
        for dirEntry in os.listdir(path):
            dirEntryPath = os.path.join(path, dirEntry)
            if os.path.isfile(dirEntryPath) and dirEntryPath.endswith(".spec") and os.path.basename(dirEntryPath) not in constants.skipSpecsForArch.get(platform.machine(),[]):
                listSpecFiles.append(dirEntryPath)
            elif os.path.isdir(dirEntryPath):
                self.getListSpecFiles(listSpecFiles,dirEntryPath)

    def getBuildRequiresForPackage(self, package):
        specName=self.getSpecName(package)
        return self.mapSpecObjects[specName].buildRequirePackages

    def getRequiresForPackage(self, package):
        specName=self.getSpecName(package)
        if self.mapSpecObjects[specName].installRequiresPackages.has_key(package):
            return self.mapSpecObjects[specName].installRequiresPackages[package]
        return None

    def getRelease(self, package):
        specName=self.getSpecName(package)
        return self.mapSpecObjects[specName].release

    def getVersion(self, package):
        specName=self.getSpecName(package)
        return self.mapSpecObjects[specName].version

    def getSpecFile(self, package):
        specName=self.getSpecName(package)
        return self.mapSpecObjects[specName].specFile

    def getPatches(self, package):
        specName=self.getSpecName(package)
        return self.mapSpecObjects[specName].listPatches

    def getSources(self, package):
        specName=self.getSpecName(package)
        return self.mapSpecObjects[specName].listSources

    def getPackages(self, package):
        specName=self.getSpecName(package)
        return self.mapSpecObjects[specName].listPackages

    def getSpecName(self,package):
        if self.mapPackageToSpec.has_key(package):
            specName=self.mapPackageToSpec[package]
            if self.mapSpecObjects.has_key(specName):
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

    def getSecurityHardeningOption(self, package):
        specName=self.getSpecName(package)
        return self.mapSpecObjects[specName].securityHardening

    def getSpecDetails(self, name):
        print self.getPkgNamesFromObj(self.mapSpecObjects[name].installRequiresAllPackages)

