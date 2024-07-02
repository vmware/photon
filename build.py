#!/usr/bin/env python3

# built-in imports
import os
import sys
import docker
import glob
import json
import shutil
import traceback

from argparse import ArgumentParser
from pathlib import PurePath, Path
from urllib.parse import urlparse

# photon imports
sys.path.append(
    f"{os.path.dirname(os.path.realpath(__file__))}/support/package-builder"
)
sys.path.append(
    f"{os.path.dirname(os.path.realpath(__file__))}/support/spec-checker",
)

import GenerateOSSFiles
import PullSources as downloader

from builder import Builder
from constants import constants
from CommandUtils import CommandUtils
from Logger import Logger
from PackageManager import PackageManager
from StringUtils import StringUtils
from SpecDeps import SpecDependencyGenerator
from SpecData import SPECS
from check_spec import check_specs


targetDict = {
    "image": [
        "iso",
        "ami",
        "gce",
        "azure",
        "rpi",
        "ova",
        "all",
        "src-iso",
        "ls1012afrwy",
        "photon-docker-image",
        "k8s-docker-images",
        "all-images",
        "minimal-iso",
        "basic-iso",
        "rt-iso",
    ],
    "rpmBuild": [
        "packages",
        "packages-minimal",
        "packages-basic",
        "packages-rt",
        "packages-initrd",
        "packages-docker",
        "updated-packages",
        "tool-chain-stage1",
        "tool-chain-stage2",
        "check-packages",
        "ostree-repo",
        "generate-yaml-files",
        "create-repo",
        "distributed-build",
        "extra-packages",
    ],
    "buildEnvironment": [
        "packages-cached",
        "sources",
        "sources-cached",
        "publish-rpms",
        "publish-x-rpms",
        "publish-rpms-cached",
        "publish-x-rpms-cached",
        "photon-stage",
    ],
    "cleanup": [
        "clean",
        "clean-install",
        "clean-chroot",
        "clean-stage-for-incremental-build",
    ],
    "tool-checkup": [
        "check-pre-reqs",
        "check-spec-files",
        "initialize-constants",
    ],
    "utilities": [
        "generate-dep-lists",
        "pkgtree",
        "imgtree",
        "who-needs",
        "print-upward-deps",
        "pull-stage-rpms",
        "clean-stage-rpms",
    ],
}

configdict = {}
check_prerequesite = {}
ph_path = ""

cmdUtils = CommandUtils()
runBashCmd = cmdUtils.runBashCmd

curDir = os.getcwd()
photonDir = os.path.dirname(os.path.realpath(__file__))


def url_validator(url):
    try:
        res = urlparse(url)
        return all([res.scheme, res.netloc])
    except:
        return False


class Build_Config:
    buildThreads = 1
    stagePath = ""
    pkgJsonInput = None
    rpmNoArchPath = ""
    chrootPath = ""
    generatedDataPath = ""
    pullPublishRPMSDir = ""
    pullPublishRPMS = ""
    pullPublishRPMSCached = ""
    updatedRpmPath = ""
    updatedRpmNoArchPath = ""
    dockerEnv = "/.dockerenv"
    updatedRpmArchPath = ""
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
        Build_Config.rpmNoArchPath = f"{constants.rpmPath}/noarch"

    @staticmethod
    def setRpmArchPath():
        Build_Config.rpmArchPath = f"{constants.rpmPath}/{constants.buildArch}"

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
        Build_Config.updatedRpmNoArchPath = f"{updatedRpmPath}/noarch"
        Build_Config.updatedRpmArchPath = (
            f"{updatedRpmPath}/{constants.buildArch}"
        )

    @staticmethod
    def setStagePath(stagePath):
        Build_Config.stagePath = stagePath

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
        pkgListFile = Build_Config.packageListFile
        Build_Config.packageListFile = f"{dataDir}/{pkgListFile}"

    @staticmethod
    def setPullPublishRPMSDir(pullPublishRPMSDir):
        Build_Config.pullPublishRPMSDir = pullPublishRPMSDir

    @staticmethod
    def setPullPublishRPMS(pullPublishRPMS):
        Build_Config.pullPublishRPMS = pullPublishRPMS

    @staticmethod
    def setPullPublishRPMSCached(pullPublishRPMSCached):
        Build_Config.pullPublishRPMSCached = pullPublishRPMSCached


"""
class Utilities is used for generating spec dependency, printing upward dependencies for package..
"""


class Utilities:

    global configdict
    global check_prerequesite

    def __init__(self, args):

        self.img = configdict.get("utility", {}).get("img", None)
        self.json_file = configdict.get("utility", {}).get(
            "file", "packages_*.json"
        )
        self.display_option = configdict.get("utility", {}).get(
            "display-option", "json"
        )
        self.input_type = configdict.get("utility", {}).get(
            "input-type", "json"
        )
        self.pkg = configdict.get("utility", {}).get("pkg", None)
        self.args = args

        self.logger = Logger.getLogger(
            "SpecDeps", constants.logPath, constants.logLevel
        )
        if not os.path.isdir(Build_Config.generatedDataPath):
            runBashCmd(f"mkdir -p {Build_Config.generatedDataPath}")

        if configdict["targetName"] in [
            "pkgtree",
            "who_needs",
            "print_upward_deps",
        ]:
            if "pkg" not in os.environ:
                if not args or len(args) != 1:
                    raise Exception(
                        "Please provide package name as a parameter or as an environment variable pkg=<pkg-name>"
                    )
                self.pkg = args[0]
            else:
                self.pkg = os.environ["pkg"]
            self.display_option = "tree"

        if configdict["targetName"] == "imgtree" and "img" not in os.environ:
            raise Exception("img not present in os.environ")

        if configdict["targetName"] == "imgtree":
            self.json_file = "packages_" + os.environ["img"] + ".json"

        self.specDepsObject = SpecDependencyGenerator(
            constants.logPath, constants.logLevel
        )

    def generate_dep_lists(self):
        check_prerequesite["generate-dep-lists"] = True
        list_json_files = glob.glob(
            os.path.join(Build_Config.dataDir, self.json_file)
        )
        # Generate the expanded package dependencies json file based on package_list_file
        self.logger.info(
            "Generating the install time dependency list for all json files"
        )
        if list_json_files:
            runBashCmd(
                f"cp {Build_Config.dataDir}/build_install_options_all.json"
                f" {Build_Config.dataDir}/build_install_options_minimal.json"
                f" {Build_Config.dataDir}/build_install_options_basic.json"
                f" {Build_Config.dataDir}/build_install_options_rt.json"
                f" {Build_Config.generatedDataPath}"
            )

        for json_file in list_json_files:
            output_file = None
            if self.display_option == "json":
                output_file = os.path.join(
                    Build_Config.generatedDataPath,
                    os.path.splitext(os.path.basename(json_file))[0]
                    + "_expanded.json",
                )
                self.specDepsObject.process(
                    self.input_type,
                    json_file,
                    self.display_option,
                    output_file,
                )
                shutil.copyfile(
                    json_file,
                    os.path.join(
                        Build_Config.generatedDataPath,
                        os.path.basename(json_file),
                    ),
                )

    def pkgtree(self):
        self.input_type = "pkg"
        self.specDepsObject.process(
            self.input_type, self.pkg, self.display_option
        )

    def who_needs(self):
        self.input_type = "who-needs"
        self.specDepsObject.process(
            self.input_type, self.pkg, self.display_option
        )

    def imgtree(self):
        self.input_type = "json"
        self.generate_dep_lists()

    def print_upward_deps(self):
        whoNeedsList = self.specDepsObject.process(
            "get-upward-deps", self.pkg, self.display_option
        )
        self.logger.info("Upward dependencies: " + str(whoNeedsList))

    def pull_stage_rpms(self):
        if not self.args or len(self.args) != 1:
            raise Exception("Please provide pull url as a parameter")

        url = self.args[0]
        files = self.specDepsObject.listRPMfilenames()
        notFound = []
        for f in files:
            dst = os.path.join(constants.rpmPath, f)
            if os.path.exists(dst):
                continue
            src = f"{url}/{f}"
            print(f"Downloading {f}")
            try:
                downloader.downloadFile(src, dst)
            except Exception:
                self.logger.info("Not found")
                notFound.append(f)
        if notFound:
            self.logger.info("List of missing files: " + str(notFound))

    def clean_stage_rpms(self):
        keepFiles = self.specDepsObject.listRPMfilenames(True)
        rpmpath = os.path.join(constants.rpmPath, constants.currentArch)

        allFiles = []
        for f in os.listdir(rpmpath):
            if os.path.isfile(f"{rpmpath}/{f}"):
                allFiles.append(f"{constants.currentArch}/{f}")

        rpmpath = f"{constants.rpmPath}/noarch"
        for f in os.listdir(rpmpath):
            if os.path.isfile(f"{rpmpath}/{f}"):
                allFiles.append(f"noarch/{f}")

        removeFiles = list(set(allFiles) - set(keepFiles))
        for f in removeFiles:
            filePath = os.path.join(constants.rpmPath, f)
            print("Removing {}".format(f))
            try:
                os.remove(filePath)
            except Exception as error:
                print(
                    "Error while removing file {0}: {1}".format(
                        filePath, error
                    )
                )


