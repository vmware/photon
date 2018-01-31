import copy
from Logger import Logger
from constants import constants
from SpecData import SPECS
from collections import OrderedDict

def removeDuplicateEntries(myList):
    myListCopy = list(OrderedDict.fromkeys(myList))
    return myListCopy

class PackageBuildDataGenerator(object):

    cycleCount = 0

    def __init__(self, logName=None, logPath=None):
        if logName is None:
            logName = "PackageBuildDataGenerator"
        if logPath is None:
            logPath = constants.logPath
        self.logName = logName
        self.logPath = logPath
        self.logger = Logger.getLogger(logName, logPath)
        self.__mapCyclesToPackageList = {}
        self.__mapPackageToCycle = {}
        self.__buildDependencyGraph = {}
        self.__runTimeDependencyGraph = {}
        self.__sortedPackageList = []
        self.__sortedBuildDependencyGraph = {}

    def getPackageBuildData(self, listPackages):
        self._readDependencyGraphAndCyclesForGivenPackages(listPackages)
        self._getSortedBuildOrderListForGivenPackages(listPackages)
        return self.__mapCyclesToPackageList, self.__mapPackageToCycle, self.__sortedPackageList

    #todo
    def _findCompleteListOfPackagesRequiredToBuildGivenPackages(self, listPackages):
        return list(self.__buildDependencyGraph.keys())

    def _createSortListForPkg(self, pkg):
        runTimeDepPkgList = self.__runTimeDependencyGraph[pkg]
        runTimeDepPkgList.append(pkg)
        sortListForPkg = []

        for p in runTimeDepPkgList:
            basePkg = SPECS.getData().getSpecName(p)
            for bPkg in self.__sortedBuildDependencyGraph[basePkg]:
                if bPkg not in sortListForPkg:
                    sortListForPkg.append(bPkg)

        return sortListForPkg

    def _getCircularDependentPackages(self, pkg):
        circularDependentPackages = []
        if pkg in self.__mapPackageToCycle:
            circularDependentPackages.extend(
                self.__mapCyclesToPackageList[self.__mapPackageToCycle[pkg]])
            circularDependentPackages.remove(pkg)
        return circularDependentPackages

    def _getSortedBuildOrderListForGivenPackages(self, listPackages):

        alreadyProcessedPackages = set()
        sortedList = []
        completeListPackagesToBuild = self._findCompleteListOfPackagesRequiredToBuildGivenPackages(
            listPackages)
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
            sortListForPkg = self._createSortListForPkg(pkg)

            #remove any cyclic packages in sortListForPkg if they already exists in sortedList
            circularDependentPackages = self._getCircularDependentPackages(pkg)
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
                self.logger.info("Removing duplicates in sortedList")
                sortedList = removeDuplicateEntries(sortedList)
            else:
                prevSortListLen = len(sortedList)

        self.logger.info("Removing duplicates in sorted list")
        sortedList = removeDuplicateEntries(sortedList)

        self.logger.info("Sorted list:")
        self.logger.info(sortedList)
        self.__sortedPackageList = sortedList

    def _constructBuildAndRunTimeDependencyGraph(self, package):
        basePackage = SPECS.getData().getSpecName(package)

        addBuildTimeGraph = True
        addRunTimeGraph = True
        if basePackage in self.__buildDependencyGraph:
            addBuildTimeGraph = False
        if basePackage in self.__runTimeDependencyGraph:
            addRunTimeGraph = False

        nextPackagesToConstructGraph = set()
        if addBuildTimeGraph:
            listDependentRpmPackages = SPECS.getData().getBuildRequiresForPackage(basePackage)
            listDependentPackages = set()
            for rpmPkg in listDependentRpmPackages:
                basePkg = SPECS.getData().getSpecName(rpmPkg)
                listDependentPackages.add(basePkg)
            self.__buildDependencyGraph[basePackage] = listDependentPackages
            nextPackagesToConstructGraph.update(listDependentPackages)

        if addRunTimeGraph:
            listRpmPackages = SPECS.getData().getPackages(basePackage)
            for rpmPkg in listRpmPackages:
                listDependentRpmPackages = SPECS.getData().getRequiresAllForPackage(rpmPkg)
                self.__runTimeDependencyGraph[rpmPkg] = copy.copy(listDependentRpmPackages)
                nextPackagesToConstructGraph.update(listDependentRpmPackages)

        for pkg in nextPackagesToConstructGraph:
            self._constructBuildAndRunTimeDependencyGraph(pkg)

    def _readDependencyGraphAndCyclesForGivenPackages(self, listPackages):
        self.logger.info("Reading dependency graph to check for cycles")
        for pkg in listPackages:
            self._constructBuildAndRunTimeDependencyGraph(pkg)

        for pkg in self.__buildDependencyGraph.keys():
            sortedPackageList, circularDependentPackages = self._topologicalSortPackages(
                self.__buildDependencyGraph, pkg)
            if len(circularDependentPackages) > 0:
                self.logger.error("Found circular dependency")
                self.logger.error(circularDependentPackages)
                raise Exception("Build Time Circular Dependency")
            self.__sortedBuildDependencyGraph[pkg] = sortedPackageList
        sortedPackageList, circularDependentPackages = self._topologicalSortPackages(
            self.__runTimeDependencyGraph)
        if len(circularDependentPackages) > 0:
            self._findCircularDependencies(circularDependentPackages)

    def _topologicalSortPackages(self, dependencyGraph, package=None):
        noDepPackages = set()
        sortedPackageList = []
        dependentOfPackage = dict()

        dependentPackages = {}
        if package is None:
            dependentPackages = copy.deepcopy(dependencyGraph)
        else:
            listDepPkgs = set()
            listDepPkgs.add(package)
            while listDepPkgs:
                pkg = listDepPkgs.pop()
                if pkg in dependentPackages:
                    continue
                dependentPackages[pkg] = copy.copy(dependencyGraph[pkg])
                for depPkg in dependencyGraph[pkg]:
                    listDepPkgs.add(depPkg)

        #Find packages with no dependencies and generate dependentof_package edge list
        for pkg in dependentPackages:
            if len(dependentPackages[pkg]) == 0:
                noDepPackages.add(pkg)
            else:
                for depPkg in dependentPackages[pkg]:
                    if depPkg not in dependentOfPackage:
                        dependentOfPackage[depPkg] = {pkg}
                    else:
                        dependentOfPackage[depPkg].add(pkg)

        while noDepPackages:
            pkg = noDepPackages.pop()
            sortedPackageList.append(pkg)
            if pkg in dependentOfPackage:
                for childPkg in list(dependentOfPackage[pkg]):
                    dependentOfPackage[pkg].remove(childPkg)
                    dependentPackages[childPkg].remove(pkg)
                    if len(dependentPackages[childPkg]) == 0:
                        noDepPackages.add(childPkg)

        # creating circular dependency graph for given dependency graph
        circularDependencyGraph = {}
        for pkg in dependentPackages.keys():
            if dependentPackages[pkg]:
                circularDependencyGraph[pkg] = dependentPackages[pkg]

        #return (non-circular dependent package in sorted order and circular dependent
        #package list in a dependencyGraph)
        return sortedPackageList, circularDependencyGraph

    def _constructDependencyMap(self, yclicDependencyGraph):
        self.logger.info("Constructing dependency map from circular dependency graph.....")
        constructDependencyMap = {}
        for node in cyclicDependencyGraph.keys():
            tmpDepNodeList = []
            tmpDepNodeList.append(node)
            depNodeList = []
            while len(tmpDepNodeList) != 0:
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
            constructDependencyMap[node] = depNodeList
        self.logger.info("Dependency Map:")
        self.logger.info(constructDependencyMap)
        return constructDependencyMap

    def _findCircularDependencies(self, cyclicDependencyGraph):
        self.logger.info("Looking for circular dependencies")
        if len(cyclicDependencyGraph) == 0:
            return
        #step1: construct dependency map from dependency graph
        constructDependencyMap = self._constructDependencyMap(cyclicDependencyGraph)

        #step2: find cycles in dependency map
        self.logger.info("Finding and adding cycles using constructed dependency map......")
        cycleCount = 0
        for node in cyclicDependencyGraph.keys():
            listDepPkg = constructDependencyMap[node]
            cycPkgs = []
            if node not in self.__mapPackageToCycle:
                for depPkg in listDepPkg:
                    x = constructDependencyMap[depPkg]
                    if node in x:
                        cycPkgs.append(depPkg)

                if len(cycPkgs) != 0:
                    cycPkgs.append(node)
                    cycleName = "cycle" + str(PackageBuildDataGenerator.cycleCount)
                    PackageBuildDataGenerator.cycleCount += 1
                    for x in cycPkgs:
                        self.__mapPackageToCycle[x] = cycleName
                    self.__mapCyclesToPackageList[cycleName] = cycPkgs
                    self.logger.info("New circular dependency found:")
                    self.logger.info(cycleName + " " + ",".join(cycPkgs))
                    cycleCount += 1

        if cycleCount > 0:
            self.logger.info("Found " + str(cycleCount) + " cycles.")
            self.logger.info("Successfully added all detected circular dependencies to list.")
        else:
            self.logger.info("No circular dependencies found.")
