---
title:  Configuring a Master Node
weight: 1
---

This section describes how to configure a master node with the following details:

**Node Name**: kube-master  
**Node IP Address**: 10.197.103.246

## Host Names

Change the host name on the VM using the following command:

```
hostnamectl set-hostname kube-master
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

```
Firewall Settings
```
```
# ping
iptables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT
  
# etcd
iptables -A INPUT -p tcp -m tcp --dport 2379:2380 -j ACCEPT
  
# kubernetes
iptables -A INPUT -p tcp -m tcp --dport 6443 -j ACCEPT
iptables -A INPUT -p tcp -m tcp --dport 10250:10252 -j ACCEPT
  
# calico
iptables -A INPUT -p tcp -m tcp --dport 179 -j ACCEPT
iptables -A INPUT -p tcp -m tcp --dport 4789 -j ACCEPT
  
# save rules
iptables-save > /etc/systemd/scripts/ip4save
```   

### Kernel Configuration

You need to enable IPv4 IP forwarding and iptables filtering on the bridge devices. Create the file `/etc/sysctl.d/kubernetes.conf` as follows: 

```
# Load br_netfilter module to facilitate traffic between pods
modprobe br_netfilter
 
 
cat /etc/sysctl.d/kubernetes.conf
net.ipv4.ip_forward = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-arptables = 1
```   

Apply the new `sysctl` setttings as follows:

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

Use the following command to install `crictl` and use containerd as runtime endpoint:

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

Use `systemd` as cgroup for containerd as shown in the followng command:


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

Install kubernetes-kubeadm and other packages on the master node, and then use Kubeadm to install and configure Kubernetes.

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

### Run Kubeadm

Use the following commands to run Kubeadm and initialize the system:

	kubeadm init
```
#For Flannel/Canal
kubeadm init --pod-network-cidr=10.244.0.0/16
 
 
I0420 05:45:08.440671    2794 version.go:256] remote version is much newer: v1.27.1; falling back to: stable-1.26
[init] Using Kubernetes version: v1.26.4
..........
..........
 
Your Kubernetes control-plane has initialized successfully!
 
To start using your cluster, you need to run the following as a regular user:
 
  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config
 
Alternatively, if you are the root user, you can run:
 
  export KUBECONFIG=/etc/kubernetes/admin.conf
 
You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io./concepts/cluster-administration/addons/
 
Then you can join any number of worker nodes by running the following on each as root:
 
kubeadm join 10.197.103.246:6443 --token bf9mwy.vhs88r1g2vlwprsg \
    --discovery-token-ca-cert-hash sha256:be5f76dde01285a6ec9515f20abc63c4af890d9741e1a6e43409d1894043c19b
 
 
#For Calico
kubeadm init --pod-network-cidr=192.168.0.0/16
```   

If everything goes well, the `kubeadm init` command should end with a message as displayed above. 

**Note**: Copy and save the `sha256` token value at the end. You need to use this token for the worker node to join the cluster.

The `--pod-network-cidr` parameter is a requirement for Calico. The 192.168.0.0/16 network is Calico's default. For Flannel/Canal, it is 10.244.0.0/16.

You need to export the kubernetes configuration. For any new session, this step of export is repeated.

Also, untaint the control plane VM to schedule pods on the master VM.

Use the following command to export the Kubernetes configuration and untaint the control plane VM: 

```
export KUBECONFIG=/etc/kubernetes/admin.conf
kubectl taint nodes --all node-role.kubernetes.io/control-plane-
```

## The Network Plugin

Install the Canal network plugin using the following command:

```
#canal
curl https://raw.githubusercontent.com/projectcalico/calico/v3.25.0/manifests/canal.yaml -o canal.yaml
 
# Alternatively if using flannel
curl https://raw.githubusercontent.com/flannel-io/flannel/v0.21.4/Documentation/kube-flannel.yml -o flannel.yaml
# Alternatively if using calico
curl  https://raw.githubusercontent.com/projectcalico/calico/v3.25.0/manifests/calico.yaml -o calico.yaml
```   

Get cni images for the network policy to work:

```
tdnf install -y docker
systemctl restart docker
docker login -u $username
 
docker pull calico/cni:v3.25.0
docker pull calico/node:v3.25.0
docker pull flannelcni/flannel:v0.16.3
docker pull calico/kube-controllers:v3.25.0
```

**Note**: Here we are proceeding with the downloading images required by canal.


Use the following command to apply the network policy:

```
#Apply network plugin configuration
kubectl apply -f canal.yaml
```   
The Kubernetes master node should be up and running now. Try the following commands to verify the state of the cluster:

```
kubectl cluster-info
Kubernetes control plane is running at https://10.197.103.246:6443
CoreDNS is running at https://10.197.103.246:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
 
To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
 
kubectl get nodes
NAME          STATUS   ROLES           AGE   VERSION
kube-master   Ready    control-plane   10m   v1.26.1
 
kubectl get pods --all-namespaces
NAMESPACE     NAME                                      READY   STATUS    RESTARTS   AGE
kube-system   calico-kube-controllers-57b57c56f-qxz4s   1/1     Running   0          6m54s
kube-system   canal-w4d5r                               1/2     Running   0          6m54s
kube-system   coredns-787d4945fb-nnll2                  1/1     Running   0          10m
kube-system   coredns-787d4945fb-wfv8j                  1/1     Running   0          10m
kube-system   etcd-kube-master                          1/1     Running   1          11m
kube-system   kube-apiserver-kube-master                1/1     Running   1          11m
kube-system   kube-controller-manager-kube-master       1/1     Running   1          11m
kube-system   kube-proxy-vjwwr                          1/1     Running   0          10m
kube-system   kube-scheduler-kube-master                1/1     Running   1          11m
```   

