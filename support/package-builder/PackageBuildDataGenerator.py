from Logger import Logger
from constants import constants
from sets import Set
import copy

     
class PackageBuildDataGenerator(object):
    
    cycleCount=0
    
    def __init__(self,logName=None,logPath=None):
        if logName is None:
            logName = "PackageBuildDataGenerator"
        if logPath is None:
            logPath = constants.logPath
        self.logName=logName
        self.logPath=logPath
        self.logger=Logger.getLogger(logName,logPath)
        self.__mapCyclesToPackageList={}
        self.__mapPackageToCycle={}
        self.__buildDependencyGraph={}
        self.__runTimeDependencyGraph={}
        self.__sortedPackageList=[]
        self.__sortedBuildDependencyGraph={}
    
    def getPackageBuildData(self,listPackages):
        if not self.__readDependencyGraphAndCyclesForGivenPackages(listPackages):
            return False,None,None,None
        
        self.logger.info("sorted build order")
        self.logger.info(self.__sortedBuildDependencyGraph)
        #self.logger.info("Map cycles to package list")
        #self.logger.info(self.__mapCyclesToPackageList)

        if not self.__getSortedBuildOrderListForGivenPackages(listPackages):
            return False,None,None,None
        
        return True,self.__mapCyclesToPackageList,self.__mapPackageToCycle,self.__sortedPackageList
        
    def __getSortedBuildOrderListForGivenPackages(self,listPackages):
        #should not include toolchain packages
        
        alreadyProcessedPackages=[]
        sList=[]
        listPackagesCopy=self.__buildDependencyGraph.keys()#listPackages[:]
        sortedListIndex = 0
        
        listPkgsRequiredToBuildToolchain=["linux-api-headers", "glibc","glibc-devel",  "zlib","zlib-devel",  "file",
            "binutils","binutils-devel",  "gmp","gmp-devel", "mpfr", "mpfr-devel", "mpc",
            "libgcc","libgcc-devel","libstdc++","libstdc++-devel","libgomp","libgomp-devel","gcc",
            "pkg-config", "ncurses", "bash", "bzip2", "sed","ncurses-devel","procps-ng","coreutils", "m4","grep",
            "readline", "diffutils","gawk", "findutils", "gettext", "gzip","make",  "patch",
            "util-linux", "tar", "xz","libtool", "flex",  "bison",
            "readline-devel", "lua","lua-devel","popt","popt-devel","nspr","sqlite-autoconf","nss","nss-devel",
            "bzip2-devel","elfutils-libelf","elfutils","elfutils-libelf-devel","elfutils-devel",
            "expat","libffi","libpipeline", "gdbm","perl","texinfo","autoconf","automake",
            "openssl","openssl-devel","python2","python2-libs","python2-devel","rpm",
            "groff", "man-db", "man-pages","cpio"]
        '''
        toolChainPackagesCount=0
        toolChainPackagelist=[]
        for p in listPkgsRequiredToBuildToolchain:
            basePkg=constants.specData.getSpecName(p)
            if basePkg in listPackagesCopy:
                listPackagesCopy.remove(basePkg)
                toolChainPackagelist.append(basePkg)
                toolChainPackagesCount = toolChainPackagesCount + 1
        '''
        sListLenBackUp=0
        while listPackagesCopy:
            pkg = None
            lenIndex=len(sList)
            for  i in range(lenIndex):
                if sList[i] in alreadyProcessedPackages:
                    continue
                pkg = sList[i]
                sortedListIndex = i
                break
            
                
            if pkg is None:
                pkg = listPackagesCopy.pop()
                sortedListIndex = len(sList)
            
            rbrList=[]
            for p in self.__runTimeDependencyGraph[pkg]:
                if p not in rbrList:
                    rbrList.append(p)
            rbrList.append(pkg)
            brList=[]
            
            for p in rbrList:
                basePkg=constants.specData.getSpecName(p)
                for bPkg in self.__sortedBuildDependencyGraph[basePkg]:
                    if bPkg not in brList:
                        brList.append(bPkg)
            
            #remove any cyclic packages in brList if they exists in sList
            circularDependentPackages=[]
            if self.__mapPackageToCycle.has_key(pkg):
                circularDependentPackages.extend(self.__mapCyclesToPackageList[self.__mapPackageToCycle[pkg]])
                circularDependentPackages.remove(pkg)
            
            for p in circularDependentPackages:
                if p in sList:
                    if p in brList:
                        brList.remove(p)
            
            index=sortedListIndex
            subList=[]
            if sortedListIndex > 0:
                subList=sList[:sortedListIndex]
            for p in brList:
                if  p not in subList:
                    sList.insert(index, p)
                    index = index + 1
            alreadyProcessedPackages.append(p)
        
            if (len(sList)-sListLenBackUp) > 100 :
                self.logger.info("Removing duplicates in sList")
                sListCopy=[]
                for p in sList:
                    if p not in sListCopy:
                        sListCopy.append(p)
                sList = sListCopy
            else:
                sListLenBackUp=len(sList)
                
        self.logger.info("Only final step remains....")
        sListCopy=[]
        for p in sList:
            #if p in toolChainPackagelist:
            #    continue
            if p not in sListCopy:
                sListCopy.append(p)
        sList = sListCopy
        
        
        self.logger.info("sorted list")
        self.logger.info(sList)
        self.__sortedPackageList=sList
        return True
        
    def __constructBuildTimeDependencyGraph(self,package):
        if self.__buildDependencyGraph.has_key(package):
            return True
        listDependentRpmPackages=constants.specData.getBuildRequiresForPackage(package)
        listDependentPackages=[]
        for rpmPkg in listDependentRpmPackages:
            basePkg=constants.specData.getSpecName(rpmPkg)
            if basePkg not in listDependentPackages:
                listDependentPackages.append(basePkg)
                
        self.__buildDependencyGraph[package]=listDependentPackages
        for basePkg in listDependentPackages:
            self.__constructBuildTimeDependencyGraph(basePkg)
            self.__constructRunTimeDependencyGraph(basePkg)
    
    def __constructRunTimeDependencyGraph(self,package):
        if self.__runTimeDependencyGraph.has_key(package):
            return True
        listRpmPackages=constants.specData.getPackages(package)
        for rpmPkg in listRpmPackages:
            listDependentRpmPackages=constants.specData.getRequiresAllForPackage(rpmPkg)
            self.__runTimeDependencyGraph[rpmPkg]=listDependentRpmPackages[:]
        for rpmPkg in listRpmPackages:
            for pkg in self.__runTimeDependencyGraph[rpmPkg]:
                self.__constructRunTimeDependencyGraph(pkg)
                self.__constructBuildTimeDependencyGraph(pkg)

    def __readDependencyGraphAndCyclesForGivenPackages(self,listPackages):
        for pkg in listPackages:
            self.__constructBuildTimeDependencyGraph(pkg)
            self.__constructRunTimeDependencyGraph(pkg)
        
        packagesToBUild=self.__buildDependencyGraph.keys()
        for pkg in packagesToBUild:
            sortedPackageList,circularDependentPackages = self.topologicalSortPackages(self.__buildDependencyGraph,pkg)
            if len(circularDependentPackages) > 0 :
                self.logger.error("Found circular dependency")
                self.logger.error(circularDependentPackages)
                return False
            self.__sortedBuildDependencyGraph[pkg]=sortedPackageList
        sortedPackageList,circularDependentPackages = self.topologicalSortPackages(self.__runTimeDependencyGraph)
        if len(circularDependentPackages) > 0 :
            self.__findCircularDependencies(circularDependentPackages)
        return True
    
    def topologicalSortPackages(self, dependentPackages1, package=None):
        noDepPackages = Set()
        sortedPackageList = []
        dependentOfPackage = dict()
        
        dependentPackages={}
        if package is None:
            dependentPackages=copy.deepcopy(dependentPackages1)
        else:
            listDepPkgs= Set()
            listDepPkgs.add(package)
            while listDepPkgs:
                pkg = listDepPkgs.pop()
                if dependentPackages.has_key(pkg):
                    continue
                dependentPackages[pkg]=dependentPackages1[pkg][:]
                for depPkg in dependentPackages1[pkg]:
                    listDepPkgs.add(depPkg)
        #Find packages with no dependencies and generate dependentof_package edge list
        for pkg in dependentPackages:
            if len(dependentPackages[pkg]) == 0:
                noDepPackages.add(pkg)
            else:
                for depPkg in dependentPackages[pkg]:
                    if not dependentOfPackage.has_key(depPkg):
                        dependentOfPackage[depPkg]=[pkg]
                    else:
                        if pkg not in dependentOfPackage[depPkg]:
                            dependentOfPackage[depPkg].append(pkg)
        
        while noDepPackages:
            pkg = noDepPackages.pop()
            sortedPackageList.append(pkg)
            if dependentOfPackage.get(pkg) is not None:
                for childPkg in list(dependentOfPackage.get(pkg)):
                    dependentOfPackage.get(pkg).remove(childPkg)
                    dependentPackages[childPkg].remove(pkg)
                    if len(dependentPackages[childPkg])==0:
                        noDepPackages.add(childPkg)
        
        circularDependentGraph={}
        listCircularPkg = dependentPackages.keys()
        for pkg in listCircularPkg:
            if len(dependentPackages[pkg]) != 0:
                circularDependentGraph[pkg]=dependentPackages[pkg]
            
        #return (non-circular dependent package in sorted order and circular dependent package list in a dependencyGraph)
        return sortedPackageList,circularDependentGraph
    
    def __findCircularDependencies(self,cyclicDependentGraph):
        if len(cyclicDependentGraph) == 0:
            return True
        #step1: construct dependency map from dependency graph
        constructDependencyMap={}
        listNodes=cyclicDependentGraph.keys()
        for node in listNodes:
            tmpDepNodeList=[]
            tmpDepNodeList.append(node)
            depNodeList=[]
            while len(tmpDepNodeList)!=0:
                currentNode = tmpDepNodeList.pop()
                addDepNodeList = cyclicDependentGraph[currentNode]
                depNodeList.append(currentNode)
                for depNode in addDepNodeList:
                    if depNode in depNodeList:
                        continue
                    else:
                        if depNode not in tmpDepNodeList:
                            tmpDepNodeList.append(depNode)
            depNodeList.remove(node)
            constructDependencyMap[node]=depNodeList
        self.logger.info("Dependency Map:")
        self.logger.info(constructDependencyMap)
        
        #find cycles in dependency map
        for node in listNodes:
            listDepPkg=constructDependencyMap[node]
            cycPkgs=[]
            if not self.__mapPackageToCycle.has_key(node):
                for depPkg in listDepPkg:
                    x = constructDependencyMap[depPkg]
                    if node in x:
                        cycPkgs.append(depPkg)
                
                if len(cycPkgs) != 0:
                    cycPkgs.append(node)
                    cycleName="cycle"+str(PackageBuildDataGenerator.cycleCount)
                    PackageBuildDataGenerator.cycleCount=PackageBuildDataGenerator.cycleCount+1
                    for x in cycPkgs:
                        self.__mapPackageToCycle[x]=cycleName
                    self.__mapCyclesToPackageList[cycleName]=cycPkgs
                    self.logger.info("New Circular dependency found")
                    self.logger.info(cycPkgs)
        return True
    

    
    