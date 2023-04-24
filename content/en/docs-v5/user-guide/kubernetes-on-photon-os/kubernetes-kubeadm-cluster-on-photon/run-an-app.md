---
title:  Run a Hello-World Application
weight: 3
---

Run a hello-world application to verify that the new two-node cluster works properly. All commands in this section must be executed from `kube-master`.

Create a pod with the name "hello" to print "Hello Kubernetes".

Use the following command to create a pod with the name "hello":

```
cat hello.yaml
 
apiVersion: v1
kind: Pod
metadata:
  name: hello
spec:
  restartPolicy: Never
  containers:
  - name: hello
    image: projects.registry.vmware.com/photon/photon4:latest
    command: ["/bin/bash"]
    args: ["-c", "echo Hello Kubernetes"]
```   

Use the following command to create a hello Kubernetes application:

```
kubectl apply -f hello.yaml
#check status
kubectl get pods
#check logs
kubectl logs hello | grep "Hello Kubernetes"
```   

You have successfully set up the two VM Kubernetes Kubeadm Cluster.