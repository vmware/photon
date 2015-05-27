from PackageBuildDataGenerator import PackageBuildDataGenerator
from Logger import Logger
import threading
from constants import constants
import time
from PackageBuilder import PackageBuilder
import os
from PackageUtils import PackageUtils
from ToolChainUtils import ToolChainUtils

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
    
    def getRequiredPackages(self,package):
        listRequiredRPMPackages=[]
        listRequiredRPMPackages.extend(constants.specData.getBuildRequiresForPackage(package))
        listRequiredRPMPackages.extend(constants.specData.getRequiresAllForPackage(package))
        
        listRequiredPackages=[]
        for pkg in listRequiredRPMPackages:
            basePkg=constants.specData.getSpecName(pkg)
            if basePkg not in listRequiredPackages:
                listRequiredPackages.append(basePkg)
        
        return listRequiredPackages
                
    
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
    
    def checkIfAnyThreadsAreCompleted(self):
        readyToLaunchMoreThreads = False
        listThreadsObjToRemove=[]
        for t in self.listThreads:
            self.logger.debug("Checking thread "+t +", whether it is completed or not")
            #check if any thread is completed. If completed, we can start more threads.
            if self.mapOutputThread.has_key(t):
                output = self.mapOutputThread[t]
                self.logger.info("Output of thread "+t+" "+str(output))
                if not output:
                    self.logger.error("Thread "+ t+" is failed ")
                    self.logger.error("Unable to build package "+t)
                    raise Exception("Package builder failed")
                else:
                    self.logger.debug("Still running, not completed yet")
                    readyToLaunchMoreThreads=True
                    self.listPackagesToBuild.remove(t)
                    self.listOfPackagesAlreadyBuilt.append(t)
                    listThreadsObjToRemove.append(t)
                    if self.mapPackageToCycle.has_key(t):
                        self.listAvailableCyclicPackages.append(t)
        
        if not readyToLaunchMoreThreads:
            return False
            
        for k in listThreadsObjToRemove:
            tObj=self.listThreads.pop(k)
            if tObj.isAlive():
                self.logger.info("Thread is alive")
            else:
                self.logger.info("Thread is dead")
            self.logger.info(tObj.isAlive())

        return True
    
    #just to be safe, we have this method
    def checkIfAnyThreadsAreHanged(self):
        currentTime = time.time()
        listThreadsHanged=[]
        for t in self.listThreads:
            self.logger.debug("Checking thread "+t +", whether it is hanged or not")
            if not self.mapOutputThread.has_key(t):
                self.logger.debug("Calculating running time for thread "+t)
                launchTime = self.mapThreadsLaunchTime[t]
                if (currentTime - launchTime) > 7200.0:
                    listThreadsHanged.append(t)
            
        if len(listThreadsHanged) > 0:
            self.logger.info("Following threads are hanged")
            self.logger.info(listThreadsHanged)
            raise Exception("Threads are hanged")
    
    def waitTillNewThreadsCanBeSpawned(self):
        if len(self.listThreads) == 0:
            return
        while True:
            if self.checkIfAnyThreadsAreCompleted():
                break
            self.checkIfAnyThreadsAreHanged()
            self.logger.info("Sleeping for 10 seconds")
            time.sleep(10)
    
    def buildToolChain(self):
        try:
            tUtils=ToolChainUtils()
            tUtils.buildToolChain()
        except Exception as e:
            self.logger.error("Unable to build tool chain")
            self.logger.error(e)
            return False
        
        return True
        
    def buildPackages (self, listPackages):
        
        if not self.buildToolChain():
            return False

        returnVal=self.calculateParams(listPackages)
        if not returnVal:
            self.logger.error("Unable to set paramaters. Terminating the package manager.")
            return False
        
        returnVal = True
        try:
            while len(self.listPackagesToBuild) > 0:
                #Free some threads to launch next threads
                self.waitTillNewThreadsCanBeSpawned()
                
                listOfPackagesCanBeBuild=self.findNextPackageToBuild()
                if len(listOfPackagesCanBeBuild) == 0 and len(self.listPackagesToBuild) != 0:
                    self.logger.info("Waiting for current threads to complete to launch building new packages")
                
                for pkg in listOfPackagesCanBeBuild:
                    currentTime = time.time()
                    pkgBuilder = PackageBuilder(self.mapPackageToCycle,self.listAvailableCyclicPackages,"build-"+pkg,constants.logPath)
                    t = threading.Thread(target=pkgBuilder.buildPackageThreadAPI,args=(pkg,self.mapOutputThread,pkg))
                    self.listThreads[pkg]=t
                    self.mapThreadsLaunchTime[pkg]=currentTime
                    self.logger.info("Launching thread for package:"+pkg)
                    t.start()
                    self.logger.info("Started the thread for "+pkg)
                
                if len(self.listThreads) == 0 and len(self.listPackagesToBuild) != 0:
                    self.logger.error("Following packages are waiting for unknown package")
                    self.logger.error(self.listPackagesToBuild)
                    raise Exception("Invalid Schedule order")
                    
            self.logger.info( "Successfully built all the packages")

        except Exception as e:
            self.logger.error(str(e))
            self.logger.error("Caught exception.")
            self.logger.error("Failed and exited gracefully")
            returnVal = False
        finally:
            self.waitForRemainingThreads()
        return returnVal
    
    def waitForRemainingThreads(self):
        self.logger.info("Waiting for all remaining threads to complete")
        for t in self.listThreads:
            self.listThreads[t].join()
        return

    def findNextPackageToBuild(self):
        listOfPackagesNextToBuild=[]
        self.logger.info("Checking for next possible packages to build")
        for pkg in self.listPackagesToBuild:
            if self.listThreads.has_key(pkg):
                continue
            listRequiredPackages=self.getRequiredPackages(pkg)
            canBuild=True
            self.logger.info("Required packages for "+ pkg + " are:")
            self.logger.info(listRequiredPackages)
            for reqPkg in listRequiredPackages:
                if reqPkg not in self.listOfPackagesAlreadyBuilt:
                    canBuild=False
                    self.logger.info(reqPkg+" is not available. So we cannot build "+ pkg +" at this moment.")
                    break
            if canBuild:
                listOfPackagesNextToBuild.append(pkg)
        return listOfPackagesNextToBuild
                
                 
            
            
        
    
    
