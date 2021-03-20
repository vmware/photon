---
title:  Adding a New Repository
weight: 3
---

On Photon OS, you can add a new repository from which `tdnf` installs packages. To add a new repository, you create a repository configuration file with a `.repo` extension and place it in `/etc/yum.repos.d`. The repository can be on either the Internet or a local server containing your in-house applications. 

Be careful if you add a repository  that is on the Internet. Installing packages from untrusted or unverified sources might put the security, stability, or compatibility of your system at risk. It might also make your system harder to maintain.  

On Photon OS, the existing repositories appear in the `/etc/yum.repos.d` directory:

	ls /etc/yum.repos.d/
	photon-extras.repo
	photon-iso.repo
	photon-updates.repo
	photon.repo 

To view the the format and information that a new repository configuration file should contain, see one of the `.repo` files. The following is an example:


	baseurl=https://https://packages.vmware.com/photon/
    metalink=http://example.com/*username*/metalink/metalink
	gpgkey=file:///etc/pki/rpm-gpg/VMWARE-RPM-GPG-KEY
	gpgcheck=1
	enabled=1
	skip_if_unavailable=True

The repository settings details are as follows:



- The minimal information needed to establish a repository is an ID and human-readable name of the repository and its base URL. The ID, which appears in square brackets, must be one word that is unique amoung the system's repositories; `.



- The `baseurl` is a URL for the repository's repodata directory. For a repository on a local server that can be accessed directly or mounted as a file system, the base URL can be a file referenced by `file://`. Example:  

	baseurl=file:///server/repo/



- By using `metalink`, you can point to multiple URLs to download the `repomd.xml` file. A sample metalink file is as follows:

    `cat metalink`

    ```xml    
    <?xml version="1.0" encoding="utf-8"?>
    
    <metalink version="3.0" xmlns="http://www.metalinker.org/" type="dynamic" pubdate="Wed, 05 Feb 2020 08:14:56 GMT" generator="mirrormanager" xmlns:mm0="http://fedorahosted.org/mirrormanager">
    
     <files>
    
      <file name="repomd.xml">
    
       <size>2035</size>
    
       <verification>
    
    <hash type="sha1">478437547dac9f5a73fe905d2ed2a0a5b153ef46</hash>
    
    <hash type="sha512">6c6fbfba288ec90905a8d2220a0bfd2a50e835b7faaefedb6978df6ca59c5bce25cc1ddd33023e305b20bcffc702ee2bd61d0855f4f1b2fd7c8f5109e428a764</hash>
    
       </verification>
    
       <resources maxconnections="1">
    
    <url protocol="http" type="http" location="IN" preference=“100”>https://packages.vmware.com/photon/3.0/photon_updates_3.0_x86_64/repodata/repomd.xml</url>
     
       </resources>
    
      </file>
    
     </files>
    
    </metalink>
    ```

    
  In the metalink file, provide the preference for each url, so `tdnf` first tries to sync the repository data from the mirror which has the highest preference. If it fails due to any reason, `tdnf` will sync to the next mirror url with the lower preference than before one.

  Note: Ensure that the shasum for `respomd.xml` in all the mirrors should be same


- The `gpgcheck` setting specifies whether to check the GPG signature.

- The `repo_gpgcheck` setting allows `tdnf` to verify the signature of a repository metadata before downloading the repository artifacts. When `repo_gpgcheck` is set to `1` in the tdnf.conf file, all repositories will be checked for the metadata signatures. The default value is `0`.
  If a repository has `repo_gpgcheck` enabled,a `repomd.xml.asc` file is downloaded and the API equivalent of `gpg --verify repomd.xml.asc repomd.xml` is done. If `repomd.xml.asc` is missing, repository is disabled. If `repomd.xml.asc` fails to verify, the repository is disabled. The public key for verification must be manually installed for the initial implementation.

  Note: Ensure that you have installed `libgcrypt` for this implementation.

- The `gpgkey` setting furnishes the URL for the repository's ASCII-armored GPG key file. `tdnf` uses the GPG key to verify a package if its key has not been imported into the RPM database. 

  The repository configuration also supports public keys that are remote for the `gpgkey` option. So, the URLs starting with `http`, `https`, or `ftp` can be used for `gpgkey`.

  For example:
    gpgkey=http://build-squid.eng.vmware.com/build/mts/release/bora-16633979/publish/packages/keys/vmware.asc 


- The `enabled` setting tells `tdnf` whether to poll the repository. If `enabled` is set to `1`, `tdnf` polls it; if it is set to `0`, `tdnf` ignores it. 


- The `skip_if_unavailable` setting instructs `tdnf` to continue running if the repository goes offline.

- The `retries` setting in the repository configuration specifies the number of retries when downloading a file throws an error. The default is `10`. 

- The `timeout` setting specifies the number of seconds that a download is allowed to take or `0` for no limit. Note that this is an absolute value and may interrupt large file downloads.

- The `minrate` setting specifies the limit below which if the download rate falls, `tdnf` will abort the download. The default value is `0 `(`no limit`).

- The `maxrate` setting specifies the maximum download rate (throttle). The default value is `0 `(`no limit`).



- Other options and variables can appear in the repository file. The variables that are used with some of the options can reduce future changes to the repository configuration files. There are variables to replace the value of the version of the package and to replace the base architecture. For more information, see the man page for `yum.conf` on the full version of Photon OS: `man yum.conf`

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
	Refreshing metadata for: 'VMware Photon Linux 1.0(x86_64)Updates'
	Refreshing metadata for: 'VMware Photon Extras 1.0(x86_64)'
	Refreshing metadata for: 'Local In-House Applications(x86_64)'
	Refreshing metadata for: 'VMware Photon Linux 1.0(x86_64)'
	Metadata cache created.