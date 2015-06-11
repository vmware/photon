import ThreadPool
from constants import constants
from Logger import Logger
import threading 

class Scheduler(object):
    
    lock=threading.Lock()
    listOfAlreadyBuiltPackages=[]
    listOfPackagesToBuild=[]
    listOfPackagesCurrentlyBuilding=[]
    sortedList=[]
    listOfPackagesNextToBuild=[]
    listOfFailedPackages=[]
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
    def setParams(sortedList,listOfAlreadyBuiltPackages):
        Scheduler.sortedList=sortedList
        Scheduler.listOfAlreadyBuiltPackages=listOfAlreadyBuiltPackages
        for x in Scheduler.sortedList:
            if x not in Scheduler.listOfAlreadyBuiltPackages:
                Scheduler.listOfPackagesToBuild.append(x)
        Scheduler.listOfPackagesCurrentlyBuilding=[]
        Scheduler.listOfPackagesNextToBuild=[]
        Scheduler.listOfFailedPackages=[]
        
    @staticmethod
    def getRequiredPackages(package):
        listRequiredRPMPackages=[]
        listRequiredRPMPackages.extend(constants.specData.getBuildRequiresForPackage(package))
        listRequiredRPMPackages.extend(constants.specData.getRequiresAllForPackage(package))
        
        listRequiredPackages=[]
        for pkg in listRequiredRPMPackages:
            basePkg=constants.specData.getSpecName(pkg)
            if basePkg not in listRequiredPackages:
                listRequiredPackages.append(basePkg)
        
        return listRequiredPackages
    
    @staticmethod
    def __getListNextPackagesReadyToBuild():
        listOfPackagesNextToBuild=[]
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
                listOfPackagesNextToBuild.append(pkg)
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
            
        if len(Scheduler.listOfPackagesNextToBuild) == 0:
            listOfPackagesNextToBuild=Scheduler.__getListNextPackagesReadyToBuild()
            Scheduler.listOfPackagesNextToBuild=listOfPackagesNextToBuild
            
        if len(Scheduler.listOfPackagesNextToBuild) == 0:
            Scheduler.logger.info("Released scheduler lock")
            Scheduler.lock.release()
            return None
        
        package=Scheduler.listOfPackagesNextToBuild.pop(0)
        
        if len(Scheduler.listOfPackagesNextToBuild) > 0:
            ThreadPool.ThreadPool.activateWorkerThreads(len(Scheduler.listOfPackagesNextToBuild))
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
        
        