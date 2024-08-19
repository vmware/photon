#!/usr/bin/env python3

import os
import re

from StringUtils import StringUtils
from constants import constants
from SpecStructures import dependentPackageData, Package, SpecObject

strUtils = StringUtils()


class SpecParser(object):
    class rpmMacro(object):
        def __init__(self):
            self.macroName = ""
            self.macroFlag = ""
            self.content = ""
            self.position = -1
            self.endposition = -1

    def __init__(self, specfile, arch, dist):
        self.arch = arch
        self.dist = dist
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

        self.packages["default"] = Package(self.arch)
        self.currentPkg = "default"
        self._parseSpecFile(self.specfile)

    def _parseSpecFile(self, file):
        with open(file) as specFile:
            lines = specFile.readlines()
            totalLines = len(lines)

        i = 0

        def skip_conditional_body(line):
            deep = 1
            nonlocal i
            while i < totalLines and deep:
                i += 1
                line = lines[i].strip()
                if self._isConditionalMacroStart(line):
                    deep += 1
                elif self._isConditionalMacroEnd(line):
                    deep -= 1

        if not self._isConditionBranch(lines):
            return

        while i < totalLines:
            line = lines[i].strip()
            if self._isConditionalArch(line):
                if self.arch != self._readConditionalArch(line):
                    skip_conditional_body(line)
            elif self._isIfCondition(line):
                if not self._isConditionTrue(line, file):
                    skip_conditional_body(line)
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
            elif self._isChecksum(line):
                self._readChecksum(line, self.packages[self.currentPkg])
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

    def _isConditionBranch(self, lines):
        # Compile the regular expression pattern to match `%global build_for` and capture the value that follows
        pattern = re.compile(r"%global\s+build_for (.+)")

        # Iterate over each line
        for line in lines:
            match = pattern.search(line)
            if match:
                condition = match.group(1).strip()
                return self._evaluateCondition(condition)
        return True

    def _evaluateCondition(self, condition):
        err = ValueError(
            "Invalid condition format. Correct formats are:\n"
            "1. Simple value: ph5\n"
            "2. Negation: !ph5\n"
            "3. List of values: (ph5, ph6)\n"
            "4. Negation list: !(ph5, ph6)\n"
            "5. All: all\n"
            "6. None: none\n"
            "Examples:\n"
            "   %global build_for ph5\n"
            "   %global build_for !ph5\n"
            "   %global build_for (ph5, ph6)\n"
            "   %global build_for !(ph4, ph6)\n"
            "   %global build_for all\n"
            "   %global build_for none"
        )
        # Handle conditions with 'all' and 'none'
        if condition.lower() == "all":
            return True
        if condition.lower() == "none":
            return False

        # Handle negation cases (starting with '!')
        if condition.startswith("!"):
            sub_condition = condition[1:].strip()
            return not self._evaluateCondition(sub_condition)

        # Handle lists within parentheses
        if condition.startswith("(") and condition.endswith(")"):
            options = condition[1:-1].strip()
            # Handle the case where nested parentheses or negation inside parentheses
            if "!" in options or "(" in options or ")" in options:
                raise err
            options_list = [opt.strip() for opt in options.split(",")]
            return self.dist in options_list

        # Handle the case where it's neither a list nor a simple value
        if "," in condition or "(" in condition or ")" in condition:
            raise err

        return self.dist == condition

    def _isConditionalArch(self, line):
        return re.search("^%ifarch", line)

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
            "^version:",
            "^release:",
            "^distribution:",
            "^requires:",
            r"^requires\((pre|post|preun|postun)\):",
            "^provides:",
            "^obsoletes:",
            "^conflicts:",
            "^url:",
            "^source[0-9]*:",
            "^patch[0-9]*:",
            "^buildrequires:",
            "^buildprovides:",
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

    def _isChecksum(self, line):
        w = line.split()
        if len(w) != 3 or w[0] != "%define" or w[1] not in {"sha1", "sha512"}:
            return False
        return re.match(".*=[a-z0-9]+$", w[2])

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
                compare = None
                packageName = listContents[i]
                provider = constants.providedBy.get(listContents[i], None)
                if listContents[i].startswith("/"):
                    if not provider:
                        raise Exception(
                            f"Error in {self.specfile}\n"
                            f"What package does provide {listContents[i]} ? "
                            "Please modify providedBy in constants.py"
                        )
                    packageName = provider
                    i += 1
                elif provider:
                    packageName = provider
                    i += 2
                if i + 2 < len(listContents):
                    if listContents[i + 1] in (">=", "<=", "=", "<", ">"):
                        compare = listContents[i + 1]

                dpkg.package = packageName
                if compare:
                    dpkg.compare = compare
                    dpkg.version = listContents[i + 2]
                    i += 3
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
        if headerName == "version":
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
        if (
            headerName.startswith("requires")
            or headerName == "provides"
            or headerName == "obsoletes"
            or headerName == "conflicts"
            or headerName == "buildrequires"
            or headerName == "buildprovides"
        ):
            dpkg = self._readDependentPackageData(headerContent)
            if not dpkg:
                return False
            if headerName.startswith("requires"):
                pkg.requires.extend(dpkg)
            if headerName == "obsoletes":
                pkg.obsoletes.extend(dpkg)
            elif headerName == "conflicts":
                pkg.conflicts.extend(dpkg)
            elif headerName == "provides":
                pkg.provides.extend(dpkg)
            elif headerName == "buildrequires":
                if self.conditionalCheckMacroEnabled:
                    pkg.checkbuildrequires.extend(dpkg)
                else:
                    pkg.buildrequires.extend(dpkg)
            if headerName == "buildprovides":
                pkg.buildprovides.extend(dpkg)

            return True
        return False

    def _readSecurityHardening(self, line):
        data = line.lower().strip()
        words = data.split()
        nrWords = len(words)
        if nrWords != 3:
            print(f"Error: Unable to parse line: {line}")
            return False
        if words[2] not in {"none", "nonow", "nopie", "nofortify"}:
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

    def _readChecksum(self, line, pkg):
        line = self._replaceMacros(line)
        data = line.strip()
        words = data.split()
        nrWords = len(words)
        if nrWords != 3:
            print(f"Error: Unable to parse line: {line}")
            return False
        value = words[2].split("=")
        if len(value) != 2:
            print(f"Error: Unable to parse line: {line}")
            return False
        matchedSources = []
        for source in pkg.sources:
            sourceName = strUtils.getFileNameFromURL(source)
            if sourceName.startswith(value[0]):
                matchedSources.append(sourceName)
        if not matchedSources:
            print(f"Error: Can not find match for checksum {value[0]}")
            return False
        if len(matchedSources) > 1:
            print(
                "Error: Too many matched Sources:"
                + " ".join(matchedSources)
                + f" for checksum {value[0]}"
            )
            return False
        pkg.checksums[sourceName] = {words[1]: value[1]}
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

    def _isConditionTrue(self, line, spec_fn):
        words = line.strip().split()
        if len(words) < 2:
            raise Exception(f"Bad if condition {line} in {spec_fn}")

        cond = ""
        for w in words[1:]:
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

        cond = f"({cond}) != 0"
        return eval(cond)

    def _isConditionalMacroStart(self, line):
        return line.startswith("%if")

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
        specObj.version = f"{defPkg.version}-{defPkg.release}"
        specObj.release = defPkg.release
        specObj.checksums = defPkg.checksums
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
