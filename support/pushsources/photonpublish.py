#! /usr/bin/python3
#
#    Copyright (C) 2015 VMware, Inc. All rights reserved.
#    photonpublish.py
#    Allows pushing rpms and other artifacts to
#    a bintray repository.
#    Allows queying a repository to get existing
#    file details.
#
#    Author(s): Priyesh Padmavilasom
#

import sys
import getopt
import json
import glob
import os

import requests
from requests.auth import HTTPBasicAuth

from publishutils import publishUtils
from publishconst import publishConst


const = publishConst()

class photonPublish:

    def __init__(self, context):
        self._context = context
        self._config = {}
        self.loadConfig()

    def loadConfig(self):
        confFile = self._context['config']
        if not confFile:
            return
        with open(confFile) as jsonFile:
            self._config = json.load(jsonFile)
        #override cmdline supplied params
        if 'user' in self._context and self._context['user']:
            self._config['user'] = self._context['user']
        if 'apikey' in self._context and self._context['apikey']:
            self._config['apikey'] = self._context['apikey']


    #get details of existing files in remote
    def getPackages(self):
        auth = HTTPBasicAuth(self._config['user'], self._config['apikey'])

        #form url: https://api.com/content/vmware/photon/releases/0.9 for eg.
        url = '%s/packages/%s/%s/%s/versions/%s/files?include_unpublished=1' % \
              (self._config['baseurl'],\
               self._config['subject'],\
               self._config['repo'],\
               self._config['package'],\
               self._config['version'])

        req = requests.get(url, auth=auth)
        if req.status_code >= 300:
            raise Exception(req.text)

        return req.json()

    #return list of unpublished content
    #works with details from config file
    def getUnpublished(self):
        result = []
        pkgs = self.getPackages()
        for pkg in pkgs:
            if not pkg[const.published]:
                result.append(pkg)
        return result

    #Check if the local path has any diffs with the
    #remote repo. Compare sha1 hash
    def check(self, pkgsRoot):
        result = {
            const.updates:[],
            const.new:[],
            const.obsoletes:[],
            const.verified:[]
            }
        localFiles = publishUtils.getFilesWithRelativePath(pkgsRoot)
        pkgs = self.getPackages()
        for pkg in pkgs:
            remotePath = pkg[const.path]

            if remotePath in localFiles:
                localFiles.remove(remotePath)

            localPath = os.path.join(pkgsRoot, remotePath)
            if os.path.isfile(localPath):
                sha1 = publishUtils.sha1OfFile(localPath)
                if sha1 == pkg[const.sha1]:
                    result[const.verified].append(pkg)
                else:
                    result[const.updates].append(pkg)
            else:
                result[const.obsoletes].append(pkg)

        for newFile in localFiles:
            result[const.new].append({const.path:newFile})

        return result

    #exec results from a check against remote
    #this will make remote and local in sync
    def syncRemote(self, root, checkResults):
        updateCount = len(checkResults[const.updates])
        newCount = len(checkResults[const.new])

        if updateCount + newCount == 0:
            print('Remote is up to date.')
            return

        #push updates
        print('Updating %d files' % updateCount)
        for new in checkResults[const.updates]:
            filePath = new[const.path]
            fileName = os.path.basename(filePath)
            fullPath = os.path.join(root, filePath)
            pathName = filePath.rstrip(fileName).rstrip('/')
            self.updateFile(fullPath, pathName)

        #push new files
        print('Pushing %d new files' % newCount)
        for new in checkResults[const.new]:
            filePath = new[const.path]
            fileName = os.path.basename(filePath)
            fullPath = os.path.join(root, filePath)
            pathName = filePath.rstrip(fileName).rstrip('/')
            self.pushFile(fullPath, pathName)

    #push a folder with rpms to a specified pathname
    #in the remote repo
    def push(self, filePath, pathName):
        results = []
        filesToPush = glob.glob(filePath)
        for fileToPush in filesToPush:
            result = self.pushFile(fileToPush, pathName)
            print(result)
            results.append(result)

    def pushFile(self, fileToPush, pathName):
        print('Pushing file %s to path %s' % (fileToPush, pathName))
        result = {}
        auth = HTTPBasicAuth(self._config['user'], self._config['apikey'])

        fileName = os.path.basename(fileToPush)
        if pathName:
            pathAndFileName = '%s/%s' % (pathName, fileName)
        else:
            pathAndFileName = fileName

        #form url: https://api.com/content/vmware/photon/releases/0.9 for eg.
        url = '%s/content/%s/%s/%s/%s/%s' % \
              (self._config['baseurl'],\
               self._config['subject'],\
               self._config['repo'],\
               self._config['package'],\
               self._config['version'],\
               pathAndFileName)

        headers = {'Content-Type': 'application/octet-stream'}
        with open(fileToPush, 'rb') as chunkedData:
            req = requests.put(url,
                               auth=auth,
                               data=chunkedData,
                               headers=headers)

        if req.status_code >= 300:
            raise Exception(req.text)

        result['destPath'] = pathAndFileName
        result['sourcePath'] = fileToPush
        result['returnCode'] = req.status_code
        result['msg'] = req.text
        return result

    def updateFile(self, fileToPush, pathName):
        print('Updating file %s at path %s' % (fileToPush, pathName))
        result = {}
        auth = HTTPBasicAuth(self._config['user'], self._config['apikey'])

        fileName = os.path.basename(fileToPush)
        if pathName:
            pathAndFileName = '%s/%s' % (pathName, fileName)
        else:
            pathAndFileName = fileName

        #form url: https://api.com/content/vmware/photon/releases/0.9 for eg.
        url = '%s/content/%s/%s/%s/%s/%s?override=1' % \
              (self._config['baseurl'],\
               self._config['subject'],\
               self._config['repo'],\
               self._config['package'],\
               self._config['version'],\
               pathAndFileName)

        headers = {'Content-Type': 'application/octet-stream'}
        with open(fileToPush, 'rb') as chunkedData:
            req = requests.put(url,
                               auth=auth,
                               data=chunkedData,
                               headers=headers)

        if req.status_code >= 300:
            raise Exception(req.text)

        result['destPath'] = pathAndFileName
        result['sourcePath'] = fileToPush
        result['returnCode'] = req.status_code
        result['msg'] = req.text
        return result

    #publishes pending content. Works with details from conf file.
    def publish(self):
        print('Publishing pending files to %s/%s/%s' \
               % (self._config['repo'],
                  self._config['package'],
                  self._config['version']))
        auth = HTTPBasicAuth(self._config['user'], self._config['apikey'])

        #form url: https://api.com/content/vmware/photon/releases/0.9 for eg.
        url = '%s/content/%s/%s/%s/%s/publish' % \
              (self._config['baseurl'],\
               self._config['subject'],\
               self._config['repo'],\
               self._config['package'],\
               self._config['version'])

        req = requests.post(url, auth=auth)

        if req.status_code >= 300:
            raise Exception(req.text)

        return req.json()

