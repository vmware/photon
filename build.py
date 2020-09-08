#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "support/package-builder"))
sys.path.insert(1, os.path.join(os.path.dirname(os.path.realpath(__file__)), "support/image-builder"))
from pathlib import PurePath
from constants import constants
from argparse import ArgumentParser
from CommandUtils import CommandUtils
from builder import Builder
from Logger import Logger
from utils import Utils
import subprocess
import json
import docker
import shutil
import traceback
import glob
configdict = {}

targetList = {
        "image":["iso", "ami", "gce", "azure", "rpi3", "ova", "ova_uefi", "all", "src-iso",
                "photon-docker-image", "k8s-docker-images", "all-images", "minimal-iso", "rt-iso"],

        "rpmBuild": ["packages", "packages-minimal", "packages-initrd", "packages-docker",
                "updated-packages", "tool-chain-stage1", "tool-chain-stage2", "check",
                "ostree-repo", "generate-yaml-files", "create-repo", "distributed-build"],

        "buildEnvironment": ["packages-cached", "sources", "sources-cached", "publish-rpms",
                "publish-x-rpms", "publish-rpms-cached", "publish-x-rpms-cached", "photon-stage"],

        "cleanup": ["clean", "clean-install", "clean-chroot", "clean-stage-for-incremental-build"],

        "tool-checkup": ["check-tools", "check-docker", "check-docker-service", "check-docker-py",
                "check-bison", "check-texinfo", "check-g++", "check-gawk", "check-repo-tool",
                "check-kpartx", "check-sanity", "start-docker", "install-photon-docker-image",
                "check-spec-files", "check-pyopenssl"],

        "utilities": ["generate-dep-lists", "pkgtree", "imgtree", "who-needs", "print-upward-deps"]
        }

curDir = os.getcwd()

check_prerequesite = {
        "vixdiskutil": False,
        "tools-bin": False,
        "contain": False,
        "initialize-constants": False
        }

def vixdiskutil():
    check_prerequesite["vixdiskutil"] = True
    if not check_prerequesite["tools-bin"]:
        tools_bin()
    if subprocess.Popen(["cd " + curDir + "/tools/src/vixDiskUtil && make"], shell=True).wait() != 0:
        raise Exception("Not able to make vixDiskUtil")

def tools_bin():
    check_prerequesite["tools-bin"] = True
    if not os.path.isdir(os.path.join(curDir, "tools/bin")):
        os.mkdir(os.path.join("tools","bin"))

def contain():
    check_prerequesite["contain"] = True
    if not check_prerequesite["tools-bin"]:
        tools_bin()

    if subprocess.Popen(["gcc -O2 -std=gnu99 -Wall -Wextra " + curDir + \
            "/tools/src/contain/*.c -o tools/bin/contain_unpriv && sudo install -o root -g root \
            -m 4755 tools/bin/contain_unpriv tools/bin/contain"], shell=True).wait() != 0:
        raise Exception("contain failed")


class Build_Config:
    buildThreads = 1
    stagePath = ""
    pkgJsonInput = None
    rpmNoArchPath = ""
    chrootPath = ""
    generatedDataPath = ""
    pullPublishRPMSDir = ""
    pullPublishRPMS = ""
    pullPublishXRPMS = ""
    updatedRpmPath = ""
    updatedRpmNoArchPath = ""
    dockerEnv = "/.dockerenv"
    updatedRpmArchPath = ""
    installerPath = ""
    pkgInfoFile = ""
    rpmArchPath = ""
    commonDir = ""
    pkgBuildType = ""
    dataDir = ""
    packageListFile = "build_install_options_all.json"
    pkgToBeCopiedConfFile = None
    confFile = None
    distributedBuildFile = "distributed_build_options.json"

    @staticmethod
    def setDockerEnv(dockerEnv):
        Build_Config.dockerEnv = dockerEnv

    @staticmethod
    def setDistributedBuildFile(distributedBuildFile):
        Build_Config.distributedBuildFile = distributedBuildFile

    @staticmethod
    def setPkgToBeCopiedConfFile(pkgToBeCopiedConfFile):
        Build_Config.pkgToBeCopiedConfFile = pkgToBeCopiedConfFile

    @staticmethod
    def setRpmNoArchPath():
        Build_Config.rpmNoArchPath = os.path.join(constants.rpmPath, "noarch")

    @staticmethod
    def setRpmArchPath():
        Build_Config.rpmArchPath = os.path.join(constants.rpmPath, constants.buildArch)

    @staticmethod
    def setConfFile(confFile):
        Build_Config.confFile = confFile

    @staticmethod
    def setPkgBuildType(pkgBuildType):
        Build_Config.pkgBuildType = pkgBuildType

    @staticmethod
    def setBuildThreads(buildThreads):
        Build_Config.buildThreads = buildThreads

    @staticmethod
    def setPkgJsonInput(pkgJsonInput):
        Build_Config.pkgJsonInput = pkgJsonInput

    @staticmethod
    def setUpdatedRpmPath(updatedRpmPath):
        Build_Config.updatedRpmPath = updatedRpmPath
        Build_Config.updatedRpmNoArchPath = os.path.join(updatedRpmPath , "noarch")
        Build_Config.updatedRpmArchPath = os.path.join(updatedRpmPath, constants.buildArch)

    @staticmethod
    def setStagePath(stagePath):
        Build_Config.stagePath = stagePath

    @staticmethod
    def setInstallerPath(installerPath):
        Build_Config.installerPath = installerPath

    @staticmethod
    def setPkgInfoFile(pkgInfoFile):
        Build_Config.pkgInfoFile = pkgInfoFile

    @staticmethod
    def setChrootPath(chrootPath):
        Build_Config.chrootPath = chrootPath

    @staticmethod
    def setGeneratedDataDir(generatedDataDir):
        Build_Config.generatedDataPath = generatedDataDir

    @staticmethod
    def setCommonDir(commonDir):
        Build_Config.commonDir = commonDir

    @staticmethod
    def setDataDir(dataDir):
        Build_Config.dataDir = dataDir
        Build_Config.packageListFile = os.path.join(Build_Config.dataDir, Build_Config.packageListFile)

    @staticmethod
    def setPullPublishRPMSDir(pullPublishRPMSDir):
        Build_Config.pullPublishRPMSDir = pullPublishRPMSDir

    @staticmethod
    def setPullPublishXRPMS(pullPublishXRPMS):
        Build_Config.pullPublishXRPMS = pullPublishXRPMS

    @staticmethod
    def setPullPublishRPMS(pullPublishRPMS):
        Build_Config.pullPublishRPMS = pullPublishRPMS

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# class Utilities is used for generating spec dependency, priniting upward dependencies for package..      +
#                                                                                                          +
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Utilities:

    global configdict
    global check_prerequesite

    def __init__(self):

        from SpecDeps import SpecDependencyGenerator

        cmdUtils = CommandUtils()
        self.img = configdict.get("utility", {}).get("img", None)
        self.json_file = configdict.get("utility", {}).get("file", "packages_*.json")
        self.display_option = configdict.get("utility", {}).get("display-option", "json")
        self.input_type = configdict.get("utility", {}).get("input-type", "json")
        self.pkg = configdict.get("utility", {}).get("pkg", None)

        self.logger = Logger.getLogger("SpecDeps", constants.logPath, constants.logLevel)
        if not os.path.isdir(Build_Config.generatedDataPath):
            cmdUtils.runCommandInShell("mkdir -p " + Build_Config.generatedDataPath)

        if configdict["targetName"] in ["pkgtree", "who-needs", "print-upward-deps"] and "pkg" not in os.environ:
            raise Exception("pkg not present in os.environ")
        elif configdict["targetName"] in ["pkgtree", "who-needs", "print-upward-deps"]:
            self.pkg = os.environ["pkg"]
            self.display_option = "tree"

        if configdict["targetName"] == "imgtree" and "img" not in os.environ:
            raise Exception("img not present in os.environ")
        elif configdict["targetName"] == "imgtree":
            self.json_file = "packages_" + os.environ["img"] + ".json"

        self.specDepsObject = SpecDependencyGenerator(constants.logPath, constants.logLevel)

    def generate_dep_lists(self):
        check_prerequesite["generate-dep-lists"] = True
        list_json_files = glob.glob(os.path.join(Build_Config.dataDir, self.json_file))
        # Generate the expanded package dependencies json file based on package_list_file
        self.logger.info("Generating the install time dependency list for all json files")
        if list_json_files:
            shutil.copy2(os.path.join(Build_Config.dataDir, "build_install_options_all.json"), Build_Config.generatedDataPath)
            shutil.copy2(os.path.join(Build_Config.dataDir, "build_install_options_minimal.json"), Build_Config.generatedDataPath)
            shutil.copy2(os.path.join(Build_Config.dataDir, "build_install_options_rt.json"), Build_Config.generatedDataPath)
        for json_file in list_json_files:
            output_file = None
            if self.display_option == "json":
                output_file = os.path.join(Build_Config.generatedDataPath, os.path.splitext(os.path.basename(json_file))[0]+"_expanded.json")
                self.specDepsObject.process(self.input_type, json_file, self.display_option, output_file)
                shutil.copyfile(json_file, os.path.join(Build_Config.generatedDataPath, os.path.basename(json_file)))

    def pkgtree(self):
        self.input_type = "pkg"
        self.specDepsObject.process(self.input_type, self.pkg, self.display_option)

    def who_needs(self):
        self.input_type = "who-needs"
        self.specDepsObject.process(self.input_type, self.pkg, self.display_option)

    def imgtree(self):
        self.input_type = "json"
        self.generate_dep_lists()

    def print_upward_deps(self):
        whoNeedsList = self.specDepsObject.process("get-upward-deps", self.pkg, self.display_option)
        self.logger.info("Upward dependencies: " + str(whoNeedsList))

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  class Buildenvironmentsetup does job like pulling toolchain RPMS and creating stage...                   +
#                                                                                                           +
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


