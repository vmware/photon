'''
Created on Jan 22, 2015

@author: dthaluru
'''
import re
import os

class rpmMacro(object):
    def __init__(self):
        self.macroName=""
        self.macroFlag=""
        self.content=""
        self.position=-1
        self.endposition=-1

    def setName(self,name):
        self.macroName=name
        
    def displayMacro(self):
        print "Macro:\n", self.macroName, " ",self.macroFlag," ",self.position," ",self.endposition
        print self.content
    
class StringUtils(object):
    
    def get_string_in_brackets(self, inputstring):
        inputstring=inputstring.strip()
        m = re.search(r"^\(([A-Za-z0-9_.-]+)\)",  inputstring)
        if m is None:
            return inputstring
        return m.group(1)

    def getFileNameFromURL(self,inputstring):
        index=inputstring.rfind("/")
        return inputstring[index+1:]
        
    
class dependentPackageData(object):

    def __init__(self):
        self.package=""
        self.version=""
        self.compare=""
        
class Package(object):
    def __init__(self, basePkg=None):
        self.summary=""
        self.name=""
        self.group=""
        self.license=""
        self.version=""
        self.release=""
        self.buildarch="x86_64"
        self.distribution=""
        self.basePkgName=""
        
        self.sources=[]
        self.patches=[]
        self.buildrequires=[]
        self.buildprovides=[]
        
        
        self.requires=[]
        self.provides=[]
        self.obsoletes=[]
        self.conflicts=[]
        
        self.descriptionMacro= None #rpmMacro().setName("description")
        self.postMacro=None#rpmMacro().setName("post")
        self.postunMacro=None#rpmMacro().setName("postun")
        self.filesMacro=None#rpmMacro().setName("files")
        self.packageMacro=None#rpmMacro().setName("package")
        
        if basePkg is not None:
            self.basePkgName=basePkg.name
            self.group=basePkg.group
            self.license=basePkg.license
            self.version=basePkg.version
            self.buildarch=basePkg.buildarch
            self.release=basePkg.release
            self.distribution=basePkg.distribution
        
    def decodeContents(self,content):
        if content.find("%{name}") != -1:
            if self.basePkgName == "":
                content = content.replace('%{name}',self.name)
            else:
                content = content.replace('%{name}',self.basePkgName)
        
        if content.find("%{release}") != -1:
            content = content.replace('%{release}',self.release)
        
        if content.find("%{version}") != -1:
            content = content.replace('%{version}',self.version)
        
        return content
    
    def updatePackageMacro(self,macro):
        if macro.macroName == "%post":
            self.postMacro=macro
            return True
        if macro.macroName == "%postun":
            self.postunMacro=macro
            return True
        if macro.macroName == "%files":
            self.filesMacro=macro
            return True
        if macro.macroName == "%description":
            self.descriptionMacro = macro
            return True
        return False

class SpecFile(object):
    def __init__(self):
        self.cleanMacro=rpmMacro().setName("clean")
        self.prepMacro=rpmMacro().setName("prep")
        self.buildMacro=rpmMacro().setName("build")
        self.installMacro=rpmMacro().setName("install")
        self.changelogMacro=rpmMacro().setName("changelog")
        self.checkMacro=rpmMacro().setName("check")
        self.packages={}
        self.specAdditionalContent=""
        
    
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
                    if not self.packages.has_key(packageName):
                        return False
                    macro,i=self.readMacroFromFile(i, lines)
                    self.packages[packageName].updatePackageMacro(macro)
            elif self.isPackageHeaders(line):
                self.readPackageHeaders(line, self.packages[currentPkg])
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

        if re.search('^'+'%post',line) :
            return True
        elif re.search('^'+'%postun',line) :
            return True
        elif re.search('^'+'%files',line) :
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
            line=strUtils.get_string_in_brackets(line)
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