"""
class Buildenvironmentsetup does job like pulling toolchain RPMS and creating stage...
"""


class BuildEnvironmentSetup:

    global configdict
    global check_prerequesite

    def packages_cached():
        check_prerequesite["packages-cached"] = True

        if not configdict["additional-path"]["photon-cache-path"]:
            raise Exception("ERROR: photon-cache-path is empty")

        runBashCmd(
            f"rm -rf {Build_Config.rpmNoArchPath}/* {Build_Config.rpmArchPath}/*"
        )
        runBashCmd(
            "cp -rf "
            + configdict["additional-path"]["photon-cache-path"]
            + f"/RPMS/noarch/* {Build_Config.rpmNoArchPath}"
        )
        runBashCmd(
            "cp -rf "
            + configdict["additional-path"]["photon-cache-path"]
            + f"/RPMS/{constants.currentArch}/* {Build_Config.rpmArchPath}"
        )
        RpmBuildTarget.create_repo()

    def sources():
        if check_prerequesite["sources"]:
            return

        if not configdict["additional-path"]["photon-sources-path"]:
            check_prerequesite["sources"] = True
            if not os.path.isdir(constants.sourcePath):
                os.mkdir(constants.sourcePath)
        else:
            BuildEnvironmentSetup.sources_cached()

    def sources_cached():
        if check_prerequesite["sources-cached"]:
            return

        if not configdict["additional-path"]["photon-sources-path"]:
            raise Exception("ERROR: photon-sources-path is empty")

        print("Using cached SOURCES...")
        runBashCmd(
            "ln -sf "
            + configdict["additional-path"]["photon-sources-path"]
            + " "
            + constants.sourcePath
        )
        check_prerequesite["sources-cached"] = True

    def publish_rpms():
        if check_prerequesite["publish-rpms"]:
            return

        if not configdict["additional-path"]["photon-publish-rpms-path"]:
            print("Pulling toolchain RPMS...")
            cmd = f"cd {Build_Config.pullPublishRPMSDir} && {Build_Config.pullPublishRPMS}"
            cmd = f"{cmd} {constants.prevPublishRPMRepo} {constants.publishrpmurl} rpmfilelist"

            runBashCmd(cmd)
        else:
            BuildEnvironmentSetup.publish_rpms_cached()

        check_prerequesite["publish-rpms"] = True

    def publish_x_rpms():
        if check_prerequesite["publish-x-rpms"]:
            return

        if not configdict["additional-path"]["photon-publish-x-rpms-path"]:
            print("Pulling toolchain XRPMS...")
            cmd = f"cd {Build_Config.pullPublishRPMSDir} && {Build_Config.pullPublishRPMS}"
            cmd = f"{cmd} {constants.prevPublishXRPMRepo} {constants.publishXrpmurl} xrpmfilelist"

            runBashCmd(cmd)
        else:
            BuildEnvironmentSetup.publish_x_rpms_cached()

        check_prerequesite["publish-x-rpms"] = True

    def publish_rpms_cached():
        if check_prerequesite["publish-rpms-cached"]:
            return

        cmd = f"cd {Build_Config.pullPublishRPMSDir} &&"
        cmd = f"{cmd} {Build_Config.pullPublishRPMSCached} {constants.prevPublishRPMRepo} "
        cmd += (
            configdict["additional-path"]["photon-publish-rpms-path"]
            + " rpmfilelist"
        )
        runBashCmd(cmd)
        check_prerequesite["publish-rpms-cached"] = True

    def publish_x_rpms_cached():
        if check_prerequesite["publish-x-rpms-cached"]:
            return

        cmd = f"cd {Build_Config.pullPublishRPMSDir} &&"
        cmd = f"{cmd} {Build_Config.pullPublishRPMSCached} {constants.prevPublishXRPMRepo} "
        cmd += (
            configdict["additional-path"]["photon-publish-x-rpms-path"]
            + " xrpmfilelist"
        )
        runBashCmd(cmd)
        check_prerequesite["publish-x-rpms-cached"] = True

    def photon_stage():
        if check_prerequesite["photon-stage"]:
            return

        print("\nCreating staging folder and subitems...")

        stage_dirs = [
            Build_Config.stagePath,
            constants.buildRootPath,
            constants.rpmPath,
            Build_Config.rpmArchPath,
            Build_Config.rpmNoArchPath,
            constants.sourceRpmPath,
            Build_Config.updatedRpmNoArchPath,
            Build_Config.updatedRpmArchPath,
            constants.sourcePath,
            constants.logPath,
            constants.inputRPMSPath,
        ]

        runBashCmd(f"mkdir -p {' '.join(stage_dirs)}")

        files = ["COPYING", "NOTICE-GPL2.0", "NOTICE-Apachev2", "EULA.txt"]
        stagePath = Build_Config.stagePath
        for fn in files:
            if not os.path.isfile(f"{stagePath}/{fn}"):
                runBashCmd(f"install -m 444 {curDir}/{fn} {stagePath}")

        check_prerequesite["photon-stage"] = True


"""
class Cleanup does the job of cleaning up the stage directory...
"""


