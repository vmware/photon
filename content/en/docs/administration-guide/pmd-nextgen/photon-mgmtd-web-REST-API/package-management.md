---
title:  Package Management
weight: 5
---


You can use the `pmctl` commands to manage the available packages and perform various actions on the packages. The following section lists the `pmctl` commands for various services related to package management.


## List all packages

To list all the packages, use the following command in `pmctl`:

	pmctl pkg list

Example:

	>pmctl pkg list


## List specific packages

To list a specific package, use the following command in `pmctl`:

	pmctl pkg list <pkg>

Example:

	>pmctl pkg list lsof


## Package Details

To get the details of a specific package, use the following command in `pmctl`:

	pmctl pkg info <pkg>


Example:

	pmctl pkg info lsof


## Download metadata

To download the package metadata, use the following command in `pmctl`:

	pmctl pkg makecache

Example:
	
	>pmctl pkg makecache


## Clean cache

To clean the package cache, use the following command in `pmctl`:

	pmctl pkg clean

Example:

	>pmctl pkg clean


## List repositories

To list the repositories, use the following command in `pmctl`:

	pmctl pkg repolist

Example:

	pmctl pkg repolist


## Search packages

To search a specific package,  use the following command in `pmctl`:

	pmctl pkg search <pattern>

Example:

	pmctl pkg search lsof


## Get update info

To get the update details of the packages, use the following commands in `pmctl`:

	> pmctl pkg updateinfo
	> pmctl pkg updateinfo --list
	> pmctl pkg updateinfo --info


## Install a package

To install a specific package,  use the following command in `pmctl`:

	pmctl pkg install <pkg>

Example:

	>pmctl install lsof


## Update a package

To update a specific package, use the following command in `pmctl`:

	pmctl pkg update <pkg>

Example:

	pmctl pkg update lsof


## Remove a package

To remove a specific package, use the following command in `pmctl`:

	pmctl pkg remove <pkg>

Example:

	pmctl pkg remove lsof


## Update all

To update all the packages, use th following command in `pmctl`:

	pmctl pkg update

Example:

	pmctl pkg update


## Common options

In `pmctl`, run commands in the following format to use other common options:


	> pmctl pkg [--allowerasing][--best][--cacheonly][--config=<file>][--disablerepo=<pattern>[,..]]
		[--disableexcludes][--downloaddir=<dir>][--downloadonly][--enablerepo=<pattern>[,..]]
		[--exclude=<pkg>][--installroot=<dir>][--noautoremove][--nogpgcheck][--noplugins]
		[--rebootrequired][--refresh][--releaserver=<release>][--repoid=<repo>]
		[--repofrompath=<repo>,<dir>][--security][--secseverity=<sev>][--setopt=<key=value>[,..]]
		[--skipconflicts][--skipdigest][--skipobsletes][--skipsignature]
	pmctl pkg --repoid=photon-debuginfo list lsof*

    