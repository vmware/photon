# Mounting a Network File System

To mount a network file system, Photon OS requires `nfs-utils`. The `nfs-utils` package contains the daemon, userspace server, and client tools for the kernel Network File System (NFS). The tools include `mount.nfs`, `umount.nfs`, and `showmount`. 

The `nfs-utils` package is installed by default in the full version of Photon OS but not in the minimal version. To install `nfs-utils` in the minimal version, run the following command as root: 
	
```
tdnf install nfs-utils
```

For instructions on how to use `nfs-utils` to share files over a network, see [Photon OS nfs-utils](nfs-utils.md).