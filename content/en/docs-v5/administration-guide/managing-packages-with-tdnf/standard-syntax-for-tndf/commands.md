---
title:  tdnf Commands
weight: 1
---
**autoremove [pkg-spec]**: This command removes a package with its dependencies. This is similar to the `erase`/`remove` command. You can use this command to remove the packages that are no longer needed regardless of the `clean_requirements_on_remove` option.

`autoremove` without any arguments removes all automatically installed packages that are no longer required.

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
	Cleaning repos: photon photon-extras photon-updates
	Cleaning up everything

You can use this command to clean all configured repositories.

You can also use the following sub-commands or arguments to clean specific files:

`metadata`: This sub-command cleans up downloaded metadata from the repositories.

`dbcache`: This sub-command cleans up metadata generated from `libsolv`

`packages`: This sub-command removes downloaded packages from the cache.

`keys`: This sub-command removes downloaded keys from the cache.

`expire-cache`: This sub-command removes the cache expiry marker. This triggers a download of metadata on the next action that needs them. 


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

**erase**: This command removes the package that you specify as an argument. 

To remove a package, run the following command: 

	tdnf erase pkgname
	
The following is an example:

	tdnf erase vim
	Removing:
	vim                                   x86_64        7.4-4.ph1                 1.94 M
	Total installed size: 1.94 M
	Is this ok [y/N]:

You can also erase multiple packages: 

	tdnf erase docker cloud-init

When you remove a package, by default, `tdnf` does not remove the dependencies that are no longer used if `tdnf` installed them as dependencies. To remove the dependencies, modify the `clean_requirements_on_remove` option in the `/etc/tdnf/tdnf.conf` file to `true`, or use the `autoremove` command.


**history**: This command allows you to record every transaction (commands that install, update, or remove packages) in a database. You can roll back the transactions to a past state, or undo or redo a range of transactions.

There are five sub-commands or arguments that you can use with the history command:

`history init/update`: The sub-commands `init` or `update` initializes the history database. It is recommended that you use these commands right after `tdnf` is installed. If the database is not already initialized, any altering commands such as `install` or `erase` initializes the database.

If the database is already initialized, the commands have no effect unless an application such as an RPM command adds or removes any packages after the last recorded transaction.

`history list`: This command lists the history of transactions. Note that this result is similar when you use the `history` command without an argument or sub-command. 

The following example shows the use of the command:

```
# tdnf history
ID   cmd line                                 date/time             +added / -removed
   1 (set)                                    Thu May 05 2022 19:14 +152 / -0
   2 -y install less                          Thu May 05 2022 19:14 +1 / -0
   3 -y install lsof                          Thu May 05 2022 19:18 +2 / -0
```

You can specify the following options for this sub-command:

- `--info`: Use this option to list a more detailed history that includes added or removed packages.
- `--reverse` Use this option to list the history in reverse order.
- `--from <id> and --to <id>`: Use this option to list a range of transactions. You can specify the transaction IDs of the range in this option.

The following example shows how to use the options:

```
# tdnf history --info --from 2 --to 3
ID   cmd line                                 date/time             +added / -removed
   2 -y install less                          Thu May 05 2022 19:14 +1 / -0
added: less-551-2.ph4.aarch64

   3 -y install lsof                          Thu May 05 2022 19:18 +2 / -0
added: libtirpc-1.2.6-2.ph4.aarch64, lsof-4.91-1.ph4.aarch64
```

**history rollback --to trans_id**: This command allows you to revert to a previous state. You must specify the  ID of the desired state with the `--to` parameter. 

Example:
```
# tdnf history rollback --to 49

Upgrading:
curl-devel                               aarch64              7.82.0-3.ph4                photon-updates       885.16k 906404
curl                                     aarch64              7.82.0-3.ph4                photon-updates       256.73k 262896
...

Total installed size:   3.52M 3688748
Is this ok [y/N]: y

Downloading:
curl-devel                              793306 100%
curl                                    148725 100%
...
Testing transaction
Running transaction
Installing/Updating: rpm-libs-4.16.1.3-9.ph4.aarch64
Installing/Updating: rpm-4.16.1.3-9.ph4.aarch64
...
Complete!
```

**history undo --from trans_id [--to trans_id]**: You can use this command to undo a transaction. The parameter `--from` is mandatory, and the specified transaction in the parameter is reversed. Optionally, you can specify a range with the parameter `--to` to reverse all the specified transactions. Note that the range you specify is inclusive. For example, if you specify the range as `2 to 4`, the transactions in 2, 3, and 4 are reversed.

