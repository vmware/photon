---
title:  Remotes
weight: 11
---

In Chapter 3 we talked about the Refspec that contains a **photon:** prefix, that is the name of a remote. When a Photon host is installed, a remote is added - which contains the URL for an OSTree repository that is the origin of the commits we are going to pull from and deploy filetrees, in our case the Photon RPM-OSTree server we installed the host from. This remote is named **photon**, which may be confusing, because it's also the OS name and part of the Refspec (branch) path.

## Listing remotes

A host repo can be configured to switch between multiple remotes to pull from, however only one remote is the "active" one at a time. We can list the remotes created so far, which brings back the expected result.

```console
root@photon-7c2d910d79e9 [ ~ ]# ostree remote list
photon
```

We can inquiry about the URL for that remote name, which for the default host is the expected Photon OS online OSTree repo.

```console
root@photon-host-def [ ~ ]# ostree remote show-url photon
https://<host-name>:8080/repo
```

But where is this information stored? The repo's config file has it.

```ini
root@photon-host-def [ ~ ]# cat /ostree/repo/config 
[core]
repo_version=1
mode=bare

[remote "photon"]
url=http:<Server-IP-Address:port>/repo
gpg-verify=false
```

If same command is executed on the custom host we've installed, it's going to reveal the URL of the Photon RPM-OSTree server connected to during setup.

```console
root@photon-7c2d910d79e9 [ ~ ]# ostree remote show-url photon
https://packages.vmware.com/photon/rpm-ostree/base/4.0/x86_64/repo
```

## GPG signature verification

You may wonder what is the purpose of `gpg-verify=false` in the config file, associated with the specific remote. This will instruct any host update to skip the signing verification for the updates that come from server, resulted from tree composed locally at the server, as they are not signed. Without this, host updating will fail.  

There is a whole chapter about signing, importing keys and so on that I will not get into, but the idea is that signing adds an extra layer of security, by validating that everything you download comes from the trusted publisher and has not been altered. That is the case for all Photon OS artifacts downloaded from VMware official site. All OVAs and packages, either from the online RPMS repositories or included in the ISO file - are signed by VMware. We've seen a similar setting `gpgcheck=1` in the RPMS repo configuration files that tdnf uses to validate or not the signature for all packages downloaded to be installed.


## Switching repositories

Since mapping name/url is stored in the repo's config file, in principle you can re-assign a different URL, connecting the host to a different server. The next upgrade will get the latest commit chain from the new server.   
If we edit photon-host-def's repo config and replace the VMware Photon Packages URL by photon-srv1's IP address, all original packages in the original 4.0_minimal version will be preserved, but any new package change (addition, removal, upgrade) added after that (in 4.0_minimal.1, 4.0_minimal.2) will be reverted and all new commits from photon-srv1 (that may have same version) will be applied. This is because the two repos are identical copies, so they have the same original commit ID as a common ancestor, but they diverge from there.  
  
If the old and new repo have nothing in common (no common ancestor commit), this will undo even the original commit, so all commits from the new tree will be applied.  
A better solution would be to add a new remote that will identify where the commits come from.

## Adding and removing remotes

A cleaner way to switch repositories is to add remotes that point to different servers. Let us add another server that we will refer to as **photon2**, along with (optional) the refspecs for branches that it provides (we will see later that in the newer OSTree versions, we don't need to know the branch names, they could be [queried at run-time](#list-available-branches)). 

```console
root@photon-host-cus [ ~ ]# ostree remote add --repo=/ostree/repo -v --no-gpg-verify photon2 http://10.197.103.204:8080 photon/4.0/x86_64/minimal photon/4.0/x86_64/full
root@photon-host-cus [ ~ ]# ostree remote list
photon
photon2
root@photon-host-cus [ ~ ]# ostree remote show-url photon2
http://10.0.0.86
```

Where is this information stored? There is an extra config file created per each remote:

```console
root@photon-host-cus [ ~ ]# cat /etc/ostree/remotes.d/photon2.conf 
[remote "photon2"]
url=http://10.0.0.86
branches=photon/4.0/x86_64/minimal;photon/4.0/x86_64/full;
gpg-verify=false
```

You may have guessed what is the effect of `--no-gpg-verify option`.  
Obviously, remotes could also be deleted.

```console
root@photon-host-cus [ ~ ]# ostree remote delete photon2
root@photon-host-cus [ ~ ]# ostree remote list
photon
```

## List available branches

If a host has been deployed from a specific branch and would like to switch to a different one, maybe from a different server, how would it know what branches are available? In git, you would run ```git remote show origin``` or ```git remote -a``` (although last command would not show all branches, unless you ran ```git fetch``` first).  

In Photon OS, the hosts are able to query the server, if summary metadata has been generated, as we've seen in [Creating summary metadata](/docs/administration-guide/photon-rpm-ostree/file-oriented-server-operations/#creating-summary-metadata).  This command lists all branches available for remote **photon2**.

```console
root@photon-host-cus [ ~ ]# ostree remote refs photon2 
photon2:photon/4.0/x86_64/base
photon2:photon/4.0/x86_64/full
photon2:photon/4.0/x86_64/minimal
```

## Switching branches (rebasing)

If you have an installed Photon 3.0 that you want to carry to 4.0, you need to rebase it.

See [rebasing](/docs/administration-guide/photon-rpm-ostree/install-or-rebase-to-photon-os-4/).
