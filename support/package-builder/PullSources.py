#    Copyright (C) 2015-2017 VMware, Inc. All rights reserved.
#    pullsources.py
#    Allows pulling packages'sources from a source repository.
#
#    Author(s): Mahmoud Bassiouny (mbassiouny@vmware.com)
#               Alexey Makhalov (amakhalov@vmware.com)
#

import json
import os
import hashlib
import requests
from requests.auth import HTTPBasicAuth
from CommandUtils import CommandUtils

def getFileHash(filepath):
    sha1 = hashlib.sha1()
    f = open(filepath, 'rb')
    try:
        sha1.update(f.read())
    finally:
        f.close()
    return sha1.hexdigest()

def get(package, source, sha1, sourcesPath, configs, logger):
    cmdUtils = CommandUtils()
    sourcePath = cmdUtils.findFile(source, sourcesPath)
    if sourcePath is not None and len(sourcePath) > 0:
        if len(sourcePath) > 1:
            raise Exception("Multiple sources found for source:" + source + "\n" +
                            ",".join(sourcePath) +"\nUnable to determine one.")
        if sha1 == getFileHash(sourcePath[0]):
            # Use file from sourcesPath
            return
        else:
            logger.info("sha1 of " + sourcePath[0] + " does not match. " + sha1 +
                        " vs " + getFileHash(sourcePath[0]))
    configFiles = configs.split(":")
    for config in configFiles:
        p = pullSources(config, logger)
        package_path = os.path.join(sourcesPath, source)
        try:
            p.downloadFileHelper(package, source, package_path, sha1)
            return
        except Exception as e:
            logger.debug(e)

class pullSources:

    def __init__(self, conf_file, logger):
        self._config = {}
        self.logger = logger
        self.loadConfig(conf_file)

        # generate the auth
        self._auth = None
        if ('user' in self._config and len(self._config['user']) > 0 and
                'apikey' in self._config and len(self._config['apikey'])) > 0:
            self._auth = HTTPBasicAuth(self._config['user'], self._config['apikey'])

    def loadConfig(self, conf_file):
        with open(conf_file) as jsonFile:
            self._config = json.load(jsonFile)

    def downloadFile(self, package, filename, file_path):
        #form url: https://dl.bintray.com/vmware/photon_sources/1.0/<filename>.
        url = '%s/%s' % (self._config['baseurl'], filename)

        self.logger.debug("Downloading: " + url)

        # We need to provide atomicity for file downloads. That is,
        # the file should be visible in its canonical location only
        # when the download is complete. To achieve that, first
        # download to a temporary location (on the same filesystem)
        # and then rename it to the final destination filename.

        temp_file_path = file_path + "-" + package

        with open(temp_file_path, 'wb') as handle:
            response = requests.get(url, auth=self._auth, stream=True)

            if not response.ok:
                # Something went wrong
                raise Exception(response.text)

            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)
            handle.flush()
            response.close()

        if os.path.exists(file_path):
            os.remove(temp_file_path)
        else:
            os.rename(temp_file_path, file_path)

        return file_path

    def downloadFileHelper(self, package, filename, file_path, package_sha1=None):
        self.downloadFile(package, filename, file_path)
        if package_sha1 != getFileHash(file_path):
            raise Exception('Invalid sha1 for package %s file %s' % package, filename)