class BuildEnvironmentSetup:

    global configdict
    global check_prerequesite

    def packages_cached():
        check_prerequesite["packages-cached"]=True
        CommandUtils.runCommandInShell("rm -rf " + Build_Config.rpmNoArchPath + "/*")
        CommandUtils.runCommandInShell("rm -rf " + Build_Config.rpmArchPath + "/*")
        CommandUtils.runCommandInShell("cp -rf " + configdict["additional-path"]["photon-cache-path"] + "/RPMS/noarch/* " + Build_Config.rpmNoArchPath)
        CommandUtils.runCommandInShell("cp -rf " + configdict["additional-path"]["photon-cache-path"] + \
                "/RPMS/" + constants.currentArch + "/* " + Build_Config.rpmArchPath)
        RpmBuildTarget.create_repo()

    def sources():
        if configdict['additional-path']['photon-sources-path'] is None:
            check_prerequesite["sources"]=True
            if not os.path.isdir(constants.sourcePath):
                os.mkdir(constants.sourcePath)
        else:
            BuildEnvironmentSetup.sources_cached()

    def sources_cached():
        check_prerequesite["sources-cached"]=True
        print("Using cached SOURCES...")
        CommandUtils.runCommandInShell("ln -sf " + configdict["additional-path"]["photon-sources-path"] + "  " + constants.sourcePath)

    def publish_rpms():
        if configdict['additional-path']['photon-publish-rpms-path'] is None:
            check_prerequesite["publish-rpms"]=True
            print("Pulling toolchain RPMS...")
            if subprocess.Popen(["cd " + Build_Config.pullPublishRPMSDir + " && " \
                    + Build_Config.pullPublishRPMS + " " + constants.prevPublishRPMRepo], shell=True).wait() != 0:
                raise Exception("Cannot run publish-rpms")
        else:
            BuildEnvironmentSetup.publish_rpms_cached()

    def publish_rpms_cached():
        check_prerequesite["publish-rpms-cached"]=True
        if not os.path.isdir(constants.prevPublishRPMRepo + "/" + constants.currentArch):
            os.makedirs(constants.prevPublishRPMRepo + "/" + constants.currentArch)
        if not os.path.isdir(constants.prevPublishRPMRepo + "/noarch"):
            os.makedirs(constants.prevPublishRPMRepo + "/noarch")
        if subprocess.Popen(["cd " + Build_Config.pullPublishRPMSDir + " && " + \
                Build_Config.pullPublishRPMS + " " + constants.prevPublishRPMRepo + "  " + \
                configdict["additional-path"]["photon-publish-rpms-path"]], shell=True).wait() != 0:
            raise Exception("Cannot run publish-rpms-cached")

    def publish_x_rpms_cached():
        check_prerequesite["publish-x-rpms-cached"]=True
        if not os.path.isdir(constants.prevPublishXRPMRepo + "/" + constants.currentArch):
            os.makedirs(constants.prevPublishXRPMRepo + "/" + constants.currentArch)
        if not os.path.isdir(constants.prevPublishRPMRepo + "/noarch"):
            os.makedirs(constants.prevPublishXRPMRepo + "/noarch")
        if subprocess.Popen(["cd " + Build_Config.pullPublishRPMSDir + " && " + Build_Config.pullPublishXRPMS \
                + " " + constants.prevPublishXRPMRepo + "  " + \
                configdict["additional-path"]["photon-publish-x-rpms-path"]], shell=True).wait() != 0:
            raise Exception("Cannot run publish-x-rpms-cached")


    def publish_x_rpms():
        if configdict['additional-path']['photon-publish-x-rpms-path'] is None:
            check_prerequesite["publish-x-rpms"]=True
            print("\nPulling X toolchain RPMS...")
            if subprocess.Popen(["cd " + Build_Config.pullPublishRPMSDir + " && " + Build_Config.pullPublishXRPMS \
                    + " " + constants.prevPublishXRPMRepo], shell=True).wait() != 0:
                raise Exception("Cannot run publishx-rpms")
        else:
            BuildEnvironmentSetup.publish_x_rpms_cached()

    def photon_stage():
        check_prerequesite["photon-stage"]=True
        print("\nCreating staging folder and subitems...")

        if not os.path.isdir(Build_Config.stagePath):
            os.mkdir(Build_Config.stagePath)

        if not os.path.isdir(constants.buildRootPath):
            os.mkdir(constants.buildRootPath)

        if not os.path.isdir(constants.rpmPath):
            os.mkdir(constants.rpmPath)
            if not os.path.isdir(Build_Config.rpmArchPath):
                os.mkdir(Build_Config.rpmArchPath)
            if not os.path.isdir(Build_Config.rpmNoArchPath):
                os.mkdir(Build_Config.rpmNoArchPath)

        if not os.path.isdir(constants.sourceRpmPath):
            os.mkdir(constants.sourceRpmPath)

        if not os.path.isdir(Build_Config.updatedRpmPath):
            os.mkdir(Build_Config.updatedRpmPath)
            if not os.path.isdir(Build_Config.updatedRpmNoArchPath):
                os.mkdir(Build_Config.updatedRpmNoArchPath)
            if not os.path.isdir(Build_Config.updatedRpmArchPath):
                os.mkdir(Build_Config.updatedRpmArchPath)

        if not os.path.isdir(constants.sourcePath):
            os.mkdir(constants.sourcePath)

        if not os.path.isdir(constants.logPath):
            os.mkdir(constants.logPath)

        if not os.path.isfile(Build_Config.stagePath + "/COPYING"):
            CommandUtils.runCommandInShell("install -m 444 " + curDir + "/COPYING " + Build_Config.stagePath + "/COPYING")

        if not os.path.isfile(Build_Config.stagePath + "/NOTICE-GPL2.0"):
            CommandUtils.runCommandInShell("install -m 444 " + curDir + "/NOTICE-GPL2.0 " + Build_Config.stagePath + "/NOTICE-GPL2.0")

        if not os.path.isfile(Build_Config.stagePath + "/NOTICE-Apachev2"):
            CommandUtils.runCommandInShell("install -m 444 " + curDir + "/NOTICE-Apachev2 " + Build_Config.stagePath + "/NOTICE-Apachev2")

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# class Cleanup does the job of cleaning up the stage directory...                                              +
#                                                                                                               +
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CleanUp:

    def clean():
        CleanUp.clean_install()
        CleanUp.clean_chroot()
        print("Deleting Photon ISO...")
        CommandUtils.runCommandInShell("rm -f " + Build_Config.stagePath + "/photon-*.iso")
        print("Deleting stage dir...")
        CommandUtils.runCommandInShell("rm -rf " + Build_Config.stagePath)
        print("Deleting chroot path...")
        CommandUtils.runCommandInShell("rm -rf " + constants.buildRootPath)
        print("Deleting tools/bin...")
        CommandUtils.runCommandInShell("rm -rf tools/bin")

    def clean_install():
        print("Cleaning installer working directory...")
        if os.path.isdir(os.path.join(Build_Config.stagePath, "photon_iso")):
            if subprocess.Popen(["support/package-builder/clean-up-chroot.py", os.path.join(Build_Config.stagePath, "photon_iso")]).wait() != 0:
                raise Exception("Not able to clean chroot")

    def clean_chroot():
        print("Cleaning chroot path...")
        if os.path.isdir(constants.buildRootPath):
            if subprocess.Popen([curDir + "/support/package-builder/clean-up-chroot.py", constants.buildRootPath]).wait() != 0:
                raise Exception("Not able to clean chroot")

    def clean_stage_for_incremental_build():
        #cd /root/photon;test -z "$(git diff --name-only 84562de @ | grep SPECS)" || \
        #   /root/photon/support/package-builder/SpecDeps.py  --spec-path SPECS/
        #                                                     -i remove-upward-deps \
        #                                                     -p "$(echo `git diff --name-only 84562de @ | grep .spec | xargs -n1 basename 2>/dev/null` | tr ' ' :)"
        command = "cd %s; \
                   test -z \"$(git diff --name-only %s @ | grep SPECS)\" || \
                   %s --spec-path SPECS/ \
                      -i remove-upward-deps \
                      -p \"$(echo `git diff --name-only %s @ | grep .spec | xargs -n1 basename 2>/dev/null` | tr ' ' :)\"" % (configdict["photon-path"],
                                                                                                                              configdict["photon-build-param"]["base-commit"],
                                                                                                                              "%s/support/package-builder/SpecDeps.py" % (curDir),
                                                                                                                              configdict["photon-build-param"]["base-commit"])
        subprocess.Popen(command, shell=True).wait()

        #test -n "$(git diff --name-only @~1 @ | grep '^support/\(make\|package-builder\|pullpublishrpms\)')" && \
        # { echo "Remove all staged RPMs"; $(RM) -rf $(PHOTON_RPMS_DIR); } ||:
        command = "test -n \"$(git diff --name-only @~1 @ | grep '^support/\(make\|package-builder\|pullpublishrpms\)')\" && \
                   { cd %s; echo \"Remove all staged RPMs\"; /bin/rm -rf ./stage/RPMS; } ||:" % (configdict["photon-path"])
        if subprocess.Popen(command, shell=True).wait() != 0:
            raise Exception("Not able to run clean_stage_for_incremental_build")
        return


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# class Rpmbuildtarget does the job of building all the RPMs for the SPECS                                            +
# It uses Builder class in builder.py in order to build packages.                                                     +
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class RpmBuildTarget:

    global configdict
    global check_prerequesite

    def __init__(self):
        from SpecData import SPECS

        self.logger = Logger.getLogger("Main", constants.logPath, constants.logLevel)

        if not check_prerequesite["check-docker-py"]:
            CheckTools.check_docker_py()

        if not check_prerequesite["check-tools"]:
            CheckTools.check_tools()

        if not check_prerequesite["photon-stage"]:
            BuildEnvironmentSetup.photon_stage()

        if configdict["additional-path"]["photon-publish-x-rpms-path"] is not None and not check_prerequesite["publish-x-rpms-cached"]:
            BuildEnvironmentSetup.publish_x_rpms_cached()
        else:
            if not check_prerequesite["publish-x-rpms"]:
                BuildEnvironmentSetup.publish_x_rpms()

        if configdict["additional-path"]["photon-publish-rpms-path"] is not None and not check_prerequesite["publish-rpms-cached"]:
            BuildEnvironmentSetup.publish_rpms_cached()
        else:
            if not check_prerequesite["publish-rpms"]:
                BuildEnvironmentSetup.publish_rpms()

        if configdict["additional-path"]["photon-sources-path"] is not None and not check_prerequesite["sources-cached"]:
            BuildEnvironmentSetup.sources_cached()
        else:
            if not check_prerequesite["sources"]:
                BuildEnvironmentSetup.sources()

        if not check_prerequesite["contain"]:
            contain()

        if not check_prerequesite["check-spec-files"]:
            CheckTools.check_spec_files()

        a = Utilities()
        a.generate_dep_lists()

        if constants.buildArch != constants.targetArch:
            CommandUtils.runCommandInShell("mkdir -p " + constants.rpmPath + "/" + constants.targetArch)

        self.logger.debug("Source Path :" + constants.sourcePath)
        self.logger.debug("Spec Path :" + constants.specPath)
        self.logger.debug("Rpm Path :" + constants.rpmPath)
        self.logger.debug("Log Path :" + constants.logPath)
        self.logger.debug("Log Level :" + constants.logLevel)
        self.logger.debug("Top Dir Path :" + constants.topDirPath)
        self.logger.debug("Publish RPMS Path :" + constants.prevPublishRPMRepo)
        self.logger.debug("Publish X RPMS Path :" + constants.prevPublishXRPMRepo)

        Builder.get_packages_with_build_options(configdict['photon-build-param']['pkg-build-options'])

        os.chdir(str(PurePath(curDir, "support", "package-builder")))
        if not check_prerequesite["generate-dep-lists"]:
            SPECS()
        if constants.buildArch != constants.targetArch:
            # It is cross compilation
            # first build all native packages
            Builder.buildPackagesForAllSpecs(Build_Config.buildThreads, Build_Config.pkgBuildType, Build_Config.pkgInfoFile, self.logger)

            # Then do the build to the target
            constants.currentArch = constants.targetArch
            constants.crossCompiling = True


    @staticmethod
    def create_repo():
        check_prerequesite["create-repo"]=True
        if subprocess.Popen(["createrepo " + constants.rpmPath], shell=True).wait() != 0:
            raise Exception("Not able to create repodata")

    @staticmethod
    def ostree_repo():
        check_prerequesite["ostree-repo"]=True
        if not check_prerequesite["start-docker"]:
            CheckTools.start_docker()
        if not os.path.isfile(os.path.join(Build_Config.stagePath, "ostree-repo.tar.gz")):
            process = subprocess.Popen([curDir + "/support/image-builder/ostree-tools/make-ostree-image.sh", curDir, Build_Config.stagePath])

            retval = process.wait()
            if retval != 0:
                print("Not able to execute make-ostree-image.sh")
        else:
            print("Creating OSTree repo from local RPMs in ostree-repo.tar.gz...")

    def packages(self):
        check_prerequesite["packages"]=True
        if configdict['additional-path']['photon-cache-path'] is None:
            Builder.buildPackagesForAllSpecs(Build_Config.buildThreads,
                                                Build_Config.pkgBuildType,
                                                Build_Config.pkgInfoFile,
                                                self.logger)
            RpmBuildTarget.create_repo()
        else:
            BuildEnvironmentSetup.packages_cached()
        os.chdir(curDir)

    def package(self, pkgName):
        check_prerequesite["package"] = True
        self.logger.debug("Package to build:" + pkgName)
        Builder.buildSpecifiedPackages([pkgName], Build_Config.buildThreads, Build_Config.pkgBuildType)
        os.chdir(curDir)

    def packages_minimal(self):
        check_prerequesite["packages-minimal"] = True
        if configdict['additional-path']['photon-cache-path'] is None:
            Builder.buildPackagesInJson(os.path.join(Build_Config.dataDir, "packages_minimal.json"), \
                    Build_Config.buildThreads, Build_Config.pkgBuildType, Build_Config.pkgInfoFile, self.logger)
        else:
            BuildEnvironmentSetup.packages_cached()
        os.chdir(curDir)

    def packages_rt(self):
        check_prerequesite["packages-rt"] = True
        if configdict['additional-path']['photon-cache-path'] is None:
            Builder.buildPackagesInJson(os.path.join(Build_Config.dataDir, "packages_rt.json"), \
                    Build_Config.buildThreads, Build_Config.pkgBuildType, Build_Config.pkgInfoFile, self.logger)
        else:
            BuildEnvironmentSetup.packages_cached()
        os.chdir(curDir)

    def packages_initrd(self):
        check_prerequesite["packages-initrd"] = True
        Builder.buildPackagesInJson(os.path.join(Build_Config.dataDir, "packages_installer_initrd.json"), \
                Build_Config.buildThreads, Build_Config.pkgBuildType, Build_Config.pkgInfoFile, self.logger)
        os.chdir(curDir)

    def packages_docker(self):
        check_prerequesite["packages-docker"] = True
        Builder.buildPackagesForAllSpecs(Build_Config.buildThreads, Build_Config.pkgBuildType, Build_Config.pkgInfoFile, self.logger)
        os.chdir(curDir)

    def updated_packages(self):
        check_prerequesite["updated-packages"] = True
        constants.setRpmPath(Build_Config.updatedRpmPath)
        Builder.buildPackagesForAllSpecs(Build_Config.buildThreads, Build_Config.pkgBuildType, Build_Config.pkgInfoFile, self.logger)
        os.chdir(curDir)

    def check(self):
        check_prerequesite["check"] = True
        constants.setRPMCheck(True)
        constants.setRpmCheckStopOnError(True)
        Builder.buildPackagesForAllSpecs(Build_Config.buildThreads, Build_Config.pkgBuildType, Build_Config.pkgInfoFile, self.logger)
        os.chdir(curDir)

    def distributed_build():
        from DistributedBuilder import DistributedBuilder
        print("Building RPMS through kubernetes ...")
        os.chdir(str(PurePath(curDir, "support", "package-builder")))
        with open(Build_Config.distributedBuildFile, 'r') as configFile:
            distributedBuildConfig = json.load(configFile)

        distributedBuilder = DistributedBuilder(distributedBuildConfig)
        distributedBuilder.create()
        distributedBuilder.getLogs()
        distributedBuilder.monitorJob()
        distributedBuilder.copyFromNfs()
        distributedBuilder.deleteBuild()
        distributedBuilder.clean()

        os.chdir(curDir)

    def tool_chain_stage1(self):
        from PackageManager import PackageManager
        check_prerequesite["tool-chain-stage1"] = True
        pkgManager = PackageManager()
        pkgManager.buildToolChain()

    def tool_chain_stage2(self):
        from PackageManager import PackageManager
        check_prerequesite["tool-chain-stage2"] = True
        pkgManager = PackageManager()
        pkgManager.buildToolChainPackages(Build_Config.buildThreads)

    def generate_yaml_files(self):

        import GenerateOSSFiles

        print("Generating yaml files for packages...")
        check_prerequesite["generate-yaml-files"] = True
        if not check_prerequesite["check-tools"]:
            CheckTools.check_tools()
        if not check_prerequesite["photon-stage"]:
            BuildEnvironmentSetup.photon_stage()
        if not check_prerequesite["packages"]:
            rpmBuildTarget = RpmBuildTarget()
            rpmBuildTarget.packages()
        os.chdir(curDir + "/support/package-builder")
        if "generate-pkg-list" in configdict["photon-build-param"] and configdict["photon-build-param"]["generate-pkg-list"]:
            GenerateOSSFiles.buildPackagesList(os.path.join(Build_Config.stagePath, "packages_list.csv"))
        else:
            blackListPkgs = GenerateOSSFiles.readBlackListPackages(configdict.get("additional-path", {}).get("pkg-black-list-file", ""))
            logger = Logger.getLogger("GenerateYamlFiles", constants.logPath, constants.logLevel)
            GenerateOSSFiles.buildSourcesList(Build_Config.stagePath, blackListPkgs, logger)
            GenerateOSSFiles.buildSRPMList(constants.sourceRpmPath, Build_Config.stagePath, blackListPkgs, constants.dist, logger)
        os.chdir(curDir)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# class CheckTools does the job of checking weather all the tools required for starting build process are present on the system  +
