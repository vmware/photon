# pylint: disable=invalid-name,missing-docstring
import re
import platform
from StringUtils import StringUtils
from SpecStructures import dependentPackageData, Package, SpecObject
from constants import constants

class SpecParser(object):

    class rpmMacro(object):
        def __init__(self):
            self.macroName = ""
            self.macroFlag = ""
            self.content = ""
            self.position = -1
            self.endposition = -1

    def __init__(self, specfile):
        self.cleanMacro = None
        self.prepMacro = None
        self.buildMacro = None
        self.installMacro = None
        self.changelogMacro = None
        self.checkMacro = None
        self.packages = {}
        self.specAdditionalContent = ""
        self.globalSecurityHardening = ""
        self.defs = {}
        self.conditionalCheckMacroEnabled = False
        self.macro_pattern = re.compile(r'%{(\S+?)\}')
        self.specfile = specfile

        self._parseSpecFile()

    def _parseSpecFile(self):
        self.packages["default"] = Package()
        currentPkg = "default"
        with open(self.specfile) as specFile:
            lines = specFile.readlines()
            totalLines = len(lines)
            i = 0
            while i < totalLines:
                line = lines[i].strip()
                if self._isConditionalArch(line):
                    if platform.machine() != self._readConditionalArch(line):
                        # skip conditional body
                        deep = 1
                        while i < totalLines and deep != 0:
                            i = i + 1
                            line = lines[i].strip()
                            if self._isConditionalMacroStart(line):
                                deep = deep + 1
                            elif self._isConditionalMacroEnd(line):
                                deep = deep - 1
                elif self._isIfCondition(line):
                    if not self._isConditionTrue(line):
                        # skip conditional body
                        deep = 1
                        while i < totalLines and deep != 0:
                            i = i + 1
                            line = lines[i].strip()
                            if self._isConditionalMacroStart(line):
                                deep = deep + 1
                            elif self._isConditionalMacroEnd(line):
                                deep = deep - 1
                elif self._isSpecMacro(line):
                    macro, i = self._readMacroFromFile(i, lines)
                    self._updateSpecMacro(macro)
                elif self._isPackageMacro(line):
                    defaultpkg = self.packages.get('default')
                    returnVal, packageName = self._readPkgNameFromPackageMacro(line,
                                                                               defaultpkg.name)
                    packageName = self._replaceMacros(packageName)
                    if not returnVal:
                        return False
                    if line.startswith('%package'):
                        pkg = Package(defaultpkg)
                        pkg.name = packageName
                        currentPkg = packageName
                        self.packages[pkg.name] = pkg
                    else:
                        if defaultpkg.name == packageName:
                            packageName = 'default'
                        macro, i = self._readMacroFromFile(i, lines)
                        if packageName not in self.packages:
                            i = i + 1
                            continue
                        self.packages[packageName].updatePackageMacro(macro)
                elif self._isPackageHeaders(line):
                    self._readPackageHeaders(line, self.packages[currentPkg])
                elif self._isGlobalSecurityHardening(line):
                    self._readSecurityHardening(line)
                elif self._isChecksum(line):
                    self._readChecksum(line, self.packages[currentPkg])
                elif self._isExtraBuildRequires(line):
                    self._readExtraBuildRequires(line, self.packages[currentPkg])
                elif self._isDefinition(line):
                    self._readDefinition(line)
                elif self._isConditionalCheckMacro(line):
                    self.conditionalCheckMacroEnabled = True
                elif self.conditionalCheckMacroEnabled and self._isConditionalMacroEnd(line):
                    self.conditionalCheckMacroEnabled = False
                else:
                    self.specAdditionalContent += line + "\n"
                i = i + 1

    def _readPkgNameFromPackageMacro(self, data, basePkgName=None):
        data = " ".join(data.split())
        pkgHeaderName = data.split(" ")
        lenpkgHeaderName = len(pkgHeaderName)
        i = 1
        pkgName = None
        while i < lenpkgHeaderName:
            if pkgHeaderName[i] == "-n" and i+1 < lenpkgHeaderName:
                pkgName = pkgHeaderName[i+1]
                break
            if pkgHeaderName[i].startswith('-'):
                i = i + 2
            else:
                pkgName = basePkgName + "-" + pkgHeaderName[i]
                break
        if pkgName is None:
            return True, basePkgName
        return True, pkgName

    def _replaceMacros(self, string):
        """Replace all macros in given string with corresponding values.

        For example: a string '%{name}-%{version}.tar.gz' will be transformed to 'foo-2.0.tar.gz'.

        :return A string where all macros in given input are substituted as good as possible.

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
            return (macro in self.defs.keys()) or (macro in constants.userDefinedMacros.keys()) \
                or (macro in constants.getAdditionalMacros(self.packages["default"].name).keys())

        def _get_macro(macro):
            if macro in self.defs.keys():
                return self.defs[macro]
            elif macro in constants.userDefinedMacros.keys():
                return constants.userDefinedMacros[macro]
            elif macro in constants.getAdditionalMacros(self.packages["default"].name).keys():
                return constants.getAdditionalMacros(self.packages["default"].name)[macro]
            raise Exception("Unknown macro: " + macro)

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
                    if not _is_macro_defined(parts[0]):
                        if len(parts) == 2:
                            retv = parts[1]
                return retv

            if _is_macro_defined(macro_name):
                return _get_macro(macro_name)
            return match.string[match.start():match.end()]

        #User macros
        for macroName, value in constants.userDefinedMacros.items():
            macro = "%" + macroName
            if string.find(macro) != -1:
                string = string.replace(macro, value)
        #Spec definitions
        for macroName, value in self.defs.items():
            macro = "%" + macroName
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
            macro.macroFlag = line[flagindex+1:]
            macro.macroName = line[:flagindex]
        else:
            macro.macroName = line

        if currentPos + 1 < len(lines) and self._isMacro(lines[currentPos+1]):
            return macro, currentPos

        for j in range(currentPos + 1, endPos):
            content = lines[j]
            if j+1 < endPos and self._isMacro(lines[j+1]):
                return macro, j
            macro.content += content +'\n'
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
        return (self._isPackageMacro(line) or
                self._isSpecMacro(line) or
                self._isConditionalMacroStart(line) or
                self._isConditionalMacroEnd(line))

    def _isConditionalArch(self, line):
        if re.search('^'+'%ifarch', line):
            return True
        return False

    def _isSpecMacro(self, line):
        if line.startswith(('%clean', '%prep', '%build', '%install', '%changelog', '%check')):
            return True
        return False

    def _isPackageMacro(self, line):
        line = line.strip()
        if line.startswith(('%post', '%postun', '%files', '%description', '%package')):
            return True
        return False

    def _isPackageHeaders(self, line):
        headersPatterns = ['^summary:', '^name:', '^group:',
                           '^license:', '^version:', '^release:',
                           '^distribution:', '^requires:',
                           r'^requires\((pre|post|preun|postun)\):',
                           '^provides:', '^obsoletes:', '^conflicts:',
                           '^url:', '^source[0-9]*:', '^patch[0-9]*:',
                           '^buildrequires:', '^buildprovides:',
                           '^buildarch:']
        if any([re.search(r, line, flags=re.IGNORECASE) for r in headersPatterns]):
            return True
        return False

    def _isGlobalSecurityHardening(self, line):
        if re.search('^%global *security_hardening', line, flags=re.IGNORECASE):
            return True
        return False

    def _isExtraBuildRequires(self, line):
        if re.search('^%define *extrabuildrequires', line, flags=re.IGNORECASE):
            return True
        return False

    def _isChecksum(self, line):
        if re.search('^%define *sha1', line, flags=re.IGNORECASE):
            return True
        return False

    def _isDefinition(self, line):
        if line.startswith(('%define', '%global')):
            return True
        return False

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
            print(line)
            print("Error:Invalid header")
            return False, None, None
        headerName = line[0:headerSplitIndex].lower()
        headerContent = line[headerSplitIndex + 1:].strip()
        return True, headerName, headerContent

    def _readDependentPackageData(self, line):
        strUtils = StringUtils()
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
                if listContents[i].startswith("/"):
                    provider = constants.providedBy.get(listContents[i], None)
                    if provider is not None:
                        packageName = provider
                    else:
                        raise Exception('Which package provides %s? Please modify providedBy in constants.py' % (listContents[i]))
                    i += 1
                if i + 2 < len(listContents):
                    if listContents[i+1] in (">=", "<=", "=", "<", ">"):
                        compare = listContents[i+1]

                if compare is not None:
                    dpkg.package = packageName
                    dpkg.compare = compare
                    dpkg.version = listContents[i+2]
                    i = i + 3
                else:
                    dpkg.package = packageName
                    i = i + 1
                listdependentpkgs.append(dpkg)
        return listdependentpkgs

    def _readPackageHeaders(self, line, pkg):
        returnVal, headerName, headerContent = self._readHeader(line)
        if not returnVal:
            return False

        headerContent = self._replaceMacros(headerContent)
        if headerName == 'summary':
            pkg.summary = headerContent
            return True
        if headerName == 'name':
            pkg.name = headerContent
            if pkg == self.packages["default"]:
                self.defs["name"] = pkg.name
            return True
        if headerName == 'group':
            pkg.group = headerContent
            return True
        if headerName == 'license':
            pkg.license = headerContent
            return True
        if headerName == 'version':
            pkg.version = headerContent
            if pkg == self.packages["default"]:
                self.defs["version"] = pkg.version
            return True
        if headerName == 'buildarch':
            pkg.buildarch = headerContent
            return True
        if headerName == 'release':
            pkg.release = headerContent
            if pkg == self.packages["default"]:
                self.defs["release"] = pkg.release
            return True
        if headerName == 'distribution':
            pkg.distribution = headerContent
            return True
        if headerName == 'url':
            pkg.URL = headerContent
            return True
        if 'source' in headerName:
            pkg.sources.append(headerContent)
            return True
        if 'patch' in headerName:
            pkg.patches.append(headerContent)
            return True
        if (headerName.startswith('requires') or
                headerName == 'provides' or
                headerName == 'obsoletes' or
                headerName == 'conflicts' or
                headerName == 'buildrequires' or
                headerName == 'buildprovides'):
            dpkg = self._readDependentPackageData(headerContent)
            if dpkg is None:
                return False
            if headerName.startswith('requires'):
                pkg.requires.extend(dpkg)
            if headerName == 'provides':
                pkg.provides.extend(dpkg)
            if headerName == 'obsoletes':
                pkg.obsoletes.extend(dpkg)
            if headerName == 'conflicts':
                pkg.conflicts.extend(dpkg)
            if headerName == 'buildrequires':
                if self.conditionalCheckMacroEnabled:
                    pkg.checkbuildrequires.extend(dpkg)
                else:
                    pkg.buildrequires.extend(dpkg)
            if headerName == 'buildprovides':
                pkg.buildprovides.extend(dpkg)

            return True
        return False

    def _readSecurityHardening(self, line):
        data = line.lower().strip()
        words = data.split(" ")
        nrWords = len(words)
        if nrWords != 3:
            print("Error: Unable to parse line: " + line)
            return False
        if words[2] != "none" and words[2] != "nonow" and \
                words[2] != "nopie" and words[2] != "nofortify":
            print("Error: Invalid security_hardening value: " + words[2])
            return False
        self.globalSecurityHardening = words[2]
        return True

    def _readExtraBuildRequires(self, line, pkg):
        data = line.strip()
        words = data.split(" ", 2)
        if len(words) != 3:
            print("Error: Unable to parse line: " + line)
            return False
        dpkg = self._readDependentPackageData(words[2])
        if dpkg is None:
            return False
        pkg.extrabuildrequires.extend(dpkg)
        return True

    def _readChecksum(self, line, pkg):
        strUtils = StringUtils()
        line = self._replaceMacros(line)
        data = line.strip()
        words = data.split()
        nrWords = len(words)
        if nrWords != 3:
            print("Error: Unable to parse line: " + line)
            return False
        value = words[2].split("=")
        if len(value) != 2:
            print("Error: Unable to parse line: "+line)
            return False
        matchedSources = []
        for source in pkg.sources:
            sourceName = strUtils.getFileNameFromURL(source)
            if sourceName.startswith(value[0]):
                matchedSources.append(sourceName)
        if not matchedSources:
            print("Error: Can not find match for sha1 " + value[0])
            return False
        if len(matchedSources) > 1:
            print("Error: Too many matched Sources:" +
                  ' '.join(matchedSources) + " for sha1 " + value[0])
            return False
        pkg.checksums[sourceName] = value[1]
        return True

    def _isConditionalCheckMacro(self, line):
        data = line.strip()
        words = data.split()
        nrWords = len(words)
        if nrWords != 2:
            return False
        if words[0] != "%if" or words[1] != "%{with_check}":
            return False
        return True

    def _isIfCondition(self, line):
        return line.startswith("%if ")

    # Supports only %if %{}
    def _isConditionTrue(self, line):
        data = line.strip()
        words = data.split()
        nrWords = len(words)
        # condition like %if a > b is not supported
        if nrWords != 2:
            return True
        if self._replaceMacros(words[1]) == "0":
            return False
        return True

    def _isConditionalMacroStart(self, line):
        return line.startswith("%if")

    def _isConditionalMacroEnd(self, line):
        return line.strip() == "%endif"

    ########################################################################
    # SpecObject generating functions
    ########################################################################

    #
    # @requiresType: "build" for BuildRequires or
    #                "install" for Requires dependencies.
    def _getRequiresTypeAllPackages(self, requiresType):
        dependentPackages = []
        for pkg in self.packages.values():
            if requiresType == "build":
                dependentPackages.extend(pkg.buildrequires)
            elif requiresType == "install":
                dependentPackages.extend(pkg.requires)
        listDependentPackages = dependentPackages.copy()
        packageNames = self._getPackageNames()
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

    def _getPackageNames(self):
        packageNames = []
        for pkg in self.packages.values():
            packageNames.append(pkg.name)
        return packageNames

    def _getSourceNames(self):
        sourceNames = []
        strUtils = StringUtils()
        pkg = self.packages.get('default')
        for source in pkg.sources:
            sourceName = strUtils.getFileNameFromURL(source)
            sourceNames.append(sourceName)
        return sourceNames

    def _getPatchNames(self):
        patchNames = []
        strUtils = StringUtils()
        pkg = self.packages.get('default')
        for patch in pkg.patches:
            patchName = strUtils.getFileNameFromURL(patch)
            patchNames.append(patchName)
        return patchNames

    def _getSourceURL(self):
        pkg = self.packages.get('default')
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
        defPkg = self.packages.get('default')
        specObj.name = defPkg.name
        specObj.version = defPkg.version
        specObj.release = defPkg.release
        specObj.checksums = defPkg.checksums
        specObj.license = defPkg.license
        specObj.url = defPkg.URL
        specObj.securityHardening = self.globalSecurityHardening
        specObj.isCheckAvailable = self.checkMacro is not None
        specObj.buildRequires = self._getRequiresTypeAllPackages("build")
        specObj.installRequires = self._getRequiresTypeAllPackages("install")
        specObj.checkBuildRequires = self._getCheckBuildRequiresAllPackages()
        specObj.extraBuildRequires = self._getExtraBuildRequires()
        specObj.listPackages = self._getPackageNames()
        specObj.listSources = self._getSourceNames()
        specObj.listPatches = self._getPatchNames()
        specObj.sourceurl = self._getSourceURL()

        for pkg in self.packages.values():
            specObj.installRequiresPackages[pkg.name] = pkg.requires
            specObj.buildarch[pkg.name] = pkg.buildarch
            if pkg.filesMacro:
                specObj.listRPMPackages.append(pkg.name)

        return specObj
