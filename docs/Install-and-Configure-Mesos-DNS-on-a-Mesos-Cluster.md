# Install and Configure Mesos DNS on a Mesos Cluster

## Overview 

Before you read this How-To, please read: [Install and Configure a Production-Ready Mesos Cluster on PhotonOS](Install-and-Configure-a-Production-Ready-Mesos-Cluster-on-Photon-OS.md), [Install and Configure Marathon for Mesos Cluster on PhotonOS](Install-and-Configure-Marathon-for-Mesos-Cluster-on-PhotonOS.md) and [Install and Configure DCOS CLI for Mesos](Install-and-Configure-DCOS-CLI-for-Mesos.md).

After you have fully installed and configured the Mesos cluster, you can execute jobs on it. However, if you want a service discovery and load balancing capabilities you will need to use Mesos-DNS and Haproxy. In this How-To I will explain how to install and configure Mesos-DNS for your Mesos cluster.
Mesos-DNS supports service discovery in Apache Mesos clusters. It allows applications and services running on Mesos to find each other through the domain name system (DNS), similarly to how services discover each other throughout the Internet. Applications launched by Marathon are assigned names like search.marathon.mesos. Mesos-DNS translates these names to the IP address and port on the machine currently running each application. To connect to an application in the Mesos datacenter, all you need to know is its name. Every time a connection is initiated, the DNS translation will point to the right machine in the datacenter.

![Architecture](images/architecture.png)

## Installation

I will explain how to configure Mesos-DNS docker and run it through Marathon. I will show you how to create a configuration file for a mesos-dns-docker container and how to run it via Marathon.

```
root@pt-mesos-node1 [ ~ ]# cat /etc/mesos-dns/config.json
{
  "zk": "zk://192.168.0.1:2181,192.168.0.2:2181,192.168.0.3:2181/mesos",
  "masters": ["192.168.0.1:5050", "192.168.0.2:5050", "192.168.0.3:5050"],
  "refreshSeconds": 60,
  "ttl": 60,
  "domain": "mesos",
  "port": 53,
  "resolvers": ["8.8.8.8"],
  "timeout": 5,
  "httpon": true,
  "dnson": true,
  "httpport": 8123,
  "externalon": true,
  "SOAMname": "ns1.mesos",
  "SOARname": "root.ns1.mesos",
  "SOARefresh": 60,
  "SOARetry":   600,
  "SOAExpire":  86400,
  "SOAMinttl": 60
}
```

### Create Application Run File

Next step is to create a json file and run the service from Marathon for HA. It is possible to run the service via API or via DCOS CLI.

```
client:~/mesos/jobs$ cat mesos-dns-docker.json
{
    "args": [
        "/mesos-dns",
        "-config=/config.json"
    ],
    "container": {
        "docker": {
            "image": "mesosphere/mesos-dns",
            "network": "HOST"
        },
        "type": "DOCKER",
        "volumes": [
            {
                "containerPath": "/config.json",
                "hostPath": "/etc/mesos-dns/config.json",
                "mode": "RO"
            }
        ]
    },
    "cpus": 0.2,
    "id": "mesos-dns-docker",
    "instances": 3,
    "constraints": [["hostname", "CLUSTER", "pt-mesos-node2.example.com"]]
}
```

Now we can see in the Marthon and Mesos UI that we launched the application.


### Setup Resolvers and Testing

To allow Mesos tasks to use Mesos-DNS as the primary DNS server, you must edit the file */etc/resolv.conf* in every slave and add a new nameserver. For instance, if *mesos-dns* runs on the server with IP address *192.168.0.5* at the beginning of */etc/resolv.conf* on every slave.

```
root@pt-mesos-node2 [ ~/mesos-dns ]# cat /etc/resolv.conf
# This file is managed by systemd-resolved(8). Do not edit.
#
# Third party programs must not access this file directly, but
#only through the symlink at /etc/resolv.conf. To manage
# resolv.conf(5) in a different way, replace the symlink by a
# static file or a different symlink.
nameserver 192.168.0.5
nameserver 192.168.0.4
nameserver 8.8.8.8
```

