---
title:  Configure a Worker Node
weight: 2
---

This section describes how to configure a worker node with the following details:

**Node Name**: kube-worker
**Node IP Address**: 10.197.103.232

Install the worker VM using the same Photon OS image.

**Note**: The VM configuration is similar to that of the master node, just with a different IP address.

## Host Names

Change the hostname on the VM using the following command:

```
hostnamectl set-hostname kube-worker
```   

To ensure connectivity with the future working node, kube-worker, modify the file `/etc/hosts` as follows: 

```
cat /etc/hosts
# Begin /etc/hosts (network card version)
10.197.103.246 kube-master
10.197.103.232 kube-worker
  
::1         ipv6-localhost ipv6-loopback
127.0.0.1   localhost.localdomain
127.0.0.1   localhost
127.0.0.1   photon-machine
# End /etc/hosts (network card version)
```

## System Tuning

### IP Tables

Run the following `iptables` commands to open the required ports for Kubernetes to operate.
Save the updated set of rules so that they become available the next time you reboot the VM.

	Firewall settings
```
# ping
iptables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT
  
# kubernetes
iptables -A INPUT -p tcp -m tcp --dport 10250:10252 -j ACCEPT
  
# workloads
iptables -A INPUT -p tcp -m tcp --dport 30000:32767 -j ACCEPT
  
# calico
iptables -A INPUT -p tcp -m tcp --dport 179 -j ACCEPT
iptables -A INPUT -p tcp -m tcp --dport 4789 -j ACCEPT
  
# save rules
iptables-save > /etc/systemd/scripts/ip4save
```    

### Kernel Configuration

You need to enable IPv4 IP forwarding and `iptables` filtering on the bridge devices. Create the file `/etc/sysctl.d/kubernetes.conf` as follows: 

```
# Load br_netfilter module to facilitate traffic between pods
modprobe br_netfilter
 
 
cat /etc/sysctl.d/kubernetes.conf
net.ipv4.ip_forward = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-arptables = 1
```   

Apply the new `sysctl` settings as follows:

```
sysctl --system
...
 
* Applying /etc/sysctl.d/kubernetes.conf ...
.........
/proc/sys/net/ipv4/ip_forward = 1
/proc/sys/net/bridge/bridge-nf-call-ip6tables = 1
/proc/sys/net/bridge/bridge-nf-call-iptables = 1
/proc/sys/net/bridge/bridge-nf-call-arptables = 1
```

### Containerd Runtime Configuration

Use the following command to install `crictl` and use containerd as the runtime endpoint:

```
#install crictl
tdnf install -y cri-tools
 
#modify crictl.yaml
cat /etc/crictl.yaml
runtime-endpoint: unix:///run/containerd/containerd.sock
image-endpoint: unix:///run/containerd/containerd.sock
timeout: 2
debug: false
pull-image-on-create: false
disable-pull-on-run: false
```

Use `systemd` as cgroup for containerd as shown in the following command:


	Configuration File
```
cat /etc/containerd/config.toml
#disabled_plugins = ["cri"]
 
#root = "/var/lib/containerd"
#state = "/run/containerd"
#subreaper = true
#oom_score = 0
version = 2
 
#[grpc]
#  address = "/run/containerd/containerd.sock"
#  uid = 0
#  gid = 0
 
[plugins."io.containerd.grpc.v1.cri"]
enable_selinux = true
  [plugins."io.containerd.grpc.v1.cri".containerd]
      [plugins."io.containerd.grpc.v1.cri".containerd.runtimes]
        [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
          runtime_type = "io.containerd.runc.v2"
          [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
            SystemdCgroup = true
 
#[debug]
#  address = "/run/containerd/debug.sock"
#  uid = 0
#  gid = 0
#  level = "info"
```

Use the following command to check if containerd is running with `systemd cgroup`:

	Restart containerd service
```
systemctl daemon-reload
systemctl restart containerd
systemctl enable containerd.service
systemctl status containerd
 
crictl info | grep -i cgroup | grep true
            "SystemdCgroup": true

```   

## Kubeadm

Install kubernetes-kubeadm and other packages on the worker node, and then use Kubeadm to install and configure Kubernetes.

### Installing Kubernetes

Run the following commands to install `kubeadm`, `kubectl`, `kubelet`, and `apparmor-parser`:

```
tdnf install -y kubernetes-kubeadm apparmor-parser
systemctl enable --now kubelet
```
Pull the Kubernetes images using the following commands:

```
kubeadm config images pull
```

### Join the Cluster

Use Kubeadm to join the cluster with the token you got after running the `kubeadm init` command on the master node. Use the following command to join the cluster:

```
Join the master
```   
```
kubeadm join 10.197.103.246:6443 --token eaq5cl.gqnzgmqj779xtym7 \
    --discovery-token-ca-cert-hash sha256:90b9da1b34de007c583aec6ca65f78664f35b3ff03ceffb293d6ec9332142d05
```   
Use the following command to get cni images for network policy pods to work:

```
Pull required docker images
```   

```
tdnf install -y docker
systemctl restart docker
docker login -u $username
 
docker pull calico/cni:v3.25.0
docker pull calico/node:v3.25.0
docker pull flannelcni/flannel:v0.16.3
docker pull calico/kube-controllers:v3.25.0
```

### Cluster Test

The Kubernetes worker node should be up and running now. Run the following command from  the kube-master node to verify the state of the cluster:

```
kubectl get nodes
NAME          STATUS   ROLES           AGE     VERSION
kube-master   Ready    control-plane   21m     v1.26.1
kube-worker   Ready    <none>          6m26s   v1.26.1
```

It takes a few seconds for the kube-worker node to appear and display the ready status.
