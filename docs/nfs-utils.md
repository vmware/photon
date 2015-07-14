# Photon NFS utils

To mount network file in Photon


## Check a remote nfs server
showmount  -e nfs-servername or ip

for example : showmount  -e discus-filer.eng.vmware.com

              showmount -e 10.118.100.122

## Mount the nfs

mount -t nfs nfs-servername:/export /mnt

for example : mount -t nfs discus-filer.eng.vmware.com:/export/filer /mnt

              mount -t nfs 10.118.100.122:/export /mnt
