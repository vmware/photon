
import WorkerThread
class ThreadPool(object):
    
    mapWorkerThreads={}
    activeWorkerThreads=[]
    inactiveWorkerThreads=[]
    mapPackageToCycle={}
    listAvailableCyclicPackages=[]
    listBuildOptionPackages=[]
    pkgBuildOptionFile=""
    pkgBuildType=""
    logger=None
    statusEvent=None
    
    @staticmethod
    def clear():
        ThreadPool.mapWorkerThreads.clear()
        ThreadPool.activeWorkerThreads=[]
        ThreadPool.inactiveWorkerThreads=[]
    
    @staticmethod
    def getAllWorkerObjects():
        listWorkerObjs=[]
        listWorkerKeys = ThreadPool.mapWorkerThreads.keys()
        for x in listWorkerKeys:
            xobj=ThreadPool.mapWorkerThreads[x]
            listWorkerObjs.append(xobj)
        return listWorkerObjs
        
    @staticmethod
    def addWorkerThread(workerThreadName):
        workerThread = WorkerThread.WorkerThread(
                ThreadPool.statusEvent,
                workerThreadName,
                ThreadPool.mapPackageToCycle,
                ThreadPool.listAvailableCyclicPackages,
                ThreadPool.logger,
                ThreadPool.listBuildOptionPackages,
                ThreadPool.pkgBuildOptionFile,
                ThreadPool.pkgBuildType)
        ThreadPool.mapWorkerThreads[workerThreadName]=workerThread
   
    @staticmethod
    def makeWorkerThreadActive(threadName):
        if threadName in ThreadPool.inactiveWorkerThreads:
            ThreadPool.inactiveWorkerThreads.remove(threadName)
        ThreadPool.activeWorkerThreads.append(threadName)
        
    @staticmethod
    def makeWorkerThreadInActive(threadName):
        if threadName in ThreadPool.activeWorkerThreads:
            ThreadPool.activeWorkerThreads.remove(threadName)
        ThreadPool.inactiveWorkerThreads.append(threadName)
    
    @staticmethod
    def startWorkerThread(threadName):
        ThreadPool.mapWorkerThreads[threadName].start()
    
    @staticmethod
    def getListInactiveWorkerThreads():
        return ThreadPool.inactiveWorkerThreads
    
    @staticmethod
    def activateWorkerThreads(numOfThreadsToActivate):
        while len(ThreadPool.inactiveWorkerThreads) > 0 and numOfThreadsToActivate > 0:
            threadName=ThreadPool.inactiveWorkerThreads.pop()
            ThreadPool.addWorkerThread(threadName)
            ThreadPool.startWorkerThread(threadName)
            ThreadPool.makeWorkerThreadActive(threadName)
            numOfThreadsToActivate = numOfThreadsToActivate -1

            