class Specutils(object):
    
    def __init__(self,specfile):
        self.specfile=""
        self.spec = SpecFile()
        if self.isSpecFile(specfile):
            self.specfile=specfile
            self.spec.parseSpecFile(self.specfile)
    
    def isSpecFile(self,specfile):
        if os.path.isfile(specfile) and specfile[-5:] == ".spec":
            return True
        return False
    
    def getSourceNames(self):
        sourceNames=[]
        strUtils = StringUtils()
        pkg = self.spec.packages.get('default')
        if pkg is None:
            return None
        for source in pkg.sources:
            sourceName=strUtils.getFileNameFromURL(source)
            sourceNames.append(sourceName)
        return sourceNames
    
    def getPatchNames(self):
        patchNames=[]
        strUtils = StringUtils()
        pkg = self.spec.packages.get('default')
        if pkg is None:
            return None
        for patch in pkg.patches:
            patchName=strUtils.getFileNameFromURL(patch)
            patchNames.append(patchName)
        return patchNames
    
    def getPackageNames(self):
        packageNames=[]
        for key in self.spec.packages.keys():
            pkg = self.spec.packages.get(key)
            packageNames.append(pkg.name)
        return packageNames
    
    def getRPMNames(self):
        rpmNames=[]
        for key in self.spec.packages.keys():
            pkg = self.spec.packages.get(key)
            rpmName=pkg.name+"-"+pkg.version+"-"+pkg.release
            rpmNames.append(rpmName)
        return rpmNames

    def getRPMName(self, pkgName):
        rpmName=None
        for key in self.spec.packages.keys():
            pkg = self.spec.packages.get(key)
            if pkg.name == pkgName:
               rpmName=pkg.name+"-"+pkg.version+"-"+pkg.release
               break
        return rpmName

    def getRPMVersion(self, pkgName):
        version=None
        for key in self.spec.packages.keys():
            pkg = self.spec.packages.get(key)
            if pkg.name == pkgName:
               version=pkg.version
               break
        return version

    def getRPMRelease(self, pkgName):
        release=None
        for key in self.spec.packages.keys():
            pkg = self.spec.packages.get(key)
            if pkg.name == pkgName:
               release=pkg.release
               break
        return release

    def getLicense(self, pkgName):
        license=None
        for key in self.spec.packages.keys():
            pkg = self.spec.packages.get(key)
            if pkg.name == pkgName:
               license=pkg.license
               break
        return license

    def getBuildArch(self, pkgName):
        buildArch="x86_64"
        for key in self.spec.packages.keys():
            pkg = self.spec.packages.get(key)
            if pkg.name == pkgName:
               buildArch=pkg.buildarch
               break
        return buildArch
    
    def getRequiresAllPackages(self):
        depedentPackages=[]
        for key in self.spec.packages.keys():
            pkg = self.spec.packages.get(key)
            for dpkg in pkg.requires:
                depedentPackages.append(dpkg.package)
        depedentPackages=list(set(depedentPackages))
        packageNames=self.getPackageNames()
        for pkgName in packageNames:
            if pkgName in depedentPackages:
                depedentPackages.remove(pkgName)
        return depedentPackages
    
    def getBuildRequiresAllPackages(self):
        depedentPackages=[]
        for key in self.spec.packages.keys():
            pkg = self.spec.packages.get(key)
            for dpkg in pkg.buildrequires:
                depedentPackages.append(dpkg.package)
        depedentPackages=list(set(depedentPackages))
        packageNames=self.getPackageNames()
        for pkgName in packageNames:
            if pkgName in depedentPackages:
                depedentPackages.remove(pkgName)
        return depedentPackages
    
    
    def getRequires(self,pkgName):
        dependentPackages=[]
        for key in self.spec.packages.keys():
            pkg = self.spec.packages.get(key)
            if pkg.name == pkgName:
               for dpkg in pkg.requires:
                  dependentPackages.append(dpkg.package)
        return dependentPackages

    def getBuildRequires(self,pkgName):
        dependentPackages=[]
        for key in self.spec.packages.keys():
            pkg = self.spec.packages.get(key)
            if pkg.name == pkgName:
               for dpkg in pkg.buildrequires:
                  dependentPackages.append(dpkg.package)
        return dependentPackages
        
    def getProvides(self,packageName):
        depedentPackages=[]
        defaultPkgName=self.spec.packages['default'].name
        pkg = None
        if self.spec.packages.has_key(packageName):
            pkg = self.spec.packages.get(packageName)
        if defaultPkgName == packageName:
            pkg=self.spec.packages['default']
        if pkg is not None:
            for dpkg in pkg.provides:
                depedentPackages.append(dpkg.package)
        else:
            print "package not found"
        return depedentPackages
    
    def getVersion(self):
        pkg = self.spec.packages.get('default')
        return pkg.version
    
    def getRelease(self):
        pkg = self.spec.packages.get('default')
        return pkg.release
        
def main():
    spec = Specutils("/workspace1/myrepos/photon/SPECS/docker/docker.spec")
    print "packages",spec.getPackageNames()
    print "packages",spec.getRPMNames()
    print "sources",spec.getSourceNames()
    print "patches",spec.getPatchNames()  
    print "requires",spec.getRequires('libltdl-devel')
    print "requires",spec.getRequires('libtool')
    
    print "provides",spec.getProvides('libtool')  
    print "all-requires",spec.getRequiresAllPackages()
    print "all-build-requires",spec.getBuildRequiresAllPackages()
    
if __name__ == '__main__':
    main()
    

        
        
