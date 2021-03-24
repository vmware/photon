---
title:  Prepare the Hosts
weight: 2
---

The following packages have to be installed. If the `tdnf` command returns "Nothing to do," the package is already installed.
    
* Install Kubernetes on all hosts (both `photon-master` and `photon-node`).

    ```console
    tdnf install kubernetes
    ``` 

* Install iptables on photon-master and photon-node:

    ```console
    tdnf install iptables
    ```

* Open the tcp port 8080 (api service) on the photon-master in the firewall

    ```console
    iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
    ```

* Open the tcp port 10250 (api service) on the photon-node in the firewall

    ```console
    iptables -A INPUT -p tcp --dport 10250 -j ACCEPT
    ```


* Install Docker on photon-node:

    ```console
    tdnf install docker
    ```

* Add master and node to /etc/hosts on all machines (not needed if the hostnames are already in DNS). Make sure that communication works between photon-master and photon-node by using a utility such as ping.

    ```sh
    echo "192.168.121.9	photon-master
    192.168.121.65	photon-node" >> /etc/hosts
    ```

* Edit /etc/kubernetes/config, which will be the same on all the hosts (master and node), so that it contains the following lines:

    ```ini
    # Comma separated list of nodes in the etcd cluster
    KUBE_MASTER="--master=http://photon-master:8080"

    # logging to stderr routes it to the systemd journal
    KUBE_LOGTOSTDERR="--logtostderr=true"

    # journal message level, 0 is debug
    KUBE_LOG_LEVEL="--v=0"

    # Should this cluster be allowed to run privileged docker containers
    KUBE_ALLOW_PRIV="--allow_privileged=false"
    ```
