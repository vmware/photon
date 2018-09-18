import threading
from queue import PriorityQueue
import json
from ThreadPool import ThreadPool
from constants import constants
from Logger import Logger
from SpecData import SPECS

class Scheduler(object):

    lock = threading.Lock()
    listOfAlreadyBuiltPackages = set()
    listOfPackagesToBuild = []
    listOfPackagesCurrentlyBuilding = set()
    sortedList = []
    listOfPackagesNextToBuild = PriorityQueue()
    listOfFailedPackages = []
    alldependencyGraph = {}
    dependencyGraph = {}
    priorityMap = {}
    pkgWeights = {}
    logger = None
    event = None
    stopScheduling = False

    @staticmethod
    def setEvent(event):
        Scheduler.event = event

    @staticmethod
    def setLog(logName, logPath):
        Scheduler.logger = Logger.getLogger(logName, logPath)

    @staticmethod
    def setParams(sortedList, listOfAlreadyBuiltPackages):
        Scheduler.sortedList = sortedList
        Scheduler.listOfAlreadyBuiltPackages = listOfAlreadyBuiltPackages
        for x in Scheduler.sortedList:
            if x not in Scheduler.listOfAlreadyBuiltPackages or x in constants.testForceRPMS:
                Scheduler.listOfPackagesToBuild.append(x)
        Scheduler.listOfPackagesCurrentlyBuilding = set()
        Scheduler.listOfPackagesNextToBuild = PriorityQueue()
        Scheduler.listOfFailedPackages = []
        Scheduler._setPriorities()

    @staticmethod
    def notifyPackageBuildCompleted(package):
        with Scheduler.lock:
            if package in Scheduler.listOfPackagesCurrentlyBuilding:
                Scheduler.listOfPackagesCurrentlyBuilding.remove(package)
                Scheduler.listOfAlreadyBuiltPackages.add(package)

    @staticmethod
    def notifyPackageBuildFailed(package):
        with Scheduler.lock:
            if package in Scheduler.listOfPackagesCurrentlyBuilding:
                Scheduler.listOfPackagesCurrentlyBuilding.remove(package)
                Scheduler.listOfFailedPackages.append(package)

    @staticmethod
    def isAllPackagesBuilt():
        if Scheduler.listOfPackagesToBuild:
            return False
        return True

    @staticmethod
    def isAnyPackagesFailedToBuild():
        if Scheduler.listOfFailedPackages:
            return True
        return False

    @staticmethod
    def getNextPackageToBuild():
        Scheduler.logger.info("Waiting to acquire scheduler lock")
        with Scheduler.lock:
            if Scheduler.stopScheduling:
                return None

            if not Scheduler.listOfPackagesToBuild:
                if Scheduler.event is not None:
                    Scheduler.event.set()

            if Scheduler.listOfPackagesNextToBuild.empty():
                Scheduler._getListNextPackagesReadyToBuild()

            if Scheduler.listOfPackagesNextToBuild.empty():
                return None

            packageTup = Scheduler.listOfPackagesNextToBuild.get()

            package = packageTup[1]
            Scheduler.logger.info("PackagesNextToBuild " + str(packageTup))
            if Scheduler.listOfPackagesNextToBuild.qsize() > 0:
                ThreadPool.activateWorkerThreads(
                    Scheduler.listOfPackagesNextToBuild.qsize())
            Scheduler.listOfPackagesCurrentlyBuilding.add(package)
            Scheduler.listOfPackagesToBuild.remove(package)
            return package

    @staticmethod
    def _getBuildRequiredPackages(package):
        listRequiredRPMPackages = []
        listRequiredRPMPackages.extend(SPECS.getData().getBuildRequiresForPackage(package))

        listRequiredPackages = []

        for pkg in listRequiredRPMPackages:
            basePkg = SPECS.getData().getSpecName(pkg.package)
            if basePkg not in listRequiredPackages:
                listRequiredPackages.append(basePkg)

        return listRequiredPackages


    @staticmethod
    def _getDependencies(package, parentPackage, k):

        for node in list(Scheduler.alldependencyGraph[package].keys()):
            Scheduler._getDependencies(node, package, k)

        if parentPackage is None:
            return
        else:
            for node in Scheduler.alldependencyGraph[package].keys():
                try:
                    Scheduler.alldependencyGraph[parentPackage][node] = max(
                        Scheduler.alldependencyGraph[parentPackage][node],
                        Scheduler.alldependencyGraph[package][node] * k)
                except KeyError:
                    Scheduler.alldependencyGraph[parentPackage][node] = (
                        Scheduler.alldependencyGraph[package][node] * k)

    @staticmethod
    def _makeGraph():
        k = 2
        for package in Scheduler.sortedList:
                Scheduler.dependencyGraph[package] = {}
                Scheduler.alldependencyGraph[package] = {}
                for child_package in Scheduler._getBuildRequiredPackages(package):
                    Scheduler.dependencyGraph[package][child_package] = 1
                for child_package in Scheduler._getRequiredPackages(package):
                    Scheduler.alldependencyGraph[package][child_package] = 1
        for package in Scheduler.sortedList:
            for child_pkg in list(Scheduler.dependencyGraph[package].keys()):
                Scheduler._getDependencies(child_pkg, package, k)
                for node in list(Scheduler.alldependencyGraph[child_pkg].keys()):
                    try:
                        Scheduler.dependencyGraph[package][node] = max(
                            Scheduler.dependencyGraph[package][node],
                            Scheduler.alldependencyGraph[child_pkg][node] * k)
                    except KeyError:
                        Scheduler.dependencyGraph[package][node] = (
                            Scheduler.alldependencyGraph[child_pkg][node] * k)
        if constants.publishBuildDependencies:
            dependencyLists = {}
            for package in list(Scheduler.dependencyGraph.keys()):
                dependencyLists[package] = []
                for dependency in list(Scheduler.dependencyGraph[package].keys()):
                    dependencyLists[package].append(dependency)
            with open(str(constants.logPath) + "/BuildDependencies.json", 'w') as graphfile:
                graphfile.write(json.dumps(dependencyLists, sort_keys=True, indent=4))

    @staticmethod
    def _parseWeights():
        Scheduler.pkgWeights.clear()
        with open(constants.packageWeightsPath, 'r') as weightFile:
            Scheduler.pkgWeights = json.load(weightFile)

    @staticmethod
    def _getWeight(package):
        try:
            return float(Scheduler.pkgWeights[package])
        except KeyError:
            return 0

    @staticmethod
    def _getPriority(package):
        try:
            return float(Scheduler.priorityMap[package])
        except KeyError:
            return 0


    @staticmethod
    def _setPriorities():
        if constants.packageWeightsPath is None:
            Scheduler.logger.info("Priority Scheduler disabled")
            if constants.publishBuildDependencies:
                Scheduler.logger.info("Publishing Build dependencies")
                Scheduler._makeGraph()
        else:
            Scheduler.logger.info("Priority Scheduler enabled")
            Scheduler._parseWeights()

            Scheduler._makeGraph()
            for package in Scheduler.sortedList:
                try:
                    Scheduler.priorityMap[package] = Scheduler._getWeight(package)
                except KeyError:
                    Scheduler.priorityMap[package] = 0
                for child_pkg in Scheduler.dependencyGraph[package].keys():
                    Scheduler.priorityMap[child_pkg] = (
                        Scheduler.priorityMap[child_pkg]
                        + (Scheduler.dependencyGraph[package][child_pkg]
                        * (Scheduler._getWeight(package))))
            Scheduler.logger.info("set Priorities: Priority of all packages")
            Scheduler.logger.info(Scheduler.priorityMap)


    @staticmethod
    def _getRequiredPackages(package):
        listRequiredRPMPackages = []
        listRequiredRPMPackages.extend(SPECS.getData().getBuildRequiresForPackage(package))
        listRequiredRPMPackages.extend(SPECS.getData().getRequiresAllForPackage(package))

        listRequiredPackages = []

        for pkg in listRequiredRPMPackages:
            basePkg = SPECS.getData().getSpecName(pkg.package)
            if basePkg not in listRequiredPackages:
                listRequiredPackages.append(basePkg)

        return listRequiredPackages

    @staticmethod
    def _getListNextPackagesReadyToBuild():
        Scheduler.logger.info("Checking for next possible packages to build")
        for pkg in Scheduler.listOfPackagesToBuild:
            if pkg in Scheduler.listOfPackagesCurrentlyBuilding:
                continue
            listRequiredPackages = Scheduler._getRequiredPackages(pkg)
            canBuild = True
            for reqPkg in listRequiredPackages:
                if reqPkg not in Scheduler.listOfAlreadyBuiltPackages:
                    canBuild = False
                    break
            if canBuild:
                Scheduler.listOfPackagesNextToBuild.put((-Scheduler._getPriority(pkg), pkg))
                Scheduler.logger.info("Adding " + pkg + " to the schedule list")