class CleanUp:
    def clean():
        CleanUp.clean_install()
        CleanUp.clean_chroot()
        print("Deleting Photon ISO...")
        runBashCmd(f"rm -f {Build_Config.stagePath}/photon-*.iso")
        print("Deleting stage dir...")
        runBashCmd(f"rm -rf {Build_Config.stagePath}")
        print("Deleting chroot path...")
        runBashCmd(f"rm -rf {constants.buildRootPath}")
        print("Deleting tools/bin...")
        runBashCmd("rm -rf tools/bin")

    def clean_install():
        print("Cleaning installer working directory...")
        if os.path.isdir(os.path.join(Build_Config.stagePath, "photon_iso")):
            cmd = f"{photonDir}/support/package-builder/clean-up-chroot.py {Build_Config.stagePath}/photon_iso"
            runBashCmd(cmd)

    def clean_chroot():
        print("Cleaning chroot path...")
        if os.path.isdir(constants.buildRootPath):
            cmd = f"{photonDir}/support/package-builder/clean-up-chroot.py {constants.buildRootPath}"
            runBashCmd(cmd)

    def removeUpwardDeps(pkg, display_option):
        specDeps = SpecDependencyGenerator(
            constants.logPath, constants.logLevel
        )
        isToolChainPkg = specDeps.process(
            "is-toolchain-pkg", pkg, display_option
        )
        if isToolChainPkg:
            specDeps.logger.info(
                "Removing all staged RPMs since toolchain packages were modified"
            )
            runBashCmd(f"rm -rf {constants.rpmPath}")
        else:
            whoNeedsList = specDeps.process(
                "get-upward-deps", pkg, display_option
            )
            specDeps.logger.info(
                "Removing upward dependencies: " + str(whoNeedsList)
            )
            for pkg in whoNeedsList:
                package, version = StringUtils.splitPackageNameAndVersion(pkg)
                for p in SPECS.getData().getPackages(package, version):
                    buildarch = SPECS.getData().getBuildArch(p, version)
                    rpmFile = os.path.join(
                        constants.rpmPath,
                        buildarch,
                        f"{p}-{version}*{buildarch}.rpm",
                    )
                    runBashCmd(f"rm -f {rpmFile}")

    def clean_stage_for_incremental_build():
        rpm_path = constants.rpmPath

        basecommit = ""
        if "base-commit" in configdict["photon-build-param"]:
            basecommit = str(configdict["photon-build-param"].get("base-commit"))

        if basecommit:
            cmd = f"git -C {ph_path} diff --name-only {basecommit}"
        else:
            cmd = f"git -C {ph_path} diff --name-only @~1 @"

        out, _, _ = runBashCmd(cmd, capture=True)
        if ("support/package-builder" in out) or ("support/pullpublishrpms" in out):
            print("Remove all staged RPMs")
            runBashCmd(f"rm -rf {rpm_path}")

        if not os.path.exists(rpm_path):
            print(f"{rpm_path} is empty, return ...")
            return

        if not basecommit:
            return

        cmd = (
            f"echo $(git -C {ph_path} diff --name-only {basecommit} | grep '.spec$' | "
            "xargs -n1 basename 2>/dev/null) | tr ' ' :"
        )

        spec_fns, _, _ = runBashCmd(cmd, capture=True)
        if not spec_fns:
            print("No spec files were changed in this incremental build")
            return

        try:
            spec_fns = spec_fns.strip("\n")
            CleanUp.removeUpwardDeps(spec_fns, "tree")
        except Exception as error:
            print(f"Error in clean_stage_for_incremental_build: {error}")


"""
class Rpmbuildtarget does the job of building all the RPMs for the SPECS
It uses Builder class in builder.py in order to build packages.
"""


