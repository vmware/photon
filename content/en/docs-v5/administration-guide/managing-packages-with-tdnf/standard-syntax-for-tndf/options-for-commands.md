---
title:  tdnf Command Options
weight: 2
---

You can add the following options to `tdnf` commands. If the option to override a configuration is unavailable in a command, you can add it to the `/etc/tdnf/tdnf.conf` configuration file.

|	OPTION 					|                    DESCRIPTION |
|---------------------------|--------------------------------|
|	--allowerasing			|   Allow erasing of installed packages to resolve dependencies|
|	--assumeno    			|   Answer no for all questions|
|	--best         			|   Try the best available package versions in transactions|
|	--debugsolver  			|   Dump data aiding in dependency solver debugging info.|
|	--disablerepo=<repoid> 	|    Disable specific repositories by an id or a glob.|
|	--enablerepo=<repoid>   |   Enable specific repositories|
|	-h, --help              |   Display help|
|	--refresh               |   Set metadata as expired before running command|
|	--nogpgcheck            |   Skip gpg check on packages|
|rpmverbosity=\<debug level name>|	                           Debug level for rpm|
|	--version               |  Displays the `tdnf` version and exit|
|	-y, --assumeyes         |   Answer yes to all questions|
|	-q, --quiet             |   Quiet operation|
|    --downloadonly         |    Enables you to download the packages and dependencies that are not installed to the cache.|
|--alldeps					|	Enables you to downloads all dependencies for a package regardless of whether they are installed. This command is valid when used together with  --downloadonly  command.|
|    --downloaddir=dir      |    Downloads the packages to the specified directory |
|-C, --cacheonly			|	Disables downloading metadata, and enables usage of the cached metadata even if it is expired.|
|--config file, -c file		|	Use an alternative configuration file|
|--exclude=package1[,package2[...]] | Enables you to list the packages that you want to exclude from  the operations.|
|--disableexcludes			|	Disables `excludes` even if the `excludes` option is present in the configuration file.|
|--disablerepo=pattern		|	Disables one or more repositories. You can set it to a `repoid` or a pattern. You can also use it together with `--enablerepo`, but it is mutually exclusive with `--repo`/`--repoid`. For example, `tdnf --disablerepo=* --enablerepo=photon list`.
|--enablerepo=pattern		|	Enables one or more repositories. You can set it to a `repoid` or a pattern. This command is mutually exclusive with `--repo`/`--repoid`.|
|--downloaddir=directory	|	Specifies a directory where to download the packages. If the directory is not specified, the package is downloaded in the cache directory. You can only use it together with `--downloadonly`.|
|--installroot=directory	|	Allows you to install packages relative to this directory. Unless you specify with `-c` or `--config`, `tdnf` uses the following configuration file in this directory: `etc/tdnf/tdnf.conf`. If the configuration file is not present in this directory, `tdnf` uses the following configuration file in the host: `/etc/tdnf/tdnf.conf`. This is the same for the repository configurations. The cache directory is relative to the `installroot`. Note that the cache directory is created, if necessary.|
|--json, -j					|	Enables you to get the output information in `JSON` format. Using `tdnf` with its alias `tdnfj` is similar to using `tdnf` with `tdnf -j -y`.
|--noautoremove				|	Disables automatic removal of orphaned dependencies regardless of the `clean_requirements_on_remove` option.|
|--repofrompath=repoid,baseurl	|	Adds a repository with the id `repoid` and `baseurl` as the base url. This is equivalent to adding a repository with the repoid and the baseurl. You can reference the repository with the id, for example, with `--repoid`. <p> Example: `tdnf repofrompath=local,file:///usr/src/photon/RPMS --repoid=local install lsof` to install packages from `usr/src/photon/RPMS` (after using `createrepo /usr/src/photon/RPMS)`. <p> You can use this multiple times to add multiple repositories.|
|--repoid id, --repo id		|	Enables you to select a particular repository based on its ID. For example, `--repoid=photon` is equivalent to `--disablerepo=* --enablerepo=photon`. You can specify the repository multiple times.
|--releasever				|	Enables you to specify the release version of the distribution. If installed, the version is taken from the package that provides the system-release unless configured otherwise. Setting this is useful while installing the distribution when you use `--installroot`.|
|--skip-broken				|	Allows skipping failures if a package is not available or has broken dependencies.|
|--testonly					|	Tests RPM transactions. Note that this command does not install anything.|


The following is an example that adds the short form of the `assumeyes` option to the install command:

	tdnf -y install gcc
	Upgrading:
	gcc 	x86_64	5.3.0-1.ph1 	91.35 M

The following is an example for the `downloadonly` option with the install command:

    tdnf install --downloadonly less
        
    Installing:
        
    lessx86_64551-2.ph4 photon234.35k 239976
           
    Total installed size: 234.35k 239976
      
    tdnf will only download packages needed for the transaction
       
    Is this ok [y/N]: y
    
    Downloading:
       
    less117650   100%
        
    Complete!
       
    Packages have been downloaded to cache.

The following is an example for the `downloaddir=dir` option with the install command:

    tdnf install --downloadonly --downloaddir=/tmp less
     
    Installing:
    
    lessx86_64551-2.ph4 photon234.35k 239976
            
    Total installed size: 234.35k 239976
    
    tdnf will only download packages needed for the transaction
    
    Is this ok [y/N]: y
    
    Downloading:
    
    less117650   100%
    
        
    Complete!
    
    Packages have been downloaded to /tmp.
    
    root [ /build/build ]# ls -l /tmp/less-551-2.ph4.x86_64.rpm 
    
    -rw-r--r-- 1 root root 117650 Feb 22 18:43 /tmp/less-551-2.ph4.x86_64.rpm


    