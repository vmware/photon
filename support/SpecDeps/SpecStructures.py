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
        
        self.descriptionMacro= None
        self.postMacro=None
        self.postunMacro=None
        self.filesMacro=None
        self.packageMacro=None
        
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
        
        if content.find("%{?dist}") != -1:
            content = content.replace('%{?dist}',self.distribution)

        if content.find("%{dist}") != -1:
            content = content.replace('%{dist}',self.distribution)
        
        # TODO: A temporary hack here. The reason is this macro
        # can't be subsitute properly.
        # At this file level, we won't be able to obtain any other
        # packages' information. This macro requires the information
        # of package linux. Besides, there is a huge diversion
        # between package-builder and SpecDeps.
        if content.find("%{?kernelsubrelease}") != -1:
            content = content.replace('%{?kernelsubrelease}',"")

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