class RpmBuildTarget:
    global configdict
    global check_prerequesite

    def __init__(self):
        self.logger = Logger.getLogger(
            "Main", constants.logPath, constants.logLevel
        )

        BuildEnvironmentSetup.photon_stage()

        if (
            configdict["additional-path"]["photon-publish-x-rpms-path"]
            is not None
        ):
            BuildEnvironmentSetup.publish_x_rpms_cached()
        else:
            BuildEnvironmentSetup.publish_x_rpms()

        if (
            configdict["additional-path"]["photon-publish-rpms-path"]
            is not None
        ):
            BuildEnvironmentSetup.publish_rpms_cached()
        else:
            BuildEnvironmentSetup.publish_rpms()

        if configdict["additional-path"]["photon-sources-path"] is not None:
            BuildEnvironmentSetup.sources_cached()
        else:
            BuildEnvironmentSetup.sources()

        CheckTools.check_spec_files()

        runBashCmd("./tools/scripts/generate-specs-from-templates.sh")

        Utilities(None).generate_dep_lists()

        if constants.buildArch != constants.targetArch:
            runBashCmd(f"mkdir -p {constants.rpmPath}/{constants.targetArch}")

        self.logger.debug(f"Source Path : {constants.sourcePath}")
        self.logger.debug(f"Spec Path : {constants.specPath}")
        self.logger.debug(f"Rpm Path : {constants.rpmPath}")
        self.logger.debug(f"Log Path : {constants.logPath}")
        self.logger.debug(f"Log Level : {constants.logLevel}")
        self.logger.debug(f"Top Dir Path : {constants.topDirPath}")
        self.logger.debug(
            f"Publish RPMS Path : {constants.prevPublishRPMRepo}"
        )
        self.logger.debug(
            f"Publish X RPMS Path : {constants.prevPublishXRPMRepo}"
        )

        Builder.get_packages_with_build_options(
            configdict["photon-build-param"]["pkg-build-options"]
        )

        if constants.buildArch != constants.targetArch:
            # It is cross compilation
            # first build all native packages
            Builder.buildPackagesForAllSpecs(
                Build_Config.buildThreads,
                Build_Config.pkgBuildType,
                Build_Config.pkgInfoFile,
                self.logger,
            )

            # Then do the build to the target
            constants.currentArch = constants.targetArch
            constants.crossCompiling = True

    @staticmethod
    def create_repo():
        if check_prerequesite["create-repo"]:
            return

        createrepo_cmd = configdict["createrepo-cmd"]
        runBashCmd(f"{createrepo_cmd} --general-compress-type=gz --update {constants.rpmPath}")
        check_prerequesite["create-repo"] = True

    @staticmethod
    def ostree_repo():
        if check_prerequesite["ostree-repo"]:
            return

        ph_docker_img = configdict["photon-build-param"]["photon-docker-image"]
        if not os.path.isfile(
            os.path.join(Build_Config.stagePath, "ostree-repo.tar.gz")
        ):
            print(
                "Creating OSTree repo from local RPMs in ostree-repo.tar.gz..."
            )
            RpmBuildTarget.create_repo()
            cmd = (
                f"{photonDir}/support/image-builder/ostree-tools/make-ostree-image.sh"
                f" {photonDir} {Build_Config.stagePath} {constants.releaseVersion} {ph_docker_img}"
            )
            runBashCmd(cmd)
        else:
            print("OSTree repo already exists...")

        check_prerequesite["ostree-repo"] = True

    def packages(self):
        if check_prerequesite["packages"]:
            return

        if not configdict["additional-path"]["photon-cache-path"]:
            Builder.buildPackagesForAllSpecs(
                Build_Config.buildThreads,
                Build_Config.pkgBuildType,
                Build_Config.pkgInfoFile,
                self.logger,
            )
            RpmBuildTarget.create_repo()
        else:
            BuildEnvironmentSetup.packages_cached()
        check_prerequesite["packages"] = True

    def package(self, pkgName):
        self.logger.debug(f"Package to build: {pkgName}")
        if pkgName in constants.extraPackagesList:
            constants.extraPackagesList.remove(pkgName)
        Builder.buildSpecifiedPackages(
            [pkgName], Build_Config.buildThreads, Build_Config.pkgBuildType
        )

    def packages_minimal(self):
        if check_prerequesite["packages-minimal"]:
            return

        if not configdict["additional-path"]["photon-cache-path"]:
            Builder.buildPackagesInJson(
                os.path.join(Build_Config.dataDir, "packages_minimal.json"),
                Build_Config.buildThreads,
                Build_Config.pkgBuildType,
                Build_Config.pkgInfoFile,
                self.logger,
            )
        else:
            BuildEnvironmentSetup.packages_cached()
        check_prerequesite["packages-minimal"] = True

    def packages_basic(self):
        if check_prerequesite["packages-basic"]:
            return

        if not configdict["additional-path"]["photon-cache-path"]:
            Builder.buildPackagesInJson(
                os.path.join(
                    Build_Config.dataDir, "packages_basic.json"
                ),
                Build_Config.buildThreads,
                Build_Config.pkgBuildType,
                Build_Config.pkgInfoFile,
                self.logger,
            )
        else:
            BuildEnvironmentSetup.packages_cached()
        check_prerequesite["packages-basic"] = True

    def packages_rt(self):
        if check_prerequesite["packages-rt"]:
            return

        if not configdict["additional-path"]["photon-cache-path"]:
            Builder.buildPackagesInJson(
                os.path.join(Build_Config.dataDir, "packages_rt.json"),
                Build_Config.buildThreads,
                Build_Config.pkgBuildType,
                Build_Config.pkgInfoFile,
                self.logger,
            )
        else:
            BuildEnvironmentSetup.packages_cached()
        check_prerequesite["packages-rt"] = True

    def packages_initrd(self):
        if check_prerequesite["packages-initrd"]:
            return

        Builder.buildPackagesInJson(
            os.path.join(
                Build_Config.dataDir, "packages_installer_initrd.json"
            ),
            Build_Config.buildThreads,
            Build_Config.pkgBuildType,
            Build_Config.pkgInfoFile,
            self.logger,
        )
        check_prerequesite["packages-initrd"] = True

    def packages_docker(self):
        if check_prerequesite["packages-docker"]:
            return

        Builder.buildPackagesForAllSpecs(
            Build_Config.buildThreads,
            Build_Config.pkgBuildType,
            Build_Config.pkgInfoFile,
            self.logger,
        )
        check_prerequesite["packages-docker"] = True

    def updated_packages(self):
        if check_prerequesite["updated-packages"]:
            return

        constants.setRpmPath(Build_Config.updatedRpmPath)
        Builder.buildPackagesForAllSpecs(
            Build_Config.buildThreads,
            Build_Config.pkgBuildType,
            Build_Config.pkgInfoFile,
            self.logger,
        )
        check_prerequesite["updated-packages"] = True

    def check_packages(self):
        if check_prerequesite["check-packages"]:
            return

        constants.setRPMCheck(True)
        constants.setRpmCheckStopOnError(True)
        Builder.buildPackagesForAllSpecs(
            Build_Config.buildThreads,
            Build_Config.pkgBuildType,
            Build_Config.pkgInfoFile,
            self.logger,
        )
        check_prerequesite["check-packages"] = True

    def extra_packages(self):
        if check_prerequesite["extra-packages"]:
            return

        Builder.buildSpecifiedPackages(
            constants.extraPackagesList,
            Build_Config.buildThreads,
            Build_Config.pkgBuildType,
            Build_Config.pkgInfoFile,
            self.logger,
            build_extra_pkgs=True,
        )

        check_prerequesite["extra-packages"] = True

    def distributed_build():
        # TODO: should be moved to top
        import DistributedBuilder

        print("Distributed Building using kubernetes ...")
        with open(Build_Config.distributedBuildFile, "r") as configFile:
            distributedBuildConfig = json.load(configFile)

        DistributedBuilder.main(distributedBuildConfig)

    def tool_chain_stage1(self):
        if check_prerequesite["tool-chain-stage1"]:
            return

        pkgManager = PackageManager()
        pkgManager.buildToolChain()
        check_prerequesite["tool-chain-stage1"] = True

    def tool_chain_stage2(self):
        if check_prerequesite["tool-chain-stage2"]:
            return

        pkgManager = PackageManager()
        pkgManager.buildToolChainPackages(Build_Config.buildThreads)
        check_prerequesite["tool-chain-stage2"] = True

    def generate_yaml_files(self):
        if check_prerequesite["generate-yaml-files"]:
            return

        print("Generating yaml files for packages...")
        BuildEnvironmentSetup.photon_stage()

        RpmBuildTarget().packages()
        if configdict["photon-build-param"].get("generate-pkg-list", ""):
            GenerateOSSFiles.buildPackagesList(
                os.path.join(Build_Config.stagePath, "packages_list.csv")
            )
        else:
            blackListPkgs = GenerateOSSFiles.readBlackListPackages(
                configdict.get("additional-path", {}).get(
                    "pkg-black-list-file", ""
                )
            )
            logger = Logger.getLogger(
                "GenerateYamlFiles", constants.logPath, constants.logLevel
            )
            GenerateOSSFiles.buildSourcesList(
                Build_Config.stagePath, blackListPkgs, logger
            )

            GenerateOSSFiles.buildSRPMList(
                constants.sourceRpmPath,
                Build_Config.stagePath,
                blackListPkgs,
                constants.dist,
                logger,
            )
        check_prerequesite["generate-yaml-files"] = True


"""
class CheckTools does the job of checking weather all the tools required for
starting build process are present on the system
"""