**history redo --from trans_id [--to trans_id]**: You can use this command to redo a transaction. The parameter `--from` is mandatory, and the specified transaction in the parameter is redone. Optionally, you can specify a range with the parameter `--to` to redo all the specified transactions. The range you specify in the parameters is inclusive.

***NOTE***

`Deltas`: When you make changes using history commands, the changes are resolved based on the total deltas between the start and the target states. For each range of transactions, the intermediate states are irrelevant. For example, in a range of transactions where one transaction installs a package and the last one removes the package, the final installed state of the package remains the same from start to end.

`Unresolved Packages`: If a package is not found, `tdnf` fails with an error message. For instance, when you roll back to a state before an update, the system might not find all the required installation packages in the repository. In such a case, you can enable the additional repositories to successfully revert. 

Example:

The following example shows how the `tdnf` fails with an error message for the unavilable packages:
```
# tdnf history rollback --to 1
The following packages could not be resolved:

curl-libs-7.82.0-1.ph4.aarch64
rpm-libs-4.16.1.3-7.ph4.aarch64
...

The package(s) may have been moved out of the enabled repositories since the
last time they were installed. You may be able to resolve this by enabling
additional repositories.
Error(1011) : No matching packages
```

The following example shows how you can enable the repository to resolve the issue:

```
tdnf --enablerepo=photon history rollback --to 1

Downgrading:
curl-devel                               aarch64              7.82.0-1.ph4                photon               885.16k 906404
rpm-build                                aarch64              4.16.1.3-7.ph4              photon               434.00k 444418
...

Total installed size:   4.26M 4463905

Removing:
wget                                     aarch64              1.21.3-1.ph4                @System                3.02M 3168291
tdnf-test-cleanreq-required              aarch64              1.0.1-3                     @System                    0.00b 0
lsof                                     aarch64              4.91-1.ph4                  @System              202.36k 207218
libtirpc                                 aarch64              1.2.6-2.ph4                 @System              193.33k 197970
gdb                                      aarch64              10.1-2.ph4                  @System               12.60M 13214814

Total installed size:  16.01M 16788293
Is this ok [y/N]: 
```

`Transactions outside tdnf`: `tdnf` keeps track of the  transactions it performs. However, other tools such as `rpm` can also add or remove packages. While performing the next transaction, if `tdnf` detects transactions performed by other tools, it records such transactions as pseudo transactions. 

Example:
```
# tdnf history --info --from 49 --to 49
ID   cmd line                                 date/time.            +added / -removed
  49 (unknown)                                Thu May 05 2022 23:38 +1 / -0
added: gdb-10.1-2.ph4.aarch64
```

`Dependencies`: The `undo` and `redo` actions might need to install additional depedencies apart from the previously existing packages. For example, when you redo a transaction that installs a single package which was earlier removed along with its depedencies, the command also attempts to install the dependecies. 

Note that this is not an issue for the `rollback` command because the entire set of packages is restored assuming that the dependecies are also satisfied at the state.

**info**: This command displays information about packages. It can take the name of a package. Or it can take one of the following arguments: all, available, installed, extras, obsoletes, recent, upgrades. The following are examples:

	tdnf info ruby
	tdnf info obsoletes
	tdnf info upgrades

**install**: This command takes the name of a package as its argument. It then installs the package and its dependencies. 

To install a package, run the following command:

	tdnf install pkgname
The following are examples:

	tdnf install kubernetes

You can also install multiple packages: 

	tdnf install python-curses lsof audit gettext chkconfig ntsysv bindutils 
		 wget gawk irqbalance lvm2 cifs-utils c-ares distrib-compat
	

**list**: This command lists the packages of the package that you specify as the argument. The command can take one of the following arguments: all, available, installed, extras, obsoletes, recent, upgrades. 

	tdnf list updates

The list of packages might be long. To more easily view it, you can concatenate it into a text file, and then open the text file in a text editor: 

	tdnf list all > pkgs.txt
	vi pkgs.txt

To list enabled repositories, run the following command:

	tdnf repolist

**makecache**: This command updates the cached binary metadata for all known repositories. The following is an example:

	tdnf makecache
	Refreshing metadata for: 'VMware Lightwave 1.0(x86_64)'
	Refreshing metadata for: 'VMware Photon Linux 1.0(x86_64)Updates'
	Refreshing metadata for: 'VMware Photon Extras 1.0(x86_64)'
	Refreshing metadata for: 'VMware Photon Linux 1.0(x86_64)'
	Metadata cache created.

**mark install|remove pkg_spec**: Mark one or more packages as auto installed (remove) or unmark as auto installed (install), which means it is user-installed. This is used to determine if this package gets removed on autoinstall.

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


