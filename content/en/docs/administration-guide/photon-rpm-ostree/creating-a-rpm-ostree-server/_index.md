---
title:  Creating a Server
weight: 6
---

Photon OS 4.0 includes a `rpm-ostree-repo` package that can be installed on a VM.

This package provides an automated script that creates a repo tree that acts as a server.

Run the following commands to create a server:

```console
tdnf install rpm-ostree-repo
```

A script is created, which provides options to create a server.
<p>Script to create a Photon OSTree repo
Usage: 

```console
/usr/bin/rpm-ostree-server/mkostreerepo -r=<repo path> 
/usr/bin/rpm-ostree-server/mkostreerepo -r=<repo path> -p=<json treefile>
/usr/bin/rpm-ostree-server/mkostreerepo -c -r=<repo path> -p=<json treefile>
-r|--repopath   <Provide repo path> 
-p|--jsonfile   <Provide Json file> 
-c|--customrepo <Provide custom repo file inside repo path directory>
```
**Note**

- Use `PATH=$PATH:/usr/bin/rpm-ostree-server` and then use `mkostreerepo` from any directory for ease of use.
- `mkostreerepo` is used to create the fresh tree for ostree.
- `mkostreerepo` is also used to update a new commit to the existing tree.
- You can also use custom repo as to create/append the tree.




Run the following command to initiate the script, choose different help options to create a server.


```console
mkostreerepo
```

## Manually Composing your OSTree repo  

Use the following commands to initialize a new repo and to compose it.

```console
root [ ~ ]# cd /srv/rpm-ostree
root [ /srv/rpm-ostree ]# ostree --repo=repo init --mode=archive-z2
root [ /srv/rpm-ostree ]# rpm-ostree compose tree --repo=repo photon-base.json
```

You can now deploy a host. For more information, see [File oriented server operations](/docs/administration-guide/photon-rpm-ostree/file-oriented-server-operations) and [Package oriented server operations](/docs/administration-guide/photon-rpm-ostree/package-oriented-server-operations/) to learn how to create your own customized file tree.