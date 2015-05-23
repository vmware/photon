#! /usr/bin/python2

from optparse import OptionParser
from Specutils import Specutils
import shutil
import subprocess
import os
import re
from sets import Set


def getListSpecFiles(listSpecFiles,path):
    for dir_entry in os.listdir(path):
        dir_entry_path = os.path.join(path, dir_entry)
        if os.path.isfile(dir_entry_path) and dir_entry_path.endswith(".spec"):
            listSpecFiles.append(dir_entry_path)
        elif os.path.isdir(dir_entry_path):
            getListSpecFiles(listSpecFiles,dir_entry_path)

def getListPackages(specPath):
    list_packages=[]
    listSpecFiles=[]
    getListSpecFiles(listSpecFiles,specPath)
    for specFile in listSpecFiles:
        spec = Specutils(specFile)
        l = spec.getPackageNames()
        for pkg in l:
            list_packages.append(pkg)
    return list_packages

class commandsUtils(object):
    def __init__(self):
        self.rpmbuild_binary = "rpmbuild"
        self.rpmbuild_buildall_option = "-ba"
        self.rpmbuild_nocheck_option = "--nocheck"
        self.rpm_binary = "rpm"
        self.install_rpm_package_options = "-Uvh"
        self.nodeps_rpm_package_options = "--nodeps"
        self.query_rpm_package_options = "-qa"
        self.force_rpm_package_options = "--force"
        self.find_command = "find"


    def find_file (self, filename, sourcePath):
        process = subprocess.Popen([self.find_command,  sourcePath,  "-name", filename],  stdout=subprocess.PIPE)
        returnVal = process.wait()
        result=process.communicate()[0]
        if result is None:
            return None
        return result.split()

    def run_command(self,cmd,logfilePath=None,chrootCmd=None):
        if chrootCmd is not None:
            cmd = chrootCmd+" "+cmd
        if logfilePath is None:
            logfilePath=os.devnull
        logfile=open(logfilePath,"w")
        process = subprocess.Popen("%s" %cmd,shell=True,stdout=logfile)
        retval = process.wait()
        logfile.close()
        if retval==0:
            return True
        return False

    def find_installed_rpm_packages(self, chrootCmd=None):
        cmd = self.rpm_binary+" "+self.query_rpm_package_options
        if chrootCmd is not None:
            cmd = chrootCmd+" "+cmd
        #process may hang if buffer is full
        process = subprocess.Popen("%s" %cmd,shell=True,stdout=subprocess.PIPE)
        retval = process.wait()
        result = process.communicate()[0]
        return result.split()

    def installRPM(self, rpmfilepath,logfilePath, chrootCmd=None, withNodeps=False):
        print "Installing RPM...",rpmfilepath
        rpmInstallcmd=self.rpm_binary+" "+ self.install_rpm_package_options

        if withNodeps:
            rpmInstallcmd+=" "+self.nodeps_rpm_package_options

        rpmInstallcmd+=" "+rpmfilepath
        if chrootCmd is not None:
            rpmInstallcmd= chrootCmd +" "+rpmInstallcmd
        logfile=open(logfilePath,'w')
        process = subprocess.Popen("%s" %rpmInstallcmd,shell=True,stdout=logfile,stderr=logfile)
        retval = process.wait()
        logfile.close()
        if retval != 0:
            return False
        return True

    def buildRPM(self, specfilepath, logfilePath, chrootCmd=None):
        print "Building RPM...",specfilepath
        rpmBuildcmd= self.rpmbuild_binary+" "+self.rpmbuild_buildall_option+" "+self.rpmbuild_nocheck_option
        rpmBuildcmd+=" "+specfilepath
        if chrootCmd is not None:
            rpmBuildcmd=chrootCmd +" "+rpmBuildcmd

        logfile=open(logfilePath,'w')
        process = subprocess.Popen("%s" %rpmBuildcmd,shell=True,stdout=logfile,stderr=logfile)
        retval = process.wait()
        logfile.close()
        if retval != 0:
            print "Building rpm is failed"
            return False, None

        #Extracting rpms created from log file
        logfile=open(logfilePath,'r')
        fileContents=logfile.readlines()
        logfile.close()
        listRpms=[]
        for i in range(0,len(fileContents)):
            if re.search("^Wrote:",fileContents[i]):
                listcontents=fileContents[i].split()
                if (len(listcontents) == 2) and listcontents[1].strip()[-4:] == ".rpm" and listcontents[1].find("/RPMS/") != -1:
                    listRpms.append(listcontents[1])

        return True, listRpms