**repoquery [args]**: The `repoquery` command allows you to query packages from the repositories and installed packages with different criteria and output options. It can take multiple package specifications as arguments.

Example:

```
$ tdnf repoquery vim 
vim-8.2.4925-1.ph4.aarch64
vim-8.2.1361-1.ph4.aarch64

$ tdnf repoquery vim*
vim-8.2.4925-1.ph4.aarch64
vim-8.2.1361-1.ph4.aarch64
vim-extra-8.2.4925-1.ph4.aarch64
vim-extra-8.2.1361-1.ph4.aarch64

$ tdnf repoquery --installed vim
vim-8.2.4925-1.ph4.aarch64

$ tdnf repoquery --requires vim
ld-linux-aarch64.so.1()(64bit)
ld-linux-aarch64.so.1(GLIBC_2.17)(64bit)
libc.so.6(GLIBC_2.17)(64bit)
...
```

The following groups of options are available for `repoquery`: 

- `select option`: Use this option to filter the list of packages. You can use the following parameters with the select option:
	- `--available`: Use this parameter to show available packages in the repositories.
	- `--duplicates`: Use this parameter to show duplicate installed packages.
	- `--extras`: Use this parameter to show the packages that are installed but not in any repositories. 
	- `--file` **file**: Use this parameter to show packages that contain the specified files.
	- `--installed`: Use this parameter to show the installed packages.
	- `--userinstalled`: Use this parameter to show the user-installed packages.
	- `--whatdepends, --whatenhances, --whatobsoletes, --whatprovides, --whatrecommends, whatrequires, --whatsuggests, --whatsupplements capability`: Use these parameters to show packages that have the specified dependency on capability.
	
		Example:

		```
		$ tdnf repoquery --whatrequires vim
		minimal-0.1-6.ph4.aarch64
		vim-extra-8.2.4925-1.ph4.aarch64
		minimal-0.1-4.ph4.aarch64

- `query option`: Use this option to control what you want the command to display. The query option lists the selected packages by default. You can use the following parameters to get the required output:
	- `--list`: Use this parameter to list all files of the selected packages.
	- `--depends, --enhances, --obsoletes, --provides, --recommends, requires, requires-pre, --suggests, --supplements`: Use these parameters to list specified dependencies.


**reoposync**: This command synchronizes a remote repository with a local one. By default, all packages are downloaded to a local directory unless they already exist. Optionally, metadata is also downloaded.

You can use the following options with the command:

`--delete`: Use this option to remove old packages that are not part of the repository any more.

`--download-metadata`: Use this option to download the metadata. After you download the the metadata, you can use the directory as a repository.

`--gpgcheck`: Use this option to check the gpg signature. If invalid, the package is deleted.

`--norepopath`: When you use this option, no subdirectory with the repo name is created. This option is only valid if you configure more than one repository.

`--urls`: When you use this option, instead of downloading, the URLs of all files are printed to `stdout`.

`--download-path`: Use this option to specify the download path. By default, files are downloaded relative to the current directory.

`--metadata-path`: Use this option to specify the download path. You can download metadata to a different directory.

`--arch`: Use this option to download specific architectures. You can use this option repeatedly.

`--source`: Use this option to download only source packages. This option is similar to `--arch src`. Note that this option is incompatible with the `--arch` option.

`--newest-only`: Use this option to download only the latest versions of the repository.


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

**updateinfo**: This command displays security advisories about packages. The following is an example:

    tdnf updateinfo info

    Name : unzip-6.0-15.ph3.x86_64.rpm
    Update ID : patch:PHSA-2020-3.0-0083
    Type : Security
    Updated : Fri Apr 24 01:15:03 2020
    Needs Reboot: 0
    Description : Security fixes for {'CVE-2018-1000035'}
    Name : runc-1.0.0.rc9-3.ph3.x86_64.rpm
    Update ID : patch:PHSA-2020-3.0-0102
    Type : Security
    Updated : Tue Jun  9 06:01:28 2020
    Needs Reboot: 0
    Description : Security fixes for {'CVE-2019-19921'}
    Name : ruby-2.5.8-2.ph3.x86_64.rpm
    Update ID : patch:PHSA-2020-3.0-0163
    Type : Security
    Updated : Thu Nov 19 17:21:29 2020
    Needs Reboot: 0

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

**upgrade-to**: This command upgrades to the version of the package that you specify. The following is an example: 

	tdnf upgrade-to ruby2.3

The commands and options of tdnf are a subset of those of dnf. For more help with `tdnf` commands, see the [DNF documentation](https://media.readthedocs.org/pdf/dnf/latest/dnf.pdf).