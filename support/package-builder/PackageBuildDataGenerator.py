from Logger import Logger
from collections import OrderedDict
from constants import constants
from sets import Set
import copy
from SpecData import SPECS



class PackageBuildDataGenerator(object):

    cycleCount=0

    def __init__(self,logName=None,logPath=None):
        if logName is None:
            logName = "PackageBuildDataGenerator"
        if logPath is None:
            logPath = constants.logPath
        self.logName=logName
        self.logPath=logPath
        self.logger=Logger.getLogger(logName,logPath)
        self.__mapCyclesToPackageList={}
        self.__mapPackageToCycle={}
        self.__buildDependencyGraph={}
        self.__runTimeDependencyGraph={}
        self.__sortedPackageList=[]
        self.__sortedBuildDependencyGraph={}

    def removeDuplicateEntries(self, myList):
        myListCopy = list(OrderedDict.fromkeys(myList))
        return myListCopy

    def getPackageBuildData(self,listPackages):
        basePackages = []
        for pkg in listPackages:
            basePackages.append(SPECS.getData().getBasePkg(pkg))
        self.__readDependencyGraphAndCyclesForGivenPackages(basePackages)
        self.__getSortedBuildOrderListForGivenPackages()
        return self.__mapCyclesToPackageList, self.__mapPackageToCycle, self.__sortedPackageList

    #todo
    def findCompleteListOfPackagesRequiredToBuildGivenPackages(self):
        return list(self.__buildDependencyGraph.keys())

    def createSortListForPkg(self,pkg):
        runTimeDepPkgList=list(set(self.__runTimeDependencyGraph[pkg]))
        runTimeDepPkgList.append(pkg)
        sortListForPkg=[]

        for p in runTimeDepPkgList:
            basePkg=SPECS.getData().getBasePkg(p)
            for bPkg in self.__sortedBuildDependencyGraph[basePkg]:
                if bPkg not in sortListForPkg:
                    sortListForPkg.append(bPkg)

        return sortListForPkg

    def getCircularDependentPackages(self,pkg):
        circularDependentPackages=[]
        if self.__mapPackageToCycle.has_key(pkg):
            circularDependentPackages.extend(self.__mapCyclesToPackageList[self.__mapPackageToCycle[pkg]])
            circularDependentPackages.remove(pkg)
        return circularDependentPackages

    def __getSortedBuildOrderListForGivenPackages(self):

        alreadyProcessedPackages = set()
        sortedList = []
        completeListPackagesToBuild = self.findCompleteListOfPackagesRequiredToBuildGivenPackages()
        packageIndexInSortedList = 0
        prevSortListLen = 0

        while completeListPackagesToBuild:

            # find next package to process
            pkg = None
            index = -1
            lenList = len(sortedList)
            for i in range(lenList):
                if sortedList[i] in alreadyProcessedPackages:
                    continue
                pkg = sortedList[i]
                packageIndexInSortedList = i
                break

            if pkg is None:
                pkg = completeListPackagesToBuild.pop()
                packageIndexInSortedList = len(sortedList)

            #creating sort list for package
            sortListForPkg = self.createSortListForPkg(pkg)

            #remove any cyclic packages in sortListForPkg if they already
            #exists in sortedList
            circularDependentPackages = self.getCircularDependentPackages(pkg)
            for p in circularDependentPackages:
                if p in sortedList and p in sortListForPkg:
                    sortListForPkg.remove(p)

            # insert sort list of package in global sorted list
            index = packageIndexInSortedList
            subList = []
            if packageIndexInSortedList > 0:
                subList = sortedList[:packageIndexInSortedList]
            for p in sortListForPkg:
                if  p not in subList:
                    sortedList.insert(index, p)
                    index = index + 1

            alreadyProcessedPackages.add(p)

            # Remove duplicate entries in sorted list in intervals
            if (len(sortedList) - prevSortListLen) > 100:
                self.logger.debug("Removing duplicates in sortedList")
                sortedList = self.removeDuplicateEntries(sortedList)
            else:
                prevSortListLen = len(sortedList)

        self.logger.debug("Removing duplicates in sorted list")
        sortedList = self.removeDuplicateEntries(sortedList)

        self.logger.debug("Sorted list: ")
        self.logger.debug(sortedList)
        self.__sortedPackageList = sortedList

    def __constructBuildAndRunTimeDependencyGraph(self, basePackage):
        addBuildTimeGraph = True
        addRunTimeGraph = True
        if basePackage in self.__buildDependencyGraph:
            addBuildTimeGraph = False
        if basePackage in self.__runTimeDependencyGraph:
            addRunTimeGraph = False

        nextPackagesToConstructGraph = set()
        if addBuildTimeGraph:
            dependentRpmPackages = SPECS.getData().getBuildRequiresForPkg(basePackage)
            dependentPackages = set()
            for dependentPkg in dependentRpmPackages:
                dependentPackages.add(SPECS.getData().getBasePkg(dependentPkg))
            self.__buildDependencyGraph[basePackage] = dependentPackages
            nextPackagesToConstructGraph.update(dependentPackages)

        if addRunTimeGraph:
            dependentPackages = set()
            for rpmPkg in SPECS.getData().getPackagesForPkg(basePackage):
                dependentRpmPackages = SPECS.getData().getRequiresAllForPkg(rpmPkg)
                self.__runTimeDependencyGraph[rpmPkg] = copy.copy(set(dependentRpmPackages))
                for pkg in dependentRpmPackages:
                    dependentPackages.add(SPECS.getData().getBasePkg(pkg))
            nextPackagesToConstructGraph.update(dependentPackages)
        for pkg in nextPackagesToConstructGraph:
            self.__constructBuildAndRunTimeDependencyGraph(pkg)

    def __readDependencyGraphAndCyclesForGivenPackages(self,listPackages):
        self.logger.info("Reading dependency graph to check for cycles")
        for pkg in listPackages:
            self.__constructBuildAndRunTimeDependencyGraph(pkg)
        packagesToBUild=self.__buildDependencyGraph.keys()
        for pkg in packagesToBUild:
            sortedPackageList,circularDependentPackages = self.topologicalSortPackages(self.__buildDependencyGraph,pkg)
            if len(circularDependentPackages) > 0 :
                self.logger.error("Found circular dependency")
                self.logger.error(circularDependentPackages)
                raise Exception("Build Time Circular Dependency")
            self.__sortedBuildDependencyGraph[pkg]=sortedPackageList
        sortedPackageList,circularDependentPackages = self.topologicalSortPackages(self.__runTimeDependencyGraph)
        if len(circularDependentPackages) > 0 :
            self.__findCircularDependencies(circularDependentPackages)

    @staticmethod
    def _buildDependentPackages(dependencyGraph, package):
        dependentPackages = {}
        if package is None:
            dependentPackages = copy.deepcopy(dependencyGraph)
        else:
            depPkgs = set()
            depPkgs.add(package)
            while depPkgs:
                pkg = depPkgs.pop()
                if pkg in dependentPackages:
                    continue
                dependentPackages[pkg] = copy.copy(dependencyGraph[pkg])
                for depPkg in dependencyGraph[pkg]:
                    depPkgs.add(depPkg)
        return dependentPackages

    @staticmethod
    def _buildDependentOfPackages(dependentPackages):
        dependentOfPackage = dict()
        for pkg in dependentPackages:
            if dependentPackages[pkg]:
                for depPkg in dependentPackages[pkg]:
                    if depPkg not in dependentOfPackage:
                        dependentOfPackage[depPkg] = {pkg}
                    else:
                        dependentOfPackage[depPkg].add(pkg)
        return dependentOfPackage

    @staticmethod
    def topologicalSortPackages(dependencyGraph, package=None):
        sortedPackageList = []
        noDepPackages = set()
        dependentPackages = PackageBuildDataGenerator._buildDependentPackages(
            dependencyGraph, package)
        dependentOfPackage = PackageBuildDataGenerator._buildDependentOfPackages(
            dependentPackages)

        #Find packages with no dependencies and generate dependentof_package edge list
        for pkg in dependentPackages:
            if not dependentPackages[pkg]:
                noDepPackages.add(pkg)

        while noDepPackages:
            pkg = noDepPackages.pop()
            sortedPackageList.append(pkg)
            if pkg in dependentOfPackage:
                for childPkg in list(dependentOfPackage[pkg]):
                    dependentOfPackage[pkg].remove(childPkg)
                    dependentPackages[childPkg].remove(pkg)
                    if not dependentPackages[childPkg]:
                        noDepPackages.add(childPkg)

        # creating circular dependency graph for given dependency graph
        circularDependencyGraph = {}
        for pkg in dependentPackages.keys():
            if dependentPackages[pkg]:
                circularDependencyGraph[pkg] = dependentPackages[pkg]

        #return (non-circular dependent package in sorted order and circular dependent
        #package list in a dependencyGraph)
        return sortedPackageList, circularDependencyGraph

    def __constructDependencyMap(self,cyclicDependencyGraph):
        self.logger.info("Constructing dependency map from circular dependency graph.....")
        constructDependencyMap={}
        listNodes=cyclicDependencyGraph.keys()
        for node in listNodes:
            tmpDepNodeList=[]
            tmpDepNodeList.append(node)
            depNodeList=[]
            while len(tmpDepNodeList)!=0:
                currentNode = tmpDepNodeList.pop()
                addDepNodeList = cyclicDependencyGraph[currentNode]
                depNodeList.append(currentNode)
                for depNode in addDepNodeList:
                    if depNode in depNodeList:
                        continue
                    else:
                        if depNode not in tmpDepNodeList:
                            tmpDepNodeList.append(depNode)
            depNodeList.remove(node)
            constructDependencyMap[node]=depNodeList
        self.logger.info("Dependency Map:")
        self.logger.info(constructDependencyMap)
        return constructDependencyMap


    def __findCircularDependencies(self,cyclicDependencyGraph):
        self.logger.info("Looking for circular dependencies")
        if len(cyclicDependencyGraph) == 0:
            return
        #step1: construct dependency map from dependency graph
        constructDependencyMap=self.__constructDependencyMap(cyclicDependencyGraph)

        #step2: find cycles in dependency map
        self.logger.info("Finding and adding cycles using constructed dependency map......")
        cycleCount=0
        listNodes=cyclicDependencyGraph.keys()
        for node in listNodes:
            listDepPkg=constructDependencyMap[node]
            cycPkgs=[]
            if not self.__mapPackageToCycle.has_key(node):
                for depPkg in listDepPkg:
                    x = constructDependencyMap[depPkg]
                    if node in x:
                        cycPkgs.append(depPkg)

                if len(cycPkgs) != 0:
                    cycPkgs.append(node)
                    cycleName="cycle"+str(PackageBuildDataGenerator.cycleCount)
                    PackageBuildDataGenerator.cycleCount=PackageBuildDataGenerator.cycleCount+1
                    for x in cycPkgs:
                        self.__mapPackageToCycle[x]=cycleName
                    self.__mapCyclesToPackageList[cycleName]=cycPkgs
                    self.logger.info("New circular dependency found:")
                    self.logger.info(cycleName+" "+ ",".join(cycPkgs))
                    cycleCount = cycleCount + 1

        if cycleCount > 0 :
            self.logger.info("Found "+str(cycleCount) + " cycles.")
            self.logger.info("Successfully added all detected circular dependencies to list.")
        else:
            self.logger.info("No circular dependencies found.")

