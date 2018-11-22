import json
import ThreadPool
from constants import constants
from Logger import Logger
import threading
from Queue import PriorityQueue
from SpecData import SPECS

class Scheduler(object):

    lock=threading.Lock()
    listOfAlreadyBuiltPackages=[]
    listOfPackagesToBuild=[]
    listOfPackagesCurrentlyBuilding=[]
    sortedList=[]
    listOfPackagesNextToBuild=PriorityQueue()
    listOfFailedPackages=[]
    alldependencyGraph = {}
    dependencyGraph = {}
    priorityMap = {}
    pkgWeights={}
    isPriorityScheduler=1
    logger=None
    event=None
    stopScheduling=False

    @staticmethod
    def setEvent(event):
        Scheduler.event=event

    @staticmethod
    def setLog(logName,logPath):
        Scheduler.logger = Logger.getLogger(logName, logPath)

    @staticmethod
    def getBuildRequiredPackages(package):
        listRequiredRPMPackages = []
        listRequiredRPMPackages.extend(SPECS.getData().getBuildRequiresForPkg(package))
        listRequiredPackages = []

        for pkg in listRequiredRPMPackages:
            basePkg = SPECS.getData().getBasePkg(pkg)
            if basePkg not in listRequiredPackages:
                listRequiredPackages.append(basePkg)

        return listRequiredPackages


    @staticmethod
    def getDependencies(package, parentPackage, k):

        for node in Scheduler.alldependencyGraph[package].keys():
                Scheduler.getDependencies(node, package, k)

        if parentPackage == None:
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
            for child_pkg in Scheduler.dependencyGraph[package].keys():
                Scheduler.getDependencies(child_pkg, package, k)
                for node in Scheduler.alldependencyGraph[child_pkg].keys():
                    try:
                        Scheduler.dependencyGraph[package][node] = max(
                            Scheduler.dependencyGraph[package][node],
                            Scheduler.alldependencyGraph[child_pkg][node] * k)
                    except KeyError:
                        Scheduler.dependencyGraph[package][node] = \
                            Scheduler.alldependencyGraph[child_pkg][node] * k
	if constants.publishBuildDependencies:
	    dependencyLists = {}
	    for package in Scheduler.dependencyGraph.keys():
		dependencyLists[package] = []
		for dependency in Scheduler.dependencyGraph[package].keys():
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
	if constants.packageWeightsPath == None:
            Scheduler.logger.info("Priority Scheduler disabled")
            Scheduler.isPriorityScheduler = 0
	else:
	    Scheduler.parseWeights()

        for package in Scheduler.sortedList:
            Scheduler.dependencyGraph[package] = {}
            Scheduler.alldependencyGraph[package] = {}
            for child_package in Scheduler.getBuildRequiredPackages(package):
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


    @staticmethod
    def setParams(sortedList,listOfAlreadyBuiltPackages):
        Scheduler.sortedList=sortedList
        Scheduler.listOfAlreadyBuiltPackages=listOfAlreadyBuiltPackages
        for x in Scheduler.sortedList:
            if x not in Scheduler.listOfAlreadyBuiltPackages or x in constants.testForceRPMS:
                Scheduler.listOfPackagesToBuild.append(x)
        Scheduler.listOfPackagesCurrentlyBuilding=[]
        Scheduler.listOfPackagesNextToBuild=[]
        Scheduler.listOfFailedPackages=[]
        Scheduler.setPriorities()

    @staticmethod
    def getRequiredPackages(package):
        listRequiredRPMPackages=[]
        listRequiredRPMPackages.extend(SPECS.getData().getBuildRequiresForPkg(package))
        listRequiredRPMPackages.extend(SPECS.getData().getRequiresAllForPkg(package))
        listRequiredPackages=[]

        for pkg in listRequiredRPMPackages:
            basePkg=SPECS.getData().getBasePkg(pkg)
            if basePkg not in listRequiredPackages:
                listRequiredPackages.append(basePkg)
        return listRequiredPackages

    @staticmethod
    def __getListNextPackagesReadyToBuild():
        listOfPackagesNextToBuild=PriorityQueue()
        Scheduler.logger.info("Checking for next possible packages to build")
        for pkg in Scheduler.listOfPackagesToBuild:
            if pkg in Scheduler.listOfPackagesCurrentlyBuilding:
                continue
            listRequiredPackages=Scheduler.getRequiredPackages(pkg)
            canBuild=True
            Scheduler.logger.info("Required packages for "+ pkg + " are:")
            Scheduler.logger.info(listRequiredPackages)
            for reqPkg in listRequiredPackages:
                if reqPkg not in Scheduler.listOfAlreadyBuiltPackages:
                    canBuild=False
                    Scheduler.logger.info(reqPkg+" is not available. So we cannot build "+ pkg +" at this moment.")
                    break
            if canBuild:
                listOfPackagesNextToBuild.put((-Scheduler.priorityMap[pkg], pkg))
                Scheduler.logger.info("Adding "+ pkg +" to the schedule list")
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

        packageTup=Scheduler.listOfPackagesNextToBuild.get()

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
            ThreadPool.ThreadPool.activateWorkerThreads(Scheduler.listOfPackagesNextToBuild.qsize())
        Scheduler.logger.info("Released scheduler lock")
        Scheduler.lock.release()
        Scheduler.listOfPackagesCurrentlyBuilding.append(package)
        Scheduler.listOfPackagesToBuild.remove(package)
        return package

    #can be synchronized TODO
    @staticmethod
    def notifyPackageBuildCompleted(package):
        if package in Scheduler.listOfPackagesCurrentlyBuilding:
            Scheduler.listOfPackagesCurrentlyBuilding.remove(package)
            Scheduler.listOfAlreadyBuiltPackages.append(package)


    #can be synchronized TODO
    @staticmethod
    def notifyPackageBuildFailed(package):
        if package in Scheduler.listOfPackagesCurrentlyBuilding:
            Scheduler.listOfPackagesCurrentlyBuilding.remove(package)
            Scheduler.listOfFailedPackages.append(package)

    @staticmethod
    def isAllPackagesBuilt():
        if len(Scheduler.listOfPackagesToBuild) == 0 :
            return True
        return False

    @staticmethod
    def isAnyPackagesFailedToBuild():
        if len(Scheduler.listOfFailedPackages) != 0:
            return True
        return False

