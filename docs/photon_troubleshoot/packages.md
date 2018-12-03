# Troubleshooting Packages

On Photon OS, `tdnf` is the default package manager. The standard syntax for `tdnf` commands is the same as that for DNF and Yum: 
	
```
tdnf [options] <command> [<arguments>...]
```

The main configuration files reside in `/etc/tdnf/tdnf.conf`. The repositories appear in `/etc/yum.repos.d/` with `.repo` file extensions. For more information, see the [Photon OS Administration Guide](https://github.com/vmware/photon/blob/master/docs/photon-admin-guide.md).

The cache files for data and metadata reside in `/var/cache/tdnf`. The local cache is populated with data from the repository: 
	
```
ls -l /var/cache/tdnf/photon
	total 8
	drwxr-xr-x 2 root root 4096 May 18 22:52 repodata
	d-wxr----t 3 root root 4096 May  3 22:51 rpms
```

You can clear the cache to help troubleshoot a problem, but doing so might slow the performance of `tdnf` until the cache becomes repopulated with data. Cleaning the cache can remove stale information. Clear the cache as follows: 
	
```
tdnf clean all
	Cleaning repos: photon photon-extras photon-updates lightwave
	Cleaning up everything
```

Some tdnf commands can help you troubleshoot problems with packages:

- `makecache` 

    This command updates the cached binary metadata for all known repositories. You can run it after you clean the cache to make sure you are working with the latest repository data as you troubleshoot. 
    
    Example:
       
    ```
    tdnf makecache
           	Refreshing metadata for: 'VMware Lightwave 1.0(x86_64)'
           	Refreshing metadata for: 'VMware Photon Linux 1.0(x86_64)Updates'
           	Refreshing metadata for: 'VMware Photon Extras 1.0(x86_64)'
           	Refreshing metadata for: 'VMware Photon Linux 1.0(x86_64)'
           	Metadata cache created.
    ```

- `tdnf check-local`
    
    This command resolves dependencies by using the local RPMs to help check RPMs for quality assurance before publishing them. To check RPMs with this command, you must create a local directory and place your RPMs in it. The command, which includes no options, takes the path to the local directory containing the RPMs as its argument. The command does not, however, recursively parse directories; it checks the RPMs only in the directory that you specify. 
    
    For example, after creating a directory named `/tmp/myrpms` and placing your RPMs in it, you can run the following command to check them:  
    
    	tdnf check-local /tmp/myrpms
    	Checking all packages from: /tmp/myrpms
    	Found 10 packages
    	Check completed without issues
    
- `tdnf provides`
    
    This command finds the packages that provide the package that you supply as an argument. If you are used to a package name for another system, you can use `tdnf provides` to find the corresponding name of the package on Photon OS. 
    
    Example: 
    
    	tdnf provides docker
    	docker-1.11.0-1.ph1.x86_64 : Docker
    	Repo     : photon
    	docker-1.11.0-1.ph1.x86_64 : Docker
    	Repo     : @System

    For a file, you must provide the full path. Example: 

	tdnf provides /usr/include/stdio.h
	glibc-devel-2.22-8.ph1.x86_64 : Header files for glibc
	Repo     : photon
	glibc-devel-2.22-8.ph1.x86_64 : Header files for glibc
	Repo     : @System

    The following example shows you how to find the package that provides a pluggable authentication module, which you might need to find if the system is mishandling passwords. 

    ```
    tdnf provides /etc/pam.d/system-account
    	shadow-4.2.1-7.ph1.x86_64 : Programs for handling passwords in a secure way
    	Repo     : photon
    	shadow-4.2.1-8.ph1.x86_64 : Programs for handling passwords in a secure way
    	Repo     : photon-updates
    ```

    For more commands see the [Photon OS Administration Guide](photon_admin/README.md).

If a package that is installed is not working, try re-installing it. 
Example: 
    	
    ```
    tdnf reinstall shadow
    	Reinstalling:
    	shadow 	x86_64 	4.2.1-7.ph1   3.85 M
    ```
