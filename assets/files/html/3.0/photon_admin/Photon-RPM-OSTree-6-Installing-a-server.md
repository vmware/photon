# Installing a Photon RPM-OSTree Package

Photon OS 3.0 includes a `rpm-ostree-repo` package that can be installed on a VM.

This package provides an automated script that creates a repo tree that acts as a server.

## Composing your first OSTree repo  

Use the following commands to initialize a new repo and to compose it.

```
root [ ~ ]# cd /srv/rpm-ostree
root [ /srv/rpm-ostree ]# ostree --repo=repo init --mode=archive-z2
root [ /srv/rpm-ostree ]# rpm-ostree compose tree --repo=repo photon-base.json
```

You can now deploy a host. For more information, see [File oriented server operations](Photon-RPM-OStree-8-File-oriented-server-operations.md) and [Package oriented server operations](Photon-RPM-OSTree-9-Package-oriented-server-operations.md) to learn create your own customized file tree.   


