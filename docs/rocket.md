Running Rocket Containers on Photon OS
======================================

Rocket is a container runtime created by [CoreOS](http://coreos.com). It is designed for composability, security, and speed. 

A command-line interface for running application containers, rkt (pronounced _"rock-it"_) implements the [App Container Spec](https://github.com/coreos/rkt/blob/master/Documentation/app-container.md).

The rkt package is installed by default in the full version of Photon OS. In the minimal version, rkt is an optional package. You can install it by running the following commands as root:

```
tdnf install rocket
```

For more information about the tdnf command, see the [Photon OS Administration Guide](https://github.com/vmware/photon/blob/master/docs/photon-admin-guide.md).


### Running an App Container Image

rkt uses content addressable storage (CAS) for storing an app container image (ACI) on disk. In the following example, the image is downloaded and added to the CAS.

Since rkt verifies signatures by default, you need to first [trust](https://github.com/coreos/rkt/blob/master/Documentation/signing-and-verification-guide.md#establishing-trust) the [CoreOS public key](https://coreos.com/dist/pubkeys/aci-pubkeys.gpg) used to sign the image:

```
$ sudo rkt trust --prefix coreos.com/etcd
Prefix: "coreos.com/etcd"
Key: "https://coreos.com/dist/pubkeys/aci-pubkeys.gpg"
GPG key fingerprint is: 8B86 DE38 890D DB72 9186  7B02 5210 BD88 8818 2190
        CoreOS ACI Builder <release@coreos.com>
Are you sure you want to trust this key (yes/no)? yes
Trusting "https://coreos.com/dist/pubkeys/aci-pubkeys.gpg" for prefix "coreos.com/etcd".
Added key for prefix "coreos.com/etcd" at "/etc/rkt/trustedkeys/prefix.d/coreos.com/etcd/8b86de38890ddb7291867b025210bd8888182190"
```

Now that you have trusted the CoreOS public key, you can bring up a simple etcd instance using the ACI format:

```
$ privateIp=$(ip -4 -o addr show eth0 | cut -d' ' -f7 | cut -d'/' -f1)
$ sudo rkt run coreos.com/etcd:v2.0.4 -- -name vmware-cna \
> -listen-client-urls http://0.0.0.0:2379 \
> -advertise-client-urls http://${privateIp}:2379 \
> -listen-peer-urls http://0.0.0.0:2380 \
> -initial-advertise-peer-urls http://${privateIp}:2380 \
> -initial-cluster vmware-cna=http://${privateIp}:2380 \
> -initial-cluster-state new

rkt: searching for app image coreos.com/etcd:v2.0.4
rkt: fetching image from https://github.com/coreos/etcd/releases/download/v2.0.4/etcd-v2.0.4-linux-amd64.aci
Downloading signature from https://github.com/coreos/etcd/releases/download/v2.0.4/etcd-v2.0.4-linux-amd64.aci.asc
Downloading ACI: [========================================     ] 3.38 MB/3.76 MB
rkt: signature verified:
  CoreOS ACI Builder <release@coreos.com>
Timezone UTC does not exist in container, not updating container timezone.
2015/04/02 13:18:39 no data-dir provided, using default data-dir ./vmware-cna.etcd
2015/04/02 13:18:39 etcd: listening for peers on http://0.0.0.0:2380
2015/04/02 13:18:39 etcd: listening for client requests on http://0.0.0.0:2379
2015/04/02 13:18:39 etcdserver: name = vmware-cna
2015/04/02 13:18:39 etcdserver: data dir = vmware-cna.etcd
2015/04/02 13:18:39 etcdserver: member dir = vmware-cna.etcd/member
2015/04/02 13:18:39 etcdserver: heartbeat = 100ms
2015/04/02 13:18:39 etcdserver: election = 1000ms
2015/04/02 13:18:39 etcdserver: snapshot count = 10000
2015/04/02 13:18:39 etcdserver: advertise client URLs = http://192.168.35.246:2379
2015/04/02 13:18:39 etcdserver: initial advertise peer URLs = http://192.168.35.246:2380
2015/04/02 13:18:39 etcdserver: initial cluster = vmware-cna=http://192.168.35.246:2380
2015/04/02 13:18:39 etcdserver: start member 8f79fa9a50a1689 in cluster 75c533bd1f49730b
2015/04/02 13:18:39 raft: 8f79fa9a50a1689 became follower at term 0
2015/04/02 13:18:39 raft: newRaft 8f79fa9a50a1689 [peers: [], term: 0, commit: 0, applied: 0, lastindex: 0, lastterm: 0]
2015/04/02 13:18:39 raft: 8f79fa9a50a1689 became follower at term 1
2015/04/02 13:18:39 etcdserver: added local member 8f79fa9a50a1689 [http://192.168.35.246:2380] to cluster 75c533bd1f49730b
2015/04/02 13:18:41 raft: 8f79fa9a50a1689 is starting a new election at term 1
2015/04/02 13:18:41 raft: 8f79fa9a50a1689 became candidate at term 2
2015/04/02 13:18:41 raft: 8f79fa9a50a1689 received vote from 8f79fa9a50a1689 at term 2
2015/04/02 13:18:41 raft: 8f79fa9a50a1689 became leader at term 2
2015/04/02 13:18:41 raft.node: 8f79fa9a50a1689 elected leader 8f79fa9a50a1689 at term 2
2015/04/02 13:18:41 etcdserver: published {Name:vmware-cna ClientURLs:[http://192.168.35.246:2379]} to cluster 75c533bd1f49730b
```

When you are done, press the `^]` key three times to kill the container. To generate `^]` on a U.S. keyboard, type Ctrl+] (hold down the Ctrl key and then press the `]` key). The key combination to generate the `^]` escape character might differ on keyboard layouts other than the U.S. keyboard. 

