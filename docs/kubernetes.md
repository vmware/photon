Running Kubernetes on Photon OS
-----------------------------------------------------

**Table of Contents**

- [Prerequisites](#prerequisites)
- [Instructions](#instructions)

## Prerequisites

* You need 2 or more machines with Photon installed.

## Instructions

This document gets you started using Kubernetes with Photon OS. The instructions present a manual configuration that gets one worker node running to help you understand  the underlying packages, services, ports, and so forth. 

The Kubernetes package provides several services: kube-apiserver, kube-scheduler, kube-controller-manager, kubelet, kube-proxy.  These services are managed by systemd. Their configuration resides in a central location: /etc/kubernetes.  

The following instructions break the services up between the hosts.  The first host, photon-master, will be the Kubernetes master.  This host will run the kube-apiserver, kube-controller-manager, and kube-scheduler.  In addition, the master will also run _etcd_ (not needed if _etcd_ runs on a different host but this guide assumes that _etcd_ and Kubernetes master run on the same host).  The remaining host, photon-node will be the node and run kubelet, proxy and docker.

**System Information:**

Hosts:

```
photon-master = 192.168.121.9
photon-node = 192.168.121.65
```

**Prepare the hosts:**
    
* Install Kubernetes on all hosts - photon-{master,node}.

```sh
tdnf install kubernetes
```

* Install etcd and iptables on photon-master

```sh
tdnf install etcd iptables
```

* Install docker on photon-node

```sh
tdnf install docker
```

* Add master and node to /etc/hosts on all machines (not needed if hostnames already in DNS). Make sure that communication works between photon-master and photon-node by using a utility such as ping.

```sh
echo "192.168.121.9	photon-master
192.168.121.65	photon-node" >> /etc/hosts
```

* Edit /etc/kubernetes/config which will be the same on all hosts (master and node) to contain:

```sh
# Comma separated list of nodes in the etcd cluster
KUBE_MASTER="--master=http://photon-master:8080"

# logging to stderr routes it to the systemd journal
KUBE_LOGTOSTDERR="--logtostderr=true"

# journal message level, 0 is debug
KUBE_LOG_LEVEL="--v=0"

# Should this cluster be allowed to run privileged docker containers
KUBE_ALLOW_PRIV="--allow_privileged=false"
```

**Configure the Kubernetes services on the master.**

* Edit /etc/kubernetes/apiserver to appear as such.  The service_cluster_ip_range IP addresses must be an unused block of addresses, not used anywhere else.  They do not need to be routed or assigned to anything.

```sh
# The address on the local server to listen to.
KUBE_API_ADDRESS="--address=0.0.0.0"

# Comma separated list of nodes in the etcd cluster
KUBE_ETCD_SERVERS="--etcd_servers=http://127.0.0.1:4001"

# Address range to use for services
KUBE_SERVICE_ADDRESSES="--service-cluster-ip-range=10.254.0.0/16"

# Add your own
KUBE_API_ARGS=""
```

* Start the appropriate services on master:

```sh
for SERVICES in etcd kube-apiserver kube-controller-manager kube-scheduler; do
	systemctl restart $SERVICES
	systemctl enable $SERVICES
	systemctl status $SERVICES
done
```

* Addition of nodes:

* Create following node.json file on Kubernetes master node:

```json
{
    "apiVersion": "v1",
    "kind": "Node",
    "metadata": {
        "name": "photon-node",
        "labels":{ "name": "photon-node-label"}
    },
    "spec": {
        "externalID": "photon-node"
    }
}
```

Now create a node object internally in your Kubernetes cluster by running:

```console
$ kubectl create -f ./node.json

$ kubectl get nodes
NAME                LABELS              STATUS
photon-node         name=photon-node-label     Unknown
```

Please note that in the above, it only creates a representation for the node
_photon-node_ internally. It does not provision the actual _photon-node_. Also, it
is assumed that _photon-node_ (as specified in `name`) can be resolved and is
reachable from Kubernetes master node. This guide will discuss how to provision
a Kubernetes node (photon-node) below.

**Configure the Kubernetes services on the node.**

***We need to configure the kubelet on the node.***

* Edit /etc/kubernetes/kubelet to appear as such:

```sh
###
# Kubernetes kubelet (node) config

# The address for the info server to serve on (set to 0.0.0.0 or "" for all interfaces)
KUBELET_ADDRESS="--address=0.0.0.0"

# You may leave this blank to use the actual hostname
KUBELET_HOSTNAME="--hostname_override=photon-node"

# location of the api-server
KUBELET_API_SERVER="--api_servers=http://photon-master:8080"

# Add your own
#KUBELET_ARGS=""
```

* Start the appropriate services on the node (photon-node).

```sh
for SERVICES in kube-proxy kubelet docker; do 
    systemctl restart $SERVICES
    systemctl enable $SERVICES
    systemctl status $SERVICES 
done
```

* Check to make sure now the cluster can see the photon-node on photon-master, and its status changes to _Ready_.

```console
kubectl get nodes
NAME                LABELS              STATUS
photon-node          name=photon-node-label     Ready
```

* Deletion of nodes:

To delete _photon-node_ from your Kubernetes cluster, one should run the following on photon-master (Please do not do it, it is just for information):

```sh
kubectl delete -f ./node.json
```

*You should be finished.*

**The cluster should be running. Launch a test pod.**

You should have a functional cluster. Check out [101](https://github.com/GoogleCloudPlatform/kubernetes/blob/master/docs/user-guide/walkthrough/README.md).


