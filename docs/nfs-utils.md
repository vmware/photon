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

* tdnf Required repositories

Create photon-extras.repo as follows (in /etc/yum.repos.d) - this is for likewise-open and dependencies.
```
root@photon-machine [ /etc/yum.repos.d ]# cat photon-extras.repo 
[photon-extras]
name=VMware Photon Extras
baseurl=https://packages.vmware.com/photon/1.0/photon_extras
gpgkey=file:///etc/pki/rpm-gpg/PHOTON-RPM-GPG-KEY
gpgcheck=0
enabled=1
skip_if_unavailable=True
```
Create photon-demo.repo as follows (in /etc/yum.repos.d) - this is for tdnfd and tdnfd-cli
```
root@photon-machine [ /etc/yum.repos.d ]# cat photon-demo.repo 
[photon-demo]
name=VMware Photon Demo
baseurl=http://discus-repo-mirror.eng.vmware.com/discus/releases/demo
gpgkey=file:///etc/pki/rpm-gpg/PHOTON-RPM-GPG-KEY
gpgcheck=0
enabled=1
skip_if_unavailable=True
```


* install nfs-utils by tdnf
```
root@photon94 [ ~ ]# tdnf install nfs-utils
```
* mount nfs
```
mount -t nfs nfs-ServernameOrIp:/exportfolder /mnt/folder
```
