#!/usr/bin/env python3

from argparse import ArgumentParser
import os.path
import collections
import traceback
import sys
import json
import copy
from CommandUtils import CommandUtils
from Logger import Logger
from constants import constants
from PackageManager import PackageManager
from SpecData import SPECS
from PackageInfo import PackageInfo

class Builder:

    def buildSpecifiedPackages(listPackages, buildThreads, pkgBuildType, pkgInfoJsonFile=None, logger=None):
        if constants.rpmCheck:
            constants.setTestForceRPMS(copy.copy(listPackages))
        pkgManager = PackageManager(pkgBuildType=pkgBuildType)
        pkgManager.buildPackages(listPackages, buildThreads)

        if pkgInfoJsonFile is not None:
            # Generating package info file which is required by installer
            if logger is not None:
                logger.debug("Writing Package info to the file:" + pkgInfoJsonFile)
            pkgInfo = PackageInfo()
            pkgInfo.loadPackagesData()
            pkgInfo.writePkgListToFile(pkgInfoJsonFile)


    def buildPackagesInJson(pkgJsonInput, buildThreads, pkgBuildType, pkgInfoJsonFile, logger):
        listPackages = []
        with open(pkgJsonInput) as jsonData:
            pkg_list_json = json.load(jsonData)
            listPackages = pkg_list_json["packages"]
        Builder.buildSpecifiedPackages(listPackages, buildThreads, pkgBuildType, pkgInfoJsonFile, logger)


    def buildPackagesForAllSpecs(buildThreads, pkgBuildType, pkgInfoJsonFile, logger):
        listPackages = SPECS.getData().getListPackages()
        Builder.buildSpecifiedPackages(listPackages, buildThreads, pkgBuildType, pkgInfoJsonFile, logger)


    def get_packages_with_build_options(pkg_build_options_file):
        if os.path.exists(pkg_build_options_file):
            with open(pkg_build_options_file) as jsonData:
                pkg_build_option_json = json.load(jsonData, object_pairs_hook=collections.OrderedDict)
                constants.setBuildOptions(pkg_build_option_json)

    def get_baseurl(conf_file):
        with open(conf_file) as jsonFile:
            config = json.load(jsonFile)
        return config['baseurl']

    def get_all_package_names(build_install_option):
        base_path = os.path.dirname(build_install_option)
        packages = []

        with open(build_install_option) as jsonData:
            option_list_json = json.load(jsonData, object_pairs_hook=collections.OrderedDict)
            options_sorted = option_list_json.items()

            for install_option in options_sorted:
                filename = os.path.join(base_path, install_option[1]["file"])
                with open(filename) as pkgJsonData:
                    package_list_json = json.load(pkgJsonData)
                packages = packages + package_list_json["packages"]

        return packages
