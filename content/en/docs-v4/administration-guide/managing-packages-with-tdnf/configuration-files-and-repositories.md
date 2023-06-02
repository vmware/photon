---
title:  Configuration Files and Repositories
weight: 2
---

The main configuration files reside in /etc/tdnf/tdnf.conf. The configuration file appears as follows: 

	cat /etc/tdnf/tdnf.conf
	[main]
	gpgcheck=1
	installonly_limit=3
	clean_requirements_on_remove=true
	repodir=/etc/yum.repos.d
	cachedir=/var/cache/tdnf

The cache files for data and metadata reside in /var/cache/tdnf. 

The following repositories appear in /etc/yum.repos.d/ with `.repo` file extensions:

	ls -l /etc/yum.repos.d/
	total 24
	-rw-r--r-- 1 root root 268 Feb 24  2021 photon-debuginfo.repo
	-rw-r--r-- 1 root root 253 Feb 24  2021 photon-extras.repo
	-rw-r--r-- 1 root root 193 Feb 24  2021 photon-iso.repo
	-rw-r--r-- 1 root root 254 Feb 24  2021 photon-release.repo
	-rw-r--r-- 1 root root 238 Feb 24  2021 photon.repo
	-rw-r--r-- 1 root root 262 Feb 24  2021 photon-updates.repo

You can list the the repositories by using the `tdnf repolist` command. Tdnf filters the results with `enabled`, `disabled`, and `all`. Running the command without specifying an argument returns the enabled repositories:  

	tdnf repolist
	repo id             repo name                               status
	photon-extras       VMware Photon Extras 4.0 (x86_64)       enabled
	photon-updates      VMware Photon Linux 4.0 (x86_64) Updatesenabled
	photon-release      VMware Photon Linux 4.0 (x86_64)        enabled


The `photon-iso.repo`, however, does not appear in the list of repositories because it is unavailable on the virtual machine from which these examples are taken. The `photon-iso.repo` is the default repository and it points to /media/cdrom. The `photon-iso.repo` appears as follows: 

	cat /etc/yum.repos.d/photon-iso.repo
	[photon-iso]
	name=VMWare Photon Linux ISO $releasever ($basearch)
	baseurl=file:///mnt/cdrom/RPMS
	gpgkey=file:///etc/pki/rpm-gpg/VMWARE-RPM-GPG-KEY
	gpgcheck=1
	enabled=0
	skip_if_unavailable=True

The local cache is populated with data from the repository: 

	ls -l /var/cache/tdnf/photon
	total 8
	drwxr-xr-x 2 root root 4096 May 18 22:52 repodata
	d-wxr----t 3 root root 4096 May  3 22:51 rpms

You can clear the cache to help troubleshoot a problem, but doing so might slow the performance of `tdnf` until the cache becomes repopulated with data. To clear the cache, use the following command: 

	tdnf clean all
	Cleaning repos: photon-release photon-updates photon-extras
	Cleaning up everything

The command purges the repository data from the cache: 

	ls -l /var/cache/tdnf/photon
	ls: cannot access '/var/cache/tdnf/photon': No such file or directory
