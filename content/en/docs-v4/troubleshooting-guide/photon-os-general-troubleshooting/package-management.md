---
title:  Package Management
weight: 2
---

[TDNF](https://github.com/vmware/tdnf) is the default package manager for Photon OS. The standard syntax for `tdnf` commands is the same as that for DNF and YUM. TDNF reads YUM repositories from **/etc/yum.repos.d/**.

To find the main configuration file and see its contents, run the following command:
```
cat /etc/tdnf/tdnf.conf
[main]
gpgcheck=1
installonly_limit=3
clean_requirements_on_remove=true
repodir=/etc/yum.repos.d
cachedir=/var/cache/tdnf
```

Repositories have a **.repo** file extension, The following repositories are available in **/etc/yum.repos.d/** :
```
ls /etc/yum.repos.d/
photon-extras.repo
photon-iso.repo
photon-updates.repo
photon.repo
```

Use the `tdnf repolist` command to list the repositories. Tdnf filters the results by their status **enabled**, **disabled**, and **all**. Running the `tdnf repolist` command without arguments displays the enabled repositories.
```
#tdnf repolist

repo id repo name status
photon-extras        VMware Photon Extras 3.0(x86_64) enabled
photon-debuginfo VMware Photon Linux debuginfo 3.0(x86_64)enabled
photon                    VMware Photon Linux 3.0(x86_64) enabled
photon-updates     VMware Photon Linux 3.0(x86_64) Updates enabled
root@photon-75829bfd01d0 [ ~ ]#
```

The following repositories are important for Photon:

- photon-updates : This repo contains RPM updates for CVE/version and updates/others fixes.
- photon-debuginfo : This repo contains information about RPMs with debug symbols.
- photon : This repo generally contains the RPM versions packaged with the released ISO.

To check the local cache data from the repository, run the following command:
```
# ls -l /var/cache/tdnf/photon
total 12
-r--r----- 1 root root 0 Apr 3 22:34 lastrefresh
drwxr-x--- 2 root root 4096 Apr 3 22:34 repodata
drwxr-x--- 4 root root 4096 Feb 4 14:31 rpms
drwxr-x--- 2 root root 4096 Apr 3 22:34 solvcache
```

##Usage
The `tdnf` command can be used in the following ways:

`#tdnf repolist --refresh` : This command is used to refresh the repolist. Generally there is a cache of the repo data stored in the local VM.

`#tdnf install <rpm name>` : This command is used to install a RPM. This command installs the latest version of the RPM.

`#tdnf install <pkg-name>-<verison>-<release>.<photon-release>` : This command is used to install a particular RPM version. For example, run `# tdnf install systemd-239-11.ph3`.

`#tdnf list systemd` : This command is used to list the available RPM versions in the repository.

`#tdnf makecache` : This command updates the cached binary metadata for all known repositories.

`tdnf clean all` : This command cleans up temporary files, data, and metadata. It takes the argument `all`.
```
#tdnf list systemd

Refreshing metadata for: 'VMware Photon Linux 3.0(x86_64)'

systemd.x86_64                                                                       239-15.ph3                                            @System

systemd.x86_64                                                                       239-11.ph3                                     photon-updates

systemd.x86_64                                                                       239-12.ph3                                     photon-updates

systemd.x86_64                                                                       239-13.ph3                                     photon-updates

systemd.x86_64                                                                       239-14.ph3                                     photon-updates

systemd.x86_64                                                                       239-15.ph3                                     photon-updates

systemd.x86_64                                                                       239-17.ph3                                     photon-updates

systemd.x86_64                                                                       239-18.ph3                                     photon-updates

systemd.x86_64                                                                       239-19.ph3                                     photon-updates

systemd.x86_64                                                                       239-10.ph3                                             photon

systemd.x86_64                                                                       239-10.ph3                                             photon

root@photon-4a0e7f2307d4 [ /WS/photon-dev/photon ]#
```
Here, `@System` indicates that the particular RPM is installed in the VM.

To upgrade/downgrade RPMs run the following commands:
```
#tdnf upgrade <pkg-name>

#tdnf downgrade <pkg-name>
```
After upgrade/downgrade the dependent packages must be manually upgraded/downgraded as well. Use the `#tdnf remove <pkg-name>` command to remove packages and `# tdnf clean all` to clear cached packages, metadata, dbcache, plugins and expire-cache.

#RPM
RPM is an open source package management system capable of building software from source into easily distributable packages. It is used for installing, updating and uninstalling packaged software.
RPM can also be used to query detailed information about the packaged software and to check if a particular package is installed or not.

You can do the following operation using the RPM binaries:

- Install/Upgrade/Downgrade/Remove RPMs from a virtual machine.
- Check the version of the packages installed.
- Check the package contents.
- Check the dependencies of a package.
- Find the source package of a file.

To find the package that contains a particular binary, run `rpm -q —whatprovides <binary/file path>` command.

##Usage
The `rpm` command can be used in the following ways:

- `rpm -ivh <rpm file path>` : This command installs the RPM in a virtual machine.
- `rpm -Uvh <rpm file path>` : This command is used to upgrade/downgrade the RPM.
- `rpm -e <rpm file path>` : This command uninstalls the RPM from the virtual machine.
- `rpm -qp <rpm file path> --provides` : This displays the libraries provided by the RPM.
- `rpm -qp <rpm file path> --requires` : This displays the binaries/libraries required to install a particular rpm.
- `rpm -qa` : This displays a list of all installed packages.
- `rpm -ql <package file.rpm>` : This command lists all files in the package file.

