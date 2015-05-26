import subprocess
import os
import re

class CommandUtils(object):
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