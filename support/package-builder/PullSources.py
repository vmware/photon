#!/usr/bin/env python3

import os
import hashlib
import requests
import string
import random

from CommandUtils import CommandUtils


"""
TODO: need to remove sha1sum support from here in future
All the spec files are using sha1sum currently
Eventually it will be replaced with sha512 because of enforcement in check_spec.py
"""


def isFileHashOkay(filepath, checksum):
    if "md5" in checksum:
        csum = hashlib.md5()
        chash = checksum["md5"]
    elif "sha1" in checksum:
        csum = hashlib.sha1()
        chash = checksum["sha1"]
    elif "sha256" in checksum:
        csum = hashlib.sha256()
        chash = checksum["sha256"]
    else:
        csum = hashlib.sha512()
        chash = checksum["sha512"]

    try:
        f = open(filepath, "rb")
        csum.update(f.read())
    finally:
        f.close()

    return csum.hexdigest() == chash


def get(package, source, checksum, sourcesPath, URLs, logger):
    if not os.path.isdir(sourcesPath):
        os.mkdir(sourcesPath)

    cmdUtils = CommandUtils()
    sourcePath = cmdUtils.findFile(source, sourcesPath)
    if sourcePath is not None and len(sourcePath) > 0:
        if len(sourcePath) > 1:
            raise Exception("Multiple sources found for source:" + source + "\n" +
                            ",".join(sourcePath) +"\nUnable to determine one.")
        if isFileHashOkay(sourcePath[0], checksum):
            # Use file from sourcesPath
            return
        logger.info("checksum of " + sourcePath[0] + " does not match.")
    for baseurl in URLs:
        #form url: https://packages.vmware.com/photon/photon_sources/1.0/<filename>.
        url = '%s/%s' % (baseurl, source)
        destfile = os.path.join(sourcesPath, source)
        logger.debug("Downloading: " + url)
        try:
            downloadFile(url, destfile)
            if not isFileHashOkay(destfile, checksum):
                raise Exception('Invalid checksum for package %s file %s' % (package, source))
            return
        except requests.exceptions.HTTPError as e:
            logger.exception(e)
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

    response = requests.get(url, stream=True)

    if not response.ok:
        # Something went wrong
        response.raise_for_status()

    with open(temp_file, 'wb') as handle:
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
