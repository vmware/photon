# Adding a New Repository

On Photon OS, you can add a new repository from which `tdnf` installs packages. To add a new repository, you create a repository configuration file with a `.repo` extension and place it in `/etc/yum.repos.d`. The repository can be on either the Internet or a local server containing your in-house applications. 

Be careful if you add a repository  that is on the Internet. Installing packages from untrusted or unverified sources might put the security, stability, or compatibility of your system at risk. It might also make your system harder to maintain.  

On Photon OS, the existing repositories appear in the `/etc/yum.repos.d` directory:

	ls /etc/yum.repos.d/
	lightwave.repo
	photon-extras.repo
	photon-iso.repo
	photon-updates.repo
	photon.repo 

To view the the format and information that a new repository configuration file should contain, see one of the `.repo` files. The following is an example:

	cat /etc/yum.repos.d/lightwave.repo
	[lightwave]
	name=VMware Lightwave 1.0(x86_64)
	baseurl=https://dl.bintray.com/vmware/lightwave
	gpgkey=file:///etc/pki/rpm-gpg/VMWARE-RPM-GPG-KEY
	gpgcheck=1
	enabled=1
	skip_if_unavailable=True

The minimal information needed to establish a repository is an ID and human-readable name of the repository and its base URL. The ID, which appears in square brackets, must be one word that is unique amoung the system's repositories; in the example above, it is `[lightwave]`.

The `baseurl` is a URL for the repository's repodata directory. For a repository on a local server that can be accessed directly or mounted as a file system, the base URL can be a file referenced by `file://`. Example:  

	baseurl=file:///server/repo/

The `gpgcheck` setting specifies whether to check the GPG signature. The `gpgkey` setting furnishes the URL for the repository's ASCII-armored GPG key file. Tdnf uses the GPG key to verify a package if its key has not been imported into the RPM database.

The `enabled` setting tells `tdnf` whether to poll the repository. If `enabled` is set to `1`, `tdnf` polls it; if it is set to `0`, `tdnf` ignores it. 

The `skip_if_unavailable` setting instructs `tdnf` to continue running if the repository goes offline.

Other options and variables can appear in the repository file. The variables that are used with some of the options can reduce future changes to the repository configuration files. There are variables to replace the value of the version of the package and to replace the base architecture. For more information, see the man page for `yum.conf` on the full version of Photon OS: `man yum.conf`

The following is an example of how to add a new repository for a local server that `tdnf` polls for packages:

	cat > /etc/yum.repos.d/apps.repo << "EOF"
	[localapps]
	name=Local In-House Applications(x86_64)
	baseurl=file:///appserver/apps
	enabled=1
	skip_if_unavailable=True
	EOF

Because this new repository resides on a local server, make sure the Photon OS machine can connect to it by mounting it. 

After establishing a new repository, you must run the following command to update the cached binary metadata for the repositories that `tdnf` polls:

	tdnf makecache
	Refreshing metadata for: 'VMware Lightwave 1.0(x86_64)'
	Refreshing metadata for: 'VMware Photon Linux 1.0(x86_64)Updates'
	Refreshing metadata for: 'VMware Photon Extras 1.0(x86_64)'
	Refreshing metadata for: 'Local In-House Applications(x86_64)'
	Refreshing metadata for: 'VMware Photon Linux 1.0(x86_64)'
	Metadata cache created.