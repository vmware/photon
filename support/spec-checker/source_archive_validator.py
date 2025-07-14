#!/usr/bin/env python3

import os
import sys
import yaml
import copy

from collections import defaultdict


class SourceArchiveChecker:
    def __init__(self, specPaths):
        self.archiveMap = defaultdict(list)
        self.loadedFiles = {}
        self.specPaths = specPaths

    def loadYamlFile(self, path):
        if path in self.loadedFiles:
            return self.loadedFiles[path]
        try:
            with open(path, "r", encoding="utf-8") as file:
                data = yaml.safe_load(file)
                self.loadedFiles[path] = data
                return data
        except yaml.YAMLError as e:
            raise Exception(f"YAML error in {path}: {e}")
        except FileNotFoundError as e:
            raise Exception(f"Included file not found: {e}")

    def collectSourcesFromFile(self, filePath):
        rawData = self.loadYamlFile(filePath)
        rawSources = rawData.get("sources", [])
        sharedSources = rawData.get("shared_sources", [])

        mergedSources = []

        for entry in rawSources:
            new_entry = copy.deepcopy(entry)
            new_entry["_src_origin"] = filePath
            mergedSources.append(new_entry)

        for entry in sharedSources:
            includeFile = None
            for specDir in self.specPaths:
                includeFile = f"{specDir}/{entry}"
                if os.path.exists(includeFile):
                    break

            if not includeFile:
                raise Exception(f"ERROR: {entry} not found ...")

            includeData = self.loadYamlFile(includeFile)
            if isinstance(includeData, dict):
                includeSources = includeData.get("sources", [])
            elif isinstance(includeData, list):
                includeSources = includeData
            else:
                raise Exception(f"Invalid format in included file: {includeFile}")

            if not isinstance(includeSources, list):
                raise Exception(f"'sources' must be a list in include file: {includeFile}")

            for includedEntry in includeSources:
                new_inc_entry = copy.deepcopy(includedEntry)
                new_inc_entry["_src_origin"] = includeFile
                mergedSources.append(new_inc_entry)

        return mergedSources

    def scanDirectory(self, rootDir):
        self.archiveMap.clear()
        self.loadedFiles.clear()

        for subdir, _, files in os.walk(rootDir):
            for file in files:
                if file != "config.yaml":
                    continue

                configPath = os.path.join(subdir, file)
                sources = self.collectSourcesFromFile(configPath)

                seen_archives_per_origin = set()

                for src in sources:
                    archive = src.get("archive")
                    if not archive:
                        continue
                    origin = src.get("_src_origin", configPath)

                    key = (archive, origin)
                    if key in seen_archives_per_origin:
                        continue
                    seen_archives_per_origin.add(key)

                    # Store only src and configPath; origin is always in src["_src_origin"]
                    self.archiveMap[archive].append((src, configPath))

    def checkConflicts(self, verbose=False):
        hasConflict = False
        outputLines = []

        for archiveName, entries in self.archiveMap.items():
            # Read all origins from src["_src_origin"] inside entries
            uniqueOrigins = {src["_src_origin"] for src, _ in entries}

            if len(uniqueOrigins) > 1:
                hasConflict = True
                outputLines.append(f"\nDuplicate archive found: {archiveName}")
                for src, usedIn in entries:
                    outputLines.append(f" - Used in: {usedIn} Defined in: {src['_src_origin']}")

        if verbose:
            if hasConflict:
                outputLines.append("\nERROR: Duplicate archive names found.")
                print("\n".join(outputLines), file=sys.stderr)
            else:
                outputLines.append("No duplicate archive names found.")

            return hasConflict

        return hasConflict, outputLines

    def getArchiveMap(self):
        return self.archiveMap


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <specs_directory>", file=sys.stderr)
        sys.exit(1)

    specsDir = sys.argv[1]

    checker = SourceArchiveChecker()
    checker.scanDirectory(specsDir)
    hasConflict = checker.checkConflicts(verbose=True)
    sys.exit(hasConflict)
