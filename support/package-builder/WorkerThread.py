#!/usr/bin/env python3

import threading
import Scheduler
import ThreadPool

from PackageBuilder import PackageBuilder


class WorkerThread(threading.Thread):

    def __init__(self, event, name, mapPackageToCycle, logger, pkgBuildType):
        threading.Thread.__init__(self)
        self.statusEvent = event
        self.name = name
        self.mapPackageToCycle = mapPackageToCycle
        self.logger = logger
        self.pkgBuildType = pkgBuildType

    def run(self):
        ThreadPool.ThreadPool.makeWorkerThreadActive(self.name)
        self.logger.debug("Thread " + self.name + " is starting now")
        while True:
            pkg = Scheduler.Scheduler.getNextPackageToBuild()
            doneList = Scheduler.Scheduler.getDoneList()
            if pkg is None:
                break
            pkgBuilder = PackageBuilder(pkg, self.mapPackageToCycle, self.pkgBuildType)

            try:
                pkgBuilder.build(doneList)
            except Exception as e:
                self.logger.exception(e)
                Scheduler.Scheduler.notifyPackageBuildFailed(pkg)
                self.logger.debug(
                    "Thread " + self.name + " stopped building package:" + pkg
                )
                self.statusEvent.set()
                break
            Scheduler.Scheduler.notifyPackageBuildCompleted(pkg)

        ThreadPool.ThreadPool.makeWorkerThreadInActive(self.name)
        self.logger.debug("Thread " + self.name + " is going to rest")
