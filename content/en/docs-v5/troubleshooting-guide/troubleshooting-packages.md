---
title:  Troubleshooting Packages
weight: 8
---

On Photon OS, `tdnf` is the default package manager. The standard syntax for `tdnf` commands is the same as that for DNF and Yum: 
	
```console
tdnf [options] <command> [<arguments>...]
```

The main configuration files reside in `/etc/tdnf/tdnf.conf`. The repositories appear in `/etc/yum.repos.d/` with `.repo` file extensions. For more information, see the [Photon OS Administration Guide](../../administration-guide/).

The cache files for data and metadata reside in `/var/cache/tdnf`. The local cache is populated with data from the repository: 
	
```console
ls -l /var/cache/tdnf/photon
total 8
-r--r--r-- 1 root root    0 Apr 20 13:32 lastrefresh
drwxr-xr-x 2 root root 4096 Apr 20 13:32 repodata
drwxr-xr-x 2 root root 4096 Apr 20 13:32 solvcache
```

You can clear the cache to help troubleshoot a problem, but doing so might slow the performance of `tdnf` until the cache becomes repopulated with data. Cleaning the cache can remove stale information. Clear the cache as follows: 
	
```console
tdnf clean all
cleaning photon-iso: metadata dbcache packages keys expire-cache
cleaning photon-release: metadata dbcache packages keys expire-cache
cleaning photon-updates: metadata dbcache packages keys expire-cache
cleaning photon: metadata dbcache packages keys expire-cache
cleaning photon-debuginfo: metadata dbcache packages keys expire-cache
cleaning photon-srpms: metadata dbcache packages keys expire-cache
Done.
```

Some tdnf commands can help you troubleshoot problems with packages:

- `makecache` 

    This command updates the cached binary metadata for all known repositories. You can run it after you clean the cache to make sure you are working with the latest repository data as you troubleshoot. 
    
    Example:
       
    ```
    tdnf makecache
    Refreshing metadata for: 'VMware Photon Linux 5.0 (x86_64) Updates'
    Refreshing metadata for: 'VMware Photon Linux 5.0 (x86_64)'
    Metadata cache created.                   3107 100%
    ```

- `tdnf check-local`
    
    This command resolves dependencies by using the local RPMs to help check RPMs for quality assurance before publishing them. To check RPMs with this command, you must create a local directory and place your RPMs in it. The command, which includes no options, takes the path to the local directory containing the RPMs as its argument. The command does not, however, recursively parse directories; it checks the RPMs only in the directory that you specify. 
    
    For example, after creating a directory named `/tmp/myrpms` and placing your RPMs in it, you can run the following command to check them:  
		
	```
	tdnf check-local /tmp/myrpms
	Checking all packages from: /tmp/myrpms
	Found 10 packages
	Check completed without issues
	```

- `tdnf provides`
    
	This command finds the packages that provide the package that you supply as an argument. If you are used to a package name for another system, you can use `tdnf provides` to find the corresponding name of the package on Photon OS. 
    
    Example: 

	```    
	tdnf provides docker
	docker-23.0.2-1.ph5.x86_64 : Docker
	Repo     : photon
	docker-23.0.1-2.ph5.x86_64 : Docker
	Repo     : photon-updates
	docker-23.0.2-1.ph5.x86_64 : Docker
	Repo     : @System
	```

    For a file, you must provide the full path. Example: 
	
	```
	tdnf provides /usr/include/stdio.h
	[using file list match for '/usr/include/stdio.h']
	glibc-devel-2.36-4.ph5.x86_64 : Header files for glibc
	Repo     : photon
	glibc-devel-2.36-3.ph5.x86_64 : Header files for glibc
	Repo     : photon-updates
	```

    The following example shows you how to find the package that provides a pluggable authentication module, which you might need to find if the system is mishandling passwords. 

    ```
    tdnf provides /etc/pam.d/system-account
    [using file list match for '/etc/pam.d/system-account']
    shadow-4.13-3.ph5.x86_64 : Programs for handling passwords in a secure way
    Repo     : photon
    shadow-4.13-3.ph5.x86_64 : Programs for handling passwords in a secure way
    Repo     : photon-updates
    shadow-4.13-3.ph5.x86_64 : Programs for handling passwords in a secure way
    Repo     : @System
    ```

    For more commands see the [Photon OS Administration Guide](../administration-guide/).
    
- `tdnf reinstall`
    
	If a package that is installed is not working, try re-installing it. 
        Example:

    ```
    tdnf reinstall shadow
    Reinstalling:
    shadow                   x86_64             4.13-3.ph5               photon-updates       1.87M           368.07k
    
    Total installed size:   1.87M
    Total download size: 368.07k
    Is this ok [y/N]: y
    shadow                                  376905 100%
    Testing transaction
    Running transaction
    Installing/Updating: shadow-4.13-3.ph5.x86_64
    Removing: shadow-4.13-3.ph5.x86_64
    ```
