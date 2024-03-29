# Running Kubernetes on Photon OS

The procedure describes how to break the services up between the hosts.  

The first host, `photon-master`, is the Kubernetes master.  This host runs the `kube-apiserver`, `kube-controller-manager`, and `kube-scheduler`.  In addition, the master also runs `etcd`. Although `etcd` is not needed on the master if `etcd` runs on a different host, this guide assumes that `etcd` and the Kubernetes master run on the same host. The remaining host, `photon-node`, is the node and runs `kubelet`, `proxy`, and `docker`.

