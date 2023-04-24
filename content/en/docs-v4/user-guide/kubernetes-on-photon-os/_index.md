---
title:  Kubernetes on Photon OS
weight: 4
---

You can use Kubernetes with Photon OS. The instructions in this section present a manual configuration that gets one worker node running to help you understand the underlying packages, services, ports, and so forth. 

The Kubernetes package provides several services: kube-apiserver, kube-scheduler, kube-controller-manager, kubelet, kube-proxy.  These services are managed by systemd. Their configuration resides in a central location: /etc/kubernetes.