from SpecUtils import Specutils
from StringUtils import StringUtils
import operator
import os
import collections
import Queue
import json

class SerializableSpecObject(object):
    def __init__(self):
        self.listPackages=[]
        self.name=""
        self.version=""
        self.release=""
        self.buildRequirePackages=[]
        self.installRequiresAllPackages=[]
        self.installRequiresPackages={}
        self.specFile=""
        self.listSources=[]
        self.listPatches=[]
        self.securityHardening=""

class SerializedSpecObjects(object):

    def __init__(self, inputDataDir, stageDir):
        self.mapSerializableSpecObjects={}
        self.mapPackageToSpec={}
        self.jsonFilesOutPath = stageDir + "/common/data/"
        self.inputDataDir = inputDataDir

    def findTotalRequires(self, allDeps, depQue, parent, displayOption):
        while not depQue.empty():
            specPkg = depQue.get()
            specName = self.getSpecName(specPkg)
            specObj = self.mapSerializableSpecObjects[specName]
            for depPkg in specObj.installRequiresPackages[specPkg]:
                if depPkg in allDeps:
                    if(allDeps[depPkg] < allDeps[specPkg] + 1):
                        allDeps[depPkg] = allDeps[specPkg] + 1
                        parent[depPkg] = specPkg
                        self.updateLevels(allDeps, depPkg, parent, allDeps[depPkg])
                else:
                    allDeps[depPkg] = allDeps[specPkg] + 1
                    parent[depPkg] = specPkg
                    depQue.put(depPkg)

    def printTree(self, allDeps, children, curParent , depth):
        if (curParent in children):
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
        specObj = self.mapSerializableSpecObjects[specName]
        for depPkg in specObj.installRequiresPackages[inPkg]:
            if (depPkg in allDeps and allDeps[depPkg] < level + 1):
                allDeps[depPkg] = level + 1
                parent[depPkg] = inPkg
                self.updateLevels(allDeps, depPkg, parent, allDeps[depPkg])

    def readSpecsAndConvertToSerializableObjects(self, specFilesPath, inputType, inputValue, displayOption):
        children = {}
        listSpecFiles=[]
        whoNeedsList=[]
        independentRPMS=[] # list of all RPMS not built from photon and that must be blindly copied.
        allDeps={}
        parent={}
        depQue = Queue.Queue()
        packageFound = False
        self.getListSpecFiles(listSpecFiles,specFilesPath)
        for specFile in listSpecFiles:
            spec=Specutils(specFile)
            specName=spec.getBasePackageName()
            specObj=SerializableSpecObject()
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
                        if depPkg not in allDeps:
                            allDeps[depPkg] = 0
                            parent[depPkg] = ""
                            depQue.put(depPkg)
                if (inputType == "who-needs" and (inputValue in specObj.installRequiresPackages[specPkg])):
                    whoNeedsList.append(specPkg)
                self.mapPackageToSpec[specPkg]=specName
            self.mapSerializableSpecObjects[specName]=specObj

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
                if pkg not in allDeps:
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
            if "" in children:
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
            if os.path.isfile(dirEntryPath) and dirEntryPath.endswith(".spec"):
                listSpecFiles.append(dirEntryPath)
            elif os.path.isdir(dirEntryPath):
                self.getListSpecFiles(listSpecFiles,dirEntryPath)

    def getBuildRequiresForPackage(self, package):
        specName=self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].buildRequirePackages

    def getRequiresForPackage(self, package):
        specName=self.getSpecName(package)
        if package in self.mapSerializableSpecObjects[specName].installRequiresPackages:
            return self.mapSerializableSpecObjects[specName].installRequiresPackages[package]
        return None

    def getRelease(self, package):
        specName=self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].release

    def getVersion(self, package):
        specName=self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].version

    def getSpecFile(self, package):
        specName=self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].specFile

    def getPatches(self, package):
        specName=self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].listPatches

    def getSources(self, package):
        specName=self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].listSources

    def getPackages(self, package):
        specName=self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].listPackages

    def getSpecName(self,package):
        if package in self.mapPackageToSpec:
            specName=self.mapPackageToSpec[package]
            if specName in self.mapSerializableSpecObjects:
                return specName
            else:
                print "SpecDeps: Could not able to find " + package + " package from specs"
                raise Exception("Invalid package:" + package)
        else:
            return None

    def isRPMPackage(self,package):
        if package in self.mapPackageToSpec:
            specName=self.mapPackageToSpec[package]
        if specName in self.mapSerializableSpecObjects:
            return True
        return False

    def getSecurityHardeningOption(self, package):
        specName=self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].securityHardening

    def getSpecDetails(self, name):
        print self.mapSerializableSpecObjects[name].installRequiresAllPackages

