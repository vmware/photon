import threading
from queue import PriorityQueue
import json
from ThreadPool import ThreadPool
from constants import constants
from Logger import Logger
from SpecData import SPECS
from StringUtils import StringUtils


class DependencyGraphNode(object):

    def __init__(self, packageName, packageVersion, pkgWeight):

        self.packageName = packageName
        self.packageVersion = packageVersion

        self.buildRequiresPkgNodes = set() # Same as in spec file
        self.installRequiresPkgNodes = set() # Same as in spec file

        # Auxiliary build-requires packages.
        #
        # This is the result of "moving up" the (weak)
        # install-requires package dependencies to their ancestors
        # that actually need them as a build dependency (more details
        # in the code below). This is used to optimize the dependency
        # graph by reorganizing parent-child relationships based on
        # strong dependencies.
        self.auxBuildRequiresPkgNodes = set()

        # Accumulated install-requires packages.
        #
        # This is mostly used as a helper when building the graph
        # (specifically, as an intermediate step when computing
        # auxBuildRequiredPkgNodes), and is later unused.
        self.accumInstallRequiresPkgNodes = set()

        self.childPkgNodes = set() # Packages that I depend on.
        self.parentPkgNodes = set() # Packages that depend on me.

        self.selfWeight = pkgWeight # Own package weight.

        # Critical-chain-weight: The key scheduling metric.
        #
        # Weight of the critical chain that can be built starting from
        # this package. Higher the criticalChainWeight, more the
        # benefit from building this package as early as possible.
        self.criticalChainWeight = 0

        # Internal data-structure used to perform controlled
        # traversals of the dependency graph, as well as certain
        # sanity checks.
        self.numVisits = 0