#                                                                                                                                +
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class CheckTools:

    global configdict
    global check_prerequesite

    def check_tools():
        check_prerequesite["check-tools"] = True
        CheckTools.check_bison()
        CheckTools.check_gplusplus()
        CheckTools.check_gawk()
        CheckTools.check_repo_tool()
        CheckTools.check_texinfo()
        CheckTools.check_sanity()
        CheckTools.check_docker()
        CheckTools.check_pyopenssl()

    def check_bison():
        check_prerequesite["check-bison"]=True
        if shutil.which("bison") is None:
            raise Exception("bison not present")

    def check_gplusplus():
        check_prerequesite["check-gplusplus"]=True
        if shutil.which('g++') is None:
            raise Exception("g++ not present")

    def check_gawk():
        check_prerequesite["check-gawk"]=True
        if shutil.which('gawk') is None:
            raise Exception("gawk not present")

    def check_repo_tool():
        check_prerequesite["check-repotool"]=True
        if shutil.which('createrepo') is None:
            raise Exception("createrepo not present")

    def check_texinfo():
        check_prerequesite["check-texinfo"]=True
        if shutil.which('makeinfo') is None:
            raise Exception("texinfo not present")

    def check_sanity():
        check_prerequesite["check-sanity"]=True
        if subprocess.Popen([curDir + "/support/sanity_check.sh"], shell=True).wait() != 0:
            raise Exception("Not able to run script sanity_check.sh")

    def check_docker():
        check_prerequesite["check-docker"]=True
        if not glob.glob(Build_Config.dockerEnv) and shutil.which('docker') is None:
            raise Exception("docker not present")

    def check_docker_service():
        check_prerequesite["check-docker-service"]=True
        if not glob.glob(Build_Config.dockerEnv) and subprocess.Popen(["docker ps >/dev/null 2>&1"], shell=True).wait() != 0:
            raise Exception("Docker service is not running. Aborting.")

    def check_docker_py():
        check_prerequesite["check-docker-py"]=True
        if not glob.glob(Build_Config.dockerEnv) and docker.__version__ < "2.3.0":
            raise Exception("Error: Python3 package docker-py3 2.3.0 not installed.\nPlease use: pip3 install docker==2.3.0")

    def check_pyopenssl():
        check_prerequesite["check-pyopenssl"]=True
        try:
            import OpenSSL
        except Exception as e:
            raise Exception(e)

    def check_spec_files():
        check_prerequesite["check-spec-files"]=True
        print()
        if "base-commit" in configdict["photon-build-param"]:
            command = ["./tools/scripts/check_spec_files.sh", str(configdict["photon-build-param"].get("base-commit"))]
        else:
            command = ["./tools/scripts/check_spec_files.sh"]
        if subprocess.Popen(command, shell=True).wait() != 0:
            raise Exception("spec file check failed")

    def check_kpartx():
        check_prerequesite["check-kpartx"]=True
        if shutil.which('kpartx') is None:
            raise Exception("Package kpartx not installed. Aborting.")

    def start_docker():
        check_prerequesite["start-docker"]=True
        CheckTools.check_docker()
        if subprocess.Popen(["systemctl start docker"], shell=True).wait() != 0:
            raise Exception("Not able to start docker")

    def install_photon_docker_image():
        if not check_prerequesite["photon-docker-image"]:
            BuildImage.photon_docker_image()
        if subprocess.Popen("sudo docker build -t photon:tdnf .").wait() != 0:
            raise Exception("Not able to install photon docker image")

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# class BuildImage does the job of building all the images like iso, rpi3, ami, gce, azure, ova...                              +
# It uses class ImageBuilder to build different images.                                                                         +
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class BuildImage:

    global configdict
    global check_prerequesite

    def __init__(self, imgName):
        self.src_root = configdict["photon-path"]
        self.installer_path = Build_Config.installerPath
        self.generated_data_path = Build_Config.dataDir
        self.stage_path = Build_Config.stagePath
        self.log_path = constants.logPath
        self.log_level = constants.logLevel
        self.config_file = configdict["additional-path"]["conf-file"]
        self.img_name = imgName
        self.rpm_path = constants.rpmPath
        self.srpm_path = constants.sourceRpmPath
        self.pkg_to_rpm_map_file = os.path.join(Build_Config.stagePath, "pkg_info.json")

    def set_Iso_Parameters(self, imgName):
        self.generated_data_path = Build_Config.stagePath + "/common/data"
        self.src_iso_path = None
        if imgName == "iso":
            self.iso_path = os.path.join(Build_Config.stagePath, "photon-"+constants.releaseVersion+"-"+constants.buildNumber+".iso")
            self.debug_iso_path = self.iso_path.rpartition(".")[0]+".debug.iso"

        if imgName == "minimal-iso":
            self.iso_path = os.path.join(Build_Config.stagePath, "photon-minimal-"+constants.releaseVersion+"-"+constants.buildNumber+".iso")
            self.debug_iso_path = self.iso_path.rpartition(".")[0]+".debug.iso"
            self.package_list_file = os.path.join(Build_Config.dataDir, "build_install_options_minimal.json")
            self.pkg_to_be_copied_conf_file = os.path.join(Build_Config.generatedDataPath, "build_install_options_minimal.json")
        elif imgName == "rt-iso":
            self.iso_path = os.path.join(Build_Config.stagePath, "photon-rt-"+constants.releaseVersion+"-"+constants.buildNumber+".iso")
            self.debug_iso_path = self.iso_path.rpartition(".")[0]+".debug.iso"
            self.package_list_file = os.path.join(Build_Config.dataDir, "build_install_options_rt.json")
            self.pkg_to_be_copied_conf_file = os.path.join(Build_Config.generatedDataPath, "build_install_options_rt.json")

        else:
            self.pkg_to_be_copied_conf_file = Build_Config.pkgToBeCopiedConfFile
            self.package_list_file = Build_Config.packageListFile

        if imgName == "src-iso":
            self.iso_path = None
            self.debug_iso_path = None
            self.src_iso_path = os.path.join(Build_Config.stagePath, "photon-"+constants.releaseVersion+"-"+constants.buildNumber+".src.iso")


    def build_iso(self):

        import imagebuilder

        rpmBuildTarget = RpmBuildTarget()
        if not check_prerequesite["check-tools"]:
            CheckTools.check_tools()
        if not check_prerequesite["photon-stage"]:
            BuildEnvironmentSetup.photon_stage()
        if self.img_name == "iso" and not check_prerequesite["packages"]:
            rpmBuildTarget.packages()
        elif self.img_name == "rt-iso":
            rpmBuildTarget.packages_rt()
        else:
            rpmBuildTarget.packages_minimal()
        if self.img_name == "rt-iso" or "minimal-iso" and not check_prerequesite["packages-initrd"]:
            rpmBuildTarget.packages_initrd()
        if not check_prerequesite["create-repo"]:
            RpmBuildTarget.create_repo()
        if self.img_name != "minimal-iso" and not check_prerequesite["ostree-repo"]:
            RpmBuildTarget.ostree_repo()
        self.generated_data_path = Build_Config.generatedDataPath
        print("Building Full ISO...")
        os.chdir(str(PurePath(curDir, "support", "image-builder")))
        imagebuilder.createIso(self)
        os.chdir(curDir)

    def build_image(self):

        import imagebuilder

        if not check_prerequesite["check-kpartx"]:
            CheckTools.check_kpartx()
        if not check_prerequesite["photon-stage"]:
            BuildEnvironmentSetup.photon_stage()
        if not check_prerequesite["vixdiskutil"]:
            vixdiskutil()
        rpmBuildTarget = None
        if not check_prerequesite["packages"]:
            rpmBuildTarget = RpmBuildTarget()
            rpmBuildTarget.packages()
        if not check_prerequesite["ostree-repo"]:
            RpmBuildTarget.ostree_repo()
        print("Building image " + self.img_name)
        os.chdir(str(PurePath(curDir, "support", "image-builder")))
        imagebuilder.createImage(self)
        os.chdir(curDir)

    @staticmethod
    def photon_docker_image():
        if not check_prerequesite["create-repo"]:
            RpmBuildTarget.create_repo()
        if subprocess.Popen(["cd " + configdict["photon-path"] + ";sudo docker build --no-cache --tag photon-build " + curDir + "/support/dockerfiles/photon && sudo docker run --rm --privileged --net=host -e PHOTON_BUILD_NUMBER="+constants.buildNumber + " -e PHOTON_RELEASE_VERSION="+constants.releaseVersion + " -v "+curDir+":/workspace -v "+Build_Config.stagePath+":/workspace/stage photon-build ./support/dockerfiles/photon/make-docker-image.sh tdnf"], shell=True).wait() != 0:
            raise Exception("Not able to run photon-docker-image")

    def k8s_docker_images(self):
        if not check_prerequesite["start-docker"]:
            CheckTools.start_docker()
        if not check_prerequesite["photon-docker-image"]:
            BuildImage.photon_docker_image()
        if not os.path.isdir(os.path.join(Build_Config.stagePath, "docker_images")):
            os.mkdir(os.path.join(Build_Config.stagePath, "docker_images"))
        os.chdir(os.path.join(curDir, 'support/dockerfiles/k8s-docker-images'))
        if subprocess.Popen(['./build-k8s-base-image.sh', constants.releaseVersion, constants.buildNumber, Build_Config.stagePath]).wait() == 0 and \
        subprocess.Popen(['./build-k8s-docker-images.sh', configdict["photon-build-param"]["photon-dist-tag"], constants.releaseVersion, constants.specPath, Build_Config.stagePath]).wait() == 0 and \
        subprocess.Popen(['./build-k8s-metrics-server-image.sh', configdict["photon-build-param"]["photon-dist-tag"], constants.releaseVersion, constants.specPath, Build_Config.stagePath]).wait() ==0 and \
        subprocess.Popen(['./build-k8s-coredns-image.sh', configdict["photon-build-param"]["photon-dist-tag"], constants.releaseVersion, constants.specPath, Build_Config.stagePath]).wait() == 0 and \
        subprocess.Popen(['./build-k8s-dns-docker-images.sh', configdict["photon-build-param"]["photon-dist-tag"], constants.releaseVersion, constants.specPath, Build_Config.stagePath]).wait() == 0 and \
        subprocess.Popen(['./build-k8s-dashboard-docker-images.sh', configdict["photon-build-param"]["photon-dist-tag"], constants.releaseVersion, constants.specPath, Build_Config.stagePath]).wait() == 0 and \
        subprocess.Popen(['./build-flannel-docker-image.sh', configdict["photon-build-param"]["photon-dist-tag"], constants.releaseVersion, constants.specPath, Build_Config.stagePath]).wait() == 0 and \
        subprocess.Popen(['./build-calico-docker-images.sh', configdict["photon-build-param"]["photon-dist-tag"], constants.releaseVersion, constants.specPath, Build_Config.stagePath]).wait() == 0 and \
        subprocess.Popen(['./build-k8s-heapster-image.sh', configdict["photon-build-param"]["photon-dist-tag"], constants.releaseVersion, constants.specPath, Build_Config.stagePath]).wait() == 0 and \
        subprocess.Popen(['./build-k8s-nginx-ingress.sh', configdict["photon-build-param"]["photon-dist-tag"], constants.releaseVersion, constants.specPath, Build_Config.stagePath]).wait() == 0 and \
        subprocess.Popen(['./build-wavefront-proxy-docker-image.sh', configdict["photon-build-param"]["photon-dist-tag"], constants.releaseVersion, constants.specPath, Build_Config.stagePath]).wait() == 0:
            print("Successfully built all the docker images")

        else:
            raise Exception("k8s-docker-images build failed")
        os.chdir(curDir)

    def all_images(self):
        images = ["ami", "gce", "azure", "ova_uefi", "ova" ]
        for img in images:
           self.img_name = img
           self.build_image()

    def all(self):
        images = ["iso", "photon-docker-image", "k8s-docker-images", "all-images", "src-iso", "minimal-iso"]
        for img in images:
            self.img_name = img
            self.set_Iso_Parameters(img)
            if img in ["iso", "src-iso"]:
                self.build_iso()
            else:
                configdict["targetName"] = img.replace('-', '_')
                getattr(self, configdict["targetName"])()

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# initialize_constants initialize all the paths like stage Path, spec path, rpm path, and other parameters           +
# used by package-builder and imagebuilder...                                                                        +
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def initialize_constants():

    global configdict
    global check_prerequesite
    check_prerequesite["initialize-constants"]=True

    Build_Config.setStagePath(os.path.join(str(PurePath(configdict["photon-path"], configdict["stage-path"])), "stage"))
    constants.setSpecPath(os.path.join(str(PurePath(configdict["photon-path"], configdict["spec-path"])), "SPECS"))
    Build_Config.setBuildThreads(configdict["photon-build-param"]["threads"])
    Build_Config.setPkgBuildType(configdict["photon-build-param"]["photon-build-type"])
    Build_Config.setPkgJsonInput(configdict.get("additional-path", {}).get("pkg-json-input", None))
    constants.setLogPath(os.path.join(Build_Config.stagePath ,"LOGS"))
    constants.setLogLevel(configdict["photon-build-param"]["loglevel"])
    constants.setDist(configdict["photon-build-param"]["photon-dist-tag"])
    constants.setBuildNumber(configdict["photon-build-param"]["input-photon-build-number"])
    constants.setReleaseVersion(configdict["photon-build-param"]["photon-release-version"])
    constants.setPullSourcesURL(Builder.get_baseurl(configdict["pull-sources-config"]))
    constants.setRPMCheck(configdict["photon-build-param"].get("rpm-check-flag", False))
    constants.setRpmCheckStopOnError(configdict["photon-build-param"].get("rpm-check-stop-on-error", False))
    constants.setPublishBuildDependencies(configdict["photon-build-param"].get("publish-build-dependencies", False))
    constants.setRpmPath(os.path.join(Build_Config.stagePath ,"RPMS"))
    Build_Config.setRpmNoArchPath()
    Build_Config.setRpmArchPath()
    constants.setSourceRpmPath(os.path.join(Build_Config.stagePath ,"SRPMS"))
    Build_Config.setUpdatedRpmPath(os.path.join(Build_Config.stagePath ,"UPDATED_RPMS"))
    constants.setSourcePath(os.path.join(Build_Config.stagePath ,"SOURCES"))
    constants.setPrevPublishRPMRepo(os.path.join(Build_Config.stagePath , "PUBLISHRPMS"))
    constants.setPrevPublishXRPMRepo(os.path.join(Build_Config.stagePath , "PUBLISHXRPMS"))
    Build_Config.setInstallerPath(os.path.join(configdict["photon-path"], "installer"))
    Build_Config.setPkgInfoFile(os.path.join(Build_Config.stagePath ,"pkg_info.json"))
    constants.setBuildRootPath(os.path.join(Build_Config.stagePath ,"photonroot"))
    Build_Config.setGeneratedDataDir(os.path.join(Build_Config.stagePath ,"common/data"))
    constants.setTopDirPath("/usr/src/photon")
    Build_Config.setCommonDir(os.path.join(curDir ,"common"))
    Build_Config.setDataDir(os.path.join(curDir, "common/data"))
    constants.setInputRPMSPath(configdict.get("input-rpms-path", os.path.join(curDir,"inputRPMS")))
    Build_Config.setPullPublishRPMSDir(os.path.join(curDir, "support/pullpublishrpms"))
    Build_Config.setPullPublishRPMS(os.path.join(Build_Config.pullPublishRPMSDir ,"pullpublishrpms.sh"))
    Build_Config.setPullPublishXRPMS(os.path.join(Build_Config.pullPublishRPMSDir ,"pullpublishXrpms.sh"))
    constants.setPackageWeightsPath(os.path.join(Build_Config.dataDir ,"packageWeights.json"))
    constants.setKatBuild(configdict["photon-build-param"].get("kat-build", False))
    Build_Config.setConfFile(configdict["additional-path"]["conf-file"])
    Build_Config.setPkgToBeCopiedConfFile(configdict.get("additional-path", {}).get("pkg-to-be-copied-conf-file"))
    Build_Config.setDistributedBuildFile(configdict.get("additional-path", {}).get("distributed-build-option-file", PurePath(curDir, "common", "data", "distributed_build_options.json")))
    Builder.get_packages_with_build_options(configdict['photon-build-param']['pkg-build-options'])
    Build_Config.setCommonDir(PurePath(curDir, "common", "data"))
    constants.setStartSchedulerServer(configdict["photon-build-param"]['start-scheduler-server'])
    constants.initialize()


