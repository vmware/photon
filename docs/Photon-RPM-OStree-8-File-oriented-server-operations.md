In this chapter, we will checkout a filetree into a writable directory structure on disk, make several file changes and commit the changes back into the repository. Then we will download this commit and apply at the host. As you may have guessed, this chapter is mostly about OSTree - the base technology. I've not mentioned anything about packages, although it is quite possible to install packages (afler all, packages are made of files, right?) and commit without the help of rpm-ostree, but it's too much of a headache and not worth the effort, since rpm-ostree does it simpler and better.  

When would you want to do that? When you want for all your hosts to get an application or configuration customization that is not encapsulated as part of a package upgrade.

### 8.1 Starting a fresh OSTree repo  
If you want to start fresh with your own branch and/or versioning scheme, you can delete the OSTree repo created during the Photon 1.0 RPM-OSTree server install and re-create it empty. For Photon OS 2.0 RPM-OSTree, this is a required step, as the installer will not create an OSTree repo for you, as you can see in 12.1.  
```
root [ /srv/rpm-ostree ]# rm -rf repo

root [ /srv/rpm-ostree ]# ostree --repo=repo init --mode=archive-z2

root [ /srv/rpm-ostree ]# ls repo                                  
config  objects  refs  state  tmp  uncompressed-objects-cache

root [ /srv/rpm-ostree ]# cat repo/config
[core]
repo_version=1
mode=archive-z2
```

### 8.2 Checking out a filetree
[content to be added]

### 8.3 Committing changes to a filetree
[content to be added]

### 8.4 Downloading the changes at the host
[content to be added]

### 8.5 Creating summary metadata
A newer ostree feature, available in Photon OS 2.0 and higher, allows the OSTree server admin to create server summary metadata, that includes among other things the list of available branches and the list of static deltas, so they could be discovered by hosts. To create a summary, run this command after you committed for your branches:
```
root [ /srv/rpm-ostree ]# ostree summary -u "This is BigData's OSTree server, it has three branches"
```  
We will find out later how the [[hosts query for branches list|Photon-RPM-OSTree:-10-Remotes#105-list-available-branches]]. 

[[Back to main page|Photon-RPM-OSTree:-a-simple-guide]] | [[Previous page|Photon-RPM-OSTree:-7-Installing-a-host-against-a-custom-server-repository]] | [[Next page >|Photon-RPM-OSTree:-9-Package-oriented-server-operations]] 