class CheckTools:
    global configdict
    global check_prerequesite

    def check_pre_reqs():
        if check_prerequesite["check-pre-reqs"]:
            return

        CheckTools.check_all_tools()
        CheckTools.check_sanity()
        CheckTools.check_docker()
        CheckTools.create_ph_builder_img()
        CheckTools.check_contain()
        CheckTools.check_git_hooks()
        check_prerequesite["check-pre-reqs"] = True

    def create_ph_builder_img():
        ph_docker_img = configdict["photon-build-param"]["photon-docker-image"]
        ph_docker_img_url = configdict["photon-build-param"][
            "ph-docker-img-url"
        ]
        ph_builder_tag = configdict["photon-build-param"]["ph-builder-tag"]

        ph_docker_img_url = ph_docker_img_url.replace(
            "ARCH", constants.currentArch
        )

        cmd = (
            f"{photonDir}/tools/scripts/ph-docker-img-import.sh {ph_docker_img_url}"
            f" {ph_docker_img} {ph_builder_tag}"
        )
        runBashCmd(cmd)

    def check_git_hooks():
        if not os.path.exists(f"{photonDir}/.git"):
            print("Not building Photon from a git repo, return ...")
            return

        git_hooks_path = f"{photonDir}/.git/hooks"
        hook_scripts_path = f"{photonDir}/tools/scripts"

        for fn in {"commit-msg", "pre-push"}:
            if not os.path.exists(f"{git_hooks_path}/{fn}"):
                print(f"{hook_scripts_path}/{fn} doesn't exist, create ...")
                runBashCmd(
                    f"ln -srv {hook_scripts_path}/{fn} {git_hooks_path}/{fn}"
                )

    def check_contain():
        if not os.path.exists(f"{photonDir}/tools/bin/contain_unpriv"):
            runBashCmd(f"bash {photonDir}/tools/src/contain/make.sh")

    def check_all_tools():
        tools = ["bison", "g++", "gawk", "makeinfo", "kpartx"]
        for tool in tools:
            if not shutil.which(tool):
                raise Exception(f"{tool} not present")

        runBashCmd("pip3 show pyOpenSSL &>/dev/null")

        createrepo_cmd = ""
        for tool in {"createrepo", "createrepo_c"}:
            createrepo_cmd = shutil.which(tool)
            if createrepo_cmd:
                break

        if not createrepo_cmd:
            raise Exception("createrepo not found")

        configdict["createrepo-cmd"] = createrepo_cmd

    def check_sanity():
        script = f"{photonDir}/tools/scripts/sanity_check.sh"
        runBashCmd(script)

    def check_docker():
        if not glob.glob(Build_Config.dockerEnv) and not shutil.which(
            "docker"
        ):
            raise Exception("docker not present")

        runBashCmd("systemctl start docker")

        if not glob.glob(Build_Config.dockerEnv):
            runBashCmd("docker ps &>/dev/null")

        docker_py_ver = "2.3.0"
        if (
            not glob.glob(Build_Config.dockerEnv)
            and docker.__version__ < docker_py_ver
        ):
            print(
                f"\nError: Python3 package docker-{docker_py_ver} not installed."
            )
            print(f"Please use: pip3 install docker=={docker_py_ver}\n")
            raise Exception()

    def check_spec_files():
        if check_prerequesite["check-spec-files"]:
            return

        script_fn = f"{photonDir}/tools/scripts/get_modified_files.sh"
        cmd = f"{script_fn} {configdict['photon-path']} && {script_fn} {configdict['release-branch-path']}"

        if "base-commit" in configdict["photon-build-param"]:
            commit_id = str(
                configdict["photon-build-param"].get("base-commit")
            )
            if commit_id:
                cmd = f"git -C {ph_path} diff --name-only {commit_id}"

        files, _, _ = runBashCmd(cmd, capture=True)
        files = files.splitlines()

        if check_specs(files):
            raise Exception("Spec file check failed")

        check_prerequesite["check-spec-files"] = True


"""
class BuildImage does the job of building all the images like iso, rpi, ami, gce, azure, ova and ls1012afrwy
It uses class ImageBuilder to build different images.
"""


class BuildImage:

    global configdict
    global check_prerequesite

    def __init__(self, imgName):
        self.src_root = configdict["photon-path"]
        self.generated_data_path = Build_Config.dataDir
        self.stage_path = Build_Config.stagePath
        self.log_path = constants.logPath
        self.log_level = constants.logLevel

        self.config_file = None
        if configdict["additional-path"]["conf-file"] is not None:
            self.config_file = os.path.abspath(configdict["additional-path"]["conf-file"])

        self.img_name = imgName
        self.rpm_path = constants.rpmPath
        self.srpm_path = constants.sourceRpmPath
        self.pkg_to_rpm_map_file = os.path.join(
            Build_Config.stagePath, "pkg_info.json"
        )
        self.ph_docker_image = configdict["photon-build-param"][
            "photon-docker-image"
        ]
        self.ph_builder_tag = configdict["photon-build-param"][
            "ph-builder-tag"
        ]
        self.poi_image = configdict["photon-build-param"].get("poi-image", None)

        self.ova_cloud_images = ["ami", "gce", "azure", "ova"]
        self.photon_release_version = constants.releaseVersion

    def set_Iso_Parameters(self, imgName):
        self.generated_data_path = f"{Build_Config.stagePath}/common/data"
        self.src_iso_path = None
        imgType = "photon"

        if imgName in ["minimal-iso", "rt-iso", "basic-iso"]:
            flavor = imgName.strip("-iso").replace("-", "_")
            imgType = f"photon-{flavor}"
            self.package_list_file = (
                f"{Build_Config.dataDir}/build_install_options_{flavor}.json"
            )
            self.pkg_to_be_copied_conf_file = f"{Build_Config.generatedDataPath}/build_install_options_{flavor}.json"
        else:
            self.pkg_to_be_copied_conf_file = (
                Build_Config.pkgToBeCopiedConfFile
            )
            self.package_list_file = Build_Config.packageListFile

        self.iso_path = (
            f"{Build_Config.stagePath}/{imgType}-"
            f"{constants.releaseVersion}-"
            f"{constants.buildNumber}.{constants.currentArch}.iso"
        )
        self.debug_iso_path = self.iso_path.rpartition(".")[0] + ".debug.iso"

        if "SKIP_DEBUG_ISO" in os.environ:
            self.debug_iso_path = None

        if imgName == "src-iso":
            self.src_iso_path = self.iso_path.rpartition(".")[0] + ".src.iso"
            self.iso_path = None
            self.debug_iso_path = None

    def img_present(self, img):
        if os.environ.get("FORCE_IMG_BUILD", 0):
            return False

        build_num = constants.buildNumber
        release_ver = constants.releaseVersion
        img_fn = (
            f"{Build_Config.stagePath}/{img}/photon-{img}-{release_ver}-"
            f"{build_num}.{constants.currentArch}"
        )

        if img == "ova":
            img_fn = f"{img_fn}.ova"
        elif img in {"ami", "gce"}:
            img_fn = f"{img_fn}.tar.gz"
        elif img == "azure":
            img_fn = f"{img_fn}.vhd.tar.gz"
        elif img in {
            "iso",
            "rt-iso",
            "src-iso",
            "minimal-iso",
            "basic-iso",
        }:
            img = img.strip("-iso")
            if img:
                img = f"-{img}"
            img_fn = (
                f"{Build_Config.stagePath}/photon{img}-{release_ver}-"
                f"{build_num}.{constants.currentArch}.iso"
            )
        elif img in {"rpi", "ls1012afrwy"}:
            img_fn = f"{img_fn}.xz"
        else:
            raise Exception(f"Invalid image format {img}")

        retval = os.path.exists(img_fn)
        if retval:
            print(f"{img_fn} already exists ...")

        return retval

    def run_poi(self):
        args = []
        if self.config_file is not None:
            args.append(f"--config={self.config_file}")
        if self.poi_image is not None:
            args.append(f"--docker-image={self.poi_image}")
        args.append(f"--stage-dir={Build_Config.stagePath}")
        args = " ".join(args)
        cmd = f"cd {photonDir}/support/poi && ./poi.py {args} {self.img_name} "
        print(f"running {cmd}")
        runBashCmd(cmd)

    def build_iso(self):
        if self.img_present(self.img_name):
            return

        rpmBuildTarget = RpmBuildTarget()
        BuildEnvironmentSetup.photon_stage()
        if self.img_name == "iso":
            rpmBuildTarget.packages()
        elif self.img_name == "rt-iso":
            rpmBuildTarget.packages_rt()
        elif self.img_name == "basic-iso":
            rpmBuildTarget.packages_basic()
        else:
            rpmBuildTarget.packages_minimal()

        if self.img_name in ["rt-iso", "minimal-iso", "basic-iso"]:
            rpmBuildTarget.packages_initrd()

        RpmBuildTarget.create_repo()

        if self.img_name not in ["minimal-iso", "basic-iso"]:
            RpmBuildTarget.ostree_repo()
        self.generated_data_path = Build_Config.generatedDataPath

        print("Building Full ISO...")
        self.run_poi()
        # poi puts the image into stage/iso/, build expects it in stage/
        for iso in glob.glob(os.path.join(Build_Config.stagePath, "iso", "*.iso")):
            shutil.move(iso, Build_Config.stagePath)

    def build_image(self):
        if self.img_present(self.img_name):
            return

        BuildEnvironmentSetup.photon_stage()

        local_build = not configdict["photon-build-param"][
            "start-scheduler-server"
        ]

        if local_build:
            RpmBuildTarget.ostree_repo()

        print(f"Building {self.img_name} image")
        self.run_poi()

    @staticmethod
    def photon_docker_image():
        if check_prerequesite["photon-docker-image"]:
            return

        img_fname = f"photon-rootfs-{constants.releaseVersion}-{constants.buildNumber}.{constants.currentArch}.tar.gz"
        if os.path.isfile(os.path.join(Build_Config.stagePath, img_fname)):
            check_prerequesite["photon-docker-image"] = True
            print(f"{img_fname} already exists ...")
            return

        RpmBuildTarget.create_repo()

        docker_file_dir = "support/dockerfiles/photon"
        docker_script = f"{docker_file_dir}/make-docker-image.sh"

        cmd = (
            f"cd {photonDir} && DOCKER_BUILDKIT=0 "
            f" docker build --ulimit nofile=1024:1024 --no-cache --tag "
            f" photon-build {docker_file_dir} && "
            f" docker run --ulimit nofile=1024:1024 --rm --privileged --net=host"
            f" -e PHOTON_BUILD_NUMBER={constants.buildNumber}"
            f" -e PHOTON_RELEASE_VERSION={constants.releaseVersion}"
            f" -v {Build_Config.stagePath}:/photon/stage"
            f" -v {photonDir}:/workspace photon-build {docker_script}"
        )

        runBashCmd(cmd)
        check_prerequesite["photon-docker-image"] = True

    def k8s_docker_images(self):
        if glob.glob(f"{Build_Config.stagePath}/docker_images/*.gz"):
            print(
                f"k8s images are already present in {Build_Config.stagePath}/docker_images"
            )
            return

        BuildImage.photon_docker_image()

        if not os.path.isdir(
            os.path.join(Build_Config.stagePath, "docker_images")
        ):
            os.mkdir(os.path.join(Build_Config.stagePath, "docker_images"))

        os.chdir(f"{photonDir}/support/dockerfiles/k8s-docker-images")

        ph_dist_tag = configdict["photon-build-param"]["photon-dist-tag"]
        ph_builder_tag = configdict["photon-build-param"]["ph-builder-tag"]

        k8s_build_scripts = [
            "build-k8s-docker-images.sh",
            "build-k8s-metrics-server-image.sh",
            "build-k8s-coredns-image.sh",
            "build-k8s-dns-docker-images.sh",
            "build-k8s-dashboard-docker-images.sh",
            "build-flannel-docker-image.sh",
            "build-calico-docker-images.sh",
            "build-k8s-heapster-image.sh",
            "build-k8s-nginx-ingress.sh",
            "build-wavefront-proxy-docker-image.sh",
        ]

        script = "build-k8s-base-image.sh"
        cmd = f"./{script} {constants.releaseVersion} {constants.buildNumber}"
        cmd = f"{cmd} {Build_Config.stagePath}"
        runBashCmd(cmd)

        for script in k8s_build_scripts:
            cmd = f"./{script} {ph_dist_tag} {constants.releaseVersion}"
            cmd = f"{cmd} {constants.specPath} {Build_Config.stagePath}"
            cmd = f"{cmd} {ph_builder_tag}"
            runBashCmd(cmd)

        print("Successfully built all the k8s docker images")
        os.chdir(photonDir)

    def all_images(self):
        for img in self.ova_cloud_images:
            self.img_name = img
            self.build_image()

    def all(self):
        images = [
            "iso",
            "photon-docker-image",
            "k8s-docker-images",
            "all-images",
            "src-iso",
            "minimal-iso",
            "basic-iso",
        ]
        for img in images:
            self.img_name = img
            if img in ["iso", "src-iso", "minimal-iso", "basic-iso"]:
                self.set_Iso_Parameters(img)
                self.build_iso()
            else:
                configdict["targetName"] = img.replace("-", "_")
                getattr(self, configdict["targetName"])()


