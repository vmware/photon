import threading
from queue import PriorityQueue
import json
import ThreadPool
from constants import constants
from Logger import Logger
from SpecData import SPECS

class Scheduler(object):

    lock = threading.Lock()
    listOfAlreadyBuiltRPMs = []
    listOfPackagesToBuild = []
    listOfPackagesCurrentlyBuilding = []
    sortedList = []
    listOfPackagesNextToBuild = PriorityQueue()
    listOfFailedPackages = []
    alldependencyGraph = {}
    dependencyGraph = {}
    priorityMap = {}
    pkgWeights = {}
    isPriorityScheduler = 1
    logger = None
    event = None
    stopScheduling = False

    # New thread scheduler stuff
    threadCnt = 0
    pkgDepsCntLock = threading.Lock()
    pkgDepsCntMap = {}
    buildReqToPkgMap = {}
    pkgToBuildCnt = 0
    setOfAlreadyBuiltPkgs = set()
    # The Priority Queue to hold all the ready to be built packages
    pkgBuildQueue = PriorityQueue()

    @staticmethod
    def setEvent(event):
        Scheduler.event = event

    @staticmethod
    def setLog(logName, logPath):
        Scheduler.logger = Logger.getLogger(logName, logPath)

    @staticmethod
    def getBuildRequiredPkgs(package):
        requiredPkgsSet = set()

        for rpm in SPECS.getData().getBuildRequiresForPackage(package):
            basePkg = SPECS.getData().getSpecName(rpm)
            requiredPkgsSet.add(basePkg)

        return list(requiredPkgsSet)

    @staticmethod
    def getDependencies(package, parentPackage, k):

        for node in list(Scheduler.alldependencyGraph[package].keys()):
            Scheduler.getDependencies(node, package, k)

        if parentPackage is None:
            return
        else:
            for node in Scheduler.alldependencyGraph[package].keys():
                try:
                    Scheduler.alldependencyGraph[parentPackage][node] = max(
                        Scheduler.alldependencyGraph[parentPackage][node],
                        Scheduler.alldependencyGraph[package][node] * k)
                except KeyError:
                    Scheduler.alldependencyGraph[parentPackage][node] = \
                        Scheduler.alldependencyGraph[package][node] * k

    @staticmethod
    def makeGraph():
        k = 3
        for package in Scheduler.sortedList:
            for child_pkg in list(Scheduler.dependencyGraph[package].keys()):
                Scheduler.getDependencies(child_pkg, package, k)
                for node in list(Scheduler.alldependencyGraph[child_pkg].keys()):
                    try:
                        Scheduler.dependencyGraph[package][node] = max(
                            Scheduler.dependencyGraph[package][node],
                            Scheduler.alldependencyGraph[child_pkg][node] * k)
                    except KeyError:
                        Scheduler.dependencyGraph[package][node] = \
                            Scheduler.alldependencyGraph[child_pkg][node] * k
        if constants.publishBuildDependencies:
            dependencyLists = {}
            for package in list(Scheduler.dependencyGraph.keys()):
                dependencyLists[package] = []
                for dependency in list(Scheduler.dependencyGraph[package].keys()):
                    dependencyLists[package].append(dependency)
            graphfile = open(str(constants.logPath) + "/BuildDependencies.json", 'w')
            graphfile.write(json.dumps(dependencyLists, sort_keys=True, indent=4))
            graphfile.close()

    @staticmethod
    def parseWeights():
        Scheduler.pkgWeights.clear()
        weightFile = open(constants.packageWeightsPath, 'r')
        Scheduler.pkgWeights = json.load(weightFile)
        weightFile.close()

    @staticmethod
    def getWeight(package):
        try:
            return float(Scheduler.pkgWeights[package])
        except KeyError:
            return 0

    @staticmethod
    def setPriorities():
        if constants.packageWeightsPath is None:
            Scheduler.logger.info("Priority Scheduler disabled")
            Scheduler.isPriorityScheduler = 0
        else:
            Scheduler.parseWeights()

        for package in Scheduler.sortedList:
            Scheduler.dependencyGraph[package] = {}
            Scheduler.alldependencyGraph[package] = {}
            for child_package in Scheduler.getBuildRequiredPkgs(package):
                Scheduler.dependencyGraph[package][child_package] = 1
            for child_package in Scheduler.getRequiredPackages(package):
                Scheduler.alldependencyGraph[package][child_package] = 1
        Scheduler.makeGraph()
        for package in Scheduler.sortedList:
            try:
                Scheduler.priorityMap[package] = Scheduler.getWeight(package)
            except KeyError:
                Scheduler.priorityMap[package] = 0
            for child_pkg in Scheduler.dependencyGraph[package].keys():
                Scheduler.priorityMap[child_pkg] = Scheduler.priorityMap[child_pkg] \
                                                 + (Scheduler.dependencyGraph[package][child_pkg]
                                                    * (Scheduler.getWeight(package)))
        Scheduler.logger.info("set Priorities: Priority of all packages")
        Scheduler.logger.info(Scheduler.priorityMap)


    @classmethod
    def setParams(cls, sortedList, listOfAlreadyBuiltRPMs):
        cls.logger.info("Within the caller")
        cls.logger.info(listOfAlreadyBuiltRPMs)
        cls.sortedList = sortedList
        cls.listOfAlreadyBuiltRPMs = listOfAlreadyBuiltRPMs
        cls.pkgDepsCntMap = SPECS.getData().pkgDepsCntMap
        cls.buildReqToPkgMap = SPECS.getData().buildReqToPkgMap
        pkgToBuildSet = set()
        for rpm in cls.listOfAlreadyBuiltRPMs:
            cls.setOfAlreadyBuiltPkgs.add(SPECS.getData().getSpecName(rpm))
        cls.logger.info("List of packages that have already been built:")
        cls.logger.info(cls.setOfAlreadyBuiltPkgs)
        # 0. Calculate the noDeps packages and add to the set.
        for pkg, v in cls.pkgDepsCntMap.items():
            if v == 0 and pkg not in cls.setOfAlreadyBuiltPkgs:
                cls.logger.info("Pkg {0} is put to the toBuild set due to No Deps".format(pkg))
                pkgToBuildSet.add(pkg)
        # 1. Calculate what packages to build based on previous built packages.
        for rpm in cls.listOfAlreadyBuiltRPMs:
            cls.logger.info("RPM " + rpm + " is already built.")
            for dep in SPECS.getData().getDepPkgForRPM(rpm):
                cls.pkgDepsCntMap[dep] -= 1
                if cls.pkgDepsCntMap[dep] == 0 and dep not in cls.setOfAlreadyBuiltPkgs:
                    cls.logger.info("Pkg {0} is put to the toBuild set due to {1}".format(dep, rpm))
                    pkgToBuildSet.add(dep)
        # 2. Add the packages to the build queue.
        for pkg in pkgToBuildSet:
            cls.pkgBuildQueue.put(pkg)
        for pkg in cls.sortedList:
            if (pkg not in cls.listOfAlreadyBuiltRPMs) or (pkg in constants.testForceRPMS):
                cls.listOfPackagesToBuild.append(pkg)
        cls.pkgToBuildCnt = len(cls.listOfPackagesToBuild)
        cls.logger.info("Summary: Before build start, " + str(cls.pkgToBuildCnt) + " pkgs to build.")
        cls.listOfPackagesCurrentlyBuilding = []
        cls.listOfPackagesNextToBuild = []
        cls.listOfFailedPackages = []
        cls.setPriorities()

    @staticmethod
    def getRequiredPackages(package):
        listRequiredRPMPackages = []
        listRequiredRPMPackages.extend(SPECS.getData().getBuildRequiresForPackage(package))
        listRequiredRPMPackages.extend(SPECS.getData().getRequiresAllForPackage(package))

        listRequiredPackages = []

        for pkg in listRequiredRPMPackages:
            basePkg = SPECS.getData().getSpecName(pkg)
            if basePkg not in listRequiredPackages:
                listRequiredPackages.append(basePkg)

        return listRequiredPackages

    @staticmethod
    def __getListNextPackagesReadyToBuild():
        listOfPackagesNextToBuild = PriorityQueue()
        Scheduler.logger.info("Checking for next possible packages to build")
        for pkg in Scheduler.listOfPackagesToBuild:
            if pkg in Scheduler.listOfPackagesCurrentlyBuilding:
                continue
            listRequiredPackages = Scheduler.getRequiredPackages(pkg)
            canBuild = True
            Scheduler.logger.info("Required packages for " + pkg + " are:")
            Scheduler.logger.info(listRequiredPackages)
            for reqPkg in listRequiredPackages:
                if reqPkg not in Scheduler.listOfAlreadyBuiltRPMs:
                    canBuild = False
                    Scheduler.logger.info(reqPkg + " is not available. So we cannot build " +
                                          pkg + " at this moment.")
                    break
            if canBuild:
                listOfPackagesNextToBuild.put((-Scheduler.priorityMap[pkg], pkg))
                Scheduler.logger.info("Adding " + pkg + " to the schedule list")
        return listOfPackagesNextToBuild

    @staticmethod
    def getNextPackageToBuild():
        Scheduler.logger.info("Waiting to acquire scheduler lock")
        Scheduler.lock.acquire()

        if Scheduler.stopScheduling:
            Scheduler.logger.info("Released scheduler lock")
            Scheduler.lock.release()
            return None

        if len(Scheduler.listOfPackagesToBuild) == 0:
            if Scheduler.event is not None:
                Scheduler.event.set()

        try:
            if Scheduler.listOfPackagesNextToBuild.qsize() == 0:
                listOfPackagesNextToBuild = Scheduler.__getListNextPackagesReadyToBuild()
                Scheduler.listOfPackagesNextToBuild = listOfPackagesNextToBuild
        except:
            if len(Scheduler.listOfPackagesNextToBuild) == 0:
                listOfPackagesNextToBuild = Scheduler.__getListNextPackagesReadyToBuild()
                Scheduler.listOfPackagesNextToBuild = listOfPackagesNextToBuild

        if Scheduler.listOfPackagesNextToBuild.qsize() == 0:
            Scheduler.logger.info("Released scheduler lock")
            Scheduler.lock.release()
            return None

        packageTup = Scheduler.listOfPackagesNextToBuild.get()

        if packageTup[0] == 0 and Scheduler.isPriorityScheduler == 1:
            listOfPackagesNextToBuild = Scheduler.__getListNextPackagesReadyToBuild()
            Scheduler.listOfPackagesNextToBuild = listOfPackagesNextToBuild
            if Scheduler.listOfPackagesNextToBuild.qsize() == 0:
                Scheduler.logger.info("Released scheduler lock")
                Scheduler.lock.release()
                return None
            packageTup = Scheduler.listOfPackagesNextToBuild.get()

        package = packageTup[1]
        Scheduler.logger.info("PackagesNextToBuild " + str(packageTup))
        if Scheduler.listOfPackagesNextToBuild.qsize() > 0:
            ThreadPool.ThreadPool.activateWorkerThreads(
                Scheduler.listOfPackagesNextToBuild.qsize())
        Scheduler.logger.info("Released scheduler lock")
        Scheduler.lock.release()
        Scheduler.listOfPackagesCurrentlyBuilding.append(package)
        Scheduler.listOfPackagesToBuild.remove(package)
        return package

    @classmethod
    def getNextPkgToBuild(cls):
        cls.logger.info("Scheduler is trying to grab a pkg from pkgBuildQueue")
        pkg = cls.pkgBuildQueue.get(block=True)
        if pkg == "NoMorePkgs":
            return None
        return pkg

    @classmethod
    def notifyPkgBuildCompleted(cls, package):
        cls.logger.info("Package {0} is finished. Analyzing who build requires this package".format(package))
        for rpm in SPECS.getData().getRPMs(package):
            cls.logger.info("RPM {0} is provided".format(rpm))
            with cls.pkgDepsCntLock:
                if rpm not in cls.buildReqToPkgMap:
                    return
                for pkg in cls.buildReqToPkgMap[rpm]:
                    assert cls.pkgDepsCntMap[pkg] >= 1, "ERROR: Pkg deps count of {0} is below 0".format(pkg)
                    cls.logger.info("Pkg {0} decrements due to {1}".format(pkg, rpm))
                    cls.pkgDepsCntMap[pkg] -= 1
                    if cls.pkgDepsCntMap[pkg] == 0 and pkg not in cls.setOfAlreadyBuiltPkgs:
                        cls.pkgBuildQueue.put(pkg)
                        cls.logger.info("Pkg {0} is put to the BuildQueue due to {1}".format(pkg, rpm))
                        cls.pkgToBuildCnt -= 1
                    if cls.pkgToBuildCnt == 0:
                        for n in range(cls.threadCnt):
                            cls.logger.info("NoMorePkgs is put to the BuildQueue".format(pkg))
                            cls.pkgBuildQueue.put("NoMorePkgs")
                        # Set the threading event to True to unblock at the main thread
                        if cls.event is not None:
                            cls.event.set()
            cls.logger.info("Summary: " + str(cls.pkgToBuildCnt) + " pkgs to build.")
            cls.logger.info("Pkg Dependency Count Map:")
            cls.logger.info(cls.pkgDepsCntMap)

    #can be synchronized TODO
    @staticmethod
    def notifyPackageBuildCompleted(package):
        if package in Scheduler.listOfPackagesCurrentlyBuilding:
            Scheduler.listOfPackagesCurrentlyBuilding.remove(package)
            Scheduler.listOfAlreadyBuiltRPMs.append(package)

    #can be synchronized TODO
    @staticmethod
    def notifyPackageBuildFailed(package):
        if package in Scheduler.listOfPackagesCurrentlyBuilding:
            Scheduler.listOfPackagesCurrentlyBuilding.remove(package)
            Scheduler.listOfFailedPackages.append(package)

    @staticmethod
    def isAllPackagesBuilt():
        if len(Scheduler.listOfPackagesToBuild) == 0:
            return True
        return False

    @staticmethod
    def isAnyPackagesFailedToBuild():
        if len(Scheduler.listOfFailedPackages) != 0:
            return True
        return False
