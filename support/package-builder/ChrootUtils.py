import subprocess
from Logger import Logger
from CommandUtils import CommandUtils
import os
import threading
import time
from constants import constants

chrootRootPath="/mnt"

class ChrootUtils(object):
    counter=1
    lockForCounter=threading.Lock()
    lockForTrackingChroots=threading.Lock()
    lockForCreateChroot=threading.Lock()
    activeChroots=[]
    failureFlag=False
    numChroots=1
    
    def __init__(self,logName=None,logPath=None):
        if logName is None:
            logName = "ChrootUtils"
        if logPath is None:
            logPath = constants.logPath
        self.logName=logName
        self.logPath=logPath
        self.logger=Logger.getLogger(logName,logPath)
        
    def _getChrootUniqueID(self):
        ChrootUtils.lockForCounter.acquire()
        chrootID=chrootRootPath+"/photonroot"+str(ChrootUtils.counter)
        while os.path.isdir(chrootID):
            ChrootUtils.counter = ChrootUtils.counter +1
            chrootID=chrootRootPath+"/photonroot"+str(ChrootUtils.counter)
        ChrootUtils.counter = ChrootUtils.counter +1
        ChrootUtils.lockForCounter.release()
        return chrootID
    
    def updateParams(self):
        process = subprocess.Popen(["df" ,chrootRootPath],shell=True,stdout=subprocess.PIPE)
        retval = process.wait()
        if retval != 0:
            self.logger.error("Unable to check free space. Unknown error.")
            return False
        output = process.communicate()[0]
        device, size, used, available, percent, mountpoint = output.split("\n")[1].split()
        c =  int(available)/600000
        ChrootUtils.numChroots=int(c)
        self.logger.info("Updated number of chroots:"+str(ChrootUtils.numChroots))
    
    def checkFreeSpace(self):
        process = subprocess.Popen(["df" ,chrootRootPath],shell=True,stdout=subprocess.PIPE)
        retval = process.wait()
        if retval != 0:
            self.logger.error("Unable to check free space. Unknown error.")
            return False
        output = process.communicate()[0]
        device, size, used, available, percent, mountpoint = output.split("\n")[1].split()
        if available > 600000:
            self.logger.info("Free Space available "+ available)
            return True
        return False
    
    def createChroot(self):
        if ChrootUtils.failureFlag:
            return False
        
        ChrootUtils.lockForCreateChroot.acquire()
        if ChrootUtils.failureFlag:
            ChrootUtils.lockForCreateChroot.release()
            return False
        
        startTime=currentTime=time.time()
        timeOut=1800
        freeSpaceAvailable=False
        while currentTime < startTime + timeOut:
            #if self.checkFreeSpace():
            if len(ChrootUtils.activeChroots) < ChrootUtils.numChroots:
                freeSpaceAvailable=True
                break
            time.sleep(100)
            
        if not freeSpaceAvailable:
            self.logger.error("Unable to create chroot. No sufficient free space is available.")
            ChrootUtils.lockForCreateChroot.release()
            ChrootUtils.failureFlag=True
            return False,None
        
        chrootID=self._getChrootUniqueID()
        # need to add timeout for this step
        # http://stackoverflow.com/questions/1191374/subprocess-with-timeout
        process = subprocess.Popen("mkdir -p "+chrootID,shell=True,stdout=subprocess.PIPE)
        retval = process.wait()
        
        ChrootUtils.lockForCreateChroot.release()
        
        if retval != 0:
            self.logger.error("Unable to create chroot:"+ chrootID +".Unknown error.")
            return False,None
        
        ChrootUtils.lockForTrackingChroots.acquire()
        ChrootUtils.activeChroots.append(chrootID) 
        ChrootUtils.lockForTrackingChroots.release()           
        return True,chrootID
    
    def destroyChroot(self,chrootID):
        validChroot = True
        ChrootUtils.lockForTrackingChroots.acquire()
        if chrootID not in ChrootUtils.activeChroots:
            validChroot = False
        else:
            ChrootUtils.activeChroots.remove(chrootID)
        ChrootUtils.lockForTrackingChroots.release()
        if not validChroot:
            self.logger.error("Given chroot:"+chrootID+" is not a valid chroot. It is not created by ChrootUtils.")
            return False

        # need to add timeout for this step
        # http://stackoverflow.com/questions/1191374/subprocess-with-timeout
        process = subprocess.Popen("./cleanup-build-root.sh "+chrootID,shell=True,stdout=subprocess.PIPE)
        retval = process.wait()
        if retval != 0:
            self.logger.error("Unable to destroy chroot:"+ chrootID +".Unknown error.")
            return False
        cmdUtils=CommandUtils()
        cmdUtils.runCommandInShell("rm -rf "+chrootID)
        self.logger.info("Successfully destroyed chroot:"+chrootID)
        return True
    
    def cleanUpActiveChroots(self):
        ChrootUtils.lockForTrackingChroots.acquire()
        listChroots=self.activeChroots[:]
        ChrootUtils.lockForTrackingChroots.release()
        for chrootID in listChroots:
            self.destroyChroot(chrootID)
        self.logger.info("Successfully destroyed all active chroots")
