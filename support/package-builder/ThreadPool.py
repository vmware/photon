
class ThreadPool(object):
    
    mapWorkerThreads={}
    activeWorkerThreads=[]
    inactiveWorkerThreads=[]
    
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
    def addWorkerThread(workerThreadName,workerThread):
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
            ThreadPool.startWorkerThread(threadName)
            ThreadPool.makeWorkerThreadActive(threadName)
            numOfThreadsToActivate = numOfThreadsToActivate -1

            
