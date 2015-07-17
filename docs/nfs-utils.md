# Photon NFS utils

To mount network file system in Photon


## Check a remote nfs server

```
showmount  -e nfs-servername or ip
```

for example : 

```
showmount -e discus-filer.eng.vmware.com
showmount -e 10.118.100.122
```

## Mount the nfs in Photon full
nfs-utils is installed by default in Photon full, just use it.

```
mount -t nfs nfs-ServernameOrIp:/exportfolder /mnt/folder
```

for example : 

```
mount -t nfs discus-filer.eng.vmware.com:/export/filer /mnt/filer
mount -t nfs 10.118.100.122:/export /mnt/export
```

## Mount the nfs in Photon minimal
Nfs-utils is not installed in Photon minimal. So it should be installed by tdnf first.

* install nfs-utils by tdnf

```
root@photon94 [ ~ ]# tdnf install nfs-utils
```
* mount nfs
```
mount -t nfs nfs-ServernameOrIp:/exportfolder /mnt/folder
```
