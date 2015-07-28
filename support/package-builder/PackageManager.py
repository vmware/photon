from PackageBuildDataGenerator import PackageBuildDataGenerator
from Logger import Logger
import threading
from constants import constants
import os
from PackageUtils import PackageUtils
from ToolChainUtils import ToolChainUtils
from Scheduler import Scheduler
from ThreadPool import ThreadPool

class PackageManager(object):
    
    def __init__(self,logName=None,logPath=None):
        if logName is None:
            logName = "PackageManager"
        if logPath is None:
            logPath = constants.logPath
        self.logName=logName
        self.logPath=logPath
        self.logger=Logger.getLogger(logName,logPath)
        self.mapCyclesToPackageList={}
        self.mapPackageToCycle={}
        self.sortedPackageList=[]
        self.listOfPackagesAlreadyBuilt = []
        self.listThreads={}
        self.mapOutputThread={}
        self.mapThreadsLaunchTime={}
        self.listAvailableCyclicPackages=[]
        
    def readPackageBuildData(self, listPackages):
        try:
            pkgBuildDataGen = PackageBuildDataGenerator(self.logName,self.logPath)
            self.mapCyclesToPackageList,self.mapPackageToCycle,self.sortedPackageList = pkgBuildDataGen.getPackageBuildData(listPackages)
        except:
            self.logger.error("unable to get sorted list")
            return False
        return True
    
    def readAlreadyAvailablePackages(self):
        listAvailablePackages=[]
        listRPMFiles=[]
        listDirectorys=[]
        listDirectorys.append(constants.rpmPath)
        
        while len(listDirectorys) > 0:
            dirPath=listDirectorys.pop()
            for dirEntry in os.listdir(dirPath):
                dirEntryPath = os.path.join(dirPath, dirEntry)
                if os.path.isfile(dirEntryPath) and dirEntryPath.endswith(".rpm"):
                    listRPMFiles.append(dirEntryPath)
                elif os.path.isdir(dirEntryPath):
                    listDirectorys.append(dirEntryPath)
        pkgUtils = PackageUtils(self.logName,self.logPath)
        for rpmfile in listRPMFiles:
            package,version,release = pkgUtils.findPackageInfoFromRPMFile(rpmfile)
            if constants.specData.isRPMPackage(package):
                specVersion=constants.specData.getVersion(package)
                specRelease=constants.specData.getRelease(package)
                if version == specVersion and release == specRelease:
                    listAvailablePackages.append(package)
        self.logger.info("List of Already built packages")
        self.logger.info(listAvailablePackages)
        return listAvailablePackages
    
    def calculateParams(self,listPackages):
        self.listThreads.clear()
        self.mapOutputThread.clear()
        self.mapThreadsLaunchTime.clear()
        self.listAvailableCyclicPackages=[]
        self.mapCyclesToPackageList.clear()
        self.mapPackageToCycle.clear()
        self.sortedPackageList=[]
        
        self.listOfPackagesAlreadyBuilt = self.readAlreadyAvailablePackages()
        
        listPackagesToBuild=listPackages[:]
        for pkg in listPackages:
            if pkg in self.listOfPackagesAlreadyBuilt:
                listPackagesToBuild.remove(pkg)
        
        if not self.readPackageBuildData(listPackagesToBuild):
            return False
        return True
    
    def buildToolChain(self):
        try:
            tUtils=ToolChainUtils()
            tUtils.buildCoreToolChainPackages()
        except Exception as e:
            self.logger.error("Unable to build tool chain")
            self.logger.error(e)
            raise e
    
    def buildToolChainPackages(self, buildThreads):
        self.buildToolChain()
        self.buildGivenPackages(constants.listToolChainPackages, buildThreads)
        
    def buildPackages(self,listPackages, buildThreads):
        self.buildToolChainPackages(buildThreads)
        self.buildGivenPackages(listPackages, buildThreads)
    
    def initializeThreadPool(self,statusEvent):
        ThreadPool.clear()
        ThreadPool.mapPackageToCycle=self.mapPackageToCycle
        ThreadPool.listAvailableCyclicPackages=self.listAvailableCyclicPackages
        ThreadPool.logger=self.logger
        ThreadPool.statusEvent=statusEvent
        
    def initializeScheduler(self,statusEvent):
        Scheduler.setLog(self.logName, self.logPath)
        Scheduler.setParams(self.sortedPackageList, self.listOfPackagesAlreadyBuilt)
        Scheduler.setEvent(statusEvent)
        Scheduler.stopScheduling=False
    
    def buildGivenPackages (self, listPackages, buildThreads):
        returnVal=self.calculateParams(listPackages)
        if not returnVal:
            self.logger.error("Unable to set paramaters. Terminating the package manager.")
            raise Exception("Unable to set paramaters")
        
        statusEvent=threading.Event()
        self.initializeScheduler(statusEvent)
        self.initializeThreadPool(statusEvent)
        
        i=0
        while i < buildThreads:
            workerName="WorkerThread"+str(i)
            ThreadPool.addWorkerThread(workerName)
            ThreadPool.startWorkerThread(workerName)
            i = i + 1
        
        statusEvent.wait()
        Scheduler.stopScheduling=True
        self.logger.info("Waiting for all remaining worker threads")
        listWorkerObjs=ThreadPool.getAllWorkerObjects()
        for w in listWorkerObjs:
            w.join()
            
        setFailFlag=False
        allPackagesBuilt=False
        
        if Scheduler.isAnyPackagesFailedToBuild():
            setFailFlag=True
        
        if Scheduler.isAllPackagesBuilt():
            allPackagesBuilt=True
        
        if setFailFlag:
            self.logger.error("Some of the packages failed:")
            self.logger.error(Scheduler.listOfFailedPackages)
            raise Exception("Failed during building package")
        
        if not setFailFlag:
            if allPackagesBuilt:
                self.logger.info("All packages built successfully")
            else:
                self.logger.error("Build stopped unexpectedly.Unknown error.")
                raise Exception("Unknown error")
        
        self.logger.info("Terminated")

