import os
from os import walk
import hashlib

class publishUtils:
    @staticmethod
    def sha1OfFile(filepath):
        sha = hashlib.sha1()
        with open(filepath, 'rb') as f:
            sha.update(f.read())
        return sha.hexdigest()

    @staticmethod
    def stripBegin(str, strToStrip):
        index = str.find(strToStrip, 0, len(str))
        if index >= 0:
            index = index + len(strToStrip)
            return str[index:].lstrip('/')
        return str

    @staticmethod
    def getFilesWithRelativePath(root):
        f = []
        for (dirpath, _, filenames) in walk(root):
            strippedPath = publishUtils.stripBegin(dirpath, root)
            for filename in filenames:
                f.append(os.path.join(strippedPath, filename))
        return f
