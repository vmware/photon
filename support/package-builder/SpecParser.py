import re
import platform
from StringUtils import StringUtils
from SpecStructures import *
from constants import constants

class SpecParser(object):

    def __init__(self):
        self.cleanMacro = rpmMacro().setName("clean")
        self.prepMacro = rpmMacro().setName("prep")
        self.buildMacro = rpmMacro().setName("build")
        self.installMacro = rpmMacro().setName("install")
        self.changelogMacro = rpmMacro().setName("changelog")
        self.checkMacro = rpmMacro().setName("check")
        self.packages = {}
        self.specAdditionalContent = ""
        self.globalSecurityHardening = ""
        self.defs = {}
        self.conditionalCheckMacroEnabled = False
        self.macro_pattern = re.compile(r'%{(\S+?)\}')


    def readPkgNameFromPackageMacro(self, data, basePkgName=None):
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

    def replaceMacros(self, string):
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
            return (macro in self.defs.keys()) or (macro in constants.userDefinedMacros.keys())

        def _get_macro(macro):
            if macro in self.defs.keys():
                return self.defs[macro]
            elif macro in constants.userDefinedMacros.keys():
                return constants.userDefinedMacros[macro]
            raise Exception("Unknown macro: " + macro)

        def _macro_repl(match):
            macro_name = match.group(1)
            if _is_conditional(macro_name):
                parts = macro_name[1:].split(":")
                assert len(parts) > 0
                if _test_conditional(macro_name):  # ?
                    if _is_macro_defined(parts[0]):
                        if len(parts) == 2:
                            return parts[1]
                        else:
                            return _get_macro(parts[0])
                    else:
                        return ""
                else:  # !
                    if not _is_macro_defined(parts[0]):
                        if len(parts) == 2:
                            return parts[1]
                    return ""

            if _is_macro_defined(macro_name):
                return _get_macro(macro_name)
            return match.string[match.start():match.end()]

        #User macros
        for macroName in constants.userDefinedMacros.keys():
            value = constants.userDefinedMacros[macroName]
            macro = "%" + macroName
            if string.find(macro) != -1:
                string = string.replace(macro, value)
        #Spec definitions
        for macroName in self.defs.keys():
            value = self.defs[macroName]
            macro = "%" + macroName
            if string.find(macro) != -1:
                string = string.replace(macro, value)
        return re.sub(self.macro_pattern, _macro_repl, string)

    def parseSpecFile(self, specfile):
        self.createDefaultPackage()
        currentPkg = "default"
        with open(specfile) as specFile:
            lines = specFile.readlines()
            totalLines = len(lines)
            i = 0
            while i < totalLines:
                line = lines[i].strip()
                if self.isConditionalArch(line):
                    if platform.machine() != self.readConditionalArch(line):
                        # skip conditional body
                        deep = 1
                        while i < totalLines and deep != 0:
                            i = i + 1
                            line = lines[i].strip()
                            if self.isConditionalMacroStart(line):
                                deep = deep + 1
                            elif self.isConditionalMacroEnd(line):
                                deep = deep - 1
                elif self.isIfCondition(line):
                    if not self.isConditionTrue(line):
                        # skip conditional body
                        deep = 1
                        while i < totalLines and deep != 0:
                            i = i + 1
                            line = lines[i].strip()
                            if self.isConditionalMacroStart(line):
                                deep = deep + 1
                            elif self.isConditionalMacroEnd(line):
                                deep = deep - 1
                elif self.isSpecMacro(line):
                    macro, i = self.readMacroFromFile(i, lines)
                    self.updateMacro(macro)
                elif self.isPackageMacro(line):
                    defaultpkg = self.packages.get('default')
                    returnVal, packageName = self.readPkgNameFromPackageMacro(line, defaultpkg.name)
                    packageName = self.replaceMacros(packageName)
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
                        macro, i = self.readMacroFromFile(i, lines)
                        if packageName not in self.packages:
                            i = i + 1
                            continue
                        self.packages[packageName].updatePackageMacro(macro)
                elif self.isPackageHeaders(line):
                    self.readPackageHeaders(line, self.packages[currentPkg])
                elif self.isGlobalSecurityHardening(line):
                    self.readSecurityHardening(line)
                elif self.isChecksum(line):
                    self.readChecksum(line, self.packages[currentPkg])
                elif self.isDefinition(line):
                    self.readDefinition(line)
                elif self.isConditionalCheckMacro(line):
                    self.conditionalCheckMacroEnabled = True
                elif self.conditionalCheckMacroEnabled and self.isConditionalMacroEnd(line):
                    self.conditionalCheckMacroEnabled = False
                else:
                    self.specAdditionalContent += line + "\n"
                i = i + 1

    def createDefaultPackage(self):
        pkg = Package()
        self.packages["default"] = pkg

    def readMacroFromFile(self, currentPos, lines):
        macro = rpmMacro()
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

        if currentPos + 1 < len(lines) and self.isMacro(lines[currentPos+1]):
            return macro, currentPos

        for j in range(currentPos + 1, endPos):
            content = lines[j]
            if j+1 < endPos and self.isMacro(lines[j+1]):
                return macro, j
            macro.content += content +'\n'
            macro.endposition = j
        return macro, endPos

    def updateMacro(self, macro):
        if macro.macroName == "%clean":
            self.cleanMacro = macro
            return True
        if macro.macroName == "%prep":
            self.prepMacro = macro
            return True
        if macro.macroName == "%build":
            self.buildMacro = macro
            return True
        if macro.macroName == "%install":
            self.installMacro = macro
            return True
        if macro.macroName == "%changelog":
            self.changelogMacro = macro
            return True
        if macro.macroName == "%check":
            self.checkMacro = macro
            return True
        return False

    def isMacro(self, line):
        return (self.isPackageMacro(line) or
                self.isSpecMacro(line) or
                self.isConditionalMacroStart(line) or
                self.isConditionalMacroEnd(line))

    def isConditionalArch(self, line):
        if re.search('^'+'%ifarch', line):
            return True
        return False

    def isSpecMacro(self, line):
        if line.startswith(('%clean', '%prep', '%build', '%install', '%changelog', '%check')):
            return True
        return False

    def isPackageMacro(self, line):
        line = line.strip()
        if line.startswith(('%post', '%postun', '%files', '%description', '%package')):
            return True
        return False

    def isPackageHeaders(self, line):
        headersPatterns = ['^summary:', '^name:', '^group:',
                           '^license:', '^version:', '^release:',
                           '^distribution:', '^requires:',
                           '^requires\((pre|post|preun|postun)\):',
                           '^provides:', '^obsoletes:', '^conflicts:',
                           '^url:', '^source[0-9]*:', '^patch[0-9]*:',
                           '^buildrequires:', '^buildprovides:',
                           '^buildarch:']
        if any([re.search(r, line, flags=re.IGNORECASE) for r in headersPatterns]):
            return True
        return False

    def isGlobalSecurityHardening(self, line):
        if re.search('^%global *security_hardening', line, flags=re.IGNORECASE):
            return True
        return False

    def isChecksum(self, line):
        if re.search('^%define *sha1', line, flags=re.IGNORECASE):
            return True
        return False

    def isDefinition(self, line):
        if line.startswith(('%define', '%global')):
            return True
        return False

    def readConditionalArch(self, line):
        w = line.split()
        if len(w) == 2:
            return w[1]
        return None

    def readDefinition(self, line):
        listDefines = line.split()
        if len(listDefines) == 3:
            self.defs[listDefines[1]] = self.replaceMacros(listDefines[2])
            return True
        return False

    def readHeader(self, line):
        headerSplitIndex = line.find(":")
        if headerSplitIndex + 1 == len(line):
            print(line)
            print("Error:Invalid header")
            return False, None, None
        headerName = line[0:headerSplitIndex].lower()
        headerContent = line[headerSplitIndex + 1:].strip()
        return True, headerName, headerContent

    def readDependentPackageData(self, line):
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
                    i += 1
                    if provider is not None:
                        packageName = provider
                    else:
                        continue
                if i+2 < len(listContents):
                    if listContents[i+1] == ">=":
                        compare = "gte"
                    elif listContents[i+1] == "<=":
                        compare = "lte"
                    elif listContents[i+1] == "==":
                        compare = "eq"
                    elif listContents[i+1] == "<":
                        compare = "lt"
                    elif listContents[i+1] == ">":
                        compare = "gt"
                    elif listContents[i+1] == "=":
                        compare = "eq"

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

    def readPackageHeaders(self, line, pkg):
        returnVal, headerName, headerContent = self.readHeader(line)
        if not returnVal:
            return False

        headerContent = self.replaceMacros(headerContent)
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
        if headerName.find('source') != -1:
            pkg.sources.append(headerContent)
            return True
        if headerName.find('patch') != -1:
            pkg.patches.append(headerContent)
            return True
        if (headerName.startswith('requires') or
                headerName == 'provides' or
                headerName == 'obsoletes' or
                headerName == 'conflicts' or
                headerName == 'buildrequires' or
                headerName == 'buildprovides'):
            dpkg = self.readDependentPackageData(headerContent)
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

    def readSecurityHardening(self, line):
        data = line.lower().strip()
        words = data.split(" ")
        nrWords = len(words)
        if nrWords != 3:
            print("Error: Unable to parse line: " + line)
            return False
        if words[2] != "none" and words[2] != "nonow" and words[2] != "nopie":
            print("Error: Invalid security_hardening value: " + words[2])
            return False
        self.globalSecurityHardening = words[2]
        return True

    def readChecksum(self, line, pkg):
        strUtils = StringUtils()
        line = self.replaceMacros(line)
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
            if (sourceName.startswith(value[0])):
                matchedSources.append(sourceName)
        if (len(matchedSources) == 0):
            print("Error: Can not find match for sha1 " + value[0])
            return False
        if (len(matchedSources) > 1):
            print("Error: Too many matched Sources:" +
                  ' '.join(matchedSources) + " for sha1 " + value[0])
            return False
        pkg.checksums[sourceName] = value[1]
        return True;

    def isConditionalCheckMacro(self, line):
        data = line.strip()
        words = data.split()
        nrWords = len(words)
        if(nrWords != 2):
            return False
        if(words[0] != "%if" or words[1] != "%{with_check}"):
            return False
        return True

    def isIfCondition(self,line):
        return line.startswith("%if ")

    # Supports only %if %{}
    def isConditionTrue(self,line):
        data = line.strip()
        words = data.split()
        nrWords = len(words)
        # condition like %if a > b is not supported
        if(nrWords != 2):
            return True
        if (self.replaceMacros(words[1]) == "0"):
            return False
        return True

    def isConditionalMacroStart(self, line):
        return line.startswith("%if")

    def isConditionalMacroEnd(self, line):
        return (line.strip() == "%endif")
