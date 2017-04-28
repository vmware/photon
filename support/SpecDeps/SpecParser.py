import re
from StringUtils import StringUtils
from SpecStructures import *

class SpecParser(object):
    def __init__(self):
        self.cleanMacro=rpmMacro().setName("clean")
        self.prepMacro=rpmMacro().setName("prep")
        self.buildMacro=rpmMacro().setName("build")
        self.installMacro=rpmMacro().setName("install")
        self.changelogMacro=rpmMacro().setName("changelog")
        self.checkMacro=rpmMacro().setName("check")
        self.packages={}
        self.specAdditionalContent=""
        self.globalSecurityHardening=""
        
    
    def readPkgNameFromPackageMacro(self,data,basePkgName=None):
        data=" ".join(data.split())
        pkgHeaderName=data.split(" ")
        lenpkgHeaderName = len(pkgHeaderName)
        
        if (lenpkgHeaderName >= 3 and pkgHeaderName[1] != "-n"):
            lenpkgHeaderName = 1
        if (lenpkgHeaderName == 2 or lenpkgHeaderName == 1 ) and basePkgName is None :
            print "Invalid basePkgName"
            return False,None
        if lenpkgHeaderName == 3 :
            return True,pkgHeaderName[2]
        if lenpkgHeaderName == 2 :
            return True,basePkgName + "-"+pkgHeaderName[1]
        if lenpkgHeaderName == 1:
            return True, basePkgName
    
    def parseSpecFile(self,specfile):
        self.createDefaultPackage()
        currentPkg="default"
        specFile = open(specfile)
        lines = specFile.readlines()
        totalLines=len(lines)
        i=0
        while i < totalLines:
            line = lines[i].strip()
            if self.isSpecMacro(line):
                macro,i=self.readMacroFromFile(i, lines)
                self.updateMacro(macro)
            elif self.isPackageMacro(line):
                defaultpkg = self.packages.get('default')
                returnVal,packageName=self.readPkgNameFromPackageMacro(line, defaultpkg.name)
                packageName=defaultpkg.decodeContents(packageName)
                if not returnVal:
                    return False
                if re.search('^'+'%package',line) :
                    pkg = Package(defaultpkg)
                    pkg.name=packageName
                    currentPkg=packageName
                    self.packages[pkg.name]=pkg
                else:
                    if defaultpkg.name == packageName :
                        packageName = 'default'
                    if packageName not in self.packages:
                        return False
                    macro,i=self.readMacroFromFile(i, lines)
                    self.packages[packageName].updatePackageMacro(macro)
            elif self.isPackageHeaders(line):
                self.readPackageHeaders(line, self.packages[currentPkg])
            elif self.isGlobalSecurityHardening(line):
                self.readSecurityHardening(line)
            else:
                self.specAdditionalContent+=line+"\n"
            i=i+1
        specFile.close()
    
    def createDefaultPackage(self):
        pkg = Package()
        self.packages["default"]=pkg
    
    def readMacroFromFile(self,currentPos,lines):
        macro = rpmMacro()
        line = lines[currentPos]
        macro.position = currentPos
        macro.endposition=currentPos
        endPos=len(lines)
        line = " ".join(line.split())
        flagindex = line.find(" ")
        if flagindex != -1:
            macro.macroFlag=line[flagindex+1:]
            macro.macroName=line[:flagindex]
        else:
            macro.macroName=line

        if currentPos+1 < len(lines) and self.isMacro(lines[currentPos+1]):
            return macro,currentPos
            
        for j in range(currentPos+1,endPos):
            content = lines[j]
            if j+1 < endPos and self.isMacro(lines[j+1]):
                return macro,j
            macro.content += content +'\n'
            macro.endposition=j
        return macro,endPos
        

    def updateMacro(self,macro):
        if macro.macroName == "%clean":
            self.cleanMacro=macro
            return True
        if macro.macroName == "%prep":
            self.prepMacro=macro
            return True
        if macro.macroName == "%build":
            self.buildMacro=macro
            return True
        if macro.macroName == "%install":
            self.installMacro=macro
            return True
        if macro.macroName == "%changelog":
            self.changelogMacro=macro
            return True
        if macro.macroName == "%check":
            self.checkMacro=macro
            return True
        return False
            
    def isMacro(self,line):
        return self.isPackageMacro(line) or self.isSpecMacro(line)
    
    def isSpecMacro(self,line):
        if re.search('^'+'%clean',line) :
            return True
        elif re.search('^'+'%prep',line) :
            return True            
        elif re.search('^'+'%build',line) :
            return True
        elif re.search('^'+'%install',line) :
            return True
        elif re.search('^'+'%changelog',line) :
            return True
        elif re.search('^'+'%check',line) :
            return True
        return False
    
    def isPackageMacro(self,line):
        line=line.strip()
