import threading
from PackageBuilder import PackageBuilderChroot
from PackageBuilder import PackageBuilderContainer
import Scheduler
import ThreadPool

class WorkerThread(threading.Thread):

    def __init__(self, event, name, mapPackageToCycle, listAvailableCyclicPackages, logger,
                 listBuildOptionPackages, pkgBuildOptionFile, pkgBuildType):
        threading.Thread.__init__(self)
        self.statusEvent = event
        self.name = name
        self.mapPackageToCycle = mapPackageToCycle
        self.listAvailableCyclicPackages = listAvailableCyclicPackages
        self.logger = logger
        self.listBuildOptionPackages = listBuildOptionPackages
        self.pkgBuildOptionFile = pkgBuildOptionFile
        self.pkgBuildType = pkgBuildType

    def run(self):
        buildThreadFailed = False
        ThreadPool.ThreadPool.makeWorkerThreadActive(self.name)
        self.logger.info("Thread " + self.name + " is starting now")
        while True:
            outputMap = {}
            pkg = Scheduler.Scheduler.getNextPackageToBuild()
            if pkg is None:
                break
            self.logger.info("Thread " + self.name + " is building package:" + pkg)
            if self.pkgBuildType == "chroot":
                pkgBuilder = PackageBuilderChroot(self.mapPackageToCycle,
                                                  self.listAvailableCyclicPackages,
                                                  self.listBuildOptionPackages,
                                                  self.pkgBuildOptionFile,
                                                  self.pkgBuildType)
            elif self.pkgBuildType == "container":
                pkgBuilder = PackageBuilderContainer(self.mapPackageToCycle,
                                                     self.listAvailableCyclicPackages,
                                                     self.listBuildOptionPackages,
                                                     self.pkgBuildOptionFile,
                                                     self.pkgBuildType)
            t = threading.Thread(target=pkgBuilder.buildPackageThreadAPI,
                                 args=(pkg, outputMap, pkg))
            t.start()
            t.join()
            if pkg not in outputMap or outputMap[pkg] == False:
                buildThreadFailed = True
                Scheduler.Scheduler.notifyPackageBuildFailed(pkg)
                self.logger.info("Thread "+self.name +" stopped building package:" + pkg)
                break
            self.logger.info("Thread "+ self.name + " finished building package:" + pkg)
            Scheduler.Scheduler.notifyPackageBuildCompleted(pkg)

        if buildThreadFailed:
            self.statusEvent.set()

        ThreadPool.ThreadPool.makeWorkerThreadInActive(self.name)
        self.logger.info("Thread "+self.name +" is going to rest")
