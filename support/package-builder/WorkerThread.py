from PackageBuilder import PackageBuilder
import threading
from Scheduler import Scheduler
from constants import constants
from ThreadPool import ThreadPool
 
class WorkerThread(threading.Thread):
    
    def __init__(self,event,name,mapPackageToCycle,listAvailableCyclicPackages,logger):
        threading.Thread.__init__(self)
        self.statusEvent=event
        self.name=name
        self.mapPackageToCycle=mapPackageToCycle
        self.listAvailableCyclicPackages=listAvailableCyclicPackages
        self.logger=logger
    
    
    def run(self):
        buildThreadFailed=False
        ThreadPool.makeWorkerThreadActive(self.name)
        self.logger.info("Thread "+self.name +" is starting now")
        while True:
            outputMap={}
            pkg = Scheduler.getNextPackageToBuild()
            if pkg is None:
                break
            self.logger.info("Thread "+self.name+" is building package:"+ pkg)
            pkgBuilder = PackageBuilder(self.mapPackageToCycle,self.listAvailableCyclicPackages,"build-"+pkg,constants.logPath)
            t = threading.Thread(target=pkgBuilder.buildPackageThreadAPI,args=(pkg,outputMap,pkg))
            t.start()
            t.join()
            if outputMap.has_key(pkg):
                if outputMap[pkg] == False:
                    buildThreadFailed = True
                    Scheduler.notifyPackageBuildFailed(pkg)
                    self.logger.info("Thread "+self.name +" stopped building the "+pkg +" package")
                    break
            else:
                buildThreadFailed = True
                Scheduler.notifyPackageBuildFailed(pkg)
                self.logger.info("Thread "+self.name +" stopped building the "+pkg +" package")
                break
            
            Scheduler.notifyPackageBuildCompleted(pkg)
        
        if buildThreadFailed:
            self.statusEvent.set()
        
        ThreadPool.makeWorkerThreadInActive(self.name)
        self.logger.info("Thread "+self.name +" is going to rest")
        


                    
                
        