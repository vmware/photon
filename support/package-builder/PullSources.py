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
import string
import random
from CommandUtils import CommandUtils

def getFileHash(filepath):
    sha1 = hashlib.sha1()
    f = open(filepath, 'rb')
    try:
        sha1.update(f.read())
    finally:
        f.close()
    return sha1.hexdigest()

def get(package, source, sha1, sourcesPath, URLs, logger):
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
    for baseurl in URLs:
        #form url: https://dl.bintray.com/vmware/photon_sources/1.0/<filename>.
        url = '%s/%s' % (baseurl, filename)
        destfile = os.path.join(file_path, filename)
        logger.debug("Downloading: " + url)
        try:
            downloadFile(url, destfile)
            if sha1 != getFileHash(destfile):
                raise Exception('Invalid sha1 for package %s file %s' % package, source)
            return
        except requests.exceptions.HTTPError as e:
            # on any HTTP errors - try next config
            continue
        except Exception as e:
            logger.exception(e)
    raise Exception("Missing source: " + source)

def downloadFile(url, destfile):
    # We need to provide atomicity for file downloads. That is,
    # the file should be visible in its canonical location only
    # when the download is complete. To achieve that, first
    # download to a temporary location (on the same filesystem)
    # and then rename it to the final destination filename.

    temp_file = destfile + "-" + \
                "".join([random.choice(
                    string.ascii_letters + string.digits) for _ in range(6)])

    with open(temp_file, 'wb') as handle:
        response = requests.get(url, stream=True)

        if not response.ok:
            # Something went wrong
            response.raise_for_status()

        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)
        handle.flush()
        response.close()

    if os.path.exists(destfile):
        os.remove(temp_file)
    else:
        os.rename(temp_file, destfile)

    return destfile