# What is the point of this function?
# Why does it track post/postun sections?
#        if re.search('^'+'%post',line) :
#            return True
#        elif re.search('^'+'%postun',line) :
#            return True
        if re.search('^'+'%files',line) :
            return True
        elif re.search('^'+'%description',line) :
            return True
        elif re.search('^'+'%package',line) :
            return True
        return False
    
    def isPackageHeaders(self,line):
        if re.search('^'+'summary:',line,flags=re.IGNORECASE) :
            return True
        elif re.search('^'+'name:',line,flags=re.IGNORECASE) :
            return True
        elif re.search('^'+'group:',line,flags=re.IGNORECASE) :
            return True
        elif re.search('^'+'license:',line,flags=re.IGNORECASE) :
            return True
        elif re.search('^'+'version:',line,flags=re.IGNORECASE) :
            return True
        elif re.search('^'+'release:',line,flags=re.IGNORECASE) :
            return True
        elif re.search('^'+'distribution:',line,flags=re.IGNORECASE) :
            return True
        elif re.search('^'+'requires:',line,flags=re.IGNORECASE) :
            return True
        elif re.search('^'+'provides:',line,flags=re.IGNORECASE) :
            return True
        elif re.search('^'+'obsoletes:',line,flags=re.IGNORECASE) :
            return True
        elif re.search('^'+'conflicts:',line,flags=re.IGNORECASE) :
            return True
        elif re.search('^'+'url:',line,flags=re.IGNORECASE) :
            return True
        elif re.search('^'+'source[0-9]*:',line,flags=re.IGNORECASE) :
            return True
        elif re.search('^'+'patch[0-9]*:',line,flags=re.IGNORECASE) :
            return True
        elif re.search('^'+'buildrequires:',line,flags=re.IGNORECASE) :
            return True
        elif re.search('^'+'buildprovides:',line,flags=re.IGNORECASE) :
            return True
        elif re.search('^'+'buildarch:',line,flags=re.IGNORECASE) :
            return True
        return False

    def isGlobalSecurityHardening(self,line):
        if re.search('^%global *security_hardening',line,flags=re.IGNORECASE) :
            return True
        return False

    def readHeader(self,line):
        headerSplitIndex=line.find(":")
        if(headerSplitIndex+1 == len(line) ):
            print line
            print "Error:Invalid header"
            return False, None,None
        headerName=line[0:headerSplitIndex].lower()
        headerContent=line[headerSplitIndex+1:].strip()
        return True,headerName,headerContent


    def readDependentPackageData(self,line):
        strUtils = StringUtils()
        listPackages=line.split(",")
        listdependentpkgs=[]
        for line in listPackages:
            line=strUtils.getStringInBrackets(line)
            listContents=line.split()
            totalContents = len(listContents)
            i=0
            while i < totalContents:
                dpkg = dependentPackageData()
                compare=None
                if i+2 < len(listContents):
                    if listContents[i+1] == ">=":
                        compare="gte"
                    elif listContents[i+1] == "<=":
                        compare="lte"
                    elif listContents[i+1] == "==":
                        compare="eq"
                    elif listContents[i+1] == "<":
                        compare="lt"
                    elif listContents[i+1] == ">":
                        compare="gt"
                    elif listContents[i+1] == "=":
                        compare="eq"
                    
                if compare is not None:
                    dpkg.package=listContents[i]
                    dpkg.compare=compare
                    dpkg.version=listContents[i+2]
                    i=i+3
                else:
                    dpkg.package=listContents[i]
                    i=i+1
                listdependentpkgs.append(dpkg)
        return listdependentpkgs

    def readPackageHeaders(self,line,pkg):
        returnVal,headerName,headerContent=self.readHeader(line)
        if not returnVal:
            return False

        headerContent=pkg.decodeContents(headerContent)
        if headerName == 'summary':
            pkg.summary=headerContent
            return True
        if headerName == 'name':
            pkg.name=headerContent
            return True
        if headerName == 'group':
            pkg.group=headerContent
            return True
        if headerName == 'license':
            pkg.license=headerContent
            return True
        if headerName == 'version':
            pkg.version=headerContent
            return True
        if headerName == 'buildarch':
            pkg.buildarch=headerContent
            return True
        if headerName == 'release':
            pkg.release=headerContent
            return True
        if headerName == 'distribution':
            pkg.distribution=headerContent
            return True
        if headerName == 'url':
            pkg.URL=headerContent
            return True
        if headerName.find('source') != -1:
            pkg.sources.append(headerContent)
            return True
        if headerName.find('patch') != -1:
            pkg.patches.append(headerContent)
            return True
        if headerName == 'requires' or headerName == 'provides' or headerName == 'obsoletes' or headerName == 'conflicts' or headerName == 'buildrequires' or headerName == 'buildprovides':
            dpkg=self.readDependentPackageData(headerContent)
            if dpkg is None:
                return False
            if headerName == 'requires':
                pkg.requires.extend(dpkg)
            if headerName == 'provides':
                pkg.provides.extend(dpkg)
            if headerName == 'obsoletes':
                pkg.obsoletes.extend(dpkg)
            if headerName == 'conflicts':
                pkg.conflicts.extend(dpkg)
            if headerName == 'buildrequires':
                pkg.buildrequires.extend(dpkg)
            if headerName == 'buildprovides':
                pkg.buildprovides.extend(dpkg)
                    
            return True
        return False

    def readSecurityHardening(self,line):
        data = line.lower().strip();
        words=data.split(" ")
        nrWords = len(words)
        if (nrWords != 3):
            print "Error: Unable to parse line: "+line
            return False
        if (words[2] != "none" and words[2] != "nonow") :
            print "Error: Invalid security_hardening value: " + words[2]
            return False
        self.globalSecurityHardening = words[2]
        return True;
