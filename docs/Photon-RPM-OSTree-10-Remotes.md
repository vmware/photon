In Chapter 3 we talked about the Refspec that contains a **photon:** prefix, that is the name of a remote. When a Photon host is installed, a remote is added - which contains the URL for an OSTree repository that is the origin of the commits we are going to pull from and deploy filetrees, in our case the Photon RPM-OSTree server we installed the host from. This remote is named **photon**, which may be confusing, because it's also the OS name and part of the Refspec (branch) path.

### 10.1 Listing remotes
A host repo can be configured to switch between multiple remotes to pull from, however only one remote is the "active" one at a time. We can list the remotes created so far, which brings back the expected result.
```
root@photon-host-def [ ~ ]# ostree remote list
photon
```
We can inquiry about the URL for that remote name, which for the default host is the expected Photon OS online OSTree repo.
```
root@photon-host-def [ ~ ]# ostree remote show-url photon
https://dl.bintray.com/vmware/photon/rpm-ostree/1.0
```
But where is this information stored? The repo's config file has it.
```
root@photon-host-def [ ~ ]# cat /ostree/repo/config 
[core]
repo_version=1
mode=bare

[remote "photon"]
url=https://dl.bintray.com/vmware/photon/rpm-ostree/1.0
gpg-verify=false
```

If same command is executed on the custom host we've installed, it's going to reveal the URL of the Photon RPM-OSTree server connected to during setup.
```
root@photon-host-cus [ ~ ]# ostree remote show-url photon
http://10.118.101.168
```

### 10.2 GPG signature verification
You may wonder what is the purpose of ```gpg-verify=false``` in the config file, associated with the specific remote. This will instruct any host update to skip the signing verification for the updates that come from server, resulted from tree composed locally at the server, as they are not signed. Without this, host updating will fail.  

There is a whole chapter about signing, importing keys and so on that I will not get into, but the idea is that signing adds an extra layer of security, by validating that everything you download comes from the trusted publisher and has not been altered. That is the case for all Photon OS artifacts downloaded from VMware official site. All OVAs and packages, either from the online RPMS repositories or included in the ISO file - are signed by VMware. We've seen a similar setting ```gpgcheck=1``` in the RPMS repo configuration files that tdnf uses to validate or not the signature for all packages downloaded to be installed.


### 10.3 Switching repositories
Since mapping name/url is stored in the repo's config file, in principle you can re-assign a different URL, connecting the host to a different server. The next upgrade will get the latest commit chain from the new server.   
If we edit photon-host-def's repo config and replace the bintray URL by photon-srv1's IP address, all original packages in the original 1.0_minimal version will be preserved, but any new package change (addition, removal, upgrade) added after that (in 1.0_minimal.1, 1.0_minimal.2) will be reverted and all new commits from photon-srv1 (that may have same version) will be applied. This is because the two repos are identical copies, so they have the same original commit ID as a common ancestor, but they diverge from there.  
This may create confusion and it's one of the reasons I insisted on creating your own scheme of versioning.
  
If the old and new repo have nothing in common (no common ancestor commit), this will undo even the original commit, so all commits from the new tree will be applied.  
A better solution would be to add a new remote that will identify where the commits come from.

### 10.4 Adding and removing remotes

A cleaner way to switch repositories is to add remotes that point to different servers. Let's add another server that we will refer to as **photon2**, along with (optional) the refspecs for branches that it provides (we will see later that in the newer OSTree versions, we don't need to know the branch names, they could be [[queried at run-time|Photon-RPM-OSTree:-10-Remotes#105-listing-available-branches]]). The 'minimal' and 'full' branch ref names containing '2.0' suggest this may be a Photon OS 2.0 RPM-OSTree server. 
```
root@photon-host-cus [ ~ ]# ostree remote add --repo=/ostree/repo -v --no-gpg-verify photon2 http://10.118.101.86 photon/2.0/x86_64/minimal photon/2.0/x86_64/full
root@photon-host-cus [ ~ ]# ostree remote list
photon
photon2
root@photon-host-cus [ ~ ]# ostree remote show-url photon2
http://10.118.101.86
```
Where is this information stored? There is an extra config file created per each remote:
```
root@photon-host-cus [ ~ ]# cat /etc/ostree/remotes.d/photon2.conf 
[remote "photon2"]
url=http://10.118.101.86
branches=photon/2.0/x86_64/minimal;photon/2.0/x86_64/full;
gpg-verify=false
```
You may have guessed what is the effect of ```--no-gpg-verify option```.  
Obviously, remotes could also be deleted.
```
root@photon-host-cus [ ~ ]# ostree remote delete photon2
root@photon-host-cus [ ~ ]# ostree remote list
photon
```

### 10.5 List available branches
If a host has been deployed from a specific branch and would like to switch to a different one, maybe from a different server, how would it know what branches are available? In git, you would run ```git remote show origin``` or ```git remote -a``` (although last command would not show all branches, unless you ran ```git fetch``` first).  

Fortunately, in Photon OS 2.0 and higher, the hosts are able to query the server, if summary metadata has been generated, as we've seen in [[8.5|Photon-RPM-OSTree:-8-File-oriented-server-operations#85-creating-summary-metadata]].  This command lists all branches available for remote **photon2**.

```
root@photon-host-cus [ ~ ]# ostree remote refs photon2 
photon2:photon/2.0/x86_64/base
photon2:photon/2.0/x86_64/full
photon2:photon/2.0/x86_64/minimal
```

###10.6 Switching branches (rebasing)


[[Back to main page|Photon-RPM-OSTree:-a-simple-guide]] | [[Previous page|Photon-RPM-OSTree:-9-Package-oriented-server-operations]] | [[Next page >|Photon-RPM-OSTree:-11-Running-container-applications-between-bootable-images]]
  
