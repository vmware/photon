#!/usr/bin/env python3

import os.path
import collections
import json

from constants import constants
from PackageManager import PackageManager
from SpecData import SPECS
from PackageInfo import PackageInfo


class Builder:
    def buildToolchain(buildThreads, pkgBuildType):
        pkgManager = PackageManager(pkgBuildType=pkgBuildType)
        pkgManager.buildToolChainPackages(buildThreads)

    def generatePkgInfo(pkgInfoJsonFile=None, logger=None):
        if not pkgInfoJsonFile:
            return

        # Generating package info file which is required by installer
        # and package list file (snapshot) for tdnf
        pkgInfo = PackageInfo()
        pkgInfo.loadPackagesData()

        if logger:
            logger.debug(f"Writing Package info to the file: {pkgInfoJsonFile}")
        pkgInfo.writePkgInfoToFile(pkgInfoJsonFile)

        # Use the same filename but replace extension to .list
        filename, _ = os.path.splitext(pkgInfoJsonFile)
        pkgListFile = filename + ".list"
        if logger:
            logger.debug(f"Writing Package list to the file: {pkgListFile}")
        pkgInfo.writePkgListToFile(pkgListFile)

    def buildSpecifiedPackages(
        listPackages,
        buildThreads,
        pkgBuildType,
        pkgInfoJsonFile=None,
        logger=None,
        build_extra_pkgs=False,
    ):
        pkgManager = PackageManager(pkgBuildType=pkgBuildType)

        if not build_extra_pkgs:
            listPackages = set(listPackages) - set(constants.extraPackagesList)

        pkgManager.buildPackages(listPackages, buildThreads)

        Builder.generatePkgInfo(pkgInfoJsonFile, logger)

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
