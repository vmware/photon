---
title:  Configuration Files and Repositories
weight: 2
---

The main configuration files reside in /etc/tdnf/tdnf.conf. The configuration file appears as follows: 

	cat /etc/tdnf/tdnf.conf
	[main]
	gpgcheck=1
	installonly_limit=3
	clean_requirements_on_remove=0
	repodir=/etc/yum.repos.d
	cachedir=/var/cache/tdnf

The cache files for data and metadata reside in /var/cache/tdnf. 

The following repositories appear in /etc/yum.repos.d/ with `.repo` file extensions:

	ls -l /etc/yum.repos.d/
	total 24
	-rw-r--r-- 1 root root 313 Mar 29 19:47 photon-debuginfo.repo
	-rw-r--r-- 1 root root 238 Mar 29 19:47 photon-iso.repo
	-rw-r--r-- 1 root root 299 Mar 29 19:47 photon-release.repo
	-rw-r--r-- 1 root root 303 Mar 29 19:47 photon.repo
	-rw-r--r-- 1 root root 331 Mar 29 19:47 photon-srpms.repo
	-rw-r--r-- 1 root root 307 Mar 29 19:47 photon-updates.repo


You can list the repositories by using the `tdnf repolist` command. Tdnf filters the results with `enabled`, `disabled`, and `all`. Running the command without specifying an argument returns the enabled repositories:  

	tdnf repolist
	repo id             repo name                                status
	photon-updates      VMware Photon Linux 5.0 (x86_64) Updates enabled


The `photon-iso.repo`, however, does not appear in the list of repositories because it is unavailable on the virtual machine from which these examples are taken. The `photon-iso.repo` is the default repository and it points to /media/cdrom. The `photon-iso.repo` appears as follows: 

	cat /etc/yum.repos.d/photon-iso.repo
	[photon-iso]
	name=VMWare Photon Linux ISO $releasever ($basearch)
	baseurl=file:///mnt/cdrom/RPMS
	gpgkey=file:///etc/pki/rpm-gpg/VMWARE-RPM-GPG-KEY file:///etc/pki/rpm-gpg/VMWARE-RPM-GPG-KEY-4096
	gpgcheck=1
	enabled=0
	skip_if_unavailable=1

The local cache is populated with data from the repository, for example: 

	ls -l /var/cache/tdnf/photon-updates-a9be9ddf/
	total 8
	-r--r--r-- 1 root root    0 Apr 26 09:07 lastrefresh
	drwxr-xr-x 2 root root 4096 Apr 26 09:07 repodata
	drwxr-xr-x 2 root root 4096 Apr 26 09:07 solvcache

You can clear the cache to help troubleshoot a problem, but doing so might slow the performance of `tdnf` until the cache becomes repopulated with data. To clear the cache, use the following command: 

	tdnf clean all
	cleaning photon: metadata dbcache packages keys expire-cache
	cleaning photon-release: metadata dbcache packages keys expire-cache
	cleaning photon-srpms: metadata dbcache packages keys expire-cache
	cleaning photon-updates: metadata dbcache packages keys expire-cache
	cleaning photon-iso: metadata dbcache packages keys expire-cache
	cleaning photon-debuginfo: metadata dbcache packages keys expire-cache
	Done.

The command purges the repository data from the cache: 

	ls -l /var/cache/tdnf/photon-updates-a9be9ddf/
	ls: cannot access '/var/cache/tdnf/photon-updates-a9be9ddf/': No such file or directory
