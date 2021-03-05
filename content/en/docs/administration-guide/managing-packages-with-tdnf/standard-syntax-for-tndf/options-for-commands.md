---
title:  tdnf Command Options
weight: 2
---

You can add the following options to `tdnf` commands. If the option to override a configuration is unavailable in a command, you can add it to the `/etc/tdnf/tdnf.conf` configuration file.

	OPTION                     DESCRIPTION
	--allowerasing             Allow erasing of installed packages to resolve dependencies
	--assumeno                 Answer no for all questions
	--best                     Try the best available package versions in transactions
	--debugsolver              Dump data aiding in dependency solver debugging info.
	--disablerepo=<repoid>     Disable specific repositories by an id or a glob.
	--enablerepo=<repoid>      Enable specific repositories
	-h, --help                 Display help
	--refresh                  Set metadata as expired before running command
	--nogpgcheck               Skip gpg check on packages
	--rpmverbosity=<debug level name>
	                           Debug level for rpm
	--version                  Print version and exit
	-y, --assumeyes            Answer yes to all questions
	-q, --quiet                Quiet operation
    --downloadonly             Enables you to download the packages and dependencies that are
                               not installed to the cache.
    --downloaddir=dir          Downloads the packages to the specified directory 

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


    