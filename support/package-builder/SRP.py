import os
import json
import copy
import csv
import shutil
import tempfile
from urllib.parse import unquote

from contextlib import suppress
from constants import constants
from CommandUtils import CommandUtils
from SpecData import SPECS
from StringUtils import StringUtils
from datetime import datetime, timezone

GO_REMOTE_PREFIX="/artifactory/proxy-golang-remote/"
MAVEN_REMOTE_PREFIX="/artifactory/maven/"
GRADLE_REMOTE_PREFIX="/artifactory/plugins-gradle-org-m2/"

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
        self.srp_workdir = os.path.join(constants.stagePath, "SRP", f"{pkg}")
        self.srpcli_run = lambda args: CommandUtils.runCmd(
            [self.srpcli] + args, env={"SRP_WORKING_DIR": self.srp_workdir}
        )
        # Will be used as a package schematic json file at finalize step.
        self.schematic = {
            "schema_id": "1.0",
            "sources": {
                "source": {
                    "typename": "source_tree.git",
                    "path": f"{constants.gitSourcePath}",
                }
            },
            "input_templates": {"rpm-comps": {}, "source-comps": {}, "maven-comps": {}, "gradle-comps": {}, "go-comps": {}},
            "outputs": {},
        }
        # SPDX template for output RPMs.
        self.spdx_package_common = {
            "package": {
                "license_declared": f"{SPECS.getData().getLicense(self.package, self.fullVersion)}",
                "home_page": f"{SPECS.getData().getURL(self.package, self.fullVersion)}",
                "short_summary": f"{SPECS.getData().getSummary(self.package, self.fullVersion)}",
                "supplier": "Organization: Broadcom, Inc.",
            }
        }

    def isEnabled(self):
        return self.srpcli is not None

    def getOSRelease(self):
        path = "/etc/os-release"
        with open(path) as stream:
            reader = csv.reader(stream, delimiter="=")
            os_release = dict(reader)
        return f"{os_release['NAME']} {os_release['VERSION']}"

    def initialize(self):
        if not self.srpcli:
            return
        self.srpcli_run(["provenance", "init", f"--revision={datetime.now(timezone.utc).isoformat(timespec='seconds')}"])
        self.srpcli_run(
            [
                "provenance",
                "add-build",
                "photon",
                f"--package={self.package}",
                f"--version={self.version}",
                f"--release={self.release}",
                f"--dist-tag={self.distTag}",
                f"--arch={constants.targetArch}",
            ]
        )
        self.srpcli_run(["provenance", "action", "start", f"--name=build-{self.pkg}"])

        # Add a compute resource information. From all available types vm.nimbus is closest to Photon build VM.
        # TODO: next 3 variables must be provided by CI/CD pipeline. Variable names can be different from what specified below.
        # Do not stop the build if not provided.
        location = os.environ.get("LOCATION", "FIXME-LOCATION-NOT-DEFINED")
        build_id = os.environ.get("BUILD_ID", "FIXME-BUILD_ID-NOT-DEFINED")
        vm_template = os.environ.get("VM_TEMPLATE", "FIXME-VM_TEMPLATE-NOT-DEFINED")
        self.srpcli_run(
            [
                "provenance",
                "action",
                "add-compute-resource",
                "vm.nimbus",
                "--ephemeral=true",
                "--firewall-present=true",
                "--os-type",
                "linux",
                "--machine",
                os.uname()[1],
                "--kernel-version",
                os.uname()[2],
                "--distro-version",
                self.getOSRelease(),
                "--location",
                location,
                "--build-id",
                build_id,
                "--template",
                vm_template,
            ]
        )
        self.srpcli_run(
            ["provenance", "action", "set-process-debugger", "--enabled=false"]
        )
        self.srpcli_run(["provenance", "action", "set-root-access", "--enabled=false"])

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
            raise Exception(
                f"Can not parse dist tag: <{n}>-<{v}>-<{r}>-<{t}>-<{a}>, filename={filename}"
            )

        reponame = "photon"
        if n in constants.extraPackagesList:
            reponame = f"{reponame}_extras"
        elif n.endswith("-debuginfo"):
            reponame = f"{reponame}_debuginfo"
        elif a == "src":
            reponame = f"{reponame}_srpms"

        repo = f"https://packages-prod.broadcom.com/photon/{branch}/{reponame}_{branch}_{constants.targetArch}"
        return f"uid.obj.comp.package.rpm(name='{n}',version='{v}',release='{r}.{t}',arch='{a}',original_repository='{repo}')"

    def goDepPathToUid(self, path):
        # example: (.mod, .info, .zip)
        # /artifactory/proxy-golang-remote/sigs.k8s.io/yaml/@v/v1.3.0.mod ->
        # uid.obj.comp.package.go(name='sigs.k8s.io/yaml',version='v1.3.0')
        path = unquote(path).replace("!", "")
        path = path.removeprefix(GO_REMOTE_PREFIX)
        name, version = path.split("@v")
        name = name.removesuffix("/")
        version = version.removeprefix("/")
        if version.endswith(".mod"):
            version = version.removesuffix(".mod")
        elif version.endswith(".info"):
            version = version.removesuffix(".info")
        elif version.endswith(".zip"):
            version = version.removesuffix(".zip")
        return f"uid.obj.comp.package.go(name='{name}',version='{version}')"

    def mavenPathToUid(self, path):
        # example:
        # /artifactory/maven/org/apache/maven/doxia/doxia-sink-api/1.11.1/doxia-sink-api-1.11.1.jar ->
        # uid.obj.comp.package.maven(name='org.apache.maven.doxia:doxia-sink-api',version='1.11.1')
        path = path.removeprefix(MAVEN_REMOTE_PREFIX)
        tokenstr, _ = os.path.split(path)
        mod_str, version = os.path.split(tokenstr)
        package_path, module_name = os.path.split(mod_str)
        package_path = package_path.replace("/", ".")
        name = f"{package_path}:{module_name}"
        return f"uid.obj.comp.package.maven(name='{name}',version='{version}')"

    def gradlePathToUid(self, path):
        path = path.removeprefix(GRADLE_REMOTE_PREFIX)
        tokenstr, _ = os.path.split(path)
        mod_str, version = os.path.split(tokenstr)
        package_path, module_name = os.path.split(mod_str)
        package_path = package_path.replace("/", ".")
        name = f"{package_path}:{module_name}"
        return f"uid.obj.comp.package.gradle(name='{name}',version='{version}')"

    def extractPathsFromObservations(self, observationFile) -> list[str]:
        observations = json.load(observationFile)
        additional_paths = []
        items = observations["items"]
        for item in items:
            if item['typename'] != 'local_observation.https':
                continue
            groups = item['groups']
            for group in groups:
                if group['method'] != 'GET':
                    continue
                paths = group['paths']
                additional_paths.extend(paths)
        return additional_paths

    def addInputSource(self, file, checksum):
        if not self.srpcli:
            return

        filename = os.path.basename(file)
        self.schematic["input_templates"]["source-comps"][
            f"uid.obj.comp.fileset(org='photon.source',name='{filename}',build_id='{checksum}')"
        ] = {"incorporated": True, "is_components_source": True, "modified": True,
             "interaction_type": "static_linking","usages": ["functionality", "building",
                                                            "testing"]}

    def addInputRPMS(self, files):
        if not self.srpcli:
            return

        for file in files:
            filename = os.path.basename(file)
            try:
                self.schematic["input_templates"]["rpm-comps"][
                    self.rpmFileNameToUid(filename)
                ] = {"incorporated": False, "usages": ["building"],
                     "modified": False, "interaction_type": "dev_tools/excluded"}
            except Exception as e:
                self.logger.exception(e)

    def addAdditionalDeps(self, observationsFile):
        if not self.srpcli:
            return
        try:
            with open(observationsFile) as observationsfp:
                additional_paths = self.extractPathsFromObservations(observationsfp)
                for path in additional_paths:
                    if path.startswith(GO_REMOTE_PREFIX):
                        self.schematic["input_templates"]["go-comps"][self.goDepPathToUid(path)] = {
                            "incorporated": True, "usages": ["functionality", "building"], "modified": False, "interaction_type": "static_linking"}
                    elif path.startswith(MAVEN_REMOTE_PREFIX) and path.endswith(".jar"):
                        self.schematic["input_templates"]["maven-comps"][self.mavenPathToUid(path)] = {
                            "incorporated": False, "usages": ["building"], "modified": False, "interaction_type": "dev_tools/excluded"}
                    elif path.startswith(GRADLE_REMOTE_PREFIX) and path.endswith(".jar"):
                        self.schematic["input_templates"]["gradle-comps"][self.gradlePathToUid(path)] = {
                            "incorporated": False, "usages": ["building"], "modified": False, "interaction_type": "dev_tools/excluded"}
        except Exception as e:
            self.logger.exception(e)

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

            if n == f"{self.package}-debuginfo":
                description = f"Debuginfo for {self.package}"
            elif a == "src":
                description = f"Source RPM for {self.package}"
            else:
                fullVersion = f"{v}-{r}.{t}"
                description = f"{SPECS.getData().getDescription(n, fullVersion)}"

            spdx_info = copy.deepcopy(self.spdx_package_common)
            spdx_info["package"]["detailed_description"] = description

            self.schematic["outputs"][self.rpmFileNameToUid(filename)] = {
                "merge_input_templates": ["rpm-comps", "source-comps", "maven-comps", "gradle-comps", "go-comps"],
                "spdx_info": spdx_info,
                "inputs": {
                    "$(sources:source_uid)": {
                        "is_components_source": True,
                        "incorporated": True,
                        "usages": ["functionality", "building", "testing"],
                        "modified": False, "interaction_type": "static_linking"
                    }
                },
                "product": {
                    "distribution_type": "external",
                    "embedded_in_hardware": False
                }
            }

    def addCommand(self, cmd, env):
        if not self.srpcli:
            return

        env_str = " ".join([f"{k}={v}" for k, v in env.items()])
        if env_str:
            env_str += " "
        self.srpcli_run(
            ["provenance", "action", "import-cmd", "--cmd", env_str + " ".join(cmd)]
        )

    def addObservation(self, observation):
        if not self.srpcli:
            if observation:
                observation.close()
            return

        network_required = SPECS.getData().isNetworkRequired(
            self.package, self.fullVersion
        )
        if not observation:
            if network_required:
                raise Exception("Observation file is required but not generated")
            return

        with tempfile.NamedTemporaryFile() as temp:
            shutil.copyfileobj(observation, temp)
            temp.flush()
            self.addAdditionalDeps(temp.name)
            self.srpcli_run(
                [
                    "provenance",
                    "action",
                    "import-observation",
                    "--name=build-observation",
                    "--file",
                    temp.name,
                ]
            )

        observation.close()

    def finalize(self):
        if not self.srpcli:
            return

        schematic_filename = os.path.join(self.srp_workdir, "package.schematic.json")
        with open(schematic_filename, "w") as f:
            json.dump(self.schematic, f)
        self.srpcli_run(["provenance", "action", "stop"])
        self.srpcli_run(
            [
                "provenance",
                "schematic",
                "--verbose",
                "--no-schematic",
                "--path",
                schematic_filename,
            ]
        )
        self.srpcli_run(
            [
                "provenance",
                "compile",
                "--saveto",
                os.path.join(self.srp_workdir, f"{self.pkg}.provenance.json"),
            ]
        )
        if os.path.isfile(schematic_filename):
            os.remove(schematic_filename)
        # "_provenance.json" is a temporary file used by SRPCLI to store provenance content between SRPCLI invocations
        # It is created by "provenance init" and not removed by "compile".
        # Remove it manually.
        with suppress(Exception):
            os.remove(os.path.join(self.srp_workdir, "_provenance.json"))
