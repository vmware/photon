#! /usr/bin/python2
#
#    Copyright (C) 2015 VMware, Inc. All rights reserved.
#    pullsources.py 
#    Allows pulling packages'sources from a bintary  
#    repository.
#
#    Author(s): Mahmoud Bassiouny (mbassiouny@vmware.com)
#

from optparse import OptionParser
import json
import os
import hashlib
import string
import datetime
import copy_reg
import types
import requests
from requests.auth import HTTPBasicAuth
from multiprocessing import Pool

class pullSources:

    def __init__(self, conf_file, src_list):
        self._config = {}
        self.loadConfig(conf_file)
        self.sha1_filename = src_list

        # generate the auth
        self._auth = None
        if ('user' in self._config and len(self._config['user']) > 0 and
            'apikey' in self._config and len(self._config['apikey'])) > 0:
            self._auth = HTTPBasicAuth(self._config['user'], self._config['apikey'])

    def loadConfig(self,conf_file):
        with open(conf_file) as jsonFile:
            self._config = json.load(jsonFile)

    def getFileHash(self, filepath):
        sha1 = hashlib.sha1()
        f = open(filepath, 'rb')
        try:
            sha1.update(f.read())
        finally:
            f.close()
        return sha1.hexdigest()

    def downloadExistingFilePrompt(self, filename):
        yes = ['yes', 'y']
        no = ['no', 'n']
        while True:
            prompt = "Found a different local copy of {0}. Do you want to replace it? [y/n]:".format(filename)
            answer = raw_input(prompt).lower()
            if answer in yes:
                return True
            elif answer in no:
                return False

    def downloadFile(self, filename, file_path):
        print '%s: Downloading %s...' % (str(datetime.datetime.today()), filename)

        #form url: https://dl.bintray.com/vmware/photon_sources/1.0/<filename>.
        url = '%s/%s/%s/%s/%s' % \
              (self._config['baseurl'],\
               self._config['subject'],\
               self._config['repo'],\
               self._config['version'],\
               filename)

        with open(file_path, 'wb') as handle:
            response = requests.get(url, auth=self._auth, stream=True)

            if not response.ok:
                # Something went wrong
                raise Exception(response.text + " " + url)

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)
            response.close()
        return file_path

    def downloadFileHelper(self, package_name, package_path, package_sha1 = None):
        self.downloadFile(package_name, package_path)
        if package_sha1 != self.getFileHash(package_path):
            raise Exception('Invalid sha1 for package %s' % package_name)

    def pull(self, sources_dir):
        #Open the list of sources.
        with open(self.sha1_filename) as f:
            packages = f.readlines()

        pool = Pool(processes = 10)
        package_and_source_dir_list = map(lambda package: (package, sources_dir), packages )
        pool.map(self.ProcessDownload, package_and_source_dir_list)
        pool.close()
        pool.join()

    def ProcessDownload(self, package_and_source_dir):
        package = package_and_source_dir[0]
        sources_dir = package_and_source_dir[1]
        i = string.rindex(package, '-')

        package_name = string.strip(package[:i])
        package_sha1 = string.strip(package[i+1:])
        package_path = os.path.join(sources_dir, package_name)

        if not os.path.isfile(package_path):
            self.downloadFileHelper(package_name, package_path, package_sha1)

        elif package_sha1 != self.getFileHash(package_path):
                if self.downloadExistingFilePrompt(package_name):
                    self.downloadFileHelper(package_name, package_path, package_sha1)

def _pickle(method):
    if method.im_self is None:
        return getattr, (method.im_class, method.im_func.func_name)
    else:
        return getattr, (method.im_self, method.im_func.func_name)

copy_reg.pickle(types.MethodType, _pickle)

if __name__ == '__main__':
    usage = "Usage: %prog [options] <sources_dir>"
    parser = OptionParser(usage)

    parser.add_option("-c", "--config-path",  dest="config_path", default="./bintray.conf", help="Path to bintray configuation file")
    parser.add_option("-s", "--sources-list-file",  dest="sources_list", default="./source_list.sha1", help="SHA1 file with sources list to download")


    (options,  args) = parser.parse_args()

    if (len(args)) != 1:
            parser.error("Incorrect number of arguments")

    p = pullSources(options.config_path, options.sources_list)
    print args[0]
    p.pull(args[0])