class Scheduler(object):

    lock = threading.Lock()
    listOfAlreadyBuiltPackages = set()
    listOfPackagesToBuild = []
    listOfPackagesCurrentlyBuilding = set()
    sortedList = []
    listOfPackagesNextToBuild = PriorityQueue()
    listOfFailedPackages = []
    priorityMap = {}
    pkgWeights = {}
    logger = None
    event = None
    stopScheduling = False
    mapPackagesToGraphNodes = {}

    @staticmethod
    def setEvent(event):
        Scheduler.event = event

    @staticmethod
    def setLog(logName, logPath, logLevel):
        Scheduler.logger = Logger.getLogger(logName, logPath, logLevel)

    @staticmethod
    def setParams(sortedList, listOfAlreadyBuiltPackages):
        Scheduler.sortedList = sortedList

        Scheduler.listOfAlreadyBuiltPackages = listOfAlreadyBuiltPackages
        for x in Scheduler.sortedList:
            if x not in Scheduler.listOfAlreadyBuiltPackages or x in constants.testForceRPMS:
                Scheduler.listOfPackagesToBuild.append(x)
        Scheduler.listOfPackagesCurrentlyBuilding = set()
        Scheduler.listOfPackagesNextToBuild = PriorityQueue()
        Scheduler.listOfFailedPackages = []
        Scheduler._setPriorities()

    @staticmethod
    def notifyPackageBuildCompleted(package):
        with Scheduler.lock:
            if package in Scheduler.listOfPackagesCurrentlyBuilding:
                Scheduler.listOfPackagesCurrentlyBuilding.remove(package)
                Scheduler.listOfAlreadyBuiltPackages.add(package)

    @staticmethod
    def notifyPackageBuildFailed(package):
        with Scheduler.lock:
            if package in Scheduler.listOfPackagesCurrentlyBuilding:
                Scheduler.listOfPackagesCurrentlyBuilding.remove(package)
                Scheduler.listOfFailedPackages.append(package)

    @staticmethod
    def isAllPackagesBuilt():
        if Scheduler.listOfPackagesToBuild:
            return False
        return True

    @staticmethod
    def isAnyPackagesFailedToBuild():
        if Scheduler.listOfFailedPackages:
            return True
        return False

    @staticmethod
    def getNextPackageToBuild():
        with Scheduler.lock:
            if Scheduler.stopScheduling:
                return None

            if not Scheduler.listOfPackagesToBuild:
                if Scheduler.event is not None:
                    Scheduler.event.set()

            if Scheduler.listOfPackagesNextToBuild.empty():
                Scheduler._getListNextPackagesReadyToBuild()

            if Scheduler.listOfPackagesNextToBuild.empty():
                return None

            packageTup = Scheduler.listOfPackagesNextToBuild.get()

            package = packageTup[1]
            if Scheduler.listOfPackagesNextToBuild.qsize() > 0:
                ThreadPool.activateWorkerThreads(
                    Scheduler.listOfPackagesNextToBuild.qsize())
            Scheduler.listOfPackagesCurrentlyBuilding.add(package)
            Scheduler.listOfPackagesToBuild.remove(package)
            return package

    @staticmethod
    def getDoneList():
        return list(Scheduler.listOfAlreadyBuiltPackages)


    @staticmethod
    def _getBuildRequiredPackages(pkg):
        listRequiredRPMPackages = []
        listRequiredRPMPackages.extend(SPECS.getData().getBuildRequiresForPkg(pkg))

        listRequiredPackages = []

        for reqPkg in listRequiredRPMPackages:
            basePkg = SPECS.getData().getBasePkg(reqPkg)
            if basePkg not in listRequiredPackages:
                listRequiredPackages.append(basePkg)

        return listRequiredPackages


    def _createGraphNodes():

        # GRAPH-BUILD STEP 1: Initialize graph nodes for each package.
        #
        # Create a graph with a node to represent every package and all
        # its dependent packages in the given list.
        for package in Scheduler.sortedList:
            packageName, packageVersion = StringUtils.splitPackageNameAndVersion(package)
            node = DependencyGraphNode(packageName, packageVersion,
                                       Scheduler._getWeight(package))
            Scheduler.mapPackagesToGraphNodes[package] = node

        for package in Scheduler.sortedList:
            pkgNode = Scheduler.mapPackagesToGraphNodes[package]
            for childPackage in Scheduler._getBuildRequiredPackages(package):
                childPkgNode = Scheduler.mapPackagesToGraphNodes[childPackage]
                pkgNode.buildRequiresPkgNodes.add(childPkgNode)

            for childPackage in Scheduler._getRequiredPackages(package):
                childPkgNode = Scheduler.mapPackagesToGraphNodes[childPackage]
                pkgNode.installRequiresPkgNodes.add(childPkgNode)

        # GRAPH-BUILD STEP 2: Mark package dependencies in the graph.
        #
        # Add parent-child relationships between dependent packages.
        # If a package 'A' build-requires or install-requires package 'B', then:
        #   - Mark 'B' as a child of 'A' in the graph.
        #   - Mark 'A' as a parent of 'B' in the graph.
        #
        #                     A
        #
        #                  /     \
        #                 v       v
        #
        #                B         C
        #
        for package in Scheduler.sortedList:
            pkgNode = Scheduler.mapPackagesToGraphNodes[package]
            for childPkgNode in pkgNode.buildRequiresPkgNodes:
                pkgNode.childPkgNodes.add(childPkgNode)
                childPkgNode.parentPkgNodes.add(pkgNode)

            for childPkgNode in pkgNode.installRequiresPkgNodes:
                pkgNode.childPkgNodes.add(childPkgNode)
                childPkgNode.parentPkgNodes.add(pkgNode)

    def _optimizeGraph():

        # GRAPH-BUILD STEP 3: Convert weak (install-requires) dependencies
        #                     into strong (aux-build-requires) dependencies.
        #
        # Consider the following graph on the left, where package 'A'
        # install-requires 'B' and build-requires 'C'.  Package 'C'
        # install-requires 'D'. Package 'D' build-requires 'E' and
        # install-requires 'F'.
        #
        #  b     : build-requires dependency
        #  i     : install-requires dependency
        #  aux-b : auxiliary build-requires dependency (explained later)
        #
        # Now, we know that install-requires dependencies are weaker
        # than build-requires dependencies. That is, for example, in the
        # original graph below, package 'B' does not need to be built
        # before package 'A', but package 'C' must be built before
        # package 'A'.
        #
        # Using this knowledge, we optimize the graph by re-organizing
        # the dependencies such that all of them are strong (we call
        # these newly computed build-dependencies as "auxiliary build
        # dependencies"). The optimized graph for the example below is
        # presented on the right -- the key property of the optimized
        # graph is that every child package *MUST* be built before its
        # parent(s). This process helps relax package dependencies to
        # a great extent, by giving us the flexibility to delay
        # building certain packages until they are actually needed.
        # Another important benefit of this optimization is that it
        # nullifies certain dependencies altogether (eg: A->B), thereby
        # enabling a greater level of build-parallelism.
        #
        #      Original Graph                  Optimized Graph
        #                             +
        #          A                  |       B              A
        #                             +
        #       i / \ b               |                b/    |aux-b  \aux-b
        #        /   \                +                /     |        \
        #       v     v               |               v      v         v
        #                             +
        #      B        C             |              C       D          F
        #                             +
        #                \i           |                   b/
        #                 \           +                   /
        #                  v          |                  v
        #                             +
        #                  D          |                 E
        #                             +
        #                b/  \i       |
        #                /    \       +
        #               v      v      |
        #                             +
        #              E        F     |
        #
        #
        # In the code below, we use 'accumulated-install-requires' set
        # as a placeholder to bubble-up install-requires dependencies of
        # each package to all its ancestors. In each such path, we look
        # for the nearest ancestor that has a build-requires dependency
        # on that path going up from the given package to that ancestor.
        # If we find such an ancestor, we convert the bubbled-up
        # install-requires packages accumulated so far into the
        # auxiliary-build-requires set at that ancestor. (This is how
        # 'D' and 'F' become aux-build-requires of 'A' in the optimized
        # graph above).
        #
        # Graph Traversal : Bottom-up (starting with packages that
        #                   have no children).
        #
        nodesToVisit = set()
        for package in Scheduler.sortedList:
            pkgNode = Scheduler.mapPackagesToGraphNodes[package]
            if len(pkgNode.childPkgNodes) == 0:
                nodesToVisit.add(pkgNode)

        while nodesToVisit:
            pkgNode = nodesToVisit.pop()

            pkgNode.accumInstallRequiresPkgNodes |= pkgNode.installRequiresPkgNodes

            if len(pkgNode.childPkgNodes) == 0:
                # Count self-visit if you don't expect any other
                # visitors.
                pkgNode.numVisits += 1

            for parentPkgNode in pkgNode.parentPkgNodes:
                if (pkgNode not in parentPkgNode.buildRequiresPkgNodes) and \
                   (pkgNode not in parentPkgNode.installRequiresPkgNodes):
                    raise Exception ("Visitor to parent is not its child " + \
                                     " Visitor: " + pkgNode.packageName + \
                                     " Parent:  " + parentPkgNode.packageName)

                if pkgNode in parentPkgNode.buildRequiresPkgNodes:
                    parentPkgNode.auxBuildRequiresPkgNodes |= pkgNode.accumInstallRequiresPkgNodes
                else:
                    parentPkgNode.accumInstallRequiresPkgNodes |= pkgNode.accumInstallRequiresPkgNodes

                parentPkgNode.numVisits += 1
                # Each child is expected to visit the parent once.
                # Note that a package might have the same packages as
                # both build-requires and install-requires children.
                # They don't count twice.
                numExpectedVisits = len(parentPkgNode.childPkgNodes)
                if parentPkgNode.numVisits == numExpectedVisits:
                    nodesToVisit.add(parentPkgNode)
                elif parentPkgNode.numVisits > numExpectedVisits:
                    raise Exception ("Parent node visit count > num of children " + \
                                     " Parent node: " + parentPkgNode.packageName + \
                                     " Visit count: " + str(parentPkgNode.numVisits) + \
                                     " Num of children: " + str(numExpectedVisits))

            pkgNode.accumInstallRequiresPkgNodes.clear()

        # Clear out the visit counter for reuse.
        for package in Scheduler.sortedList:
            pkgNode = Scheduler.mapPackagesToGraphNodes[package]
            if pkgNode.numVisits == 0:
                raise Exception ("aux-build-requires calculation never visited " \
                                 "package " + pkgNode.packageName)
            else:
                pkgNode.numVisits = 0

        # GRAPH-BUILD STEP 4: Re-organize the dependencies in the graph based on
        #                     the above optimization.
        #
        # Now re-arrange parent-child relationships between packages using the
        # following criteria:
        # If a package 'A' build-requires or aux-build-requires package 'B', then:
        #   - Mark 'B' as a child of 'A' in the graph.
        #   - Mark 'A' as a parent of 'B' in the graph.
        # If a package 'A' only install-requires package 'B', then:
        #   - Remove 'B' as a child of 'A' in the graph.
        #   - Remove 'A' as a parent of 'B' in the graph.
        # No node should have a non-zero accum-install-requires set.

        for package in Scheduler.sortedList:
            pkgNode = Scheduler.mapPackagesToGraphNodes[package]
            childPkgNodesToRemove = set()
            for childPkgNode in pkgNode.childPkgNodes:
                if (childPkgNode not in pkgNode.buildRequiresPkgNodes) and \
                   (childPkgNode not in pkgNode.auxBuildRequiresPkgNodes):
                       # We can't modify a set during iteration, so we
                       # accumulate the set of children we want to
                       # remove, and delete them after the for-loop.
                       childPkgNodesToRemove.add(childPkgNode)
                       childPkgNode.parentPkgNodes.remove(pkgNode)

            pkgNode.childPkgNodes = pkgNode.childPkgNodes - \
                                    childPkgNodesToRemove

            for newChildPkgNode in pkgNode.auxBuildRequiresPkgNodes:
                pkgNode.childPkgNodes.add(newChildPkgNode)
                newChildPkgNode.parentPkgNodes.add(pkgNode)


    def _calculateCriticalChainWeights():

        # GRAPH-BUILD STEP 5: Calculate critical-chain-weight of packages.
        #
        # Calculation of critical-chain-weight (the key scheduling
        # metric):
        # --------------------------------------------------------
        # Let us define a "chain" of a given package to be the
        # sequence of parent packages that can be built starting from
        # that package. For example, if a package 'A' build-requires
        # 'B', which in turn build-requires 'C', then one of the
        # chains of 'C' is C->B->A. Now, if there are
        # multiple such chains possible from 'C', then we define the
        # "critical-chain" of 'C' to be the longest of those chains,
        # where "longest" is determined by the time it takes to build
        # all the packages in that chain. The build-times of any two
        # chains can be compared based on the sum of the
        # individual weights of each package in their respective
        # chains.
        #
        # Below, we calculate the critical-chain-weight of each
        # package (which is the maximum weight of all the paths
        # leading up to that package). Later on, we will schedule
        # package-builds by the decreasing order of the packages'
        # critical-chain-weight.
        #
        #
        #               ...  ...        ...
        #                 \   |         /
        #                  v  v        v
        #
        #                     A        B        C
        #
        #                      \       |       /
        #                       \      |      /
        #                        v     v     v
        #
        #                              D
        #
        #                            /
        #                           /
        #                          v
        #
        #                          E
        #
        #
        # In the above graph, the critical chain weight of 'D' is
        # computed as:
        # criticalChainWeight(D) = weight(D) +
        #                          max (criticalChainWeight(A),
        #                               criticalChainWeight(B),
        #                               weight(C))
        #
        # Graph Traversal : Top-down (starting with packages that
        #                   have no parents).
        #
        nodesToVisit = set()
        for package in Scheduler.sortedList:
            pkgNode = Scheduler.mapPackagesToGraphNodes[package]
            if len(pkgNode.parentPkgNodes) == 0:
                nodesToVisit.add(pkgNode)

        while nodesToVisit:
            pkgNode = nodesToVisit.pop()

            if len(pkgNode.parentPkgNodes) == 0:
                pkgNode.criticalChainWeight = pkgNode.selfWeight
                # Count self-visit if you don't expect any other
                # visitors.
                pkgNode.numVisits += 1

            for childPkgNode in pkgNode.childPkgNodes:
                if pkgNode not in childPkgNode.parentPkgNodes:
                    raise Exception ("Visitor to child node is not its parent " + \
                                     " Visitor: " + pkgNode.packageName + \
                                     " Child node: " + childPkgNode.packageName)

                if childPkgNode.numVisits == len(childPkgNode.parentPkgNodes):
                    raise Exception ("Child node visit count > number of parents " + \
                                     " Child node: " + childPkgNode.packageName + \
                                     " Visit count: " + childPkgNode.numVisits + \
                                     " Num of parents: " + \
                                     str(len(childPkgNode.parentPkgNodes)))

                childPkgNode.criticalChainWeight = max(
                    childPkgNode.criticalChainWeight,
                    pkgNode.criticalChainWeight + childPkgNode.selfWeight)

                childPkgNode.numVisits += 1
                # We can visit this package's children only after this
                # package has been visited by all its parents (thus
                # guaranteeing that its criticalChainWeight has
                # stabilized).
                if childPkgNode.numVisits == len(childPkgNode.parentPkgNodes):
                    nodesToVisit.add(childPkgNode)

        # Clear out the visit counter for reuse.
        for package in Scheduler.sortedList:
            pkgNode = Scheduler.mapPackagesToGraphNodes[package]
            if pkgNode.numVisits == 0:
                raise Exception ("critical-chain-weight calculation never visited " + \
                                 "package " + pkgNode.packageName)
            else:
                pkgNode.numVisits = 0


    def _buildGraph():
        Scheduler._createGraphNodes()
        Scheduler._optimizeGraph()
        Scheduler._calculateCriticalChainWeights()


    @staticmethod
    def _parseWeights():
        Scheduler.pkgWeights.clear()
        with open(constants.packageWeightsPath, 'r') as weightFile:
            Scheduler.pkgWeights = json.load(weightFile)

    # A package's weight is an indicator of the time required to build
    # that package, relative to other packages. These weights do not
    # take build-time/install-time dependencies into account -- they
    # are the individual build-times of the respective packages.
    # Package weights are positive integers, with a default value of 1.
    @staticmethod
    def _getWeight(package):
	# Package weights are assumed to be independent of package
	# version (i.e., in the case of multi-version packages such as
	# Go or Kubernetes, all the versions have the same weight). So
	# convert packageName-version to packageName before looking up
	# the package weight.
        package, _ = StringUtils.splitPackageNameAndVersion(package)
        try:
            return int(Scheduler.pkgWeights[package]) + 1
        except KeyError:
            return 1

    @staticmethod
    def _getPriority(package):
        try:
            return int(Scheduler.priorityMap[package])
        except KeyError:
            return 0


    @staticmethod
    def _setPriorities():
        if constants.packageWeightsPath is None:
            Scheduler.logger.debug("Priority Scheduler disabled")
            if constants.publishBuildDependencies:
                Scheduler.logger.debug("Publishing Build dependencies")
                Scheduler._buildGraph()
        else:
            Scheduler.logger.debug("Priority Scheduler enabled")
            Scheduler._parseWeights()

            Scheduler._buildGraph()

            for package in Scheduler.sortedList:
                pkgNode = Scheduler.mapPackagesToGraphNodes[package]
                Scheduler.priorityMap[package] = pkgNode.criticalChainWeight

            Scheduler.logger.debug("set Priorities: Priority of all packages")
            Scheduler.logger.debug(Scheduler.priorityMap)


    @staticmethod
    def _getRequiredPackages(pkg):
        listRequiredRPMPackages = []
        listRequiredRPMPackages.extend(SPECS.getData().getRequiresAllForPkg(pkg))

        listRequiredPackages = []

        for reqPkg in listRequiredRPMPackages:
            basePkg = SPECS.getData().getBasePkg(reqPkg)
            if basePkg not in listRequiredPackages:
                listRequiredPackages.append(basePkg)

        return listRequiredPackages

    @staticmethod
    def _getListNextPackagesReadyToBuild():
        for pkg in Scheduler.listOfPackagesToBuild:
            if pkg in Scheduler.listOfPackagesCurrentlyBuilding:
                continue
            listRequiredPackages = list(set(Scheduler._getBuildRequiredPackages(pkg) + \
                                   Scheduler._getRequiredPackages(pkg)))

            canBuild = True
            for reqPkg in listRequiredPackages:
                if reqPkg not in Scheduler.listOfAlreadyBuiltPackages:
                    canBuild = False
                    break
            if canBuild:
                Scheduler.listOfPackagesNextToBuild.put((-Scheduler._getPriority(pkg), pkg))
                Scheduler.logger.debug("Adding " + pkg + " to the schedule list")
