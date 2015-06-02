from PackageBuilder import PackageBuilder
import threading
import Scheduler
from constants import constants
import ThreadPool
 
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
        ThreadPool.ThreadPool.makeWorkerThreadActive(self.name)
        self.logger.info("Thread "+self.name +" is starting now")
        while True:
            outputMap={}
            pkg = Scheduler.Scheduler.getNextPackageToBuild()
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
                    Scheduler.Scheduler.notifyPackageBuildFailed(pkg)
                    self.logger.info("Thread "+self.name +" stopped building the "+pkg +" package")
                    break
            else:
                buildThreadFailed = True
                Scheduler.Scheduler.notifyPackageBuildFailed(pkg)
                self.logger.info("Thread "+self.name +" stopped building the "+pkg +" package")
                break
            
            Scheduler.Scheduler.notifyPackageBuildCompleted(pkg)
        
        if buildThreadFailed:
            self.statusEvent.set()
        
        ThreadPool.ThreadPool.makeWorkerThreadInActive(self.name)
        self.logger.info("Thread "+self.name +" is going to rest")
        


                    
                
        