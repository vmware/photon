#!/usr/bin/env python3

import os
import re
import operator

from StringUtils import StringUtils
from constants import constants
from SpecStructures import dependentPackageData
from SpecStructures import Package
from SpecStructures import SpecObject

strUtils = StringUtils()


class SpecParser(object):
    class rpmMacro(object):
        def __init__(self):
            self.macroName = ""
            self.macroFlag = ""
            self.content = ""
            self.position = -1
            self.endposition = -1

    def __init__(self, specfile, arch):
        self.arch = arch
        self.subrelease = constants.subreleaseVersion
        self.cleanMacro = None
        self.prepMacro = None
        self.buildMacro = None
        self.installMacro = None
        self.changelogMacro = None
        self.checkMacro = None
        self.packages = {}
        self.specAdditionalContent = ""
        self.globalSecurityHardening = ""
        self.networkRequired = False
        self.defs = {}
        self.defs["_arch"] = arch
        self.conditionalCheckMacroEnabled = False
        self.macro_pattern = re.compile(r"%{(\S+?)\}")
        self.specfile = specfile
        self.skipSpec = False

        self.packages["default"] = Package(self.arch)
        self.currentPkg = "default"
        self._parseSpecFile(self.specfile)

    def _parseSpecFile(self, file):
        lines = []
        inMacro = 0

        with open(file) as specFile:
            lines = specFile.read().splitlines()

        i = 0
        totalLines = len(lines)

        def skip_conditional_body():
            deep = 1
            nonlocal i
            nonlocal inMacro
            while i < totalLines and deep:
                i += 1
                line = lines[i].strip()
                if self._isConditionalMacroStart(line):
                    deep += 1
                elif self._isConditionalMacroElse(line) and deep == 1:
                    deep -= 1
                    inMacro += 1
                elif self._isConditionalMacroEnd(line):
                    deep -= 1

        while i < totalLines:
            line = lines[i].strip()
            if cond := self._isConditionalArch(line):
                if not cond(self.arch, self._readConditionalArch(line)):
                    skip_conditional_body()
                else:
                    inMacro += 1
            elif self._isIfCondition(line):
                if not self._isConditionTrue(line):
                    skip_conditional_body()
                else:
                    inMacro += 1
            elif self._isConditionalMacroElse(line) and inMacro:
                skip_conditional_body()
                inMacro -= 1
            elif self._isConditionalMacroEnd(line) and inMacro:
                inMacro -= 1
            elif self._isSpecMacro(line):
                macro, i = self._readMacroFromFile(i, lines)
                self._updateSpecMacro(macro)
            elif self._isPackageMacro(line):
                defaultpkg = self.packages.get("default")
                returnVal, packageName = self._readPkgNameFromPackageMacro(
                    line, defaultpkg.name
                )
                packageName = self._replaceMacros(packageName)
                if not returnVal:
                    return False
                if line.startswith("%package"):
                    pkg = Package(self.arch, defaultpkg)
                    pkg.name = packageName
                    self.currentPkg = packageName
                    self.packages[pkg.name] = pkg
                elif line.startswith("%description"):
                    description = None
                    while i + 1 < totalLines:
                        line = lines[i + 1].strip()
                        if line and (
                            self._isSpecMacro(line)
                            or self._isPackageMacro(line)
                            or self._isDefinition(line)
                            or self._isIfCondition(line)
                        ):
                            break
                        if description:
                            description += f" {line}"
                        else:
                            description = line
                        i += 1
                    self.packages[self.currentPkg].description = description
                else:
                    if defaultpkg.name == packageName:
                        packageName = "default"
                    macro, i = self._readMacroFromFile(i, lines)
                    if packageName not in self.packages:
                        i += 1
                        continue
                    self.packages[packageName].updatePackageMacro(macro)
            elif self._isPackageHeaders(line):
                self._readPackageHeaders(line, self.packages[self.currentPkg])
            elif self._isGlobalSecurityHardening(line):
                self._readSecurityHardening(line)
            elif self._isNetworkRequired(line):
                self._readNetworkRequired(line)
            elif self._isBuildIf(line):
                self.skipSpec = not self._parseBuildIf(line)
                if self.skipSpec:
                    return
            elif self._isExtraBuildRequires(line):
                self._readExtraBuildRequires(line, self.packages[self.currentPkg])
            elif self._isBuildRequiresNative(line):
                self._readBuildRequiresNative(line, self.packages[self.currentPkg])
            elif self._isDefinition(line):
                self._readDefinition(line)
            elif self._isConditionalCheckMacro(line):
                self.conditionalCheckMacroEnabled = True
            elif self.conditionalCheckMacroEnabled and self._isConditionalMacroEnd(
                line
            ):
                self.conditionalCheckMacroEnabled = False
            elif self._isInclude(line):
                include = line.split()
                if len(include) == 2:
                    includeFile = os.path.join(
                        os.path.dirname(file),
                        self._replaceMacros(include[1]),
                    )
                    # recursive parsing
                    self._parseSpecFile(includeFile)
            else:
                self.specAdditionalContent += f"{line}\n"
            i += 1

    def _readPkgNameFromPackageMacro(self, data, basePkgName=None):
        data = " ".join(data.split())
        pkgHeaderName = data.split(" ")
        lenpkgHeaderName = len(pkgHeaderName)
        i = 1
        pkgName = None
        while i < lenpkgHeaderName:
            if pkgHeaderName[i] == "-n" and i + 1 < lenpkgHeaderName:
                pkgName = pkgHeaderName[i + 1]
                break
            if pkgHeaderName[i].startswith("-"):
                i += 2
            else:
                pkgName = f"{basePkgName}-{pkgHeaderName[i]}"
                break
        if not pkgName:
            return True, basePkgName
        return True, pkgName

    def _replaceMacros(self, string):
        """
        Replace all macros in given string with corresponding values.

        For example: a string '%{name}-%{version}.tar.gz' will be
        transformed to 'foo-2.0.tar.gz'.

        :return A string where all macros in given input are substituted
        as good as possible.
        """

        def _is_conditional(macro):
            return macro.startswith(("?", "!"))

        def _test_conditional(macro):
            if macro[0] == "?":
                return True
            if macro[0] == "!":
                return False
            raise Exception("Given string is not a conditional macro")

        def _is_macro_defined(macro):
            return (
                (macro in self.defs.keys())
                or (macro in constants.userDefinedMacros.keys())
                or (
                    macro
                    in constants.getAdditionalMacros(
                        self.packages["default"].name
                    ).keys()
                )
            )

        def _get_macro(macro):
            if macro in self.defs.keys():
                return self.defs[macro]

            if macro in constants.userDefinedMacros.keys():
                return constants.userDefinedMacros[macro]

            if (
                macro
                in constants.getAdditionalMacros(self.packages["default"].name).keys()
            ):
                return constants.getAdditionalMacros(self.packages["default"].name)[
                    macro
                ]

            raise Exception(f"Unknown macro: {macro}")

        def _macro_repl(match):
            macro_name = match.group(1)
            if _is_conditional(macro_name):
                parts = macro_name[1:].split(":")
                assert parts
                retv = ""
                if _test_conditional(macro_name):  # ?
                    if _is_macro_defined(parts[0]):
                        if len(parts) == 2:
                            retv = parts[1]
                        else:
                            retv = _get_macro(parts[0])
                else:  # !
                    if _is_macro_defined(parts[0]):
                        if len(parts) == 2:
                            retv = parts[1]
                return retv

            if _is_macro_defined(macro_name):
                return _get_macro(macro_name)
            return match.string[match.start() : match.end()]  # noqa: E203

        # User macros
        for macroName, value in constants.userDefinedMacros.items():
            macro = f"%{macroName}"
            if string.find(macro) != -1:
                string = string.replace(macro, value)
        # Spec definitions
        for macroName, value in self.defs.items():
            macro = f"%{macroName}"
            if string.find(macro) != -1:
                string = string.replace(macro, value)
        return re.sub(self.macro_pattern, _macro_repl, string)

    def _readMacroFromFile(self, currentPos, lines):
        macro = self.rpmMacro()
        line = lines[currentPos]
        macro.position = currentPos
        macro.endposition = currentPos
        endPos = len(lines)
        line = " ".join(line.split())
        flagindex = line.find(" ")
        if flagindex != -1:
            macro.macroFlag = line[flagindex + 1 :]  # noqa: E203
            macro.macroName = line[:flagindex]
        else:
            macro.macroName = line

        if currentPos + 1 < len(lines) and self._isMacro(lines[currentPos + 1]):
            return macro, currentPos

        for j in range(currentPos + 1, endPos):
            content = lines[j]
            if j + 1 < endPos and self._isMacro(lines[j + 1]):
                return macro, j
            macro.content += f"{content}\n"
            macro.endposition = j
        return macro, endPos

    def _updateSpecMacro(self, macro):
        if macro.macroName == "%clean":
            self.cleanMacro = macro
        if macro.macroName == "%prep":
            self.prepMacro = macro
        if macro.macroName == "%build":
            self.buildMacro = macro
        if macro.macroName == "%install":
            self.installMacro = macro
        if macro.macroName == "%changelog":
            self.changelogMacro = macro
        if macro.macroName == "%check":
            self.checkMacro = macro

    def _isMacro(self, line):
        return (
            self._isPackageMacro(line)
            or self._isSpecMacro(line)
            or self._isConditionalMacroStart(line)
            or self._isConditionalMacroEnd(line)
        )

    def _parseBuildIf(self, line):
        pattern = re.compile(r"%global\s+build_if\s+(.+)")
        match = pattern.search(line)
        if not match:
            raise ValueError(f"{self.specfile}: Invalid build_if line: {line}")
        condition = match.group(1).strip()
        return self._isConditionTrue(condition, True)

    def _isConditionalArch(self, line):
        if re.search("^%ifarch", line):
            return operator.eq
        elif re.search("^%ifnarch", line):
            return operator.ne
        return None

    def _isSpecMacro(self, line):
        return line.startswith(
            ("%clean", "%prep", "%build", "%install", "%changelog", "%check")
        )

    def _isPackageMacro(self, line):
        line = line.strip()
        return line.startswith(
            ("%post", "%postun", "%files", "%description", "%package")
        )

    def _isPackageHeaders(self, line):
        headersPatterns = [
            "^summary:",
            "^name:",
            "^group:",
            "^license:",
            "^epoch:",
            "^version:",
            "^release:",
            "^distribution:",
            "^requires:",
            r"^requires\((pre|post|preun|postun)\):",
            "^provides:",
            "^url:",
            "^source[0-9]*:",
            "^patch[0-9]*:",
            "^buildrequires:",
            "^buildarch:",
        ]
        return any([re.search(r, line, flags=re.IGNORECASE) for r in headersPatterns])

    def _isGlobalSecurityHardening(self, line):
        return re.search("^%global *security_hardening", line, flags=re.IGNORECASE)

    def _isExtraBuildRequires(self, line):
        return re.search("^%define *extrabuildrequires", line, flags=re.IGNORECASE)

    def _isBuildRequiresNative(self, line):
        return re.search("^%define *buildrequiresnative", line, flags=re.IGNORECASE)

    def _isNetworkRequired(self, line):
        if re.search("^%define network_required", line, flags=re.IGNORECASE):
            return True
        return False

    def _isBuildIf(self, line):
        if re.search("^%global *build_if", line):
            return True
        return False

    def _isDefinition(self, line):
        return line.startswith(("%define", "%global"))

    def _readConditionalArch(self, line):
        w = line.split()
        if len(w) == 2:
            return w[1]
        return None

    def _readDefinition(self, line):
        listDefines = line.split()
        if len(listDefines) == 3:
            self.defs[listDefines[1]] = self._replaceMacros(listDefines[2])
            return True
        return False

    def _readHeader(self, line):
        headerSplitIndex = line.find(":")
        if headerSplitIndex + 1 == len(line):
            print(line, "\nError:Invalid header")
            return False, None, None
        headerName = line[0:headerSplitIndex].lower()
        headerContent = line[headerSplitIndex + 1 :].strip()  # noqa: E203
        return True, headerName, headerContent

    def _readDependentPackageData(self, line):
        listPackages = line.split(",")
        listdependentpkgs = []
        for line in listPackages:
            line = strUtils.getStringInConditionalBrackets(line)
            listContents = line.split()
            totalContents = len(listContents)
            i = 0
            while i < totalContents:
                dpkg = dependentPackageData()
                dpkg.package = listContents[i]
                if i + 2 < totalContents:
                    if listContents[i + 1] in {">=", "<=", "=", "<", ">", "=="}:
                        dpkg.compare = listContents[i + 1]
                        dpkg.version = listContents[i + 2]
                        i += 3
                    else:
                        i += 1
                else:
                    i += 1
                listdependentpkgs.append(dpkg)
        return listdependentpkgs

    def _readPackageHeaders(self, line, pkg):
        returnVal, headerName, headerContent = self._readHeader(line)
        if not returnVal:
            return False

        headerContent = self._replaceMacros(headerContent)
        if headerName == "summary":
            pkg.summary = headerContent
            return True
        if headerName == "name":
            pkg.name = headerContent
            if pkg == self.packages["default"]:
                self.defs["name"] = pkg.name

            return True
        if headerName == "group":
            pkg.group = headerContent
            return True
        if headerName == "license":
            pkg.license = headerContent
            return True
        if headerName in {"version", "epoch"}:
            if headerName == "epoch":
                self.defs["epoch"] = headerContent
            elif headerName == "version":
                pkg.version = headerContent
                if pkg == self.packages["default"]:
                    self.defs["version"] = pkg.version
            return True
        if headerName == "buildarch":
            pkg.buildarch = headerContent
            return True
        if headerName == "release":
            pkg.release = headerContent
            if pkg == self.packages["default"]:
                self.defs["release"] = pkg.release
            return True
        if headerName == "distribution":
            pkg.distribution = headerContent
            return True
        if headerName == "url":
            pkg.URL = headerContent
            return True
        if "source" in headerName:
            pkg.sources.append(headerContent)
            sourceNum = headerName[6:]
            self.defs[f"SOURCE{sourceNum}"] = headerContent
            return True
        if "patch" in headerName:
            pkg.patches.append(headerContent)
            return True
        if headerName == "provides":
            if pkg.name == "toybox":
                return True
            if headerContent.startswith("/"):
                # Pseudo-package, no version or comparison needed
                capability = dependentPackageData()
                capability.package = headerContent
            else:
                capability = self._readDependentPackageData(headerContent)
                if len(capability) > 1:
                    raise Exception(
                        f"ERROR: Multiple capabilities listed in one Provides: line for {pkg.name}:"
                        + f" {headerContent}. Capabilities: {capability}"
                    )
                capability = capability[0]
            constants.providedBy[capability].append(pkg.name)
            return True
        if headerName in {
            "buildrequires",
            "requires",
        } or headerName.startswith("requires"):
            dpkg = self._readDependentPackageData(headerContent)
            if not dpkg:
                return False
            if headerName.startswith("requires"):
                pkg.requires.extend(dpkg)
            else:
                if self.conditionalCheckMacroEnabled:
                    pkg.checkbuildrequires.extend(dpkg)
                else:
                    # Exclude extrabuildrequires as their spec files may not present
                    # and build will fail to construct a dependency graph.
                    dpkg = list(set(dpkg) - set(pkg.extrabuildrequires))
                    pkg.buildrequires.extend(dpkg)

            return True

        return False

    def _readSecurityHardening(self, line):
        data = line.lower().strip()
        words = data.split()
        nrWords = len(words)
        if nrWords != 3:
            print(f"Error: Unable to parse line: {line}")
            return False
        if words[2] not in {"none", "nonow", "nopie", "nofortify", "nofortify3"}:
            print(f"Error: Invalid security_hardening value: {words[2]}")
            return False
        self.globalSecurityHardening = words[2]
        return True

    def _readNetworkRequired(self, line):
        data = line.lower().strip()
        words = data.split()
        nrWords = len(words)
        if nrWords != 3:
            print("Error: Unable to parse line: " + line)
            return False
        if words[2] != "0" and words[2] != "1":
            print("Error: Invalid network_required value: " + words[2])
            return False
        self.networkRequired = bool(int(words[2]))
        return True

    def _readExtraBuildRequires(self, line, pkg):
        line = self._replaceMacros(line)
        data = line.strip()
        words = data.split(" ", 2)
        if len(words) != 3:
            print(f"Error: Unable to parse line: {line}")
            return False
        dpkg = self._readDependentPackageData(words[2])
        if not dpkg:
            return False
        pkg.extrabuildrequires.extend(dpkg)
        return True

    def _readBuildRequiresNative(self, line, pkg):
        data = line.strip()
        words = data.split(" ", 2)
        if len(words) != 3:
            print(f"Error: Unable to parse line: {line}")
            return False
        dpkg = self._readDependentPackageData(words[2])
        if not dpkg:
            return False
        pkg.buildrequiresnative.extend(dpkg)
        return True

    def _isConditionalCheckMacro(self, line):
        data = line.strip()
        words = data.split()
        if len(words) != 2:
            return False
        if words[0] != "%if" or "with_check" not in words[1]:
            return False
        return True

    def _isIfCondition(self, line):
        return line.startswith("%if ")

    def _isConditionTrue(self, line, full_condition=False):
        words = line.strip().split()
        if len(words) == 1:
            cond = self._replaceMacros(words[0])
            return eval(f"({cond}) != 0")

        cond = ""
        start_word = 0 if full_condition else 1
        for w in words[start_word:]:
            if w in {"==", ">", ">=", "<", "<=", "!=", "||", "&&"}:
                if w == "||":
                    cond = f"{cond} or "
                elif w == "&&":
                    cond = f"{cond} and "
                else:
                    cond = f"{cond} {w} "
            else:
                val = self._replaceMacros(w).lstrip("0")
                if not val:
                    val = "0"
                cond = f"{cond} {val}"

        if not full_condition:
            cond = f"({cond}) != 0"
        return eval(cond)

    def _isConditionalMacroStart(self, line):
        return line.startswith("%if")

    def _isConditionalMacroElse(self, line):
        return line.startswith("%else")

    def _isConditionalMacroEnd(self, line):
        return line.strip() == "%endif"

    def _isInclude(self, line):
        return line.startswith("%include")

    """
    SpecObject generating functions
    @requiresType: "build" for BuildRequires or
                   "install" for Requires dependencies.
    """

    def _getRequiresTypeAllPackages(self, requiresType):
        dependentPackages = []
        for pkg in self.packages.values():
            if requiresType == "build":
                dependentPackages.extend(pkg.buildrequires)
            elif requiresType == "install":
                dependentPackages.extend(pkg.requires)
        listDependentPackages = dependentPackages.copy()
        for pkg in self.packages.values():
            for objName in listDependentPackages:
                if objName.package == pkg.name:
                    dependentPackages.remove(objName)
        return dependentPackages

    def _getCheckBuildRequiresAllPackages(self):
        dependentPackages = []
        for pkg in self.packages.values():
            dependentPackages.extend(pkg.checkbuildrequires)
        return dependentPackages

    def _getExtraBuildRequires(self):
        dependentPackages = []
        for pkg in self.packages.values():
            dependentPackages.extend(pkg.extrabuildrequires)
        return dependentPackages

    def _getBuildRequiresNative(self):
        dependentPackages = []
        for pkg in self.packages.values():
            dependentPackages.extend(pkg.buildrequiresnative)
        return dependentPackages

    def _getPackageNames(self):
        packageNames = []
        for pkg in self.packages.values():
            packageNames.append(pkg.name)
        return packageNames

    def _getSourceNames(self):
        sourceNames = []
        pkg = self.packages.get("default")
        for source in pkg.sources:
            sourceName = strUtils.getFileNameFromURL(source)
            sourceNames.append(sourceName)
        return sourceNames

    def _getPatchNames(self):
        patchNames = []
        pkg = self.packages.get("default")
        for patch in pkg.patches:
            patchName = strUtils.getFileNameFromURL(patch)
            patchNames.append(patchName)
        return patchNames

    def _getSourceURL(self):
        pkg = self.packages.get("default")
        if not pkg.sources:
            return None
        sourceURL = pkg.sources[0]
        if sourceURL.startswith("http") or sourceURL.startswith("ftp"):
            return sourceURL
        return None

    def _getRequires(self, pkgName):
        dependentPackages = []
        for pkg in self.packages.values():
            if pkg.name == pkgName:
                dependentPackages.extend(pkg.requires)
        return dependentPackages

    # Convert parsed data into SpecObject
    def createSpecObject(self):
        specObj = SpecObject()
        specObj.specFile = self.specfile
        defPkg = self.packages.get("default")
        specObj.name = defPkg.name
        specObj.epoch = self.defs.get("epoch", 0)
        specObj.version = f"{defPkg.version}-{defPkg.release}"
        specObj.release = defPkg.release
        specObj.license = defPkg.license
        specObj.summary = defPkg.summary
        specObj.url = defPkg.URL
        specObj.securityHardening = self.globalSecurityHardening
        specObj.networkRequired = self.networkRequired
        specObj.isCheckAvailable = self.checkMacro is not None
        specObj.buildRequires = self._getRequiresTypeAllPackages("build")
        specObj.installRequires = self._getRequiresTypeAllPackages("install")
        specObj.checkBuildRequires = self._getCheckBuildRequiresAllPackages()
        specObj.extraBuildRequires = self._getExtraBuildRequires()
        specObj.buildRequiresNative = self._getBuildRequiresNative()
        specObj.listPackages = self._getPackageNames()
        specObj.listSources = self._getSourceNames()
        specObj.listPatches = self._getPatchNames()
        specObj.sourceurl = self._getSourceURL()

        for pkg in self.packages.values():
            specObj.installRequiresPackages[pkg.name] = pkg.requires
            specObj.buildarch[pkg.name] = pkg.buildarch
            if pkg.filesMacro:
                specObj.listRPMPackages.append(pkg.name)
            specObj.descriptions[pkg.name] = pkg.description

        return specObj


