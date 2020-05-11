#!/usr/bin/env python3

import os
import yaml
import time
import json
import subprocess
import uuid
import sys
from argparse import ArgumentParser
from Logger import Logger
from constants import constants
from kubernetes import client, config, watch
from kubernetes import stream
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

        self.aApiClient = self.getClusterAuthorization()
        self.coreV1ApiInstance = client.CoreV1Api(self.aApiClient)
        self.batchV1ApiInstance = client.BatchV1Api(self.aApiClient)
        self.AppsV1ApiInstance = client.AppsV1Api(self.aApiClient)


    def getClusterAuthorization(self):
        aToken = self.distributedBuildConfig["kubernetesAuthorizationToken"]
        aConfiguration = client.Configuration()
        aConfiguration.host = "https://" + self.distributedBuildConfig["kubernetes-master-ip"] + ":" + self.distributedBuildConfig["kubernetes-master-port"]
        aConfiguration.verify_ssl = False
        aConfiguration.ssl_ca_cert = None
        aConfiguration.api_key = {"authorization": "Bearer " + aToken}
        return client.ApiClient(aConfiguration)

    def getBuildGuid(self):
         guid = str(uuid.uuid4()).split("-")[1]
         guid = guid.lower()
         self.logger.info("guid: %s"%guid)
         return guid

    def createPersistentVolume(self):
        with open(os.path.join(os.path.dirname(__file__), "yaml/persistentVolume.yaml"), 'r') as f:
            for pvFile in yaml.safe_load_all(f):
                pvFile['metadata']['name'] += "-" + self.buildGuid
                pvFile['metadata']['labels']['storage-tier'] += "-" + self.buildGuid
                pvFile['spec']['nfs']['server'] = self.distributedBuildConfig["nfs-server-ip"]
                if 'nfspod' in pvFile['metadata']['name']:
                    pvFile['spec']['nfs']['path'] = self.distributedBuildConfig["nfs-server-path"]
                else:
                    pvFile['spec']['nfs']['path'] = self.distributedBuildConfig["nfs-server-path"] + "/build-" + self.buildGuid + pvFile['spec']['nfs']['path']

                try:
                    resp = self.coreV1ApiInstance.create_persistent_volume(body=pvFile)
                    self.logger.info("Created pv %s"%resp.metadata.name)
                except client.rest.ApiException as e:
                    self.logger.error("Exception when calling CoreV1Api->create_persistent_volume: %s\n" % e.reason)
                    self.clean()
                    sys.exit(1)

    def createPersistentVolumeClaim(self):
        with open(os.path.join(os.path.dirname(__file__), "yaml/persistentVolumeClaim.yaml"), 'r') as f:
            for pvcFile in yaml.safe_load_all(f):
                pvcFile['metadata']['name'] += "-" + self.buildGuid
                pvcFile['spec']['selector']['matchLabels']['storage-tier'] += "-" + self.buildGuid
                try:
                    resp = self.coreV1ApiInstance.create_namespaced_persistent_volume_claim(namespace='default', body=pvcFile)
                    self.logger.info("created pvc %s"%resp.metadata.name)
                except client.rest.ApiException as e:
                    self.logger.error("Exception when calling CoreV1Api->create_namespaced_persistent_volume_claim: %s\n" % e.reason)
                    self.clean()
                    sys.exit(1)

    def createNfsPod(self):
        with open(os.path.join(os.path.dirname(__file__), "yaml/nfspod.yaml")) as f:
            nfspodFile = yaml.safe_load(f)
            nfspodFile['metadata']['name'] += "-" + self.buildGuid
            nfspodFile['spec']['containers'][0]['workingDir'] += "/build-" + self.buildGuid
            nfspodFile['spec']['volumes'][0]['persistentVolumeClaim']['claimName'] += "-" + self.buildGuid
            try:
                resp = self.coreV1ApiInstance.create_namespaced_pod(namespace='default', body=nfspodFile)
                self.logger.info("created nfspod %s"%resp.metadata.name)
            except client.rest.ApiException as e:
                self.logger.error("Exception when calling CoreV1Api->create_namespaced_pod: %s\n" % e.reason)
                self.clean()
                sys.exit(1)

    def createMasterService(self):
        with open(os.path.join(os.path.dirname(__file__), "yaml/masterService.yaml")) as f:
            masterServiceFile = yaml.safe_load(f)
            masterServiceFile['metadata']['name'] += "-" + self.buildGuid
            masterServiceFile['spec']['selector']['app'] += "-" + self.buildGuid
            try:
                resp = self.coreV1ApiInstance.create_namespaced_service(namespace='default', body=masterServiceFile)
                self.logger.info("created pvc %s"%resp.metadata.name)
            except client.rest.ApiException as e:
                self.logger.error("Exception when calling CoreV1Api->create_namespaced_service: %s\n" % e.reason)
                self.clean()
                sys.exit(1)

    def createMasterJob(self):
        with open(os.path.join(os.path.dirname(__file__), "yaml/master.yaml")) as f:
            masterFile = yaml.safe_load(f)
            masterFile['metadata']['name'] += "-" + self.buildGuid
            masterFile['spec']['template']['metadata']['labels']['app'] += "-" + self.buildGuid
            masterFile['spec']['template']['spec']['volumes'][0]['persistentVolumeClaim']['claimName'] += "-" + self.buildGuid
            str = masterFile['spec']['template']['spec']['containers'][0]['args'][1]
            masterFile['spec']['template']['spec']['containers'][0]['args'][1] = str + " && " + self.distributedBuildConfig["command"]
            try:
                resp = self.batchV1ApiInstance.create_namespaced_job(namespace="default", body=masterFile)
                self.logger.info("Created Job %s"%resp.metadata.name)
            except client.rest.ApiException as e:
                self.logger.error("Exception when calling BatchV1Api->create_namespaced_job: %s\n" % e.reason)
                self.clean()
                sys.exit(1)

    def createDeployment(self):
        with open(os.path.join(os.path.dirname(__file__), "yaml/worker.yaml")) as f:
            workerFile = yaml.safe_load(f)
            workerFile['metadata']['name'] += "-" + self.buildGuid
            workerFile['spec']['template']['spec']['containers'][0]['env'][0]['value'] = self.buildGuid.upper()
            workerFile['spec']['template']['spec']['volumes'][0]['persistentVolumeClaim']['claimName'] += "-" + self.buildGuid
            workerFile['spec']['template']['spec']['volumes'][1]['persistentVolumeClaim']['claimName'] += "-" + self.buildGuid
            workerFile['spec']['template']['spec']['volumes'][2]['persistentVolumeClaim']['claimName'] += "-" + self.buildGuid
            workerFile['spec']['template']['spec']['volumes'][3]['persistentVolumeClaim']['claimName'] += "-" + self.buildGuid
            workerFile['spec']['template']['spec']['volumes'][4]['persistentVolumeClaim']['claimName'] += "-" + self.buildGuid
            workerFile['spec']['template']['spec']['volumes'][5]['persistentVolumeClaim']['claimName'] += "-" + self.buildGuid
            workerFile['spec']['replicas'] = self.distributedBuildConfig["pods"]
            try:
                resp = self.AppsV1ApiInstance.create_namespaced_deployment(body=workerFile, namespace="default")
                self.logger.info("Created deployment %s"%resp.metadata.name)
            except client.rest.ApiException as e:
                self.logger.error("Exception when calling AppsV1Api->create_namespaced_deployment: %s\n" % e.reason)
                self.clean()
                sys.exit(1)

    def deletePersistentVolume(self):
        pvNames = ["builder", "logs", "specs", "rpms", "publishrpms", "publishxrpms", "photon", "nfspod"]
        for name in pvNames:
            try:
                resp = self.coreV1ApiInstance.delete_persistent_volume(name + "-" + self.buildGuid)
                self.logger.info("Deleted pv %s"%name)
            except client.rest.ApiException as e:
                self.logger.error("Exception when calling CoreV1Api->delete_persistent_volume: %s\n" % e.reason)

    def deletePersistentVolumeClaim(self):
        pvcNames = ["builder", "logs", "specs", "rpms", "publishrpms", "publishxrpms", "photon", "nfspod"]
        for name in pvcNames:
            try:
                resp = self.coreV1ApiInstance.delete_namespaced_persistent_volume_claim(name + "-" + self.buildGuid, namespace="default")
                self.logger.info("Deleted pvc %s"%name)
            except client.rest.ApiException as e:
                self.logger.error("Exception when calling CoreV1Api->delete_namespaced_persistent_volume_claim: %s\n" % e.reason)

    def deleteMasterJob(self):
       try:
           job = "master" + "-" + self.buildGuid
           resp = self.batchV1ApiInstance.delete_namespaced_job(name=job, namespace="default", propagation_policy="Foreground", grace_period_seconds=10)
           self.logger.info("deleted job master")
       except client.rest.ApiException as e:
           self.logger.error("Exception when calling BatchV1Api->delete_namespaced_job: %s\n" % e.reason)

    def deleteBuild(self):
        count = 2
        while count:
            pod = "nfspod" + "-" + self.buildGuid
            cmd = ['/bin/sh', '-c', 'cd /root; ls; rm -rf ' + 'build-' + self.buildGuid]
            resp = stream.stream(self.coreV1ApiInstance.connect_get_namespaced_pod_exec, pod, 'default', command=cmd, stderr=True, stdin=False, stdout=True, tty=False)
            self.logger.info("%s"%resp)
            count -= 1

        self.logger.info("Deleted Build Successfully")

    def deleteNfsPod(self):
        try:
            pod = "nfspod" + "-" + self.buildGuid
            resp = self.coreV1ApiInstance.delete_namespaced_pod(name=pod, namespace="default")
            self.logger.info("deleted nfs pod")
        except client.rest.ApiException as e:
            self.logger.error("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e.reason)

    def deleteMasterService(self):
       try:
           service = "master-service" + "-" + self.buildGuid
           resp = self.coreV1ApiInstance.delete_namespaced_service(name=service, namespace="default")
           self.logger.info("deleted master service")
       except client.rest.ApiException as e:
           self.logger.error("Exception when calling BatchV1Api->delete_namespaced_service %s\n" % e.reason)

    def deleteDeployment(self):
        try:
            deploy = "worker" + "-" + self.buildGuid
            resp = self.AppsV1ApiInstance.delete_namespaced_deployment(name = deploy, namespace="default", grace_period_seconds=15)
            self.logger.info("deleted worker deployment ")
        except client.rest.ApiException as e:
            self.logger.error("Exception when calling AppsV1Api->delete_namespaced_deployment: %s\n" % e.reason)

    def copyToNfs(self):
        self.createNfsPod()
        podName = "nfspod" + "-" + self.buildGuid
        while True:
            resp = self.coreV1ApiInstance.read_namespaced_pod(name=podName, namespace='default')
            status = resp.status.phase
            if status == 'Running':
                break

        cmd = "kubectl cp " +str( os.path.join(os.path.dirname(__file__)).replace('support/package-builder', '')) \
               + " " + podName + ":/root/" + "build-" + self.buildGuid + "/photon"
        self.logger.info("%s"%cmd)
        process = subprocess.Popen("%s" %cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = process.wait()
        if retval == 0:
            self.logger.info("kubectl cp successfull.")
            self.deleteNfsPod()
        else:
            self.logger.error("kubectl cp failed.")
            self.clean()
            sys.exit(1)

    def copyFromNfs(self):
        self.createNfsPod()
        podName = "nfspod" + "-" + self.buildGuid
        while True:
            resp = self.coreV1ApiInstance.read_namespaced_pod(name=podName, namespace='default')
            status = resp.status.phase
            if status == 'Running':
                break

        cmd = "kubectl cp" + " " + podName + ":/root/" + "build-" + self.buildGuid + "/photon/stage" + " " + str( os.path.join(os.path.dirname(__file__)).replace('support/package-builder', '')) + "stage"
        self.logger.info("%s"%cmd)
        process = subprocess.Popen("%s" %cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = process.wait()
        if retval == 0:
            self.logger.info("kubectl cp successfull.")
        else:
            self.logger.error("kubectl cp failed.")
            self.deleteBuild()
            self.clean()
            sys.exit(1)

    def monitorJob(self):
        w = watch.Watch()
        for job in w.stream(self.batchV1ApiInstance.list_namespaced_job, namespace='default', timeout_seconds=21600):
            if "master" in job['object'].metadata.name:
                name = job['object']
                self.logger.info("Checking job status ...")
                self.logger.debug(name.status)
                if name.status.succeeded or name.status.failed:
                    self.logger.debug("job status ...")
                    self.logger.debug(name.status)
                    break

    def getLogs(self):
        label = "app=master" + "-" + self.buildGuid
        resp = self.coreV1ApiInstance.list_namespaced_pod(label_selector = label, namespace='default')
        podName = resp.items[0].metadata.name
        status = ''
        while True:
            resp = self.coreV1ApiInstance.read_namespaced_pod(name=podName, namespace='default')
            status = resp.status.phase
            if status == 'Running' or status == 'Succeeded':
                break

        w = watch.Watch()
        try:
            for line in w.stream(self.coreV1ApiInstance.read_namespaced_pod_log, name = podName, namespace='default'):
                self.logger.info(line)
        except Exception as e:
            self.logger.error(e)
        self.logger.info("pod terminated")

    def clean(self):
        self.logger.info("-"*45)
        self.logger.info("")
        self.logger.info("Cleaning up ...")
        self.deleteMasterJob()
        self.deleteNfsPod()
        self.deleteMasterService()
        self.deleteDeployment()
        self.deletePersistentVolumeClaim()
        self.deletePersistentVolume()

    def create(self):
        self.logger.info("-"*45)
        self.logger.info("")
        self.createPersistentVolume()
        self.createPersistentVolumeClaim()
        self.copyToNfs()
        self.createMasterService()
        self.createMasterJob()
        self.createDeployment()

if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("-g", "--distributed-build-option-file", dest="distributedBuildOptionFile",
                        default="../../common/data/distributed_build_options.json")
    parser.add_argument("-l", "--log-path", dest="logPath", default="../../stage/LOGS")
    parser.add_argument("-y", "--log-level", dest="logLevel", default="info")
    options = parser.parse_args()
    constants.setLogPath(options.logPath)
    constants.setLogLevel(options.logLevel)

    with open(os.path.join(os.path.dirname(__file__), options.distributedBuildOptionFile), 'r') as configFile:
        distributedBuildConfig = json.load(configFile)

    distributedBuilder = DistributedBuilder(distributedBuildConfig)
    distributedBuilder.create()
    distributedBuilder.getLogs()
    distributedBuilder.monitorJob()
    distributedBuilder.copyFromNfs()
    distributedBuilder.deleteBuild()
    distributedBuilder.clean()
