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
Eventually it will be replaced with sha512 because of enforcement
in spec-checker
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

    sourcePath = CommandUtils.findFile(source, sourcesPath)
    if sourcePath:
        if len(sourcePath) > 1:
            raise Exception(
                f"Multiple sources found for source: {source}\n"
                f"{','.join(sourcePath)}\nUnable to determine one."
            )
        if isFileHashOkay(sourcePath[0], checksum):
            # Use file from sourcesPath
            return
        logger.info(f"Checksum of {sourcePath[0]} does not match.")
    for baseurl in URLs:
        """
        From url:
        https://packages.vmware.com/photon/photon_sources/1.0/<filename>
        """
        url = f"{baseurl}/{source}"
        destfile = os.path.join(sourcesPath, source)
        logger.debug(f"Downloading: {url}")
        try:
            downloadFile(url, destfile)
            if not isFileHashOkay(destfile, checksum):
                raise Exception(f"Invalid checksum for package {package} file {source}")
            return
        except requests.exceptions.HTTPError as e:
            logger.exception(e)
            # on any HTTP errors - try next config
            continue
        except Exception as e:
            logger.exception(e)
    raise Exception(f"Missing source: {source}")


def downloadFile(url, destfile):
    # We need to provide atomicity for file downloads. That is,
    # the file should be visible in its canonical location only
    # when the download is complete. To achieve that, first
    # download to a temporary location (on the same filesystem)
    # and then rename it to the final destination filename.

    random_str = "".join(
        [random.choice(string.ascii_letters + string.digits) for _ in range(6)]
    )

    temp_file = f"{destfile}-{random_str}"

    response = requests.get(url, stream=True)

    if not response.ok:
        # Something went wrong
        response.raise_for_status()

    with open(temp_file, "wb") as handle:
        for block in response.iter_content(4096):
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