def set_default_value_of_config():

    global configdict

    configdict["pull-sources-config"] = os.path.join(curDir , "support/package-builder/bintray.conf")
    configdict.setdefault("additional-path", {}).setdefault("photon-cache-path", None)
    configdict["photon-build-param"]["input-photon-build-number"]=subprocess.check_output(["git rev-parse --short HEAD"], shell=True).decode('ASCII').rstrip()
    configdict.setdefault('additional-path', {}).setdefault('photon-sources-path', None)
    configdict.setdefault('additional-path', {}).setdefault('photon-publish-rpms-path', None)
    configdict.setdefault('additional-path', {}).setdefault('photon-publish-x-rpms-path', None)
    configdict['photon-build-param']['pkg-build-options'] = curDir + "/common/data/" + configdict['photon-build-param']['pkg-build-options']
    configdict.setdefault("additional-path", {}).setdefault("conf-file", None)
    configdict.setdefault("photon-build-param", {}).setdefault("start-scheduler-server", False)


def main():

    parser = ArgumentParser()

    parser.add_argument("-b", "--branch", dest="photonBranch", default=None)
    parser.add_argument("-c", "--config", dest="configPath", default=None)
    parser.add_argument("-t", "--target", dest="targetName", default=None)

    options = parser.parse_args()

    if options.photonBranch is None and options.configPath is None:
        raise Exception("Either specify branchName or configpath...")

    if options.photonBranch is not None and not os.path.isdir(os.path.join(curDir ,"photon-" + options.photonBranch)):
        CommandUtils.runCommandInShell("git clone https://github.com/vmware/photon.git -b " + options.photonBranch + " photon-" + options.photonBranch)
    elif options.photonBranch is not None:
        print("Using already cloned repository...")

    if options.configPath is None:
        options.configPath = str(PurePath(curDir, "photon-" + options.photonBranch, "config.json"))

    global configdict
    global check_prerequesite

    with open(options.configPath) as jsonData:
        configdict = json.load(jsonData)

    options.configPath = os.path.abspath(options.configPath)

    set_default_value_of_config()

    os.environ['PHOTON_RELEASE_VER']=configdict["photon-build-param"]["photon-release-version"]
    os.environ['PHOTON_BUILD_NUM']=configdict["photon-build-param"]["input-photon-build-number"]


    if configdict["photon-path"] == "":
        configdict["photon-path"] = os.path.dirname(options.configPath)

    if 'INPUT_PHOTON_BUILD_NUMBER' in os.environ:
        configdict["photon-build-param"]["input-photon-build-number"]=os.environ['IMPUT_PHOTON_BUILD_NUMBER']

    if 'BASE_COMMIT' in os.environ:
        configdict["photon-build-param"]["base-commit"] = os.environ['BASE_COMMIT']

    if 'THREADS' in os.environ:
        configdict["photon-build-param"]["threads"] = int(os.environ['THREADS'])

    if 'LOGLEVEL' in os.environ:
        configdict["photon-build-param"]["loglevel"] = os.environ["LOGLEVEL"]

    if 'PHOTON_PULLSOURCES_CONFIG' in os.environ:
        configdict['pull-sources-config'] = os.environ['PHOTON_PULLSOURCES_CONFIG']

    if 'PHOTON_CACHE_PATH' in os.environ:
        configdict.setdefault("additional-path", {}).setdefault("photon-cache-path", os.environ['PHOTON_CACHE_PATH'])

    if 'PHOTON_SOURCES_PATH' in os.environ:
        configdict.setdefault('additional-path', {}).setdefault('photon-sources-path', os.environ["PHOTON_SOURCES_PATH"])

    if 'PHOTON_PUBLISH_RPMS_PATH' in os.environ:
        configdict.setdefault('additional-path', {}).setdefault('photon-publish-rpms-path', os.environ['PHOTON_PUBLISH_RPMS_PATH'])

    if 'PHOTON_PUBLISH_XRPMS_PATH' in os.environ:
        configdict.setdefault('additional-path', {}).setdefault('photon-publish-x-rpms-path', os.environ['PHOTON_PUBLISH_XRPMS_PATH'])

    if "PHOTON_PKG_BLACKLIST_FILE" in os.environ:
        configdict["additional-path"]["pkg-black-list-file"] = os.environ["PHOTON_PKG_BLACKLIST_FILE"]

    if "DISTRIBUTED_BUILD_CONFIG" in os.environ:
        configdict["additional-path"]["distributed-build-option-file"] = os.environ["DISTRIBUTED_BUILD_CONFIG"]

    if 'RPMCHECK' in os.environ:
        if os.environ['RPMCHECK']=="enable":
            configdict['photon-build-param']['rpm-check-flag'] = True
        elif os.environ['RPMCHECK']=="enable_stop_on_error":
            configdict['photon-build-param']['rpm-check-flag'] = True
            configdict['photon-build-param']["rpm-check-stop-on-error"] = True

    if 'KAT_BUILD' in os.environ and os.environ['KAT_BUILD'] == "enable":
        configdict['photon-build-param']['kat-build'] = True

    if 'BUILDDEPS' in os.environ and os.environ['BUILDDEPS']=="True":
        configdict['photon-build-param']['publish-build-dependencies'] = True

    if 'PKG_BUILD_OPTIONS' in os.environ:
        configdict['photon-build-param']['pkg-build-options'] = os.environ['PKG_BUILD_OPTIONS']

    if 'CROSS_TARGET' in os.environ:
        configdict['photon-build-param']['tarsetdefaultArch'] = os.environ['CROSS_TARGET']

    if 'CONFIG' in os.environ:
        configdict['additional-path']['conf-file'] = os.path.abspath(os.environ['CONFIG'])
        jsonData = Utils.jsonread(os.environ['CONFIG'])
        options.targetName = jsonData['image_type']

    if 'IMG_NAME' in os.environ:
        options.targetName = os.environ['IMG_NAME']

    if 'SCHEDULER_SERVER' in os.environ and os.environ['SCHEDULER_SERVER'] == "enable":
        configdict['photon-build-param']['start-scheduler-server'] = True

    if 'DOCKER_ENV' in os.environ:
        Build_Config.setDockerEnv(os.environ['DOCKER_ENV'])


    initialize_constants()

    configdict["packageName"]=None

    for target in targetList:
        for item in targetList[target]:
            check_prerequesite[item]=False

    if options.targetName is None:
        options.targetName = configdict["photon-build-param"]["target"]

    configdict["targetName"] = options.targetName.replace('-', '_')

    try:
        if options.targetName in targetList["image"]:
            buildImage = BuildImage(options.targetName)
            if options.targetName in ["iso", "src-iso", "minimal-iso", "rt-iso"]:
                buildImage.set_Iso_Parameters(options.targetName)
                buildImage.build_iso()
            elif options.targetName in ["ami", "gce", "ova", "ova_uefi", "rpi3", "azure"]:
                buildImage.build_image()
            else:
                attr = getattr(buildImage, configdict["targetName"])
                attr()
        elif options.targetName in targetList["rpmBuild"]:
            attr = None
            if options.targetName != "distributed-build":
                rpmBuildTarget = RpmBuildTarget()
                attr = getattr(rpmBuildTarget, configdict["targetName"])
            else:
                attr = getattr(RpmBuildTarget, configdict["targetName"])
            attr()
        elif options.targetName in targetList["buildEnvironment"]:
            attr = getattr(BuildEnvironmentSetup, configdict["targetName"])
            attr()
        elif options.targetName in targetList["cleanup"]:
            attr = getattr(CleanUp, configdict["targetName"])
            attr()
        elif options.targetName in targetList["tool-checkup"]:
            if options.targetName == "check-g++":
                CheckTools.check_gplusplus()
            else:
                attr = getattr(CheckTools, configdict["targetName"])
                attr()
        elif options.targetName in targetList["utilities"]:
            utility = Utilities()
            attr = getattr(utility, configdict["targetName"])
            attr()
        else:
            rpmBuildTarget = RpmBuildTarget()
            rpmBuildTarget.package(options.targetName)
    except Exception as e:
        print(e)
        traceback.print_exc()
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
