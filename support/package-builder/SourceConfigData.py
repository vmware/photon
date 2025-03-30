import os
import yaml
from Logger import Logger
from constants import constants


class Source(object):
    def __init__(
        self,
        archive,
        archive_sha512sum,
        name,
        version,
    ):
        self.archive = archive
        self.archive_sha512sum = archive_sha512sum
        self.name = name if name else archive
        self.version = version


class SourceConfigData(object):

    def __init__(self, logPath, specFilePaths):
        self.logger = Logger.getLogger("SourceConfigData", logPath, constants.logLevel)
        self.mapSourceObjects: dict[str, Source] = {}
        self._readSpecs(specFilePaths)

    def getChecksum(self, sourceName):
        sourceDef = self.mapSourceObjects.get(sourceName, None)
        if sourceDef:
            return self.mapSourceObjects[sourceName].archive_sha512sum

        return None

    # Read all config.yaml files from the given folder
    # creates corresponding Source Objects and put them in internal mappings.
    def _readSpecs(self, specFilePaths):
        for configFile in self._getListConfigFiles(specFilePaths):
            config = self._parseConfig(configFile)

            for sourceEntry in config["sources"]:
                self.mapSourceObjects[sourceEntry.archive] = sourceEntry

    def _getListConfigFiles(self, paths):
        listConfigFiles = []
        for path in paths:
            for dirEntry in os.listdir(path):
                dirEntryPath = os.path.join(path, dirEntry)
                if os.path.isfile(dirEntryPath) and dirEntryPath.endswith("config.yaml"):
                    listConfigFiles.append(dirEntryPath)
                elif os.path.isdir(dirEntryPath) and not os.path.islink(dirEntryPath):
                    listConfigFiles.extend(self._getListConfigFiles([dirEntryPath]))
        return listConfigFiles

    def _parseConfig(self, filepath) -> dict:
        response = {}
        response["sources"] = []
        with open(filepath, "r") as file:
            config = yaml.safe_load(file)
            sources = config.get("sources", [])

            if not sources:
                self.logger.error("missing sources in package configuration")
                return response
            for sourceEntry in sources:
                # processing one source entry
                if sourceEntry and isinstance(sourceEntry, dict):
                    archive = sourceEntry.get("archive")
                    archive_sha512sum = sourceEntry.get("archive_sha512sum")
                    name = sourceEntry.get("name")
                    version = sourceEntry.get("version")
                    response["sources"].append(
                        Source(
                            archive=archive,
                            archive_sha512sum=archive_sha512sum,
                            name=name,
                            version=version,
                        )
                    )
        return response


class SOURCES(object):
    __instance = None
    sourceData: SourceConfigData

    @staticmethod
    def getData() -> SourceConfigData:
        """Static access method."""
        if SOURCES.__instance is None:
            SOURCES()
        return SOURCES.__instance.sourceData

    def __init__(self):
        """Virtually private constructor."""
        if SOURCES.__instance is not None:
            raise Exception("This class is a singleton!")

        self.initialize()
        SOURCES.__instance = self

    def initialize(self):
        self.sourceData = SourceConfigData(constants.logPath, constants.specPaths)