"""
initialize_constants initialize all the paths like stage Path, spec path, rpm path, and other parameters
used by package-builder and imagebuilder...
"""


def initialize_constants():
    global configdict
    global check_prerequesite

    if check_prerequesite["initialize-constants"]:
        return

    Build_Config.setStagePath(
        os.path.join(
            str(
                Path(
                    configdict["release-branch-path"], configdict.get("stage-path", "")
                ).resolve()
            )
        )
    )
    constants.setSpecPath(
        os.path.join(
            str(
                PurePath(
                    configdict["photon-path"], configdict.get("spec-path", "")
                )
            ),
            "SPECS",
        )
    )
    Build_Config.setBuildThreads(configdict["photon-build-param"]["threads"])
    Build_Config.setPkgBuildType(
        configdict["photon-build-param"]["photon-build-type"]
    )
    Build_Config.setPkgJsonInput(
        configdict.get("additional-path", {}).get("pkg-json-input", None)
    )
    constants.setLogPath(os.path.join(Build_Config.stagePath, "LOGS"))
    constants.setLogLevel(configdict["photon-build-param"]["loglevel"])
    constants.setDist(configdict["photon-build-param"]["photon-dist-tag"])
    constants.setBuildNumber(
        configdict["photon-build-param"]["input-photon-build-number"]
    )
    constants.setReleaseVersion(
        configdict["photon-build-param"]["photon-release-version"]
    )

    src_url = configdict["photon-build-param"].get("pull-sources-config", "")
    if not src_url:
        raise Exception("pull-sources-config is empty")

    if not url_validator(src_url) and os.path.exists(src_url):
        # TODO: can be removed in future
        constants.setPullSourcesURL(Builder.get_baseurl(src_url))
    else:
        if not url_validator(src_url):
            raise Exception(f"Invalid pull-sources-config url {src_url}")
        constants.setPullSourcesURL(src_url)

    src_url = configdict["photon-build-param"].get("publishrpm-url", "")
    if not url_validator(src_url):
        raise Exception(f"publishrpm-url is invalid {src_url}")
    constants.setPublishRpmURL(src_url)

    src_url = configdict["photon-build-param"].get("publishXrpm-url", "")
    if not url_validator(src_url):
        raise Exception(f"publishXrpm-url is invalid {src_url}")
    constants.setPublishXRpmURL(src_url)

    constants.setRPMCheck(
        configdict["photon-build-param"].get("rpm-check-flag", False)
    )
    constants.setRpmCheckStopOnError(
        configdict["photon-build-param"].get("rpm-check-stop-on-error", False)
    )
    constants.setPublishBuildDependencies(
        configdict["photon-build-param"].get(
            "publish-build-dependencies", False
        )
    )
    constants.setRpmPath(os.path.join(Build_Config.stagePath, "RPMS"))
    Build_Config.setRpmNoArchPath()
    Build_Config.setRpmArchPath()
    constants.setSourceRpmPath(os.path.join(Build_Config.stagePath, "SRPMS"))
    Build_Config.setUpdatedRpmPath(
        os.path.join(Build_Config.stagePath, "UPDATED_RPMS")
    )
    constants.setSourcePath(os.path.join(Build_Config.stagePath, "SOURCES"))
    constants.setPrevPublishRPMRepo(
        os.path.join(Build_Config.stagePath, "PUBLISHRPMS")
    )
    constants.setPrevPublishXRPMRepo(
        os.path.join(Build_Config.stagePath, "PUBLISHXRPMS")
    )
    Build_Config.setPkgInfoFile(
        os.path.join(Build_Config.stagePath, "pkg_info.json")
    )
    constants.setBuildRootPath(
        os.path.join(Build_Config.stagePath, "photonroot")
    )
    Build_Config.setGeneratedDataDir(
        os.path.join(Build_Config.stagePath, "common/data")
    )
    constants.setTopDirPath("/usr/src/photon")
    Build_Config.setCommonDir(os.path.join(photonDir, "common"))
    Build_Config.setDataDir(os.path.join(photonDir, "common/data"))
    constants.setInputRPMSPath(
        os.path.abspath(
            configdict.get(
                "input-rpms-path", os.path.join(photonDir, "inputRPMS")
            )
        )
    )
    Build_Config.setPullPublishRPMSDir(
        os.path.join(photonDir, "support/pullpublishrpms")
    )
    Build_Config.setPullPublishRPMS(
        os.path.join(Build_Config.pullPublishRPMSDir, "pullpublishrpms.sh")
    )
    Build_Config.setPullPublishRPMSCached(
        os.path.join(
            Build_Config.pullPublishRPMSDir, "pullpublishrpms-cached.sh"
        )
    )
    constants.setPackageWeightsPath(
        os.path.join(Build_Config.dataDir, "packageWeights.json")
    )
    constants.setKatBuild(
        configdict["photon-build-param"].get("kat-build", False)
    )
    constants.setCanisterBuild(
        configdict["photon-build-param"].get("canister-build", False)
    )
    constants.setAcvpBuild(
        configdict["photon-build-param"].get("acvp-build", False)
    )
    Build_Config.setConfFile(configdict["additional-path"]["conf-file"])
    Build_Config.setPkgToBeCopiedConfFile(
        configdict.get("additional-path", {}).get("pkg-to-be-copied-conf-file")
    )
    Build_Config.setDistributedBuildFile(
        os.path.join(Build_Config.dataDir, "distributed_build_options.json")
    )
    Builder.get_packages_with_build_options(
        configdict["photon-build-param"]["pkg-build-options"]
    )
    Build_Config.setCommonDir(PurePath(photonDir, "common", "data"))
    constants.setStartSchedulerServer(
        configdict["photon-build-param"]["start-scheduler-server"]
    )
    constants.setCompressionMacro(
        configdict["photon-build-param"]["compression-macro"]
    )

    constants.setPhotonDir(photonDir)

    constants.phBuilderTag = configdict["photon-build-param"]["ph-builder-tag"]

    constants.buildSrcRpm = int(
        configdict["photon-build-param"]["build-src-rpm"]
    )
    constants.buildDbgInfoRpm = int(
        configdict["photon-build-param"]["build-dbginfo-rpm"]
    )
    constants.buildDbgInfoRpmList = configdict["photon-build-param"][
        "build-dbginfo-rpm-list"
    ]

    if configdict.get("photon-build-param", {}).get(
        "ossl-fips-in-make-check", False
    ):
        constants.enable_fips_in_make_check()

    constants.extraPackagesList = configdict["photon-build-param"][
        "extra-packages-list"
    ]

    if configdict.get("photon-build-param", {}).get("resume-build", False):
        constants.set_resume_build(
            bool(configdict["photon-build-param"]["resume-build"])
        )

    constants.initialize()

    check_prerequesite["initialize-constants"] = True

