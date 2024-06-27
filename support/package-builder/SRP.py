import os.path
import json
import copy

from constants import constants
from CommandUtils import CommandUtils
from SpecData import SPECS
from StringUtils import StringUtils

class SRP(object):

    def __init__(self, pkg, logger):
        self.srpcli = constants.srpcli
        if not self.srpcli:
            logger.info("SRPCLI is not provided. SRP provenance will not be generated.")
            return

        self.pkg = pkg
        self.package, self.version, self.release, self.distTag, arch= StringUtils.splitRPMFilename(self.pkg)
        self.fullVersion = f"{self.version}-{self.release}.{self.distTag}"

        self.logger = logger
        self.cmdUtils = CommandUtils()
        self.srp_workdir = os.path.join(constants.stagePath, "SRP", f"{pkg}")
        self.schematic = {
            "schema_id": "1.0",
            "sources": {
                "source": {
                    "typename": "source_tree.git",
                    "path": f"{constants.gitSourcePath}"
                }
            },
            "input_templates": {
                "rpm-comps": {
                }
            },
            "outputs": {}
        }
        self.spdx_package_common = {
            "package": {
                "license_declared": f"{SPECS.getData().getLicense(self.package, self.fullVersion)}",
                "home_page": f"{SPECS.getData().getURL(self.package, self.fullVersion)}",
                "short_summary": f"{SPECS.getData().getSummary(self.package, self.fullVersion)}",
                "supplier": "Organization: Broadcom, Inc."
            }
        }

    def initialize(self):
        if not self.srpcli:
            return
        self.cmdUtils.runBashCmd(f"SRP_WORKING_DIR={self.srp_workdir} {self.srpcli} provenance init")
        self.cmdUtils.runBashCmd(f"SRP_WORKING_DIR={self.srp_workdir} {self.srpcli} provenance add-build photon --package={self.package} --version={self.version} --release={self.release} --dist-tag={self.distTag} --arch={constants.targetArch}")
        self.cmdUtils.runBashCmd(f"SRP_WORKING_DIR={self.srp_workdir} {self.srpcli} provenance action start  --name=build-{self.pkg}")

    def rpmFileNameToUid(self, filename):
        n, v, r, t, a = StringUtils.splitRPMFilename(filename)
        return f"uid.obj.comp.package.rpm(name='{n}',version='{v}',release='{r}.{t}',arch='{a}')"

    def addInputRPMS(self, files):
        if not self.srpcli:
            return

        for file in files:
            filename = os.path.basename(file)
            self.schematic["input_templates"]["rpm-comps"][self.rpmFileNameToUid(filename)] = {
                "incorporated": False,
                "usages": [
                    "building"
                ]
            }


    def addOutputRPMS(self, files):
        if not self.srpcli:
            return

        for file in files:
            filename = os.path.basename(file)
            n, v, r, t, a = StringUtils.splitRPMFilename(filename)

            # Old way of adding outputs
            # self.cmdUtils.runBashCmd(f"SRP_WORKING_DIR={self.srp_workdir} {self.srpcli} provenance add-output general --set-key={self.package} --action-key=build-{self.pkg} --uid-type uid.obj.comp.package.rpm --uid-arg name={n} --uid-arg version={v} --uid-arg release={r}.{t} --uid-arg arch={a}")

            if n == self.package + "-debuginfo":
                description = f"Debuginfo for {self.package}"
            elif a == "src":
                description = f"Source RPM for {self.package}"
            else:
                fullVersion = f"{v}-{r}.{t}"
                description = f"{SPECS.getData().getDescription(n, fullVersion)}"

            spdx_info = copy.deepcopy(self.spdx_package_common)
            spdx_info["package"]["detailed_description"] = description

            # New way - via schematic
            self.schematic["outputs"][self.rpmFileNameToUid(filename)] = {
                "merge_input_templates": ["rpm-comps"],
                "spdx_info": spdx_info,
                "inputs": {
                    "$(sources:source_uid)": {
                        "is_components_source": True,
                        "incorporated": True,
                        "usages": [
                            "functionality",
                            "building",
                            "testing"
                        ]
                    }
                }
            }

    def addCommand(self, cmd):
        if not self.srpcli:
            return

        _cmd = cmd.replace("\"", "\\\"")
        self.cmdUtils.runBashCmd(f"SRP_WORKING_DIR={self.srp_workdir} {self.srpcli} provenance action import-cmd --cmd=\"{_cmd}\"")

    def finalize(self):
        if not self.srpcli:
            return

        schematic_filename = f"{self.srp_workdir}/package.schematic.json"
        with open(schematic_filename, "w") as f:
            json.dump(self.schematic, f)
        self.cmdUtils.runBashCmd(f"SRP_WORKING_DIR={self.srp_workdir} {self.srpcli} provenance action stop")
        self.cmdUtils.runBashCmd(f"SRP_WORKING_DIR={self.srp_workdir} {self.srpcli} provenance schematic --verbose --no-schematic --path={schematic_filename}")
        self.cmdUtils.runBashCmd(f"SRP_WORKING_DIR={self.srp_workdir} {self.srpcli} provenance compile --saveto={self.srp_workdir}/{self.pkg}.provenance.json")
        if os.path.isfile(schematic_filename):
            os.remove(schematic_filename)
        # "_provenance.json" is a temporary file used by SRPCLI to store provenance content between SRPCLI invocations
        # It is created by "provenance init" and not removed by "compile".
        # Remove it manually.
        provenance_tmp_filename = f"{self.srp_workdir}/_provenance.json"
        if os.path.isfile(provenance_tmp_filename):
            os.remove(provenance_tmp_filename)