def showUsage():
    print('photonpublish.py --files /rpms/*.rpm')
    print('if you need to override config, --config /conf.conf')
    print('if you need to override user/apikey, provide')
    print('--user username --apikey apikey')

def validate(context):
    return context['config'] and context['files']

#test photonPublish
def main(argv):
    try:
        context = {
            'config':'/etc/photonpublish.conf',
            'user':'',
            'apikey':'',
            'files':'',
            'path':'',
            'mode':''
            }
        opts, args = getopt.getopt(
            sys.argv[1:],
            '',
            ['config=', 'user=', 'apikey=', 'files=', 'path=', 'mode='])
        for opt, arg in opts:
            if opt == '--config':
                context['config'] = arg
            elif opt == '--user':
                context['user'] = arg
            elif opt == '--apikey':
                context['apikey'] = arg
            elif opt == '--files':
                context['files'] = arg
            elif opt == '--path':
                context['path'] = arg
            elif opt == '--mode':
                context['mode'] = arg

        if not validate(context):
            showUsage()
            sys.exit(1)

        publish = photonPublish(context)
        if context['mode'] == 'upload':
            publish.push(context['files'], context['path'])
        elif context['mode'] == 'check':
            print(publish.check(context['files']))

    except Exception as e:
        print("Error: %s" % e)
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv)
