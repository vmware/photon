import os.path

class MiscUtils(object):
    
    @staticmethod
    def isOutdated(listInputFiles,listOutputFiles):
        thresholdTimeStamp=None
        if len(listInputFiles) == 0:
            return False
        if len(listOutputFiles) == 0:
            return True
        for f in listOutputFiles:
            t=os.path.getmtime(f)
            if thresholdTimeStamp is None:
                thresholdTimeStamp = t
            if t < thresholdTimeStamp:
                thresholdTimeStamp = t 
        for f in listInputFiles:
            t=os.path.getmtime(f)
            if t > thresholdTimeStamp:
                return True
        return False
    
    @staticmethod
    def getListSpecFiles(listSpecFiles,path):
        for dirEntry in os.listdir(path):
            dirEntryPath = os.path.join(path, dirEntry)
            if os.path.isfile(dirEntryPath) and dirEntryPath.endswith(".spec"):
                listSpecFiles.append(dirEntryPath)
            elif os.path.isdir(dirEntryPath):
                MiscUtils.getListSpecFiles(listSpecFiles,dirEntryPath)
    
if __name__=="__main__":
    listInputFiles=["SpecParser.py","Logger.py"]
    listOutputFiles=["builder.py"]
    print(MiscUtils.isOutdated(listInputFiles, listOutputFiles))