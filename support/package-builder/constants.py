from SpecData import SerializableSpecObjectsUtils

class constants(object):
    specPath=""
    sourcePath=""
    rpmPath=""
    toolsPath=""
    logPath=""
    incrementalBuild=False
    topDirPath=""
    specData=None
    testPath="test"
    
    
    @staticmethod
    def initialize(options):
        constants.specPath = options.specPath
        constants.sourcePath = options.sourcePath
        constants.rpmPath = options.rpmPath
        constants.toolsPath = options.toolsPath
        constants.incrementalBuild = options.incrementalBuild
        constants.topDirPath = options.topDirPath
        constants.logPath = options.logPath
        constants.specData = SerializableSpecObjectsUtils(constants.logPath)
        constants.specData.readSpecsAndConvertToSerializableObjects(constants.specPath)
        

        
        
    