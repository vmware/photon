#!/usr/bin/env python3

import os
import sys
import requests
import time

from PackageBuilder import PackageBuilder
from constants import constants


class BuilderClient:
    def __init__(self, MasterIP, PORT):
        self.MasterIP = MasterIP
        self.PORT = PORT
        self.MasterUrl = f"http://{MasterIP}:{PORT}"

    def getNextPkgToBuild(self):
        masterGetPkgApi = f"{self.MasterUrl}/package/"
        try:
            response = requests.get(masterGetPkgApi)
        except requests.exceptions.RequestException as e:
            print(f"Exception in getting response from server: {e}")
            return None

        if response.status_code != 200:
            print(
                f"No package to build\n"
                f"Response Status = {response.status_code}"
            )
            return None

        return response.text

    def getConstants(self):
        masterConstantsAPI = f"{self.MasterUrl}/constants/"
        try:
            response = requests.get(masterConstantsAPI)
        except requests.exceptions.RequestException as e:
            print(f"Exception in getting response from server: {e}")
            return None

        if response.status_code == 200:
            return response.json()

        print(
            f"Unable to get constants. response code = "
            f"{response.status_code}\n"
            f"exiting"
        )
        sys.exit(1)

    def initializeConstants(self, constant_dict):
        constants.setSpecPath(constant_dict["specPath"])
        constants.setSourcePath(constant_dict["sourcePath"])
        constants.setRpmPath(constant_dict["rpmPath"])
        constants.setSourceRpmPath(constant_dict["sourceRpmPath"])
        constants.setTopDirPath(constant_dict["topDirPath"])
        constants.setLogPath(constant_dict["logPath"])
        constants.setLogLevel(constant_dict["logLevel"])
        constants.setDist(constant_dict["dist"])
        constants.setBuildNumber(constant_dict["buildNumber"])
        constants.setCommonBuildNumber(constant_dict["commonBuildNumber"])
        constants.setReleaseVersion(constant_dict["releaseVersion"])
        constants.setPrevPublishRPMRepo(constant_dict["prevPublishRPMRepo"])
        constants.setPrevPublishXRPMRepo(constant_dict["prevPublishXRPMRepo"])
        constants.setBuildRootPath(constant_dict["buildRootPath"])
        constants.setPullSourcesURL(constant_dict["pullsourcesURL"])
        constants.setInputRPMSPath(constant_dict["inputRPMSPath"])
        constants.setRPMCheck(constant_dict["rpmCheck"])
        constants.setRpmCheckStopOnError(constant_dict["rpmCheckStopOnError"])

        constants.setPublishBuildDependencies(
            constant_dict["publishBuildDependencies"]
        )

        constants.setPackageWeightsPath(constant_dict["packageWeightsPath"])
        constants.setKatBuild(constant_dict["katBuild"])
        constants.setCanisterBuild(constant_dict["canisterBuild"])
        constants.setAcvpBuild(constant_dict['acvpBuild'])
        constants.extrasourcesURLs = constant_dict["extrasourcesURLs"]
        constants.userDefinedMacros = constant_dict["userDefinedMacros"]
        constants.tmpDirPath = constant_dict["tmpDirPath"]
        constants.buildPatch = constant_dict["buildPatch"]

    def getDoneList(self):
        masterDoneListApi = f"{self.MasterUrl}/donelist/"
        try:
            response = requests.get(masterDoneListApi)
        except requests.exceptions.RequestException as e:
            print(f"Exception in getting response from server: {e}")
            return None

        if response.status_code == 200:
            data = response.json()
            return data["packages"]

        print(
            "Unable to get DoneList, response code = ",
            response.status_code,
        )
        sys.exit(1)

    def getMapPackageToCycle(self):
        masterMapPackageToCycleApi = f"{self.MasterUrl}/mappackagetocycle/"
        try:
            response = requests.get(masterMapPackageToCycleApi)
        except requests.exceptions.RequestException as e:
            print(f"Exception in getting response from server: {e}")
            return None

        if response.status_code == 200:
            return response.json()

        print(
            "Unable to get MapPackageToCycle, response code = ",
            response.status_code,
        )
        sys.exit(1)

    def notifyMaster(self, package, buildStatus):
        masterBuildStatusApi = f"{self.MasterUrl}/notifybuild/"
        try:
            response = requests.post(
                masterBuildStatusApi,
                json={"package": package, "status": buildStatus},
            )
        except requests.exceptions.RequestException as e:
            print(f"Exception in getting response from server: {e}")
            return None

        if response.status_code == 200:
            print("master notified\n")
            return True

        print(
            "Unable to notify master, error code = %s"
            % response.status_code,
            ",response = %s" % response.json,
        )
        sys.exit(1)

    def doBuild(self, package, doneList, mapPackageToCycle):
        SUCCESS = 0
        FAILED = -1
        pkgBuilder = PackageBuilder(mapPackageToCycle, "chroot")
        status = SUCCESS
        try:
            pkgBuilder.build(package, doneList)
        except Exception as e:
            print("Building exception=", e)
            status = FAILED

        return status


if __name__ == "__main__":
    print("Getting master details ...")
    try:
        BuildId = os.environ["BUILDID"]
        MasterIP = os.environ[f"MASTER_SERVICE_{BuildId}_SERVICE_HOST"]
        PORT = os.environ[f"MASTER_SERVICE_{BuildId}_SERVICE_PORT"]
    except KeyError as e:
        print(f"{e} environment variable does not exist")
        sys.exit(1)

    builderClient = BuilderClient(MasterIP, PORT)

    # Get constants and initialize since constants will remain same
    while True:
        constants_dict = builderClient.getConstants()
        if not constants_dict:
            continue
        builderClient.initializeConstants(constants_dict)
        break

    # Get package to build and other required data to build it
    while True:
        package = builderClient.getNextPkgToBuild()
        if not package:
            time.sleep(5)
            continue
        doneList = builderClient.getDoneList()
        mapPackageToCycle = builderClient.getMapPackageToCycle()
        status = builderClient.doBuild(package, doneList, mapPackageToCycle)
        if not builderClient.notifyMaster(package, status):
            print(f"Unable to notify master for package {package}")
