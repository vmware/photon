import threading
from PackageBuilder import PackageBuilderChroot
from PackageBuilder import PackageBuilderContainer
import Scheduler
import ThreadPool

class WorkerThread(threading.Thread):

    def __init__(self, event, name, mapPackageToCycle, logger,
                 pkgBuildType):
        threading.Thread.__init__(self)
        self.statusEvent = event
        self.name = name
        self.mapPackageToCycle = mapPackageToCycle
        self.logger = logger
        self.pkgBuildType = pkgBuildType

    def run(self):
        buildThreadFailed = False
        ThreadPool.ThreadPool.makeWorkerThreadActive(self.name)
        self.logger.debug("Thread " + self.name + " is starting now")
        while True:
            pkg = Scheduler.Scheduler.getNextPackageToBuild()
            if pkg is None:
                break
            if self.pkgBuildType == "chroot":
                pkgBuilder = PackageBuilderChroot(self.mapPackageToCycle,
                                                  self.pkgBuildType)
            elif self.pkgBuildType == "container":
                pkgBuilder = PackageBuilderContainer(self.mapPackageToCycle,
                                                     self.pkgBuildType)
            try:
                pkgBuilder.buildPackageFunction(pkg)
            except Exception as e:
                self.logger.exception(e)
                buildThreadFailed = True
                Scheduler.Scheduler.notifyPackageBuildFailed(pkg)
                self.logger.debug("Thread " + self.name + " stopped building package:" + pkg)
                self.statusEvent.set()
                break
            Scheduler.Scheduler.notifyPackageBuildCompleted(pkg)

        ThreadPool.ThreadPool.makeWorkerThreadInActive(self.name)
        self.logger.debug("Thread " + self.name + " is going to rest")
