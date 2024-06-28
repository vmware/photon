# Options for Commands

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

The following is an example that adds the short form of the `assumeyes` option to the install command:

	tdnf -y install gcc
	Upgrading:
	gcc 	x86_64	5.3.0-1.ph1 	91.35 M