class BuildSystem(object):
    def __init__(self, source_path,  spec_path,  rpm_path,  build_root, tools_path, log_path):
        self.data = []
        self.source_path = source_path
        self.spec_path = spec_path
        self.rpm_path = rpm_path
        self.tools_path = tools_path
        self.build_root = build_root

        self.parent_path="/usr/src/photon"
        self.prepare_buildroot_command = "./prepare-build-root.sh"
        self.run_in_chroot_command = "./run-in-chroot.sh"
	# do not add '/' at the beginning. It's used for concat.
        self.adjust_tool_chain_script = "adjust-tool-chain.sh"
        self.adjust_gcc_specs_script = "adjust-gcc-specs.sh"
        self.localegen_script = "./locale-gen.sh"
        self.localegen_config = "./locale-gen.conf"

        self.mapPackageToSpecFile={}
        self.listInstalledPackages=[]

        self.build_root_log_path=log_path
        self.build_root_rpm_path=self.build_root+self.parent_path+"/RPMS"
        self.build_root_source_path=self.build_root+self.parent_path+"/SOURCES"
        self.build_root_spec_path=self.build_root+self.parent_path+"/SPECS"

        self.listPkgsRequiredToBuildToolchain=["linux-api-headers", "glibc","glibc-devel",  "zlib","zlib-devel",  "file",
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

        self.listPkgsToInstallToolChain=["linux-api-headers", "glibc","glibc-devel",  "zlib","zlib-devel",  "file",
            "binutils","binutils-devel",  "gmp","gmp-devel", "mpfr", "mpfr-devel", "mpc",
            "libgcc","libgcc-devel","libstdc++","libstdc++-devel","libgomp","libgomp-devel","gcc",
            "pkg-config", "ncurses", "bash", "bzip2", "sed","procps-ng","coreutils", "m4","grep",
            "readline","diffutils","gawk", "findutils", "gettext", "gzip","make",  "patch",
            "util-linux", "tar", "xz","libtool", "flex",  "bison",
            "lua","popt","nspr","sqlite-autoconf","nss","elfutils-libelf",
            "libpipeline", "gdbm","perl","texinfo","rpm",
            "autoconf","automake", "groff", "man-db", "man-pages","elfutils","cpio"]

        self.list_nodeps_packages = ["glibc","gmp","zlib","file","binutils","mpfr","mpc","gcc","ncurses","util-linux","groff","perl","texinfo","rpm","openssl","go"]
        self.readPackagesInSpecFiles()

    def prepare_build_root(self, tools_archive=""):
        process = subprocess.Popen([self.prepare_buildroot_command, self.build_root,  self.spec_path,  self.rpm_path, self.tools_path, tools_archive])
        returnVal = process.wait()
        if returnVal != 0:
            return False
        cmdUtils=commandsUtils()
        if not os.path.isdir(self.build_root_log_path):
            cmdUtils.run_command("mkdir -p "+self.build_root_log_path)
        if not os.path.isdir(self.build_root_rpm_path):
            cmdUtils.run_command("mkdir -p "+self.build_root_rpm_path)
        if not os.path.isdir(self.build_root_source_path):
            cmdUtils.run_command("mkdir -p "+self.build_root_source_path)
        if not os.path.isdir(self.build_root_spec_path):
            cmdUtils.run_command("mkdir -p "+self.build_root_spec_path)
        return True
    def adjust_tool_chain(self):
        shutil.copy2(self.adjust_tool_chain_script,  self.build_root+"/tmp/"+self.adjust_tool_chain_script)
        shutil.copy2(self.localegen_script,  self.build_root+"/sbin/locale-gen.sh")
        shutil.copy2(self.localegen_config,  self.build_root+"/etc/locale-gen.conf")
        cmdUtils=commandsUtils()
        returnVal = cmdUtils.run_command("/tmp/"+self.adjust_tool_chain_script,"/var/log/adjust_tool_chain_script.log", self.run_in_chroot_command+" "+self.build_root)
        return returnVal

    def adjust_gcc_specs(self, package):
        opt = ""
        # linux package does not require sec gcc options
        if package == "linux":
            opt = " clean"

        shutil.copy2(self.adjust_gcc_specs_script,  self.build_root+"/tmp/"+self.adjust_gcc_specs_script)
        cmdUtils=commandsUtils()
        returnVal = cmdUtils.run_command("/tmp/"+self.adjust_gcc_specs_script+opt,"/var/log/adjust_gcc_specs_script.log", self.run_in_chroot_command+" "+self.build_root)
        return returnVal

    def readPackagesInSpecFiles(self):
        self.mapPackageToSpecFile.clear()
        listSpecFiles=[]
        getListSpecFiles(listSpecFiles, self.spec_path)
        for specfile in listSpecFiles:
            specparser = Specutils(specfile)
            listPackages=specparser.getPackageNames()
            for pkg in listPackages:
                self.mapPackageToSpecFile[pkg]=specfile

    def findSpecFileForPackage(self,package):
        package=package.strip()
        if self.mapPackageToSpecFile.has_key(package):
            return self.mapPackageToSpecFile[package]
        return None

    def findPackageNameFromRPMFile(self,rpmfile):
        rpmfile=os.path.basename(rpmfile)
        releaseindex=rpmfile.rfind("-")
        if releaseindex == -1:
            print "Invalid rpm file:",rpmfile
            return None
        versionindex=rpmfile[0:releaseindex].rfind("-")
        if versionindex == -1:
            print "Invalid rpm file:",rpmfile
            return None
        packageName=rpmfile[0:versionindex]
        return packageName

    def findRPMFileForGivenPackage(self,package):
        cmdUtils = commandsUtils()
        specFile=self.findSpecFileForPackage(package)
        if specFile is None:
            print "Did not find spec file for package: ", package
            return None
        specparser = Specutils(specFile)
        version = specparser.getVersion()
        release = specparser.getRelease()
        listFoundRPMFiles = cmdUtils.find_file(package+"-"+version+"-"+release+"*.rpm",self.rpm_path)
        if len(listFoundRPMFiles) == 1 :
            return listFoundRPMFiles[0]
        if len(listFoundRPMFiles) == 0 :
            return None
        if len(listFoundRPMFiles) > 1 :
            print "Unable to determine the rpm file for package. Found multiple rpm files for given package in rpm directory"
            return None
        return None

    def copySourcesTobuildroot(self,listSourceFiles,package):
        cmdUtils = commandsUtils()
        for source in listSourceFiles:
            sourcePath = cmdUtils.find_file(source,self.source_path)
            if sourcePath is None or len(sourcePath) == 0:
                sourcePath = cmdUtils.find_file(source,self.spec_path)
            if sourcePath is None or len(sourcePath) == 0:
                print "Missing source: "+source+". Cannot find sources for package: ", package
                print "Stopping building toolchain"
                return False
            if len(sourcePath) > 1:
                print "Multiple sources found: Unable to determine one. "
                print "Stopping building toolchain"
                return False
            print "Source path :" + source + " Source filename: " + sourcePath[0]
            shutil.copyfile(sourcePath[0],  self.build_root_source_path+"/"+source)

    def buildRPMSForGivenPackage(self,package):
        print "Building package......",package
        specFile=self.findSpecFileForPackage(package)
        print "Spec file for package:",package," is ",specFile
        if specFile is None:
            print "Did not find spec file for package: ", package
            return False
        self.adjust_gcc_specs(package)

        specName=os.path.basename(specFile)
        spec=Specutils(specFile)
        listSourceFiles=[]
        listSourceFiles.extend(spec.getSourceNames())
        listSourceFiles.extend(spec.getPatchNames())
        self.copySourcesTobuildroot(listSourceFiles,package)
        shutil.copyfile(specFile,  self.build_root_spec_path+"/"+specName)
        specChrootPath=self.build_root_spec_path.replace(self.build_root,"")
        returnVal,listRPMFiles = self.buildRPM(specChrootPath+"/"+specName,self.build_root_log_path+"/"+package+".log", self.run_in_chroot_command+" "+self.build_root)
        if not returnVal:
            return False
        for rpmFile in listRPMFiles:
            self.copyRPM(self.build_root+"/"+rpmFile, self.rpm_path)
        return True

    def buildRPM(self,specFile,logFile,chrootCmd):
        cmdUtils = commandsUtils()
        returnVal,listRPMFiles = cmdUtils.buildRPM(specFile,logFile,chrootCmd)
        if not returnVal:
            print "Building rpm is failed",specFile
            return False,None
        return True,listRPMFiles

    def getRPMDestDir(self,rpmName,rpmDir):
        arch=""
        if rpmName.find("x86_64") != -1:
            arch='x86_64'
        elif rpmName.find("noarch") != -1:
            arch="noarch"
        #else: Todo throw an exeption
        rpmDestDir=rpmDir+"/"+arch
        return rpmDestDir

    def copyRPM(self,rpmFile,destDir):
        cmdUtils = commandsUtils()
        rpmName=os.path.basename(rpmFile)
        rpmDestDir=self.getRPMDestDir(rpmName,destDir)
        if not os.path.isdir(rpmDestDir):
            cmdUtils.run_command("mkdir -p "+rpmDestDir)
        rpmDestPath=rpmDestDir+"/"+rpmName
        shutil.copyfile(rpmFile,  rpmDestPath)
        return rpmDestPath

    def installRPM(self,package):

        rpmfile=self.findRPMFileForGivenPackage(package)
        if rpmfile is None:
            print "unexpected error"
            print "Stopping installing package",package
            return False

        rpmDestFile = self.copyRPM(rpmfile, self.build_root+self.parent_path+"/RPMS")
        rpmFile=rpmDestFile.replace(self.build_root,"")
        chrootCmd=self.run_in_chroot_command+" "+self.build_root
        logFile=self.build_root_log_path+"/"+package+".completed"

        cmdUtils = commandsUtils()
        nodepsOption=False
        if package in self.list_nodeps_packages:
            nodepsOption=True
        returnVal = cmdUtils.installRPM(rpmFile,logFile,chrootCmd,nodepsOption)
        if not returnVal:
            print "Installing " + rpmFile+" rpm is failed"
            return False
        self.listInstalledPackages.append(package)
        return True

    def findInstalledPackages(self):
        cmdUtils=commandsUtils()
        listInstalledRPMs=cmdUtils.find_installed_rpm_packages(self.run_in_chroot_command+" "+self.build_root)
        listInstalledPackages=[]
        for installedRPM in listInstalledRPMs:
            packageName=self.findPackageNameFromRPMFile(installedRPM)
            if packageName is not None:
                listInstalledPackages.append(packageName)
        return listInstalledPackages

    def buildToolchain(self):
        self.cleanBuildRoot()
        self.prepare_build_root()
        for package in self.listPkgsRequiredToBuildToolchain:
            rpmfile=self.findRPMFileForGivenPackage(package)
            if rpmfile is None :
                returnVal=self.buildRPMSForGivenPackage(package)
                if not returnVal:
                    print "Stopping building toolchain"
                    return False
            returnVal=self.installRPM(package)
            if not returnVal:
                print "Stopping building toolchain"
                return False
            if package =="glibc":
                self.adjust_tool_chain()
        print "Built toolchain succesfully"
        return True

    def installToolchain(self):
        flagbuildToolchain=False
        for package in self.listPkgsToInstallToolChain:
            rpmfile=self.findRPMFileForGivenPackage(package)
            if rpmfile is None :
                flagbuildToolchain = True
                break
        if flagbuildToolchain:
            returnVal=self.buildToolchain()
            if not returnVal:
                print "Stopping installing toolchain"
                return False

        self.cleanBuildRoot()
        self.prepare_build_root("minimal")
        for package in self.listPkgsToInstallToolChain:
            returnVal=self.installRPM(package)
            if not returnVal:
                print "Stopping installing toolchain"
                return False
        print "Installed toolchain succesfully"
        return True


    def constructDependencyGraph(self,package,mapPkgNRequiredPkgs):
        returnVal,listRequiredPackages=self.findBuildTimeRequiredPackages(package)
        if not returnVal:
             return False
        mapPkgNRequiredPkgs[package]=listRequiredPackages
        for requiredPkg in listRequiredPackages:
            if not mapPkgNRequiredPkgs.has_key(requiredPkg):
                returnVal=self.constructDependencyGraph(requiredPkg,mapPkgNRequiredPkgs)
                if not returnVal:
                    return False
        return True

    def findBuildTimeRequiredPackages(self,package):
        specFile=self.findSpecFileForPackage(package)
        print "Spec file for package:",package," is ",specFile
        if specFile is None:
            print "Did not find spec file for package: ", package
            return False,None
        spec=Specutils(specFile)
        listRequiredPackages=[]
        listRequiredPackages=spec.getBuildRequiresAllPackages()
        return True,listRequiredPackages

    def findRunTimeRequiredPackages(self,package):
        specFile=self.findSpecFileForPackage(package)
        print "Spec file for package:",package," is ",specFile
        if specFile is None:
            print "Did not find spec file for package: ", package
            return False,None
        spec=Specutils(specFile)
        listRequiredPackages=[]
        listRequiredPackages=spec.getRequiresAllPackages()
        return True,listRequiredPackages

    def findRunTimeRequiredRPMPackages(self,rpmPackage):
        specFile=self.findSpecFileForPackage(rpmPackage)
        print "Spec file for package:",rpmPackage," is ",specFile
        if specFile is None:
            print "Did not find spec file for package: ", rpmPackage
            return False,None
        spec=Specutils(specFile)
        listRequiredPackages=[]
        listRequiredPackages=spec.getRequires(rpmPackage)
        return True,listRequiredPackages

    def topological_sort_packages(self, dependent_packages):
        nodep_packages = Set()
        sorted_package_list = []
        dependentof_package = dict()

        #Find packages with no dependencies and generate dependentof_package edge list
        for package in dependent_packages:
            if len(dependent_packages[package]) == 0:
                nodep_packages.add(package)
            else:
                for dependent_package in dependent_packages[package]:
                    if dependentof_package.get(dependent_package) is None:
                        dependentof_package[dependent_package]=[package]
                    else:
                        dependentof_package[dependent_package].append(package)
        while nodep_packages:
            package = nodep_packages.pop()
            sorted_package_list.append(package)
            if dependentof_package.get(package) is not None:
                print "dependent of: "+package+ "  are : "+ ' '.join(dependentof_package[package])
                for child_package in list(dependentof_package.get(package)):
                    dependentof_package.get(package).remove(child_package)
                    dependent_packages[child_package].remove(package)
                    print child_package +  " depends on " + ' '.join(dependent_packages[child_package])
                    if len(dependent_packages[child_package])==0:
                        nodep_packages.add(child_package)

        return sorted_package_list


    def find_package_dependency_tree(self, package_name):
        print "finding dependency tree for : " + package_name
        dependent_packages={}
        returnVal=self.constructDependencyGraph(package_name, dependent_packages)
        if not returnVal:
            print "Not able to find depedendency tree for package ", package_name
            return False, None
        print dependent_packages
        sorted_package_list = self.topological_sort_packages(dependent_packages)
        return True,sorted_package_list

    def removeToolsTar(self):
        cmdUtils=commandsUtils()
        cmdUtils.run_command("rm -rf "+self.build_root+"/tools")
        return True

    def cleanBuildRoot(self):
        cmdUtils=commandsUtils()
        cmdUtils.run_command("./cleanup-build-root.sh "+self.build_root)
        
    def buildPackage(self,package,force_build, listFailedPkgs=[]):
        # We don't need to build this package if RPM exists && !force_build
        rpmfile = None
        if not force_build:
            rpmfile=self.findRPMFileForGivenPackage(package)
        if rpmfile is not None:
            print "The given package is already built",package
            return True

        if package in listFailedPkgs:
            print package," package is failed in previous iteration. Not building again."
            return False
        returnVal,listDependentPackages=self.find_package_dependency_tree(package)
        if not returnVal:
            print "Failed during building the package", package
            return False
        listDependentPackages.remove(package)
        listPkgsTobeBuild=[]
        returnVal,listRunTimeDependentPackages=self.findRunTimeRequiredPackages(package)
        if not returnVal:
            print "Failed during building the package", package
            return False

        for pkg in listDependentPackages:
            rpmfile=self.findRPMFileForGivenPackage(pkg)
            if rpmfile is None :
                listPkgsTobeBuild.append(pkg)

        for pkg in listRunTimeDependentPackages:
            rpmfile=self.findRPMFileForGivenPackage(pkg)
            if rpmfile is None :
                listPkgsTobeBuild.append(pkg)

        if len(listPkgsTobeBuild) != 0:
            print "Dependent packages to be build",listPkgsTobeBuild
            print "Building dependent packages.........."
            for pkg in listPkgsTobeBuild:
                returnVal = self.buildPackage(pkg,force_build,listFailedPkgs)
                if not returnVal:
                    print "Failed installing package",pkg
                    print "Stop installing package",package
                    return False
            print "Finished building dependent packages"

        # Let's build this package
        self.installToolchain()
        self.removeToolsTar()
        del self.listInstalledPackages[:]
        self.listInstalledPackages=self.findInstalledPackages()

        returnVal,listDependentPackages=self.findBuildTimeRequiredPackages(package)
        if not returnVal:
            print "Failed during building the package", package
            return False
        
        #if toolchain package called this method, preventing from installing again
        if package in self.listInstalledPackages:
            return True

        if len(listDependentPackages) != 0:
            print "Installing the build time dependent packages......"
            for pkg in listDependentPackages:
                if pkg in self.listInstalledPackages:
                    continue
                returnVal = self.installPackage(pkg)
                if not returnVal:
                    print "Failed while installing the build time dependent package",pkg
                    return False
            print "Finished installing the build time dependent packages......"

        returnVal=self.buildRPMSForGivenPackage(package)
        if not returnVal:
            print "Failed while building the package",package
            return False
        print "Successfully built the package:",package
        return True

    def installPackage(self,package):
        #if toolchain package called this method, preventing from installing again
        if package in self.listInstalledPackages:
            return True
        returnVal = self.installDependentRunTimePackages(package)
        if not returnVal:
            return False
        returnVal = self.installRPM(package)
        if not returnVal:
            print "Stop installing package",package
            return False
        print "Installed the package:",package
        return True

    def installDependentRunTimePackages(self,package):
        returnVal,listRunTimeDependentPackages=self.findRunTimeRequiredRPMPackages(package)
        if not returnVal:
            return False
        if len(listRunTimeDependentPackages) != 0:
            for pkg in listRunTimeDependentPackages:
                if pkg in self.listInstalledPackages:
                    continue
                returnVal = self.installPackage(pkg)
                if not returnVal:
                    return False
        return True

    def doCleanBuild(self):
        cmdUtils=commandsUtils()
        cmdUtils.run_command("rm -rf "+ self.rpm_path+"/*")
        cmdUtils.run_command("mkdir "+ self.rpm_path+"/x86_64")
        cmdUtils.run_command("mkdir "+ self.rpm_path+"/noarch")
        returnVal=self.buildAllPackages()
        if not returnVal:
            print "Clean build failed."
            return False
        print "Clean buils is completed successfully"
        return True
    
    def buildAllPackages(self):
        # in case previous build was terminated.
        self.cleanBuildRoot()

        listFailedPkgs=[]
        list_packages=getListPackages(self.spec_path)
        returnVal=self.installToolchain()
        if not returnVal:
            print "Not able to build toolchain"
            print "Please fix this error and continue to build all packages"
            return False
        for pkg in list_packages:
            returnVal=self.buildPackage(pkg,False,listFailedPkgs)
            if not returnVal:
                listFailedPkgs.append(pkg)
        if len(listFailedPkgs) != 0:        
            print "Some of the packages failed during clean build. Logs are locates in ", self.build_root_log_path," path."
            print "List failed Packages",listFailedPkgs
            return False
        self.cleanBuildRoot()
        print "Successfully built all packages"
        return True
    

def main():
    usage = "Usage: %prog [options] <package name>"
    parser = OptionParser(usage)
    parser.add_option("-s",  "--spec-path",  dest="spec_path",  default="../../SPECS")
    parser.add_option("-o",  "--source-path",  dest="source_path",  default="../../SOURCES")
    parser.add_option("-r",  "--rpm-path",  dest="rpm_path",  default="../../stage/RPMS")
    parser.add_option("-b",  "--build-root",  dest="build_root",  default="/mnt/photonroot")
    parser.add_option("-t",  "--install-tool-chain",  dest="install_tool_chain",  default=False,  action ="store_true")
    parser.add_option("-i",  "--install-package", dest="install_package",  default=False,  action ="store_true")
    parser.add_option("-c",  "--clean-build", dest="clean_build",  default=False,  action ="store_true")
    parser.add_option("-p",  "--tools-path", dest="tools_path",  default="../../stage")
    parser.add_option("-l",  "--log-path", dest="log_path",  default="../../stage/LOGS")
    parser.add_option("-a",  "--build-all", dest="build_all",  default=False,  action ="store_true")
    parser.add_option("-f",  "--force", dest="force_build",  default=False,  action ="store_true")
    
    (options,  args) = parser.parse_args()
    #if (len(args)) != 1:
    #    parser.error("Incorrect number of arguments")

    print "Source Path :"+options.source_path
    print "Spec Path :" + options.spec_path
    print "Rpm Path :" + options.rpm_path
    print "Tools Path :" + options.tools_path
    print "Log Path :" + options.log_path
    print "Build root :" + options.build_root

    package_builder = BuildSystem(options.source_path,  options.spec_path,  options.rpm_path,  options.build_root, options.tools_path, options.log_path)

    returnVal = True
    if options.clean_build:
        returnVal=package_builder.doCleanBuild()
    elif options.build_all:
        returnVal=package_builder.buildAllPackages()
    elif options.install_tool_chain:
        returnVal=package_builder.installToolchain()
    elif options.install_package:
        if (len(args)) != 1:
            parser.error("Incorrect number of arguments")
            returnVal=False
        else:
            returnVal=package_builder.buildPackage(args[0],options.force_build)
    return returnVal
            

if __name__ == '__main__':
    main()
