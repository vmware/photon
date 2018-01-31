import WorkerThread

class ThreadPool(object):

    mapWorkerThreads = {}
    activeWorkerThreads = []
    inactiveWorkerThreads = []
    mapPackageToCycle = {}
    pkgBuildType = "chroot"
    logger = None
    statusEvent = None

    @staticmethod
    def clear():
        ThreadPool.mapWorkerThreads.clear()
        ThreadPool.activeWorkerThreads = []
        ThreadPool.inactiveWorkerThreads = []

    @staticmethod
    def addWorkerThread(workerThreadName):
        workerThread = WorkerThread.WorkerThread(
            ThreadPool.statusEvent,
            workerThreadName,
            ThreadPool.mapPackageToCycle,
            ThreadPool.logger,
            ThreadPool.pkgBuildType)
        ThreadPool.mapWorkerThreads[workerThreadName] = workerThread

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
        while ThreadPool.inactiveWorkerThreads and numOfThreadsToActivate > 0:
            threadName = ThreadPool.inactiveWorkerThreads.pop()
            ThreadPool.addWorkerThread(threadName)
            ThreadPool.startWorkerThread(threadName)
            ThreadPool.makeWorkerThreadActive(threadName)
            numOfThreadsToActivate = numOfThreadsToActivate -1

    @staticmethod
    def join_all():
        for p in ThreadPool.mapWorkerThreads.values():
            p.join()
