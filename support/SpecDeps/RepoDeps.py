import commands

class RepoQueryDependency(object):
    def __init__(self, repoFile):
        self.repo_file = repoFile
    def getRequiresList(self,pkg):
        cmd = "repoquery -c "+self.repo_file+" -R -q "+pkg+" | xargs repoquery -c "+self.repo_file+" --whatprovides -q | sed 's/-[0-9]/ /g' | cut -f 1 -d ' ' | sort | uniq "
        status,output = commands.getstatusoutput(cmd)
        if status == 0:
            outList = output.split('\n')
            if "" in outList: outList.remove("")
            if "Options:" in outList: outList.remove("Options:")
            if "Usage:" in outList: outList.remove("Usage:")
            return outList
