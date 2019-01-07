# Photon NFS Utilities for Mounting Remote File Systems

This document describes how to mount a remote file system on Photon OS by using nfs-utils, a commonly used package that contains tools to work with the Network File System protocol (NFS).

## Check a Remote Server

```
showmount  -e nfs-servername or ip
```

Example:  

```
showmount -e eastern-filer.eng.vmware.com
showmount -e 10.109.87.129
```

## Mount a Remote File System in Photon Full

The nfs-utils package is installed by default in the full version of Photon OS. Here is how to mount a directory through NFS on Photon OS:  

```
mount -t nfs nfs-ServernameOrIp:/exportfolder /mnt/folder
```

Example:  

```
mount -t nfs eastern-filer.eng.vmware.com:/export/filer /mnt/filer
mount -t nfs 10.109.87.129:/export /mnt/export
```

## Mount a Remote File System in Photon Minimal

The nfs-utils package is not installed in the minimal version of Photon OS. You install it by running the following command: 

	tdnf install nfs-utils

For more information on installing packages with the tdnf command, see the [Photon OS Administration Guide](https://github.com/vmware/photon/blob/master/docs/photon-admin-guide.md).

Once nfs-utils is installed, you can mount a file system by running the following commands, replacing the placeholders with the path of the directory that you want to mount: 

```
mount nfs
```
mount -t nfs nfs-ServernameOrIp:/exportfolder /mnt/folder
```
