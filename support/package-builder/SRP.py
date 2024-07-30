import os
import os.path
import json
import copy
import csv

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
        rpm = StringUtils.splitRPMFilename(self.pkg)
        self.package = rpm["name"]
        self.version = rpm["version"]
        self.release = rpm["release"]
        self.distTag = rpm["tag"]
        self.fullVersion = f"{self.version}-{self.release}.{self.distTag}"

        self.logger = logger
        self.cmdUtils = CommandUtils()
        self.srp_workdir = os.path.join(constants.stagePath, "SRP", f"{pkg}")
        # Will be used as a package schematic json file at finalize step.
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
        # SPDX template for output RPMs.
        self.spdx_package_common = {
            "package": {
                "license_declared": f"{SPECS.getData().getLicense(self.package, self.fullVersion)}",
                "home_page": f"{SPECS.getData().getURL(self.package, self.fullVersion)}",
                "short_summary": f"{SPECS.getData().getSummary(self.package, self.fullVersion)}",
                "supplier": "Organization: Broadcom, Inc."
            }
        }

    def getOSRelease(self):
        path = "/etc/os-release"
        with open(path) as stream:
            reader = csv.reader(stream, delimiter="=")
            os_release = dict(reader)
        return f"{os_release['NAME']} {os_release['VERSION']}"

    def initialize(self):
        if not self.srpcli:
            return
        self.cmdUtils.runBashCmd(f"SRP_WORKING_DIR={self.srp_workdir} {self.srpcli} provenance init")
        self.cmdUtils.runBashCmd(f"SRP_WORKING_DIR={self.srp_workdir} {self.srpcli} provenance add-build photon --package={self.package} --version={self.version} --release={self.release} --dist-tag={self.distTag} --arch={constants.targetArch}")
        self.cmdUtils.runBashCmd(f"SRP_WORKING_DIR={self.srp_workdir} {self.srpcli} provenance action start  --name=build-{self.pkg}")

        # Add a compute resource information. From all available types vm.nimbus is closest to Photon build VM.
        # TODO: next 3 variables must be provided by CI/CD pipeline. Variable names can be different from what specified below.
        # Do not stop the build if not provided.
        location = os.environ.get("LOCATION", "FIXME-LOCATION-NOT-DEFINED")
        build_id = os.environ.get("BUILD_ID", "FIXME-BUILD_ID-NOT-DEFINED")
        vm_template = os.environ.get("VM_TEMPLATE", "FIXME-VM_TEMPLATE-NOT-DEFINED")
        self.cmdUtils.runBashCmd(f"SRP_WORKING_DIR={self.srp_workdir} {self.srpcli} provenance action add-compute-resource vm.nimbus --os-type linux --kernel-version {os.uname()[2]} --distro-version '{self.getOSRelease()}' --machine {os.uname()[1]} --ephemeral=true --firewall-present=true --location {location} --build-id {build_id} --template {vm_template}")
        self.cmdUtils.runBashCmd(f"SRP_WORKING_DIR={self.srp_workdir} {self.srpcli} provenance action set-process-debugger --enabled=false")
        self.cmdUtils.runBashCmd(f"SRP_WORKING_DIR={self.srp_workdir} {self.srpcli} provenance action set-root-access --enabled=false")

    def rpmFileNameToUid(self, filename):
        rpm = StringUtils.splitRPMFilename(filename)
        n = rpm["name"]
        v = rpm["version"]
        r = rpm["release"]
        t = rpm["tag"]
        a = rpm["arch"]
        if t.startswith("ph"):
            branch = f"{t[2:]}.0"
        else:
            raise Exception("Can not parse dist tag.")
        repo = f"https://packages.vmware.com/photon/{branch}/photon_{branch}_{constants.targetArch}"
        return f"uid.obj.comp.package.rpm(name='{n}',version='{v}',release='{r}.{t}',arch='{a}',original_repository='{repo}')"

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
            rpm = StringUtils.splitRPMFilename(filename)
            n = rpm["name"]
            v = rpm["version"]
            r = rpm["release"]
            t = rpm["tag"]
            a = rpm["arch"]

            if n == self.package + "-debuginfo":
                description = f"Debuginfo for {self.package}"
            elif a == "src":
                description = f"Source RPM for {self.package}"
            else:
                fullVersion = f"{v}-{r}.{t}"
                description = f"{SPECS.getData().getDescription(n, fullVersion)}"

            spdx_info = copy.deepcopy(self.spdx_package_common)
            spdx_info["package"]["detailed_description"] = description

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

    def addObservation(self, observationFile):
        if not self.srpcli:
            return

        network_required = SPECS.getData().isNetworkRequired(self.package, self.fullVersion)
        if network_required and not observationFile:
            raise Exception("Observation file is required but not generated")

        if observationFile:
            self.cmdUtils.runBashCmd(f"SRP_WORKING_DIR={self.srp_workdir} {self.srpcli} provenance action import-observation --name=build-observation --file={observationFile}")

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
