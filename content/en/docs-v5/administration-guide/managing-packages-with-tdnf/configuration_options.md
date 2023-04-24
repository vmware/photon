---
title:  Configuration Options
weight: 9
---

You can use the configuration file to set and modify the `tdnf` configuration. The `tdnf` configuration file is located in the following directory: `/etc/tdnf/tdnf.conf`

The following table lists the configuration options that you can set in the `tdnf` configuration file:


|Configuration	| Description |   
|---------------|-------------|  
|cachedir		|Type: string<br>   Default value: `/var/cache/tdnf`<br> This is the location of the cache directory. The cache directory stores the metadata. After downloading the RPMs, the cache directory also stores the RPMs temporarily.|
|clean_requirements_on_remove| Type: boolean<br> Default value: false<br>Available from `tdnf 3.3.1` onwards.<br><br> This option determines whether the automatically installed dependencies are removed when a package is removed.|
|distroarchpkg| Type: distroarchpkg<br> Default value: x86_64<br><br> The architecture of the distribution.|
|distroverpkg|Type: string<br> Default value: system-release|
|excludepkgs| Type: list<br> Default value: none<br><br> The list of packages that you want to exclude from any operations. Packages in this list are not installed, updated, or downgraded.|
|gpgcheck| Type: boolean<br> Default: false<br><br> This option determines whether the packages are checked for their gpg signature.|
|gpgcheck| Type: boolean<br> Default value: false<br><br> This option determines whether the packages are checked for their gpg signature.|
|installonly_limit| Type: integer<br> Currently not implemented.<br> This option limits the number of concurrently install only packages.|
|keepcache| Type: boolean<br> Default value: false<br><br> This option determines whether to keep the downloaded packages after installation.
|minversions| Type: list<br> Default: none<br><br> This option refers to the list of packages with a minimum version number. When you set the minimum version number, packages are not downgraded below that version. <br>Example: `minversions=tdnf=3.1.5 foo=1.2.3`. <br> This can also be configured with the `.conf` extension files located in the directory named `minversions.d`. The directory is the same as the directory of the configuration file (usually, `/etc/tdnf/minversions.d`). <br>Example: <br> `mkdir -p /etc/tdnf/minversions.d`<br>`echo tdnf=3.1.5 > /etc/tdnf/minversions.d/tdnf.conf`|
|noplugins| When you set this option, plugins are disabled.|
|pluginpath| Type: string<br> Default value: `/usr/lib/tdnf-plugins` (or the modified value at the time of build with SYSTEM_LIBDIR option)<br><br> The path for plugins.|
|pluginconfpath| Type: string<br> Default value: `/etc/tdnf/pluginconf.d` <br><br> The path for the plugin configuration.|
|proxy| Type: string<br> Default value: none<br><br>Set this to a proxy, if any.
|proxy_password| Type: string<br> Default value: none<br><br> The proxy password, if any.|
|proxy_username| Type: string<br> Default value: none<br><br> The proxy user name, if any.|
|repodir| Type: string<br> Default value: `/etc/yum.repos.d`<br><br> The location where the `.repo` files reside.|


## Configuration in sub-directories ##

There are other configurations that you can set in the subdirectories of `/etc/tdnf`.

### Package Locks ###

You can configure to lock packages in the following directory: `/etc/tdnf/locks.d`. You cannot remove, upgrade, or downgrade a locked package. You can create multiple files with multiple lines. Each line can contain a package name.

**Note:** A locked package is considered locked only after it is installed. If a package is not installed, the features of a locked package do not apply.


### Minimal Versions ###

You can configure a minimum version for a package in the following directory: `/etc/tdnf/minversions.d`. You can create multiple files with multiple lines in them. Each line can contain a package name. The package name must include a version number, and an `=` symbol must separate the name and version number. 

Example:

	# cat /etc/tdnf/minversions.d/rpm.conf 
	rpm-libs=4.16.1.3-1


You can also configure this option in the main configuration file as mentioned in the table previously.
