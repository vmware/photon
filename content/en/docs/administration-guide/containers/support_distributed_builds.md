---
title:  Support for distributed builds using Kubernetes
weight: 4
---

The distributed system using Kubernetes allows the build system to utilize the maximum CPU power across a kubernetes cluster (pods) for faster build process.

Prerequisites

- Ensure that the NFS server is running
- Ensure that you have the Kubernetes cluster ready that has access to the NFS server 
- Esure that you have installed Kubernetes package and have `kubeconfig` accessible in the build VM.

## Triggering Distributed Photon Builds ##

Perform the following steps in the Photon OS repository:

1. Update the `'common/data/distributed_build_options.json'` configuration file . The following parameters need to be filled:

- command→ target to run like `'make packages'` or `'make packages-minimal'` or `'make toolchain-stage-1'` or so on.
  Note: Keep the `command` with flag `'SCHEDULER_SERVER=enable'`.

- nfs-server-ip→ IP address of the nfs server 


- pods→ number of builder/worker pods you want such as 10 or 20. The default value is 1.


- nfs-server-path-> path of the nfs mount. For example,`/mnt/NFS_PATH/MY_DIR`

2. Run `make distributed-build`.

Note:

i)This process will make use of the `kubeconfig` file present under the home directory and start building packages over the specified cluster.

ii)It creates one Master pod and multiple worker pods (numbers defined in config.json).

iii)The master pod runs the scheduler while the worker or the builder pods build the packages.

iv)Distributed Builder monitors the build mob and deletes everything when build has either completed successfully or failed.

The master starts the scheduler server to schedule the packages that have to be built.
The worker makes REST calls to scheduler server.get package and notify after the build.

The distributed build also builds cloud images.