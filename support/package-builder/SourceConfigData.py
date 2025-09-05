#!/usr/bin/env python3

import os
import yaml


class Source:
    def __init__(self, archive, archive_sha512sum, name, version):
        self.archive = archive
        self.archive_sha512sum = archive_sha512sum
        self.name = name if name else archive
        self.version = version


class SourceConfigData:
    def __init__(self):
        self.mapSourceObjects = {}

    def getChecksum(self, sourceName):
        sourceDef = self.mapSourceObjects.get(sourceName, None)
        if sourceDef:
            return self.mapSourceObjects[sourceName].archive_sha512sum

        return None

    def _readCfgYaml(self, specDir):
        cfgYaml = f"{specDir}/config.yaml"
        if not os.path.exists(cfgYaml):
            return None

        sharedCfgs = self.getSharedCfgs(cfgYaml)
        sharedCfgs.append(cfgYaml)

        for yml in sharedCfgs:
            config = self._parseConfig(yml)
            for sourceEntry in config["sources"]:
                self.mapSourceObjects[sourceEntry.archive] = sourceEntry

    def getSharedCfgs(self, yamlFile):
        sharedCfgs = []
        data = {}

        with open(yamlFile, "r") as f:
            data = yaml.safe_load(f)

        sources = data.get("shared_sources")
        if not sources:
            return sharedCfgs

        specDir = yamlFile.split("SPECS")[0] + "SPECS"
        for item in sources:
            absPath = os.path.abspath(f"{specDir}/{item}")
            if absPath in sharedCfgs:
                m = f"ERROR: Duplicate entry '{item}' found in '{yamlFile}' ..."
                raise Exception(m)
            if not os.path.exists(absPath):
                m = f"ERROR: '{item}' file not found ..."
                raise Exception(m)
            sharedCfgs.append(absPath)
        return sharedCfgs

    def _parseConfig(self, filepath):
        response = {}
        response["sources"] = []
        with open(filepath, "r") as file:
            config = yaml.safe_load(file)

            sources = config.get("sources", [])
            if not (sources or config.get("shared_sources")):
                raise Exception(f"ERROR: Missing sources in '{filepath}' ...")
            for sourceEntry in sources:
                if not sourceEntry.get("archive", ""):
                    continue
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


class SOURCES:
    def __init__(self, specDir):
        self.sourceData = SourceConfigData()
        self.sourceData._readCfgYaml(specDir)

    def getData(self):
        return self.sourceData


def main():
    import sys

    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <spec_directory>", file=sys.stderr)
        sys.exit(1)

    specDir = sys.argv[1]
    if not os.path.isdir(specDir):
        print(f"ERROR: '{specDir}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    sources = SOURCES(specDir)
    data = sources.getData()

    print("Loaded sources:")
    for archiveName, sourceObj in data.mapSourceObjects.items():
        print(f" - Archive: {sourceObj.archive}")
        print(f"   SHA512 : {sourceObj.archive_sha512sum}")
        print(f"   Name   : {sourceObj.name}")
        print(f"   Version: {sourceObj.version}\n")


if __name__ == "__main__":
    main()