def create_new_symlink(dir_path):
    global configdict

    ph_branch = dir_path
    specs_dir = "SPECS"
    release_version = configdict["photon-build-param"][
        "photon-release-version"
    ]
    for link in os.listdir(specs_dir):
        if os.path.islink(os.path.join(specs_dir, link)):
                os.unlink(os.path.join(specs_dir, link))

    # Create new symbolic link: SPECS/ph_branch -> ../ph_branch/SPECS
    new_link_target = os.path.join("..", ph_branch, specs_dir)
    new_link_path = os.path.join(specs_dir, (f'{release_version}-SPECS'))
    os.symlink(new_link_target, new_link_path)

def set_default_value_of_config():
    global configdict

    key = "additional-path"
    cfgs = [
        "photon-sources-path",
        "photon-cache-path",
        "conf-file",
        "photon-publish-rpms-path",
        "photon-publish-x-rpms-path",
    ]

    for cfg in cfgs:
        configdict.setdefault(key, {}).setdefault(cfg, None)

    key = "photon-build-param"
    out, _, _ = runBashCmd("git rev-parse --short HEAD", capture=True)
    configdict[key]["input-photon-build-number"] = out.rstrip()

    ret = f"{curDir}/common/data/" + configdict[key]["pkg-build-options"]
    configdict[key]["pkg-build-options"] = ret
    configdict.setdefault(key, {}).setdefault("start-scheduler-server", False)
    configdict.setdefault(key, {}).setdefault("base-commit", "")


def process_env_build_params(ph_build_param):
    env_build_param_dict = {
        "INPUT_PHOTON_BUILD_NUMBER": "input-photon-build-number",
        "BASE_COMMIT": "base-commit",
        "THREADS": "threads",
        "LOGLEVEL": "loglevel",
        "PHOTON_PULLSOURCES_CONFIG": "pull-sources-config",
        "PKG_BUILD_OPTIONS": "pkg-build-options",
        "CROSS_TARGET": "tarsetdefaultArch",
        "PHOTON_DOCKER_IMAGE": "photon-docker-image",
        "KAT_BUILD": "kat-build",
        "CANISTER_BUILD": "canister-build",
        "ACVP_BUILD": "acvp-build",
        "BUILDDEPS": "publish-build-dependencies",
        "PH_DOCKER_IMAGE_URL": "ph-docker-img-url",
        "BUILD_SRC_RPM": "build-src-rpm",
        "BUILD_DBGINFO_RPM": "build-dbginfo-rpm",
        "RPMCHECK": "rpm-check-flag",
        "SCHEDULER_SERVER": "start-scheduler-server",
        "BUILD_EXTRA_PKGS": "build-extra-pkgs",
        "RESUME_BUILD": "resume-build",
        "POI_IMAGE": "poi-image",
    }

    os.environ["PHOTON_RELEASE_VER"] = ph_build_param["photon-release-version"]
    os.environ["PHOTON_BUILD_NUM"] = ph_build_param[
        "input-photon-build-number"
    ]

    for k, v in env_build_param_dict.items():
        if k not in os.environ:
            continue

        val = os.environ[k]
        if not val:
            continue

        if k == "THREADS":
            val = int(val)
        elif k in {
            "BUILD_SRC_RPM",
            "BUILD_DBGINFO_RPM",
            "KAT_BUILD",
            "BUILDDEPS",
            "SCHEDULER_SERVER",
            "CANISTER_BUILD",
            "ACVP_BUILD",
            "BUILD_EXTRA_PKGS",
            "RESUME_BUILD",
        }:
            val = cmdUtils.strtobool(val)
        elif k == "RPMCHECK":
            if val == "enable_stop_on_error" or cmdUtils.strtobool(val):
                ph_build_param[v] = True
                if val == "enable_stop_on_error":
                    ph_build_param["rpm-check-stop-on-error"] = True
                    continue

        ph_build_param[v] = val


