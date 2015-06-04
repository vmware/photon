from PackageBuildDataGenerator import PackageBuildDataGenerator
from Logger import Logger
import threading
from constants import constants
import os
from PackageUtils import PackageUtils
from ToolChainUtils import ToolChainUtils
from Scheduler import Scheduler
from ThreadPool import ThreadPool
import subprocess

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
        self.listPackagesToBuild=[]
        
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
            package = pkgUtils.findPackageNameFromRPMFile(rpmfile)
            listAvailablePackages.append(package)
        return listAvailablePackages
    
    def calculateParams(self,listPackages):
        self.listThreads.clear()
        self.mapOutputThread.clear()
        self.mapThreadsLaunchTime.clear()
        self.listAvailableCyclicPackages=[]
        self.mapCyclesToPackageList.clear()
        self.mapPackageToCycle.clear()
        self.sortedPackageList=[]
        self.listPackagesToBuild=[]
        
        if not self.readPackageBuildData(listPackages):
            return False
        
        self.listOfPackagesAlreadyBuilt = self.readAlreadyAvailablePackages()
        
        self.listPackagesToBuild=self.sortedPackageList[:]
        for pkg in self.sortedPackageList:
            if pkg in self.listOfPackagesAlreadyBuilt:
                self.listPackagesToBuild.remove(pkg)
        
        self.logger.info(self.listPackagesToBuild)
        self.logger.info(listPackages)
        
        return True
    
    def buildToolChain(self):
        try:
            tUtils=ToolChainUtils()
            tUtils.buildCoreToolChainPackages()
        except Exception as e:
            self.logger.error("Unable to build tool chain")
            self.logger.error(e)
            return False
        
        return True
    
    def calculatePossibleNumWorkerThreads(self):
        process = subprocess.Popen(["df" ,constants.buildRootPath],shell=True,stdout=subprocess.PIPE)
        retval = process.wait()
        if retval != 0:
            self.logger.error("Unable to check free space. Unknown error.")
            return False
        output = process.communicate()[0]
        device, size, used, available, percent, mountpoint = output.split("\n")[1].split()
        c =  int(available)/600000
        numChroots=int(c)
        self.logger.info("Possible number of worker threads:"+str(numChroots))
        return numChroots
    
    def buildToolChainPackages(self):
        if not self.buildToolChain():
            return False
        return self.buildGivenPackages(constants.listToolChainPackages)
        
    def buildPackages(self,listPackages):
        if not self.buildToolChainPackages():
            return False
        return self.buildGivenPackages(listPackages)
    
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
    
    def buildGivenPackages (self, listPackages):
        returnVal=self.calculateParams(listPackages)
        if not returnVal:
            self.logger.error("Unable to set paramaters. Terminating the package manager.")
            return False
        
        statusEvent=threading.Event()
        numWorkerThreads=self.calculatePossibleNumWorkerThreads()
        if numWorkerThreads > 8:
            numWorkerThreads = 8
        if numWorkerThreads == 0:
            return False
         
        self.initializeScheduler(statusEvent)
        self.initializeThreadPool(statusEvent)
        
        i=0
        while i < numWorkerThreads:
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
        
        if not setFailFlag:
            if allPackagesBuilt:
                self.logger.info("All packages built successfully")
            else:
                self.logger.error("Build stopped unexpectedly.Unknown error.")
        
        self.logger.info("Terminated")
