# Kubernetes on Photon OS
-----------------------------------------------------

You can use Kubernetes with Photon OS. The instructions in this section present a manual configuration that gets one worker node running to help you understand the underlying packages, services, ports, and so forth. 

The Kubernetes package provides several services: kube-apiserver, kube-scheduler, kube-controller-manager, kubelet, kube-proxy.  These services are managed by systemd. Their configuration resides in a central location: /etc/kubernetes.  


- [Prerequisites](prerequisites.md)
- [Running Kubernetes on Photon OS](running_kubernetes.md)
    - [System Information](system_information.md)
    - [Prepare the Hosts](prepare_the_hosts.md)
    - [Configure Kubernetes Services on Master](configure_kubernetes_on_master.md)
    - [Configure Kubernetes Services on Node](configure_kubernetes_on_node.md)


