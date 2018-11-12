# Commands

**check**: Checks for problems in installed and available packages for all enabled repositories. The command has no arguments. You can use ``--enablerepo`` and ``--disablerepo`` to control the repos used. Supported in Photon OS 2.0 (only).

**check-local**: This command resolves dependencies by using the local RPMs to help check RPMs for quality assurance before publishing them. To check RPMs with this command, you must create a local directory and place your RPMs in it. The command, which includes no options, takes the path to the local directory containing the RPMs as its argument. The command does not recursively parse directories. It checks the RPMs only in the directory that you specify. For example, after creating a directory named `/tmp/myrpms` and placing your RPMs in it, you can run the following command to check them:  

	tdnf check-local /tmp/myrpms
	Checking all packages from: /tmp/myrpms
	Found 10 packages
	Check completed without issues

**check-update**: This command checks for updates to packages. It takes no arguments. The `tdnf list updates` command performs the same function. Here is an example of the `check update` command: 

	tdnf check-update
	rpm-devel.x86_64 	4.11.2-8.ph1 	photon
	yum.noarch      	3.4.3-3.ph1 	photon

**clean**: This command cleans up temporary files, data, and metadata. It takes the argument `all`. Example: 

	tdnf clean all
	Cleaning repos: photon photon-extras photon-updates lightwave
	Cleaning up everything

**distro-sync**: This command synchronizes the machine's RPMs with the latest version of all the packages in the repository. The following is an abridged example:

	tdnf distro-sync

	Upgrading:
	zookeeper                             x86_64        3.4.8-2.ph1               3.38 M
	yum                                   noarch        3.4.3-3.ph1               4.18 M

	Total installed size: 113.01 M

	Reinstalling:
	zlib-devel                            x86_64        1.2.8-2.ph1             244.25 k
	zlib                                  x86_64        1.2.8-2.ph1             103.93 k
	yum-metadata-parser                   x86_64        1.1.4-1.ph1              57.10 k

	Total installed size: 1.75 G

	Obsoleting:
	tftp                                  x86_64        5.2-3.ph1                32.99 k

	Total installed size: 32.99 k
	Is this ok [y/N]:

**downgrade**: This command downgrades the package that you specify as an argument to the next lower package version. The following is an example: 

	tdnf downgrade boost
	Downgrading:
	boost                                 x86_64        1.56.0-2.ph1              8.20 M
	Total installed size: 8.20 M
	Is this ok [y/N]:y
	Downloading:
	boost                                  2591470    100%
	Testing transaction
	Running transaction
	Complete!

To downgrade to a version lower than the next one, you must specify it by name, epoch, version, and release, all properly hyphenated. The following is an example: 

	tdnf downgrade boost-1.56.0-2.ph1 

**erase**: This command removes the package that you specify as an argument. The following is an example:

	tdnf erase vim
	Removing:
	vim                                   x86_64        7.4-4.ph1                 1.94 M
	Total installed size: 1.94 M
	Is this ok [y/N]:

You can also erase multiple packages: 

	tdnf erase docker cloud-init

**info**: This command displays information about packages. It can take the name of a package. Or it can take one of the following arguments: all, available, installed, extras, obsoletes, recent, upgrades. The following are examples:

	tdnf info ruby
	tdnf info obsoletes
	tdnf info upgrades

**install**: This command takes the name of a package as its argument. It then installs the package and its dependencies. The following are examples:

	tdnf install kubernetes

You can also install multiple packages: 

	tdnf install python-curses lsof audit gettext chkconfig ntsysv bindutils 
		 wget gawk irqbalance lvm2 cifs-utils c-ares distrib-compat
	

**list**: This command lists the packages of the package that you specify as the argument. The command can take one of the following arguments: all, available, installed, extras, obsoletes, recent, upgrades. 

	tdnf list updates

The list of packages might be long. To more easily view it, you can concatenate it into a text file, and then open the text file in a text editor: 

	tdnf list all > pkgs.txt
	vi pkgs.txt

