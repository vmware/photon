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
			if True == allDeps.has_key(depPkg): 
				if(allDeps[depPkg] < allDeps[specPkg] + 1): 
					allDeps[depPkg] = allDeps[specPkg] + 1
					parent[depPkg] = specPkg
					self.updateLevels(allDeps, depPkg, parent, allDeps[depPkg])
			else:
				allDeps[depPkg] = allDeps[specPkg] + 1
				parent[depPkg] = specPkg
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
        specObj  = self.mapSerializableSpecObjects[specName]
        for depPkg in specObj.installRequiresPackages[inPkg]:
		if (allDeps.has_key(depPkg) and allDeps[depPkg] < level + 1): 
	   		allDeps[depPkg] = level + 1
			parent[depPkg] = inPkg
			                 
    def readSpecsAndConvertToSerializableObjects(self, specFilesPath, inputType, inputValue, displayOption):
		children = {}
		listSpecFiles=[]
		whoNeedsList=[]
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
				if( inputType == "pkg" and inputValue == specPkg): # all all the first level dependencies to a dictionary and queue 
				    packageFound = True
				    for depPkg in specObj.installRequiresPackages[specPkg]:
					if False == allDeps.has_key(depPkg):
								allDeps[depPkg] = 0
								parent[depPkg] = ""
								depQue.put(depPkg)
				if (inputType == "who-needs"):
					if (inputValue in specObj.installRequiresPackages[specPkg]):
						whoNeedsList.append(specPkg)
				self.mapPackageToSpec[specPkg]=specName
			self.mapSerializableSpecObjects[specName]=specObj		
		if (inputType == "pkg"):
			if (packageFound == True):
				self.findTotalRequires(allDeps, depQue, parent, displayOption)
			else:
				print "No spec file builds a package named",inputValue
  	  			return
		elif (inputType == "json"):
			filePath = self.inputDataDir +"/"+ inputValue
			data = self.get_all_package_names(filePath)
			#print data
			for pkg in data:
				if False == allDeps.has_key(pkg):
					allDeps[pkg] = 0 
					parent[pkg] = ""
					depQue.put(pkg)
					self.findTotalRequires(allDeps, depQue, parent, displayOption)
		elif (inputType == "who-needs"):
			print whoNeedsList
		# construct the sorted list of all packages (sorted by dependency)
		sortedList = []
		for elem in sorted(allDeps.items(), key=operator.itemgetter(1), reverse=True):
			sortedList.append(elem[0])
		# construct all children nodes
		if (displayOption == "tree"):
			#print "parent:" ,parent
			for k, v in parent.iteritems():
				children.setdefault(v, []).append(k)
			if(inputType == "json"):
				print "Dependency Mappings:\n", children
			if (children.has_key("")):
				for child in children[""]:
					print child
					self.printTree(allDeps, children, child, 1)
			else:
				if (inputType == "pkg" and len(children) > 0):
					print "cyclic dependency mappings: \n",children
		elif(displayOption == "list"):
			print sortedList
		elif(displayOption == "json" and inputType == "json"):
			d = {}
			d['packages'] = sortedList
			outFilePath = self.jsonFilesOutPath + inputValue
			with open(outFilePath, 'wb') as outfile:
    				json.dump(d, outfile)		
	
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
        if self.mapSerializableSpecObjects[specName].installRequiresPackages.has_key(package):
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
        if self.mapPackageToSpec.has_key(package):
            specName=self.mapPackageToSpec[package]
            if self.mapSerializableSpecObjects.has_key(specName):
                return specName
        print "SpecDeps: Could not able to find "+package+" package from specs"
        raise Exception("Invalid package:"+package)
    
    def isRPMPackage(self,package):
        if self.mapPackageToSpec.has_key(package):
            specName=self.mapPackageToSpec[package]
            if self.mapSerializableSpecObjects.has_key(specName):
                return True
        return False
    
    def getSecurityHardeningOption(self, package):
        specName=self.getSpecName(package)
        return self.mapSerializableSpecObjects[specName].securityHardening
        
    def getSpecDetails(self, name):
    	print self.mapSerializableSpecObjects[name].installRequiresAllPackages 

