from CommandUtils import CommandUtils
from Logger import Logger
from PackageUtils import PackageUtils
from constants import constants
import subprocess
import os.path
import shutil
import urllib
import requests
import re

class TestUtils(object):

    def __init__(self,logName=None,logPath=None):
        if logName is None:
            logName = "Test Utils"
        if logPath is None:
            logPath = constants.logPath
        self.logName=logName
        self.logPath=logPath
        self.logger=Logger.getLogger(logName,logPath)
        #self.bintrayx86_64URL="https://dl.bintray.com/vmware/photon_release_1.0_TP2_x86_64/x86_64/"
        #self.bintraynoarchURL="https://dl.bintray.com/vmware/photon_release_1.0_TP2_x86_64/noarch/"
        self.bintrayx86_64URL="https://vmware.bintray.com/photon_dev_x86_64/x86_64/"
        self.bintraynoarchURL="https://vmware.bintray.com/photon_dev_x86_64/noarch/"
        self.bintrayx86_64Content=None
        self.bintraynoarchContent=None
        self.rpmbuildCommand = "rpmbuild"
        if os.geteuid()==0:
            self.rpmCommand="rpm"
        else:
            self.rpmCommand="fakeroot-ng rpm"

    def installTestRPMS(self, package, chrootID):
        pkgUtils=PackageUtils(self.logName,self.logPath)
        installedPackages=pkgUtils.findInstalledRPMPackages(chrootID)
        pacakgesToInstall=set(constants.listMakeCheckRPMPkgtoInstall)-set(installedPackages)-set([package])
        rpmFiles = ""
        packages = ""

        self.logger.info("Installing Test RPMS.......")
        for package in pacakgesToInstall:
            rpmFile=pkgUtils.findRPMFileForGivenPackage(package)
            if rpmFile is None:
                rpmFile=self.findRPMFileInGivenLocation(package, constants.prevPublishRPMRepo)
                if rpmFile is None:
                    self.logger.error("Unable to find rpm "+ package +" in current and previous versions")
                    raise Exception("Input Error")
            rpmFiles += " " + rpmFile
            packages += " " + package

        #cmd=sedb5lf.rpmCommand + " -i --nodeps --force --root "+chrootID+" --define \'_dbpath /var/lib/rpm\' "+ rpmFiles
        cmd=self.rpmCommand + " -i --nodeps --force --root "+ chrootID +" "+ rpmFiles
        self.logger.info("Installing rpms for TEST: "+packages)
        self.logger.info("Installing rpms for TEST: "+rpmFiles)
        process = subprocess.Popen("%s" %cmd,shell=True,stdout=subprocess.PIPE)
        retval = process.wait()
        if retval != 0:
            self.logger.error("Installing Test RPMS  failed")
            raise Exception("Test RPM installation failed")
        self.logger.info("Successfully installed all Test RPMS in Chroot:"+chrootID)

    def findRPMFileInGivenLocation(self, package, rpmdirPath, depth=1):
        if depth < 0:
            self.logger.error("Can not download "+package+" rpm from "+self.bintrayx86_64URL+" or "+self.bintraynoarchURL)
            return None
        cmdUtils = CommandUtils()
        listFoundRPMFiles = cmdUtils.findFile(package+"-*.rpm",rpmdirPath)
        listFilterRPMFiles=[]
        for f in listFoundRPMFiles:
            rpmFileName=os.path.basename(f)
            checkRPMName=rpmFileName.replace(package,"")
            rpmNameSplit = checkRPMName.split("-")
            if len(rpmNameSplit) == 3:
                listFilterRPMFiles.append(f)
        if len(listFilterRPMFiles) == 1 :
            return listFilterRPMFiles[0]
        if len(listFilterRPMFiles) == 0 :
            self.copyRPMfromBintray(package, rpmdirPath)
            return self.findRPMFileInGivenLocation(package, rpmdirPath, depth-1 )
        if len(listFilterRPMFiles) > 1 :
            self.logger.error("Found multiple rpm files for given package in rpm directory.Unable to determine the rpm file for package:"+package)
            return None

    def copyRPMfromBintray(self, package, rpmdirPath):
        rpmdirPathx86_64=rpmdirPath +"/x86_64"
        pattern=re.compile(">"+package+".*.rpm</a>")

        #bintrayx86_64
        if not self.bintrayx86_64Content:
            self.bintrayx86_64Content = requests.get(self.bintrayx86_64URL).content          
        contents=re.findall(pattern, self.bintrayx86_64Content)

        for rpms in contents:
            rpmName=rpms[1:-4]
            print(rpmName)
            self.logger.info("Downloading PUBLISHEDRPM "+rpmName)
            urllib.urlretrieve(self.bintrayx86_64URL+ rpmName, rpmName)
            shutil.move(rpmName, rpmdirPathx86_64)

        #bintraynoarch
        rpmdirPathnoarch=rpmdirPath +"/noarch"
        if not self.bintraynoarchContent:
            self.bintraynoarchContent = requests.get(self.bintraynoarchURL).content

        contents=re.findall(pattern, self.bintraynoarchContent)
        for rpms in contents:
            rpmName=rpms[1:-4]

            self.logger.info("Downloading PUBLISHEDRPM " +  rpmName)
            urllib.urlretrieve(self.bintraynoarchURL+rpmName, rpmName)
            shutil.move(rpmName, rpmdirPathnoarch)
