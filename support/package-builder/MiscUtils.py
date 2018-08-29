import os.path

class MiscUtils(object):

    @staticmethod
    def isOutdated(listInputFiles, listOutputFiles):
        thresholdTimeStamp = None
        if not listInputFiles:
            return False
        if not listOutputFiles:
            return True
        for f in listOutputFiles:
            t = os.path.getmtime(f)
            if thresholdTimeStamp is None:
                thresholdTimeStamp = t
            if t < thresholdTimeStamp:
                thresholdTimeStamp = t
        for f in listInputFiles:
            t = os.path.getmtime(f)
            if t > thresholdTimeStamp:
                return True
        return False

    @staticmethod
    def getListSpecFiles(listSpecFiles, path):
        for dirEntry in os.listdir(path):
            dirEntryPath = os.path.join(path, dirEntry)
            if os.path.isfile(dirEntryPath) and dirEntryPath.endswith(".spec"):
                listSpecFiles.append(dirEntryPath)
            elif os.path.isdir(dirEntryPath):
                MiscUtils.getListSpecFiles(listSpecFiles, dirEntryPath)

if __name__ == "__main__":
    inputFiles = ["SpecParser.py", "Logger.py"]
    outputFiles = ["builder.py"]
    print(MiscUtils.isOutdated(inputFiles, outputFiles))