Let's run a simple Docker app and see if we can resolve it in DNS.

```
client:~/mesos/jobs$ cat docker.json
{
    "id": "docker-hello",
    "container": {
        "docker": {
            "image": "centos"
        },
        "type": "DOCKER",
        "volumes": []
    },
    "cmd": "echo hello; sleep 10000",
    "mem": 16,
    "cpus": 0.1,
    "instances": 10,
    "disk": 0.0,
    "ports": [0]
}
```
```
client:~/mesos/jobs$ dcos marathon app add docker.json
```

Let's try to resolve it.

```
root@pt-mesos-node2 [ ~/mesos-dns ]# dig _docker-hello._tcp.marathon.mesos SRV
;; Truncated, retrying in TCP mode.
; <<>> DiG 9.10.1-P1 <<>> _docker-hello._tcp.marathon.mesos SRV
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 25958
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 10, AUTHORITY: 0, ADDITIONAL: 10
;; QUESTION SECTION:
;_docker-hello._tcp.marathon.mesos. IN SRV
;; ANSWER SECTION:
_docker-hello._tcp.marathon.mesos. 60 IN SRV 0 0 31998 docker-hello-4bjcf-s2.marathon.slave.mesos.
_docker-hello._tcp.marathon.mesos. 60 IN SRV 0 0 31844 docker-hello-jexm6-s1.marathon.slave.mesos.
_docker-hello._tcp.marathon.mesos. 60 IN SRV 0 0 31111 docker-hello-6ms44-s2.marathon.slave.mesos.
_docker-hello._tcp.marathon.mesos. 60 IN SRV 0 0 31719 docker-hello-muhui-s2.marathon.slave.mesos.
_docker-hello._tcp.marathon.mesos. 60 IN SRV 0 0 31360 docker-hello-jznf4-s1.marathon.slave.mesos.
_docker-hello._tcp.marathon.mesos. 60 IN SRV 0 0 31306 docker-hello-t41ti-s1.marathon.slave.mesos.
_docker-hello._tcp.marathon.mesos. 60 IN SRV 0 0 31124 docker-hello-mq3oz-s1.marathon.slave.mesos.
_docker-hello._tcp.marathon.mesos. 60 IN SRV 0 0 31816 docker-hello-tcep8-s1.marathon.slave.mesos.
_docker-hello._tcp.marathon.mesos. 60 IN SRV 0 0 31604 docker-hello-5uu37-s1.marathon.slave.mesos.
_docker-hello._tcp.marathon.mesos. 60 IN SRV 0 0 31334 docker-hello-jqihw-s1.marathon.slave.mesos.
 
;; ADDITIONAL SECTION:
docker-hello-muhui-s2.marathon.slave.mesos. 60 IN A 192.168.0.5
docker-hello-4bjcf-s2.marathon.slave.mesos. 60 IN A 192.168.0.5
docker-hello-jexm6-s1.marathon.slave.mesos. 60 IN A 192.168.0.6
docker-hello-jqihw-s1.marathon.slave.mesos. 60 IN A 192.168.0.6
docker-hello-mq3oz-s1.marathon.slave.mesos. 60 IN A 192.168.0.6
docker-hello-tcep8-s1.marathon.slave.mesos. 60 IN A 192.168.0.6
docker-hello-6ms44-s2.marathon.slave.mesos. 60 IN A 192.168.0.5
docker-hello-t41ti-s1.marathon.slave.mesos. 60 IN A 192.168.0.4
docker-hello-jznf4-s1.marathon.slave.mesos. 60 IN A 192.168.0.4
docker-hello-5uu37-s1.marathon.slave.mesos. 60 IN A 192.168.0.4
;; Query time: 0 msec
;; SERVER: 192.168.0.5#53(192.168.0.5)
;; WHEN: Sun Dec 27 14:36:32 UTC 2015
;; MSG SIZE  rcvd: 1066
```

We can see that we can resolve our app.