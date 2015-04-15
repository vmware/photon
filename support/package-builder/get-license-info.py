#!/usr/bin/env python

from optparse import OptionParser
from xml.dom import minidom
from Specutils import Specutils
import os

class LicenseEnumerator(object):
    def __init__(self, manifest, src_path, spec_path):
        self.manifest = manifest
        self.src_path = src_path
        self.spec_path = spec_path

    def list(self):

        xmldoc = minidom.parse(self.manifest)
        for node in xmldoc.getElementsByTagName("packages"):
            packages = node.getElementsByTagName("package") 
            for pkg in packages:
                id_node = pkg.attributes.get("id")
                name_node = pkg.attributes.get("name")
                if name_node == None:
                    name_node = id_node
                spec_node = pkg.attributes.get("spec")
                if spec_node == None:
                    spec_part = id_node.value
                else:
                    spec_part = spec_node.value
                spec = "%s.spec" % spec_part
                spec_file_path = os.path.join(
                                        self.spec_path, 
                                        spec_part,
                                        spec)
                specparser = Specutils(spec_file_path)

                print "Package: %s; Version: %s-%s; License: %s" % (
                          name_node.value,
                          specparser.getRPMVersion(name_node.value),
                          specparser.getRPMRelease(name_node.value),
                          specparser.getLicense(name_node.value)
                      )

def main():
    usage = "Usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option(
              "-m",
              "--manifest",
              dest="manifest",
              default="build-manifest.xml")
    parser.add_option(
              "-s",
              "--spec-path",
              dest="spec_path",
              default="../../SPECS")
    parser.add_option(
              "-o",
              "--source-path",
              dest="source_path",
              default="../../SOURCES")
    (options, args) = parser.parse_args()

    licenum = LicenseEnumerator(
                  options.manifest,
                  options.source_path,
                  options.spec_path)
    licenum.list()
    
if __name__ == '__main__':
    main()
