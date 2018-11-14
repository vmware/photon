import threading
from queue import PriorityQueue
import json
from ThreadPool import ThreadPool
from constants import constants
from Logger import Logger
from SpecData import SPECS
from StringUtils import StringUtils

class Scheduler(object):

    lock = threading.Lock()
    listOfAlreadyBuiltPackages = set()
    listOfPackagesToBuild = []
    listOfPackagesCurrentlyBuilding = set()
    sortedList = []
    listOfPackagesNextToBuild = PriorityQueue()
    listOfFailedPackages = []
    priorityMap = {}
    pkgWeights = {}
    logger = None
    event = None
    stopScheduling = False

    @staticmethod
    def setEvent(event):
        Scheduler.event = event

    @staticmethod
    def setLog(logName, logPath, logLevel):
        Scheduler.logger = Logger.getLogger(logName, logPath, logLevel)

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
            if Scheduler.listOfPackagesNextToBuild.qsize() > 0:
                ThreadPool.activateWorkerThreads(
                    Scheduler.listOfPackagesNextToBuild.qsize())
            Scheduler.listOfPackagesCurrentlyBuilding.add(package)
            Scheduler.listOfPackagesToBuild.remove(package)
            return package

    @staticmethod
    def getDoneList():
        return list(Scheduler.listOfAlreadyBuiltPackages)

    @staticmethod
    def _getBuildRequiredPackages(pkg):
        listRequiredRPMPackages = []
        listRequiredRPMPackages.extend(SPECS.getData().getBuildRequiresForPkg(pkg))

        listRequiredPackages = []

        for reqPkg in listRequiredRPMPackages:
            basePkg = SPECS.getData().getBasePkg(reqPkg)
            if basePkg not in listRequiredPackages:
                listRequiredPackages.append(basePkg)

        return listRequiredPackages

    @staticmethod
    def _parseWeights():
        Scheduler.pkgWeights.clear()
        with open(constants.packageWeightsPath, 'r') as weightFile:
            Scheduler.pkgWeights = json.load(weightFile)

    # A package's weight is an indicator of the time required to build
    # that package, relative to other packages. These weights do not
    # take build-time/install-time dependencies into account -- they
    # are the individual build-times of the respective packages.
    # Package weights are positive integers, with a default value of 1.
    @staticmethod
    def _getWeight(package):
	# Package weights are assumed to be independent of package
	# version (i.e., in the case of multi-version packages such as
	# Go or Kubernetes, all the versions have the same weight). So
	# convert packageName-version to packageName before looking up
	# the package weight.
        package, _ = StringUtils.splitPackageNameAndVersion(package)
        try:
            return int(Scheduler.pkgWeights[package]) + 1
        except KeyError:
            return 1

    @staticmethod
    def _getPriority(package):
        try:
            return int(Scheduler.priorityMap[package])
        except KeyError:
            return 0


    @staticmethod
    def _setPriorities():
        if constants.packageWeightsPath is None:
            Scheduler.logger.debug("Priority Scheduler disabled")
            if constants.publishBuildDependencies:
                Scheduler.logger.debug("Publishing Build dependencies")
                Scheduler._makeGraph()
        else:
            Scheduler.logger.debug("Priority Scheduler enabled")
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
            Scheduler.logger.debug("set Priorities: Priority of all packages")
            Scheduler.logger.debug(Scheduler.priorityMap)


    @staticmethod
    def _getRequiredPackages(pkg):
        listRequiredRPMPackages = []
        listRequiredRPMPackages.extend(SPECS.getData().getBuildRequiresForPkg(pkg))
        listRequiredRPMPackages.extend(SPECS.getData().getRequiresAllForPkg(pkg))

        listRequiredPackages = []

        for reqPkg in listRequiredRPMPackages:
            basePkg = SPECS.getData().getBasePkg(reqPkg)
            if basePkg not in listRequiredPackages:
                listRequiredPackages.append(basePkg)

        return listRequiredPackages

    @staticmethod
    def _getListNextPackagesReadyToBuild():
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
                Scheduler.logger.debug("Adding " + pkg + " to the schedule list")
