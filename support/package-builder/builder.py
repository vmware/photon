#!/usr/bin/env python3

import os.path
import collections
import json
import copy

from constants import constants
from PackageManager import PackageManager
from SpecData import SPECS
from PackageInfo import PackageInfo


class Builder:
    def buildSpecifiedPackages(
        listPackages,
        buildThreads,
        pkgBuildType,
        pkgInfoJsonFile=None,
        logger=None,
        build_extra_pkgs=False,
    ):
        if constants.rpmCheck:
            constants.setTestForceRPMS(copy.copy(listPackages))

        pkgManager = PackageManager(pkgBuildType=pkgBuildType)

        if not build_extra_pkgs:
            listPackages = set(listPackages) - set(constants.extraPackagesList)

        pkgManager.buildPackages(listPackages, buildThreads)

        if pkgInfoJsonFile:
            # Generating package info file which is required by installer
            if logger:
                logger.debug(f"Writing Package info to the file: {pkgInfoJsonFile}")
            pkgInfo = PackageInfo()
            pkgInfo.loadPackagesData()
            pkgInfo.writePkgListToFile(pkgInfoJsonFile)

    def buildPackagesInJson(
        pkgJsonInput, buildThreads, pkgBuildType, pkgInfoJsonFile, logger
    ):
        listPackages = []
        with open(pkgJsonInput) as jsonData:
            pkg_list_json = json.load(jsonData)
            listPackages = pkg_list_json["packages"]
            archSpecificPkgs = f"packages_{constants.buildArch}"
            if archSpecificPkgs in pkg_list_json:
                listPackages += pkg_list_json[archSpecificPkgs]

        Builder.buildSpecifiedPackages(
            listPackages, buildThreads, pkgBuildType, pkgInfoJsonFile, logger
        )

    def buildPackagesForAllSpecs(buildThreads, pkgBuildType, pkgInfoJsonFile, logger):
        listPackages = SPECS.getData().getListPackages()
        Builder.buildSpecifiedPackages(
            listPackages, buildThreads, pkgBuildType, pkgInfoJsonFile, logger
        )

    def get_packages_with_build_options(pkg_build_options_file):
        if os.path.exists(pkg_build_options_file):
            with open(pkg_build_options_file) as jsonData:
                pkg_build_option_json = json.load(
                    jsonData, object_pairs_hook=collections.OrderedDict
                )
                constants.setBuildOptions(pkg_build_option_json)

    def get_baseurl(conf_file):
        with open(conf_file) as jsonFile:
            config = json.load(jsonFile)
        return config["baseurl"]

    def get_all_package_names(build_install_option):
        base_path = os.path.dirname(build_install_option)
        packages = []

        with open(build_install_option) as jsonData:
            option_list_json = json.load(
                jsonData, object_pairs_hook=collections.OrderedDict
            )
            options_sorted = option_list_json.items()

            for install_option in options_sorted:
                filename = os.path.join(base_path, install_option[1]["file"])
                with open(filename) as pkgJsonData:
                    package_list_json = json.load(pkgJsonData)
                packages = packages + package_list_json["packages"]

        return packages