if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser

    usage = "Usage: %prog [options]"
    parser = ArgumentParser(usage)
    parser.add_argument(dest="spec_file", default=None)
    parser.add_argument("-a", "--arch", dest="arch", default="x86_64")
    parser.add_argument("-s", "--subrelease", dest="subrelease", default="92")

    options = parser.parse_args()
    constants.addMacro("photon_subrelease", options.subrelease)
    constants.setSubreleaseVersion(options.subrelease)

    specfile = options.spec_file
    arch = options.arch

    parser = SpecParser(specfile, arch)
    if parser.skipSpec:
        print(f"Skipping spec file: {specfile}")
        sys.exit(0)

    print("========== SpecParser Raw Fields ==========")
    print(f"arch: {parser.arch}")
    print(f"specfile: {parser.specfile}")
    """

    def print_macro(name, macro):
        print(f"\n{name}:")
        if macro is None:
            print("  None")
            return
        print(f"  macroName: {macro.macroName}")
        print(f"  macroFlag: {macro.macroFlag}")
        print(f"  content: {macro.content}")
        print(f"  position: {macro.position}")
        print(f"  endposition: {macro.endposition}")

    print_macro("cleanMacro", parser.cleanMacro)
    print_macro("prepMacro", parser.prepMacro)
    print_macro("buildMacro", parser.buildMacro)
    print_macro("installMacro", parser.installMacro)
    print_macro("changelogMacro", parser.changelogMacro)
    print_macro("checkMacro", parser.checkMacro)
    """

    print(f"packages: {parser.packages}")
    for pkgname, pkg in parser.packages.items():
        print(f"Package '{pkgname}':")
        print(f"  name: {pkg.name}")
        print(f"  version: {pkg.version}")
        print(f"  release: {pkg.release}")
        print(f"  arch: {pkg.buildarch}")
        print(f"  license: {pkg.license}")
        print(f"  sources: {pkg.sources}")
        print(f"  patches: {pkg.patches}")
        print(f"  requires: {pkg.requires}")

    print(f"\nspecAdditionalContent: {parser.specAdditionalContent}")

    print(f"globalSecurityHardening: {parser.globalSecurityHardening}")
    print(f"networkRequired: {parser.networkRequired}")
    print(f"defs: {parser.defs}")
    print(f"conditionalCheckMacroEnabled: {parser.conditionalCheckMacroEnabled}")
    print(f"currentPkg: {parser.currentPkg}")

    print("\n========== SpecObject High-Level Fields ==========")
    specObj = parser.createSpecObject()
    print(f"Spec: {specObj.name}")
    print(f"Version: {specObj.version}")
    print(f"Release: {specObj.release}")
    print(f"Epoch: {specObj.epoch}")
    print(f"License: {specObj.license}")
    print(f"Summary: {specObj.summary}")
    print(f"URL: {specObj.url}")
    print(f"SpecFile: {specObj.specFile}")
    print(f"security_hardening: {specObj.securityHardening}")
    print(f"networkRequired: {specObj.networkRequired}")
    print(f"isCheckAvailable: {specObj.isCheckAvailable}")
    print(f"Source URL: {specObj.sourceurl}")

    print("\n--- Sources ---")
    for src in specObj.listSources:
        print(f"  {src}")

    print("\n--- Patches ---")
    for patch in specObj.listPatches:
        print(f"  {patch}")

    print("\n--- Packages ---")
    for pkg in specObj.listPackages:
        desc = specObj.descriptions.get(pkg, "")
        arch = specObj.buildarch.get(pkg, "")
        print(f"  Package: {pkg}")
        print(f"  Description: {desc}")
        print(f"  BuildArch: {arch}")

    def print_requires(title, requires):
        print(f"\n--- {title} ---")
        for i in requires:
            if i.compare:
                print(f"{i.package} {i.compare} {i.version}")
            else:
                print(f"{i.package}")

    print_requires("Build Requires", specObj.buildRequires)
    print_requires("Install Requires", specObj.installRequires)
    print_requires("Check Build Requires", specObj.checkBuildRequires)
    print_requires("Extra Build Requires", specObj.extraBuildRequires)
    print_requires("Build Requires Native", specObj.buildRequiresNative)