**makecache**: This command updates the cached binary metadata for all known repositories. The following is an example:

	tdnf makecache
	Refreshing metadata for: 'VMware Lightwave 1.0(x86_64)'
	Refreshing metadata for: 'VMware Photon Linux 1.0(x86_64)Updates'
	Refreshing metadata for: 'VMware Photon Extras 1.0(x86_64)'
	Refreshing metadata for: 'VMware Photon Linux 1.0(x86_64)'
	Metadata cache created.

**provides**: This command finds the packages that provide the package that you supply as an argument. The following is an example: 

	tdnf provides docker
	docker-1.11.0-1.ph1.x86_64 : Docker
	Repo     : photon
	docker-1.11.0-1.ph1.x86_64 : Docker
	Repo     : @System

**reinstall**: This command reinstalls the packages that you specify. If some packages are unavailable or not installed, the command fails. The following is an example: 

	tdnf reinstall docker kubernetes

	Reinstalling:
	kubernetes                            x86_64        1.1.8-1.ph1             152.95 M
	docker                                x86_64        1.11.0-1.ph1             57.20 M

	Total installed size: 210.15 M

**remove**: This command removes a package. When removing a package, tdnf by default also removes dependencies that are no longer used if they were was installed by tdnf as a dependency without being explicitly requested by a user. You can modify the dependency removal by changing the `clean_requirements_on_remove` option in /etc/tdnf/tdnf.conf to `false`. 

	tdnf remove packagename

**search**: This command searches for the attributes of packages. The argument can be the names of packages. The following is an example: 

	tdnf search docker kubernetes
	docker : Docker
	docker : Docker
	docker-debuginfo : Debug information for package docker
	docker : Docker
	kubernetes : Kubernetes cluster management
	kubernetes : Kubernetes cluster management
	kubernetes-debuginfo : Debug information for package kubernetes
	kubernetes : Kubernetes cluster management

The argument of the search command can also be a keyword or a combination of keywords and packages: 

	tdnf search terminal bash
	rubygem-terminal-table : Simple, feature rich ascii table generation library
	ncurses : Libraries for terminal handling of character screens
	mingetty : A minimal getty program for virtual terminals
	ncurses : Libraries for terminal handling of character screens
	ncurses : Libraries for terminal handling of character screens
	bash : Bourne-Again SHell
	bash-lang : Additional language files for bash
	bash-lang : Additional language files for bash
	bash : Bourne-Again SHell
	bash-debuginfo : Debug information for package bash
	bash : Bourne-Again SHell
	bash-lang : Additional language files for bash

**upgrade**: This command upgrades the package or packages that you specify to an available higher version that tdnf can resolve. If the package is already the latest version, the command returns `Nothing to do`. The following is an example: 

	tdnf upgrade boost

	Upgrading:
	boost                                 x86_64        1.60.0-1.ph1              8.11 M

	Total installed size: 8.11 M
	Is this ok [y/N]:y

	Downloading:
	boost                                  2785950    100%
	Testing transaction
	Running transaction

	Complete!

You can also run the `upgrade` command with the `refresh` option to update the cached metadata with the latest information from the repositories. The following example refreshes the metadata and then checks for a new version of tdnf but does not find one, so tdnf takes no action: 

	tdnf upgrade tdnf --refresh
	Refreshing metadata for: 'VMware Lightwave 1.0(x86_64)'
	Refreshing metadata for: 'VMware Photon Linux 1.0(x86_64)Updates'
	Refreshing metadata for: 'VMware Photon Extras 1.0(x86_64)'
	Refreshing metadata for: 'VMware Photon Linux 1.0(x86_64)'
	Nothing to do.

**upgrade-to**: This command upgrades to the version of the package that you specify. EThe following is an example: 

	tdnf upgrade-to ruby2.3

The commands and options of tdnf are a subset of those of dnf. For more help with `tdnf` commands, see the [DNF documentation](https://media.readthedocs.org/pdf/dnf/latest/dnf.pdf).