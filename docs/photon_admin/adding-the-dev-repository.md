# Adding the Dev Repository to Get New Packages from the GitHub Dev Branch

To try out new packages or the latest versions of existing packages as they are merged into the dev branch of the Photon OS GitHub site, add the `dev` repository to your repository list.

Perform th following steps:

1. On your Photon OS machine, run the following command as root to create a repository configuration file named `photon-dev.repo`, place it in `/etc/yum.repos.d`, and concatenate the repository information into the file: 
```
cat > /etc/yum.repos.d/photon-dev.repo << "EOF" 
    [photon-dev]
    name=VMware Photon Linux Dev(x86_64)
    baseurl=https://dl.bintray.com/vmware/photon_dev_$basearch
    gpgkey=file:///etc/pki/rpm-gpg/VMWARE-RPM-GPG-KEY
    gpgcheck=1
    enabled=1
    skip_if_unavailable=True
    EOF
``` . 

2. After establishing a new repository, run the following command to update the cached binary metadata for the repositories that `tdnf` polls: 
    
```
tdnf makecache
```

