#!/usr/bin/env python3

import os
import yaml
import time
import json
import uuid
import sys
import signal

from argparse import ArgumentParser
from Logger import Logger
from constants import constants
from kubernetes import client, config, watch
from kubernetes import stream


class DistributedBuilder:

    def __init__(self, distributedBuildConfig, logName=None, logPath=None):
        if logName is None:
            logName = "DistributedBuild"
        if logPath is None:
            logPath = constants.logPath
        self.logName = logName
        self.logPath = logPath
        self.logger = Logger.getLogger(logName, logPath, constants.logLevel)
        self.distributedBuildConfig = distributedBuildConfig
        self.buildGuid = self.getBuildGuid()

        self.aApiClient = config.load_kube_config()
        self.coreV1ApiInstance = client.CoreV1Api(self.aApiClient)
        self.batchV1ApiInstance = client.BatchV1Api(self.aApiClient)
        self.AppsV1ApiInstance = client.AppsV1Api(self.aApiClient)

    def getBuildGuid(self):
        guid = str(uuid.uuid4()).split("-")[1]
        guid = guid.lower()
        self.logger.info(f"guid: {guid}")
        return guid

    def createPersistentVolume(self):
        with open(
            os.path.join(os.path.dirname(__file__), "yaml/persistentVolume.yaml"), "r"
        ) as f:
            for pvFile in yaml.safe_load_all(f):
                pvFile["metadata"]["name"] += f"-{self.buildGuid}"
                pvFile["metadata"]["labels"]["storage-tier"] += f"-{self.buildGuid}"
                pvFile["spec"]["nfs"]["server"] = self.distributedBuildConfig[
                    "nfs-server-ip"
                ]
                if "nfspod" in pvFile["metadata"]["name"]:
                    pvFile["spec"]["nfs"]["path"] = self.distributedBuildConfig[
                        "nfs-server-path"
                    ]
                else:
                    pvFile["spec"]["nfs"]["path"] = (
                        self.distributedBuildConfig["nfs-server-path"]
                        + f"/build-{self.buildGuid}"
                        + pvFile["spec"]["nfs"]["path"]
                    )

                try:
                    resp = self.coreV1ApiInstance.create_persistent_volume(body=pvFile)
                    self.logger.info(f"Created pv {resp.metadata.name}")
                except client.rest.ApiException as e:
                    self.logger.error(
                        f"Exception when calling CoreV1Api->create_persistent_volume: {e.reason}\n"
                    )
                    self.clean()
                    sys.exit(1)

    def createPersistentVolumeClaim(self):
        with open(
            os.path.join(os.path.dirname(__file__), "yaml/persistentVolumeClaim.yaml"),
            "r",
        ) as f:
            for pvcFile in yaml.safe_load_all(f):
                pvcFile["metadata"]["name"] += f"-{self.buildGuid}"
                pvcFile["spec"]["selector"]["matchLabels"][
                    "storage-tier"
                ] += f"-{self.buildGuid}"
                try:
                    resp = self.coreV1ApiInstance.create_namespaced_persistent_volume_claim(
                        namespace="default", body=pvcFile
                    )
                    self.logger.info(f"Created pvc {resp.metadata.name}")
                except client.rest.ApiException as e:
                    self.logger.error(
                        f"Exception when calling CoreV1Api->create_namespaced_persistent_volume_claim: {e.reason}\n"
                    )
                    self.clean()
                    sys.exit(1)

    def createNfsPod(self):
        with open(os.path.join(os.path.dirname(__file__), "yaml/nfspod.yaml")) as f:
            nfspodFile = yaml.safe_load(f)
            nfspodFile["metadata"]["name"] += f"-{self.buildGuid}"
            nfspodFile["spec"]["containers"][0][
                "workingDir"
            ] += f"/build-{self.buildGuid}"
            nfspodFile["spec"]["volumes"][0]["persistentVolumeClaim"][
                "claimName"
            ] += f"-{self.buildGuid}"
            try:
                resp = self.coreV1ApiInstance.create_namespaced_pod(
                    namespace="default", body=nfspodFile
                )
                self.logger.info("Created nfspod {resp.metadata.name}")
            except client.rest.ApiException as e:
                self.logger.error(
                    f"Exception when calling CoreV1Api->create_namespaced_pod: {e.reason}\n"
                )
                self.clean()
                sys.exit(1)

    def createMasterService(self):
        with open(
            os.path.join(os.path.dirname(__file__), "yaml/masterService.yaml")
        ) as f:
            masterServiceFile = yaml.safe_load(f)
            masterServiceFile["metadata"]["name"] += f"-{self.buildGuid}"
            masterServiceFile["spec"]["selector"]["app"] += f"-{self.buildGuid}"
            try:
                resp = self.coreV1ApiInstance.create_namespaced_service(
                    namespace="default", body=masterServiceFile
                )
                self.logger.info(f"Created pvc {resp.metadata.name}")
            except client.rest.ApiException as e:
                self.logger.error(
                    f"Exception when calling CoreV1Api->create_namespaced_service: {e.reason}\n"
                )
                self.clean()
                sys.exit(1)

    def createMasterJob(self):
        with open(os.path.join(os.path.dirname(__file__), "yaml/master.yaml")) as f:
            masterFile = yaml.safe_load(f)
            masterFile["metadata"]["name"] += f"-{self.buildGuid}"
            masterFile["spec"]["template"]["metadata"]["labels"][
                "app"
            ] += f"-{self.buildGuid}"
            masterFile["spec"]["template"]["spec"]["volumes"][0][
                "persistentVolumeClaim"
            ]["claimName"] += f"-{self.buildGuid}"
            tmp_str = masterFile["spec"]["template"]["spec"]["containers"][0]["args"][1]
            masterFile["spec"]["template"]["spec"]["containers"][0]["args"][1] = (
                f"{tmp_str} && " + self.distributedBuildConfig["command"]
            )
            try:
                resp = self.batchV1ApiInstance.create_namespaced_job(
                    namespace="default", body=masterFile
                )
                self.logger.info(f"Created Job {resp.metadata.name}")
            except client.rest.ApiException as e:
                self.logger.error(
                    f"Exception when calling BatchV1Api->create_namespaced_job: {e.reason}\n"
                )
                self.clean()
                sys.exit(1)

    def createDeployment(self):
        with open(os.path.join(os.path.dirname(__file__), "yaml/worker.yaml")) as f:
            guid = f"-{self.buildGuid}"
            workerFile = yaml.safe_load(f)
            workerFile["metadata"]["name"] += guid
            workerFile["spec"]["template"]["spec"]["containers"][0]["env"][0][
                "value"
            ] = self.buildGuid.upper()
            workerFile["spec"]["template"]["spec"]["volumes"][0][
                "persistentVolumeClaim"
            ]["claimName"] += guid
            workerFile["spec"]["template"]["spec"]["volumes"][1][
                "persistentVolumeClaim"
            ]["claimName"] += guid
            workerFile["spec"]["template"]["spec"]["volumes"][2][
                "persistentVolumeClaim"
            ]["claimName"] += guid
            workerFile["spec"]["template"]["spec"]["volumes"][3][
                "persistentVolumeClaim"
            ]["claimName"] += guid
            workerFile["spec"]["template"]["spec"]["volumes"][4][
                "persistentVolumeClaim"
            ]["claimName"] += guid
            workerFile["spec"]["template"]["spec"]["volumes"][5][
                "persistentVolumeClaim"
            ]["claimName"] += guid
            workerFile["spec"]["replicas"] = self.distributedBuildConfig["pods"]
            try:
                resp = self.AppsV1ApiInstance.create_namespaced_deployment(
                    body=workerFile, namespace="default"
                )
                self.logger.info(f"Created deployment {resp.metadata.name}")
            except client.rest.ApiException as e:
                self.logger.error(
                    f"Exception when calling AppsV1Api->create_namespaced_deployment: {e.reason}\n"
                )
                self.clean()
                sys.exit(1)

    def deletePersistentVolume(self):
        pvNames = [
            "builder",
            "logs",
            "specs",
            "rpms",
            "publishrpms",
            "publishxrpms",
            "photon",
            "nfspod",
        ]
        for name in pvNames:
            try:
                resp = self.coreV1ApiInstance.delete_persistent_volume(
                    name + "-" + self.buildGuid
                )
                self.logger.info(f"Deleted pv {name}")
            except client.rest.ApiException as e:
                self.logger.error(
                    f"Exception when calling CoreV1Api->delete_persistent_volume: {e.reason}"
                )

    def deletePersistentVolumeClaim(self):
        pvcNames = [
            "builder",
            "logs",
            "specs",
            "rpms",
            "publishrpms",
            "publishxrpms",
            "photon",
            "nfspod",
        ]
        for name in pvcNames:
            try:
                resp = self.coreV1ApiInstance.delete_namespaced_persistent_volume_claim(
                    f"{name}-{self.buildGuid}", namespace="default"
                )
                self.logger.info(f"Deleted pvc {name}")
            except client.rest.ApiException as e:
                self.logger.error(
                    f"Exception when calling CoreV1Api->delete_namespaced_persistent_volume_claim: {e.reason}\n"
                )

    def deleteMasterJob(self):
        try:
            job = f"master-{self.buildGuid}"
            resp = self.batchV1ApiInstance.delete_namespaced_job(
                name=job,
                namespace="default",
                propagation_policy="Foreground",
                grace_period_seconds=10,
            )
            self.logger.info("deleted job master")
        except client.rest.ApiException as e:
            self.logger.error(
                f"Exception when calling BatchV1Api->delete_namespaced_job: {e.reason}"
            )

    def deleteBuild(self):
        self.logger.info("Removing Build folder ...")
        pod = f"nfspod-{self.buildGuid}"
        cmd = ["/bin/bash", "-c", f"rm -rf /root/build-{self.buildGuid}"]
        try:
            resp = stream.stream(
                self.coreV1ApiInstance.connect_get_namespaced_pod_exec,
                pod,
                "default",
                command=cmd,
                stderr=True,
                stdin=False,
                stdout=True,
                tty=False,
                _preload_content=False,
            )
            resp.run_forever(timeout=10)
            self.logger.info("Deleted Build folder Successfully...")
        except client.rest.ApiException as e:
            self.logger.error(
                f"Exception when calling CoreV1Api->connect_namespaced_pod_exec: {e.reason}"
            )

    def deleteNfsPod(self):
        try:
            pod = f"nfspod-{self.buildGuid}"
            resp = self.coreV1ApiInstance.delete_namespaced_pod(
                name=pod, namespace="default"
            )
            self.logger.info("deleted nfs pod")
        except client.rest.ApiException as e:
            self.logger.error(
                f"Exception when calling CoreV1Api->delete_namespaced_pod: {e.reason}"
            )

    def deleteMasterService(self):
        try:
            service = f"master-service-{self.buildGuid}"
            resp = self.coreV1ApiInstance.delete_namespaced_service(
                name=service, namespace="default"
            )
            self.logger.info("deleted master service")
        except client.rest.ApiException as e:
            self.logger.error(
                f"Exception when calling BatchV1Api->delete_namespaced_service {e.reason}\n"
            )

    def deleteDeployment(self):
        try:
            deploy = f"worker-{self.buildGuid}"
            resp = self.AppsV1ApiInstance.delete_namespaced_deployment(
                name=deploy, namespace="default", grace_period_seconds=15
            )
            self.logger.info("deleted worker deployment ")
        except client.rest.ApiException as e:
            self.logger.error(
                f"Exception when calling AppsV1Api->delete_namespaced_deployment: {e.reason}\n"
            )

    def copyToNfs(self):
        podName = f"nfspod-{self.buildGuid}"
        while True:
            resp = self.coreV1ApiInstance.read_namespaced_pod(
                name=podName, namespace="default"
            )
            status = resp.status.phase
            if status == "Running":
                break

        srcDir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        CommandUtils.runCmd(
            ["kubectl", "cp", srcDir, f"{podName}:/root/build-{self.buildGuid}/photon"],
            logfn=self.logger.info,
        )

    def copyFromNfs(self):
        podName = f"nfspod-{self.buildGuid}"
        while True:
            resp = self.coreV1ApiInstance.read_namespaced_pod(
                name=podName, namespace="default"
            )
            status = resp.status.phase
            if status == "Running":
                break

        stageDir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "stage"
        )
        CommandUtils.runCmd(
            [
                "kubectl",
                "cp",
                f"{podName}:/root/build-{self.buildGuid}/photon/stage",
                stageDir,
            ],
            logfn=self.logger.info,
        )

    def monitorJob(self):
        w = watch.Watch()
        for job in w.stream(
            self.batchV1ApiInstance.list_namespaced_job,
            namespace="default",
            timeout_seconds=21600,
        ):
            if "master" in job["object"].metadata.name:
                name = job["object"]
                self.logger.info("Checking job status ...")
                self.logger.debug(name.status)
                if name.status.succeeded or name.status.failed:
                    self.logger.debug("job status ...")
                    self.logger.debug(name.status)
                    break

    def getLogs(self):
        label = f"app=master-{self.buildGuid}"
        resp = self.coreV1ApiInstance.list_namespaced_pod(
            label_selector=label, namespace="default"
        )
        podName = resp.items[0].metadata.name
        status = ""
        while True:
            resp = self.coreV1ApiInstance.read_namespaced_pod(
                name=podName, namespace="default"
            )
            status = resp.status.phase
            if status == "Running" or status == "Succeeded":
                break

        w = watch.Watch()
        try:
            for line in w.stream(
                self.coreV1ApiInstance.read_namespaced_pod_log,
                name=podName,
                namespace="default",
            ):
                self.logger.info(line)
        except Exception as e:
            self.logger.error(e)
        self.logger.info("pod terminated")

    def signal_handler(self, signal, frame):
        self.logger.info("SIGINT received")
        self.logger.info("Stopping Build ...")
        self.clean()
        sys.exit(0)

    def clean(self):
        self.logger.info("-" * 45)
        self.logger.info("")
        self.logger.info("Cleaning up ...")
        self.deleteBuild()
        self.deleteNfsPod()
        self.deleteMasterJob()
        self.deleteMasterService()
        self.deleteDeployment()
        self.deletePersistentVolumeClaim()
        self.deletePersistentVolume()

    def create(self):
        self.logger.info("-" * 45)
        self.logger.info("")
        self.createPersistentVolume()
        self.createPersistentVolumeClaim()
        self.createNfsPod()
        self.copyToNfs()
        self.createMasterService()
        self.createMasterJob()
        self.createDeployment()


def main(distributedBuildConfig):
    distributedBuilder = DistributedBuilder(distributedBuildConfig)
    signal.signal(signal.SIGINT, distributedBuilder.signal_handler)
    distributedBuilder.create()
    distributedBuilder.getLogs()
    distributedBuilder.monitorJob()
    distributedBuilder.copyFromNfs()
    distributedBuilder.clean()


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument(
        "-g",
        "--distributed-build-option-file",
        dest="distributedBuildOptionFile",
        default="../../common/data/distributed_build_options.json",
    )
    parser.add_argument("-l", "--log-path", dest="logPath", default="../../stage/LOGS")
    parser.add_argument("-y", "--log-level", dest="logLevel", default="info")
    options = parser.parse_args()
    constants.setLogPath(options.logPath)
    constants.setLogLevel(options.logLevel)

    with open(
        os.path.join(os.path.dirname(__file__), options.distributedBuildFile), "r"
    ) as configFile:
        distributedBuildConfig = json.load(configFile)

    main(distributedBuildConfig)
