#!/usr/bin/env python3

import json
import threading
from queue import PriorityQueue

from constants import BuildMode, BuildStage, constants
from Logger import Logger
from SpecData import SPECS
from StringUtils import StringUtils
from ThreadPool import ThreadPool


class DependencyGraphNode(object):
    def __init__(self, packageName, packageVersion, pkgWeight):
        self.packageName = packageName
        self.packageVersion = packageVersion

        self.buildRequiresPkgNodes = set()  # Same as in spec file
        self.installRequiresPkgNodes = set()  # Same as in spec file

        """
        Auxiliary build-requires packages.

        This is the result of "moving up" the (weak)
        install-requires package dependencies to their ancestors
        that actually need them as a build dependency (more details
        in the code below). This is used to optimize the dependency
        graph by reorganizing parent-child relationships based on
        strong dependencies.
        """
        self.auxBuildRequiresPkgNodes = set()

        """
        Accumulated install-requires packages.

        This is mostly used as a helper when building the graph
        (specifically, as an intermediate step when computing
        auxBuildRequiredPkgNodes), and is later unused.
        """
        self.accumInstallRequiresPkgNodes = set()

        self.childPkgNodes = set()  # Package nodes that I directly depend on.
        self.allRequiredPackages = []  # Full packages list that I depend on to build myself.
        self.parentPkgNodes = set()  # Packages that depend on me.

        self.selfWeight = pkgWeight  # Own package weight.

        """
        Critical-chain-weight: The key scheduling metric.

        Weight of the critical chain that can be built starting from
        this package. Higher the criticalChainWeight, more the
        benefit from building this package as early as possible.
        """
        self.criticalChainWeight = 0

        """
        Internal data-structure used to perform controlled
        traversals of the dependency graph, as well as certain
        confidence checks.
        """
        self.numVisits = 0

        # Internal flag to check if the package is built
        self.built = 0

    def __str__(self):
        return f"{self.packageName}-{self.packageVersion}"


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
    buildStage = BuildStage.NONE
    buildMode = BuildMode.STANDARD

    # ---------- build-cost / load tracking -----------------------------------

    # Logging thresholds (in JSON units).
    BUILD_COST_WARN_THRESHOLD = 10
    # A package whose cost exceeds this threshold is treated as "standalone":
    # at most one such package may build at a time (lighter packages still run
    # freely alongside it).  Set high so only truly exceptional packages
    # trigger standalone mode; add them to packageWeights.json with cost > 1000
    # when identified.
    BUILD_COST_FAIL_THRESHOLD = 1000

    # Elapsed seconds per package name, accumulated across all build stages.
    # Used exclusively by _computeSpeedFactor() to calibrate the host speed
    # from anchor package timings. Not written to disk.
    buildTimings = {}

    # Running sum of build_costs of packages currently being built.
    currentLoad = 0

    # Maximum allowed concurrent load (0 = unlimited).
    # Set by setMaxConcurrentLoad() before the build starts.
    maxConcurrentLoad = 0

    # Number of heavy packages (cost > BUILD_COST_FAIL_THRESHOLD) currently
    # building. Capped at 1: a second heavy is always deferred until the
    # first finishes. Light packages are never blocked by this counter.
    heavyPackagesBuilding = 0

    # Packages used as calibration anchors for the speed-factor computation.
    # Populated from the "__anchors__" key in packageWeights.json at parse time.
    # When non-empty, _computeSpeedFactor() derives the machine speed ratio
    # exclusively from these packages, making normalization independent of which
    # other packages happened to be measured in a partial build.
    anchorPackages = set()

    # ---------- end build-cost / load tracking --------------------------------

    @staticmethod
    def setEvent(event):
        Scheduler.event = event

    @staticmethod
    def setBuildStage(buildStage):
        Scheduler.buildStage = buildStage

    @staticmethod
    def setBuildMode(buildMode):
        Scheduler.buildMode = buildMode

    @staticmethod
    def setLog(logName, logPath, logLevel):
        Scheduler.logger = Logger.getLogger(logName, logPath, logLevel)

    @staticmethod
    def setMaxConcurrentLoad(buildThreads):
        """
        Cap the total build-cost of simultaneously running packages.

        Budget = buildThreads × BUILD_COST_FAIL_THRESHOLD.  A package is
        "standalone" only if its cost exceeds BUILD_COST_FAIL_THRESHOLD (1000);
        no current package in packageWeights.json reaches that threshold, so
        all packages build freely in parallel up to the thread count.
        Pass buildThreads=0 to disable throttling entirely.
        """
        Scheduler.maxConcurrentLoad = buildThreads * Scheduler.BUILD_COST_FAIL_THRESHOLD
        Scheduler.currentLoad = 0
        Scheduler.heavyPackagesBuilding = 0
        # buildTimings is intentionally NOT cleared here so that timings from
        # earlier stages (CORE_TOOLCHAIN, TOOLCHAIN) survive into the parallel
        # PACKAGES stage.  _adjustWeightsForHost() uses those anchor timings to
        # calibrate the package weights before the dependency graph is built.

    @staticmethod
    def setParams(sortedList, listOfAlreadyBuiltPackages):
        Scheduler.sortedList = sortedList

        Scheduler.listOfAlreadyBuiltPackages = listOfAlreadyBuiltPackages

        for pkg in Scheduler.sortedList:
            pkgName, pkgVersion = StringUtils.splitPackageNameAndVersion(pkg)
            if pkg not in Scheduler.listOfAlreadyBuiltPackages:
                Scheduler.listOfPackagesToBuild.append(pkg)

        Scheduler.listOfPackagesCurrentlyBuilding = set()
        Scheduler.listOfPackagesNextToBuild = PriorityQueue()
        Scheduler.listOfFailedPackages = []

        # When performing (only) make-check, package dependencies are
        # irrelevant; i.e., all the packages can be "make-checked" in
        # parallel. So skip building the dependency graph. This is not
        # merely an optimization! A given package can define
        # additional packages to be installed in its build environment
        # when performing a make-check, under %if %{with_check}.
        # However, these are not really build-time-dependencies in the
        # usual sense; i.e., there is no ordering requirement when
        # building these packages; they only make sense when running a
        # `make check`. Hence, trying to build a dependency graph out
        # of them will result in anomalies such as cycles in the
        # graph. So skip building the graph altogether and schedule
        # all the `make check`s in parallel.
        skipGraphBuild = constants.rpmCheck
        Scheduler._setPriorities(skipGraphBuild)

    @staticmethod
    def notifyPackageBuildCompleted(package, elapsed=0.0):
        with Scheduler.lock:
            if package in Scheduler.listOfPackagesCurrentlyBuilding:
                Scheduler.listOfPackagesCurrentlyBuilding.remove(package)
                Scheduler.listOfAlreadyBuiltPackages.add(package)
                pkgCost = Scheduler._getWeight(package) - 1
                Scheduler.currentLoad = max(0, Scheduler.currentLoad - pkgCost)
                if pkgCost > Scheduler.BUILD_COST_FAIL_THRESHOLD:
                    Scheduler.heavyPackagesBuilding = max(
                        0, Scheduler.heavyPackagesBuilding - 1
                    )
                if elapsed > 0:
                    pkgName, _ = StringUtils.splitPackageNameAndVersion(package)
                    Scheduler.buildTimings[pkgName] = elapsed
                if not constants.rpmCheck:
                    Scheduler._markPkgNodeAsBuilt(package)
                Scheduler.printStatus()

    @staticmethod
    def notifyPackageBuildFailed(package):
        with Scheduler.lock:
            if package in Scheduler.listOfPackagesCurrentlyBuilding:
                Scheduler.listOfPackagesCurrentlyBuilding.remove(package)
                pkgCost = Scheduler._getWeight(package) - 1
                Scheduler.currentLoad = max(0, Scheduler.currentLoad - pkgCost)
                if pkgCost > Scheduler.BUILD_COST_FAIL_THRESHOLD:
                    Scheduler.heavyPackagesBuilding = max(
                        0, Scheduler.heavyPackagesBuilding - 1
                    )
                Scheduler.listOfFailedPackages.append(package)
                Scheduler.printStatus()

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
    def isAnyPackagesCurrentlyBuilding():
        if Scheduler.listOfPackagesCurrentlyBuilding:
            return True
        return False

    @staticmethod
    def getNextPackageToBuild():
        with Scheduler.lock:
            if Scheduler.stopScheduling:
                return None, Scheduler.buildStage, Scheduler.buildMode

            if not Scheduler.listOfPackagesToBuild:
                if Scheduler.event is not None:
                    Scheduler.event.set()

            if Scheduler.listOfPackagesNextToBuild.empty():
                Scheduler._getListNextPackagesReadyToBuild()

            if Scheduler.listOfPackagesNextToBuild.empty():
                return None, Scheduler.buildStage, Scheduler.buildMode

            packageTup = Scheduler.listOfPackagesNextToBuild.get()

            package = packageTup[1]
            if (
                not constants.startSchedulerServer
                and Scheduler.listOfPackagesNextToBuild.qsize() > 0
            ):
                ThreadPool.activateWorkerThreads(
                    Scheduler.listOfPackagesNextToBuild.qsize()
                )
            Scheduler.listOfPackagesCurrentlyBuilding.add(package)
            Scheduler.listOfPackagesToBuild.remove(package)
            pkgCost = Scheduler._getWeight(package) - 1
            Scheduler.currentLoad += pkgCost
            if pkgCost > Scheduler.BUILD_COST_FAIL_THRESHOLD:
                Scheduler.heavyPackagesBuilding += 1
            Scheduler.printStatus()
            return package, Scheduler.buildStage, Scheduler.buildMode

    @staticmethod
    def printStatus():
        Scheduler.logger.info(
            "Package Status: Total: {} Building: {} Broken: {} Pending: {} Done: {}".format(  # noqa: E501
                len(Scheduler.sortedList),
                len(Scheduler.listOfPackagesCurrentlyBuilding),
                len(Scheduler.listOfFailedPackages),
                len(Scheduler.listOfPackagesToBuild),
                len(Scheduler.listOfAlreadyBuiltPackages),
            )
        )

    @staticmethod
    def getDoneList():
        return list(Scheduler.listOfAlreadyBuiltPackages)

    @staticmethod
    def _publishBuildDependencies():
        Scheduler.logger.debug("Publishing Build dependencies")
        dependencyLists = {}
        for package in list(Scheduler.mapPackagesToGraphNodes.keys()):
            dependencyLists[package] = []
            pkgNode = Scheduler.mapPackagesToGraphNodes[package]
            for childPkg in list(pkgNode.childPkgNodes):
                dependencyLists[package].append(
                    childPkg.packageName + "-" + childPkg.packageVersion
                )
        with open(str(constants.logPath) + "/BuildDependencies.json", "w") as graphfile:
            graphfile.write(json.dumps(dependencyLists, sort_keys=True, indent=4))

    @staticmethod
    def __getRequiredTypePackages(pkg, requiresType):
        listRPMPackages = []
        if requiresType == "build":
            listRPMPackages.extend(SPECS.getData().getBuildRequiresForPkg(pkg))
        elif requiresType == "install":
            listRPMPackages.extend(SPECS.getData().getRequiresAllForPkg(pkg))

        # Remove duplicates.
        listRPMPackages = list(set(listRPMPackages))

        listPackages = set()

        for reqPkg in listRPMPackages:
            basePkg = SPECS.getData().getBasePkg(reqPkg)
            listPackages.add(basePkg)

        return list(listPackages)

    @staticmethod
    def _getBuildRequiredPackages(pkg):
        return Scheduler.__getRequiredTypePackages(pkg, "build")

    @staticmethod
    def _getRequiredPackages(pkg):
        return Scheduler.__getRequiredTypePackages(pkg, "install")

    def _createNodes():
        # Create a graph node to represent every package
        for package in Scheduler.sortedList:
            (
                packageName,
                packageVersion,
            ) = StringUtils.splitPackageNameAndVersion(package)
            node = DependencyGraphNode(
                packageName, packageVersion, Scheduler._getWeight(package)
            )
            Scheduler.mapPackagesToGraphNodes[package] = node

            if package in Scheduler.listOfAlreadyBuiltPackages:
                node.built = 1

    def _createGraphNodes():
        # GRAPH-BUILD STEP 1: Initialize graph nodes for each package.
        #
        # Create a graph with a node to represent every package and all
        # its dependent packages in the given list.
        Scheduler._createNodes()

        for package in Scheduler.sortedList:
            pkgNode = Scheduler.mapPackagesToGraphNodes[package]
            for childPackage in Scheduler._getBuildRequiredPackages(package):
                childPkgNode = Scheduler.mapPackagesToGraphNodes[childPackage]
                pkgNode.buildRequiresPkgNodes.add(childPkgNode)

            for childPackage in Scheduler._getRequiredPackages(package):
                childPkgNode = Scheduler.mapPackagesToGraphNodes[childPackage]
                pkgNode.installRequiresPkgNodes.add(childPkgNode)

        """
        GRAPH-BUILD STEP 2: Mark package dependencies in the graph.

        Add parent-child relationships between dependent packages.
        If a package 'A' build-requires or install-requires package 'B', then:
           - Mark 'B' as a child of 'A' in the graph.
           - Mark 'A' as a parent of 'B' in the graph.

                             A

                          /     \
                         v       v

                        B         C
       """
        for package in Scheduler.sortedList:
            pkgNode = Scheduler.mapPackagesToGraphNodes[package]

            for childPkgNode in pkgNode.buildRequiresPkgNodes:
                pkgNode.childPkgNodes.add(childPkgNode)
                childPkgNode.parentPkgNodes.add(pkgNode)

            for childPkgNode in pkgNode.installRequiresPkgNodes:
                pkgNode.childPkgNodes.add(childPkgNode)
                childPkgNode.parentPkgNodes.add(pkgNode)

    def _optimizeGraph():
        r"""
        GRAPH-BUILD STEP 3: Convert weak (install-requires) dependencies
                             into strong (aux-build-requires) dependencies.

         Consider the following graph on the left, where package 'A'
         install-requires 'B' and build-requires 'C'.  Package 'C'
         install-requires 'D'. Package 'D' build-requires 'E' and
         install-requires 'F'.

          b     : build-requires dependency
          i     : install-requires dependency
          aux-b : auxiliary build-requires dependency (explained later)

         Now, we know that install-requires dependencies are weaker
         than build-requires dependencies. That is, for example, in the
         original graph below, package 'B' does not need to be built
         before package 'A', but package 'C' must be built before
         package 'A'.

         Using this knowledge, we optimize the graph by re-organizing
         the dependencies such that all of them are strong (we call
         these newly computed build-dependencies as "auxiliary build
         dependencies"). The optimized graph for the example below is
         presented on the right -- the key property of the optimized
         graph is that every child package *MUST* be built before its
         parent(s). This process helps relax package dependencies to
         a great extent, by giving us the flexibility to delay
         building certain packages until they are actually needed.
         Another important benefit of this optimization is that it
         nullifies certain dependencies altogether (eg: A->B), thereby
         enabling a greater level of build-parallelism.

              Original Graph                  Optimized Graph
                                     +
                  A                  |       B              A
                                     +
               i / \ b               |                b/    |aux-b  \aux-b
                /   \                +                /     |        \
               v     v               |               v      v         v
                                     +
              B        C             |              C       D          F
                                     +
                        \i           |                   b/
                         \           +                   /
                          v          |                  v
                                     +
                          D          |                 E
                                     +
                        b/  \i       |
                        /    \       +
                       v      v      |
                                     +
                      E        F     |


         In the code below, we use 'accumulated-install-requires' set
         as a placeholder to bubble-up install-requires dependencies of
         each package to all its ancestors. In each such path, we look
         for the nearest ancestor that has a build-requires dependency
         on that path going up from the given package to that ancestor.
         If we find such an ancestor, we convert the bubbled-up
         install-requires packages accumulated so far into the
         auxiliary-build-requires set at that ancestor. (This is how
         'D' and 'F' become aux-build-requires of 'A' in the optimized
         graph above).

         Graph Traversal : Bottom-up (starting with packages that
                           have no children).
        """
        nodesToVisit = set()
        for package in Scheduler.sortedList:
            pkgNode = Scheduler.mapPackagesToGraphNodes[package]
            if len(pkgNode.childPkgNodes) == 0:
                nodesToVisit.add(pkgNode)

        while nodesToVisit:
            pkgNode = nodesToVisit.pop()

            pkgNode.accumInstallRequiresPkgNodes |= pkgNode.installRequiresPkgNodes

            if len(pkgNode.childPkgNodes) == 0:
                """
                Count self-visit if you don't expect any other
                visitors.
                """
                pkgNode.numVisits += 1

            for parentPkgNode in pkgNode.parentPkgNodes:
                if (pkgNode not in parentPkgNode.buildRequiresPkgNodes) and (
                    pkgNode not in parentPkgNode.installRequiresPkgNodes
                ):
                    raise Exception(
                        "Visitor to parent is not its child "
                        f"Visitor: {pkgNode.packageName} "
                        f"Parent: {parentPkgNode.packageName}"
                    )

                if pkgNode in parentPkgNode.buildRequiresPkgNodes:
                    parentPkgNode.auxBuildRequiresPkgNodes |= (
                        pkgNode.accumInstallRequiresPkgNodes
                    )
                else:
                    parentPkgNode.accumInstallRequiresPkgNodes |= (
                        pkgNode.accumInstallRequiresPkgNodes
                    )

                parentPkgNode.numVisits += 1
                """
                Each child is expected to visit the parent once.
                Note that a package might have the same packages as
                both build-requires and install-requires children.
                They don't count twice.
                """
                numExpectedVisits = len(parentPkgNode.childPkgNodes)
                if parentPkgNode.numVisits == numExpectedVisits:
                    nodesToVisit.add(parentPkgNode)
                elif parentPkgNode.numVisits > numExpectedVisits:
                    raise Exception(
                        "Parent node visit count > num of children "
                        f"Parent node: {parentPkgNode.packageName} "
                        f"Visit count: {parentPkgNode.numVisits} "
                        f"Num of children: {numExpectedVisits}"
                    )

            pkgNode.accumInstallRequiresPkgNodes.clear()

        unvisited_nodes = set()
        # Clear out the visit counter for reuse.
        for package in Scheduler.sortedList:
            pkgNode = Scheduler.mapPackagesToGraphNodes[package]
            if pkgNode.numVisits == 0:
                unvisited_nodes.add(pkgNode)
            else:
                pkgNode.numVisits = 0

        for node in unvisited_nodes:
            Scheduler.logger.debug(f"node {node.packageName} is not visited.")

        """
        GRAPH-BUILD STEP 4: Re-organize the dependencies in the graph
                            based on the above optimization.

        Now re-arrange parent-child relationships between packages using the
        following criteria:
        If a package 'A' build-requires or aux-build-requires package 'B',
        then:
          - Mark 'B' as a child of 'A' in the graph.
          - Mark 'A' as a parent of 'B' in the graph.
        If a package 'A' only install-requires package 'B', then:
          - Remove 'B' as a child of 'A' in the graph.
          - Remove 'A' as a parent of 'B' in the graph.
        No node should have a non-zero accum-install-requires set.
        """

        for package in Scheduler.sortedList:
            pkgNode = Scheduler.mapPackagesToGraphNodes[package]
            childPkgNodesToRemove = set()
            for childPkgNode in pkgNode.childPkgNodes:
                if (childPkgNode not in pkgNode.buildRequiresPkgNodes) and (
                    childPkgNode not in pkgNode.auxBuildRequiresPkgNodes
                ):
                    """
                    We can't modify a set during iteration, so we
                    accumulate the set of children we want to
                    remove, and delete them after the for-loop.
                    """
                    childPkgNodesToRemove.add(childPkgNode)
                    childPkgNode.parentPkgNodes.remove(pkgNode)

            pkgNode.childPkgNodes = pkgNode.childPkgNodes - childPkgNodesToRemove

            for newChildPkgNode in pkgNode.auxBuildRequiresPkgNodes:
                pkgNode.childPkgNodes.add(newChildPkgNode)
                newChildPkgNode.parentPkgNodes.add(pkgNode)

    def _calculateAllRequiredPackagesPerNode():
        """
        pkgNode contains information about spec package without deeping into
        subpackages.
        getRequiresTreeOfBasePkgsForPkg() creates full build time dependency
        list base on subpackages dependencies by walking the tree of:
            BuildRequires and their Requires tree + Requires and their
            Requires tree
        Let's keep graph simple by caching this preprocessed information per
        each pkgNode.
        It shouldn't add much memory overhead.
        """
        for package in Scheduler.sortedList:
            pkgNode = Scheduler.mapPackagesToGraphNodes[package]
            pkgNode.allRequiredPackages.extend(
                SPECS.getData().getRequiresTreeOfBasePkgsForPkg(package)
            )

    def _calculateCriticalChainWeights():
        r"""
        GRAPH-BUILD STEP 5: Calculate critical-chain-weight of packages.

        Calculation of critical-chain-weight (the key scheduling
        metric):
        --------------------------------------------------------
        Let us define a "chain" of a given package to be the
        sequence of parent packages that can be built starting from
        that package. For example, if a package 'A' build-requires
        'B', which in turn build-requires 'C', then one of the
        chains of 'C' is C->B->A. Now, if there are
        multiple such chains possible from 'C', then we define the
        "critical-chain" of 'C' to be the longest of those chains,
        where "longest" is determined by the time it takes to build
        all the packages in that chain. The build-times of any two
        chains can be compared based on the sum of the
        individual weights of each package in their respective
        chains.

        Below, we calculate the critical-chain-weight of each
        package (which is the maximum weight of all the paths
        leading up to that package). Later on, we will schedule
        package-builds by the decreasing order of the packages'
        critical-chain-weight.


                      ...  ...        ...
                        \   |         /
                         v  v        v

                            A        B        C

                             \       |       /
                              \      |      /
                               v     v     v

                                     D

                                   /
                                  /
                                 v

                                 E


        In the above graph, the critical chain weight of 'D' is
        computed as:
        criticalChainWeight(D) = weight(D) +
                                 max (criticalChainWeight(A),
                                      criticalChainWeight(B),
                                      weight(C))

        Graph Traversal : Top-down (starting with packages that
                          have no parents).
        """
        nodesToVisit = set()
        for package in Scheduler.sortedList:
            pkgNode = Scheduler.mapPackagesToGraphNodes[package]
            if len(pkgNode.parentPkgNodes) == 0:
                nodesToVisit.add(pkgNode)

        while nodesToVisit:
            pkgNode = nodesToVisit.pop()

            if len(pkgNode.parentPkgNodes) == 0:
                pkgNode.criticalChainWeight = pkgNode.selfWeight
                """
                Count self-visit if you don't expect any other
                visitors.
                """
                pkgNode.numVisits += 1

            for childPkgNode in pkgNode.childPkgNodes:
                if pkgNode not in childPkgNode.parentPkgNodes:
                    raise Exception(
                        "Visitor to child node is not its parent "
                        f"Visitor: {pkgNode.packageName}"
                        f"Child node: {childPkgNode.packageName}"
                    )

                if childPkgNode.numVisits == len(childPkgNode.parentPkgNodes):
                    raise Exception(
                        "Child node visit count > number of parents "
                        f"Child node: {childPkgNode.packageName}"
                        f"Visit count: {childPkgNode.numVisits}"
                        "Num of parents: " + str(len(childPkgNode.parentPkgNodes))
                    )

                childPkgNode.criticalChainWeight = max(
                    childPkgNode.criticalChainWeight,
                    pkgNode.criticalChainWeight + childPkgNode.selfWeight,
                )

                childPkgNode.numVisits += 1
                """
                We can visit this package's children only after this
                package has been visited by all its parents (thus
                guaranteeing that its criticalChainWeight has
                stabilized).
                """
                if childPkgNode.numVisits == len(childPkgNode.parentPkgNodes):
                    nodesToVisit.add(childPkgNode)

        # Clear out the visit counter for reuse.
        for package in Scheduler.sortedList:
            pkgNode = Scheduler.mapPackagesToGraphNodes[package]
            if pkgNode.numVisits == 0:
                raise Exception(
                    "critical-chain-weight calculation never visited "
                    f"package {pkgNode.packageName}"
                )
            else:
                pkgNode.numVisits = 0

    def _buildGraph():
        Scheduler._createGraphNodes()
        Scheduler._optimizeGraph()
        Scheduler._calculateAllRequiredPackagesPerNode()
        Scheduler._calculateCriticalChainWeights()

    @staticmethod
    def _parseWeights():
        Scheduler.pkgWeights.clear()
        with open(constants.packageWeightsPath, "r") as weightFile:
            Scheduler.pkgWeights = json.load(weightFile)
        # Extract anchor packages (used as speed-factor calibration references).
        # Remove the key so it is never mistaken for a real package weight.
        Scheduler.anchorPackages = set(Scheduler.pkgWeights.pop("__anchors__", []))

    """
    A package's weight is an indicator of the time required to build
    that package, relative to other packages.  Weights are expressed
    in normalized units (machine-agnostic — see _adjustWeightsForHost()), sourced
    from packageWeights.json.  Packages absent from the JSON default
    to 1.

    The returned value is offset by +1 so that the minimum scheduler
    weight is always 1 (not 0), which keeps the critical-chain math
    well-defined.
    """

    @staticmethod
    def _getWeight(package):
        """
        Weights are version-independent (Go, Kubernetes etc. share one
        entry).  Strip the version suffix before the JSON lookup.
        """
        package, _ = StringUtils.splitPackageNameAndVersion(package)
        try:
            return int(Scheduler.pkgWeights[package]) + 1
        except KeyError:
            return 1

    @staticmethod
    def _logHeavyPackages():
        """
        Emit an INFO line listing every package whose JSON build_cost
        exceeds BUILD_COST_FAIL_THRESHOLD so operators know which
        packages will drive the load-throttling logic.
        """
        heavy = []
        for pkg in Scheduler.sortedList:
            name, _ = StringUtils.splitPackageNameAndVersion(pkg)
            cost = int(Scheduler.pkgWeights.get(name, 0))
            if cost > Scheduler.BUILD_COST_FAIL_THRESHOLD:
                heavy.append(f"{name}({cost})")
        if heavy:
            Scheduler.logger.info(
                "Heavy packages (build_cost > %d units) — "
                "load-throttling will prevent these from building simultaneously: %s",
                Scheduler.BUILD_COST_FAIL_THRESHOLD,
                ", ".join(heavy),
            )

    @staticmethod
    def _computeSpeedFactor():
        """
        Return the machine's speed in seconds-per-unit.

        When packageWeights.json defines "__anchors__", the ratio is computed
        exclusively from those anchor packages — they act as a fixed reference
        whose committed weights are treated as ground truth.  This makes the
        factor stable across partial builds (a subset of packages) and across
        machines: if an anchor takes twice as long on a slow host, the factor
        doubles and all other measurements are scaled accordingly.

        Falls back to all measured packages when no anchors matched (e.g. a
        build that happened to skip every anchor package).

        Returns None when there is nothing to calibrate against.
        """
        def _ratios(candidates):
            result = []
            for pkgName in candidates:
                elapsed = Scheduler.buildTimings.get(pkgName, 0)
                if elapsed <= 0:
                    continue
                jsonCost = float(Scheduler.pkgWeights.get(pkgName, 0))
                if jsonCost > 0:
                    result.append(elapsed / jsonCost)
            return result

        ratios = _ratios(Scheduler.anchorPackages) if Scheduler.anchorPackages else []
        if not ratios:
            # Anchor packages were not measured this run; fall back to all.
            ratios = _ratios(Scheduler.pkgWeights)

        if not ratios:
            return None

        ratios.sort()
        return ratios[len(ratios) // 2]

    @staticmethod
    def _getPriority(package):
        try:
            return int(Scheduler.priorityMap[package])
        except KeyError:
            return 0

    @staticmethod
    def _adjustWeightsForHost():
        """
        Scale all entries in pkgWeights to reflect this host's actual speed,
        using anchor package timings measured in earlier build stages
        (CORE_TOOLCHAIN / TOOLCHAIN) as the calibration reference.

        The speed factor is:
            median( elapsed[anchor] / committed_weight[anchor] )

        where the median runs only over anchors that were both measured and
        present in pkgWeights.  If no anchor timings are available yet (e.g.
        the toolchain was already cached), the method is a no-op and the
        committed weights are used as-is.

        This must be called AFTER _parseWeights() and BEFORE _buildGraph() so
        that the dependency graph — and therefore every package's
        criticalChainWeight — is computed in real seconds for this host.
        """
        if not Scheduler.anchorPackages:
            return

        speedFactor = Scheduler._computeSpeedFactor()
        if speedFactor is None or speedFactor <= 0:
            Scheduler.logger.debug(
                "No anchor packages measured yet; using committed weights as-is."
            )
            return

        measured_anchors = [
            p for p in Scheduler.anchorPackages if p in Scheduler.buildTimings
        ]
        Scheduler.logger.info(
            "Host calibration: speed_factor=%.2f s/unit from anchor package(s): %s. "
            "Scaling all package weights accordingly.",
            speedFactor,
            ", ".join(sorted(measured_anchors)),
        )

        for pkg in list(Scheduler.pkgWeights):
            Scheduler.pkgWeights[pkg] = float(Scheduler.pkgWeights[pkg]) * speedFactor

    @staticmethod
    def _setPriorities(skipGraphBuild):
        if skipGraphBuild:
            for package in Scheduler.sortedList:
                Scheduler.priorityMap[package] = 0
        else:
            Scheduler._parseWeights()
            Scheduler._adjustWeightsForHost()
            Scheduler._buildGraph()
            Scheduler._logHeavyPackages()

            for package in Scheduler.sortedList:
                pkgNode = Scheduler.mapPackagesToGraphNodes[package]
                Scheduler.priorityMap[package] = pkgNode.criticalChainWeight

        Scheduler.logger.debug("set Priorities: Priority of all packages")
        Scheduler.logger.debug(Scheduler.priorityMap)

    @staticmethod
    def _checkNextPackageIsReadyToBuild(package):
        pkgNode = Scheduler.mapPackagesToGraphNodes[package]
        if pkgNode.built == 1:
            Scheduler.logger.warning(
                "This pkg %s-%s is already built,"
                "but still present in listOfPackagesToBuild"
                % (pkgNode.packageName, pkgNode.packageVersion)
            )
            return False

        if Scheduler.buildStage == BuildStage.CORE_TOOLCHAIN:
            # For CoreToolchain list just use the graph
            for childPkgNode in pkgNode.childPkgNodes:
                if childPkgNode.built == 0:
                    return False
        else:
            """
            For the rest of the packages with parallel build we have to
            consider entire
            tree of dependencies cached in allRequiredPackages set.
            """
            for p in pkgNode.allRequiredPackages:
                if not Scheduler.mapPackagesToGraphNodes[p].built:
                    return False

        return True

    @staticmethod
    def _markPkgNodeAsBuilt(package):
        pkgNode = Scheduler.mapPackagesToGraphNodes[package]
        Scheduler.logger.debug(f"Marking pkgNode as built = {pkgNode.packageName}")
        pkgNode.built = 1

    @staticmethod
    def _getListNextPackagesReadyToBuild():
        # Two separate gates, applied independently to each candidate:
        #
        # 1. Heavy gate — enforces "at most one heavy package building at a
        #    time."  A package with cost >= BUILD_COST_FAIL_THRESHOLD is
        #    skipped when:
        #      • heavyPackagesBuilding >= 1: a heavy package is already running
        #      • heavyAdmittedThisBatch: another heavy was queued earlier in
        #        this same call.  Without this flag, a single call with
        #        currentLoad=0 would bypass the running-load check and enqueue
        #        all ready heavy packages at once; waiting threads would then
        #        dequeue them simultaneously before heavyPackagesBuilding was
        #        ever incremented.
        #    Light packages (cost < BUILD_COST_FAIL_THRESHOLD) are never
        #    blocked by this gate — they always run freely alongside a heavy.
        #
        # 2. Capacity gate — limits total projected running load to
        #    maxConcurrentLoad.  Uses projectedLoad (currentLoad + costs of
        #    packages already admitted in this batch) so that the budget is not
        #    exceeded even when currentLoad hasn't been updated yet.
        heavyAdmittedThisBatch = False
        projectedLoad = Scheduler.currentLoad

        for pkg in Scheduler.listOfPackagesToBuild:
            if pkg in Scheduler.listOfPackagesCurrentlyBuilding:
                continue
            if not (constants.rpmCheck or Scheduler._checkNextPackageIsReadyToBuild(pkg)):
                continue

            pkgCost = Scheduler._getWeight(pkg) - 1
            isHeavy = pkgCost > Scheduler.BUILD_COST_FAIL_THRESHOLD

            # Gate 1 — heavy packages only
            if isHeavy and (
                Scheduler.heavyPackagesBuilding >= 1 or heavyAdmittedThisBatch
            ):
                Scheduler.logger.debug(
                    "Deferring heavy '%s' (cost=%d, heavyBuilding=%d).",
                    pkg,
                    pkgCost,
                    Scheduler.heavyPackagesBuilding,
                )
                continue

            # Gate 2 — all packages; guard (projectedLoad > 0) prevents
            # deadlock when a lone package's cost exceeds the per-thread budget.
            if (
                Scheduler.maxConcurrentLoad > 0
                and projectedLoad > 0
                and projectedLoad + pkgCost > Scheduler.maxConcurrentLoad
            ):
                Scheduler.logger.debug(
                    "Throttling '%s' (cost=%d, projected=%d, max=%d).",
                    pkg,
                    pkgCost,
                    projectedLoad,
                    Scheduler.maxConcurrentLoad,
                )
                continue

            if isHeavy:
                heavyAdmittedThisBatch = True
            projectedLoad += pkgCost
            Scheduler.listOfPackagesNextToBuild.put(
                (-Scheduler._getPriority(pkg), pkg)
            )
            Scheduler.logger.debug(f"Adding {pkg} to the schedule list")