def process_additional_cfgs(cfgdict_additional_path):
    env_additional_cfg_map = {
        "PHOTON_CACHE_PATH": "photon-cache-path",
        "PHOTON_SOURCES_PATH": "photon-sources-path",
        "PHOTON_PUBLISH_RPMS_PATH": "photon-publish-rpms-path",
        "PHOTON_PUBLISH_XRPMS_PATH": "photon-publish-x-rpms-path",
        "PHOTON_PKG_BLACKLIST_FILE": "pkg-black-list-file",
        "DISTRIBUTED_BUILD_CONFIG": "distributed-build-option-file",
    }

    for k, v in env_additional_cfg_map.items():
        if k in os.environ:
            val = os.environ[k]
            if val:
                cfgdict_additional_path[v] = os.environ[k]

def merge_dicts(dict1, dict2):
    """
    Merge two dictionaries with dict2 taking precedence over dict1.
    """
    merged_dict = dict1.copy()
    for key, value in dict2.items():
        if isinstance(value, dict) and key in merged_dict and isinstance(merged_dict[key], dict):
            merged_dict[key] = merge_dicts(merged_dict[key], value)
        elif key in merged_dict:
            raise Exception("ERROR: " + key + " is present in both configs.\nIt can only be present in one.")
        else:
            merged_dict[key] = value
    return merged_dict

def main():

    parser = ArgumentParser()
    parser.add_argument("-b", "--branch", dest="photonBranch", default=None)
    parser.add_argument("-c", "--config", dest="configPath", default=None)
    parser.add_argument("-t", "--target", dest="targetName", default=None)
    parser.add_argument("args", nargs="*")

    options = parser.parse_args()

    branch = options.photonBranch
    cfgPath = options.configPath
    targetName = options.targetName

    build_cfg = "build-config.json"

    if (
        not branch
        and not cfgPath
        and not os.path.isfile(os.path.join(curDir, build_cfg))
    ):
        raise Exception("Either specify branchName or configpath...")

    if branch is not None and not os.path.isdir(f"{curDir}/photon-{branch}"):
        runBashCmd(
            f"git clone https://github.com/vmware/photon.git -b {branch} photon-{branch}"
        )
    elif branch is not None:
        print("Using already cloned repository...")

    if not cfgPath:
        cfgPath = f"{curDir}/{build_cfg}"
        if not os.path.isfile(cfgPath) or branch:
            cfgPath = str(PurePath(curDir, f"photon-{branch}", build_cfg))

    global configdict
    global check_prerequesite
    global ph_path

    with open(cfgPath) as jsonData:
        configdict = json.load(jsonData)

    cfgPath = os.path.abspath(cfgPath)

    if os.environ.get("RELEASE_BRANCH_PATH") is not None:
        configdict["release-branch-path"] = os.environ["RELEASE_BRANCH_PATH"]

    releaseDir = Path(
        configdict["photon-path"], configdict.get("release-branch-path", "")
        ).resolve()

    releaseCfgPath = f"{releaseDir}/{build_cfg}"
    with open(releaseCfgPath) as jsonData:
        releasedict = json.load(jsonData)

    configdict = merge_dicts(releasedict, configdict)

    if os.environ.get("STAGE_PATH") is not None:
        configdict["stage-path"] = os.environ["STAGE_PATH"]
        configdict["stage-path"] = Path(
            configdict["photon-path"], configdict.get("stage-path", "")
            ).resolve()

    set_default_value_of_config()
    create_new_symlink(configdict["release-branch-path"])

    os.environ["PHOTON_RELEASE_VER"] = configdict["photon-build-param"][
        "photon-release-version"
    ]
    os.environ["PHOTON_BUILD_NUM"] = configdict["photon-build-param"][
        "input-photon-build-number"
    ]

    if not configdict.get("photon-path", ""):
        configdict["photon-path"] = os.path.dirname(cfgPath)

    ph_build_param = configdict["photon-build-param"]
    process_env_build_params(ph_build_param)

    cfgdict_additional_path = configdict["additional-path"]
    process_additional_cfgs(cfgdict_additional_path)

    if "CONFIG" in os.environ:
        configdict["additional-path"]["conf-file"] = os.path.abspath(
            os.environ["CONFIG"]
        )
        with open(os.environ["CONFIG"], "rt") as f:
            jsonData = json.load(f)

        targetName = jsonData["image_type"]

    if "IMG_NAME" in os.environ:
        targetName = os.environ["IMG_NAME"]

    if "DOCKER_ENV" in os.environ:
        Build_Config.setDockerEnv(os.environ["DOCKER_ENV"])

    configdict["packageName"] = None

    for target in targetDict:
        for item in targetDict[target]:
            check_prerequesite[item] = False

    commit_id = str(configdict["photon-build-param"].get("base-commit", ""))
    check_hash=f"git -C {configdict['release-branch-path']} merge-base --is-ancestor {commit_id} HEAD"
    _, _, rc = runBashCmd(check_hash, capture=True, ignore_rc=True)
    ph_path = configdict["photon-path"] if rc else configdict["release-branch-path"]

    initialize_constants()

    """
    Special case.
    If BUILD_EXTRA_PKGS environment variable is set
    Override everything else and build extra packages.
    """
    if configdict["photon-build-param"].get("build-extra-pkgs", False):
        # incase if build.py is invoked directly
        if targetName != "extra-packages":
            targetName = "extra-packages"

    if not targetName:
        targetName = ph_build_param["target"]

    configdict["targetName"] = targetName.replace("-", "_")

    CheckTools.check_pre_reqs()

    try:
        attr = None
        if targetName in targetDict["image"]:
            buildImage = BuildImage(targetName)
            if targetName in [
                "iso",
                "src-iso",
                "minimal-iso",
                "rt-iso",
                "basic-iso",
            ]:
                buildImage.set_Iso_Parameters(targetName)
                buildImage.build_iso()
            elif targetName in buildImage.ova_cloud_images + [
                "rpi",
            ]:
                buildImage.build_image()
            else:
                attr = getattr(buildImage, configdict["targetName"])
        elif targetName in targetDict["rpmBuild"]:
            if targetName != "distributed-build":
                attr = getattr(RpmBuildTarget(), configdict["targetName"])
            else:
                attr = getattr(RpmBuildTarget, configdict["targetName"])
        elif targetName in targetDict["buildEnvironment"]:
            attr = getattr(BuildEnvironmentSetup, configdict["targetName"])
        elif targetName in targetDict["cleanup"]:
            attr = getattr(CleanUp, configdict["targetName"])
        elif targetName in targetDict["utilities"]:
            attr = getattr(Utilities(options.args), configdict["targetName"])
        elif targetName in targetDict["tool-checkup"]:
            attr = getattr(CheckTools, configdict["targetName"])
        else:
            RpmBuildTarget().package(targetName)

        if attr:
            attr()
    except Exception as e:
        print(e)
        traceback.print_exc()
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
