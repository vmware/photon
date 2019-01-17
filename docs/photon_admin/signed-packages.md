# Signed Packages

Photon OS signs its packages and repositories with GPG signatures to enhance security. The GPG signature uses keyed-hash authentication method codes, typically the SHA1 algorithm and an RSA Data Security, Inc. MD5 Message Digest Algorithm, to simultaneously verify the integrity of a package. A keyed-hash message authentication code combines a cryptographic hash function with a secret cryptographic key.

In Photon OS, GPG signature verification automatically takes place when you install or update a package with the default package manager, tdnf. The default setting in the tdnf configuration file for checking the GPG is set to `1` for true:  

    cat /etc/tdnf/tdnf.conf
    [main]
    gpgcheck=1
    installonly_limit=3
    clean_requirements_on_remove=true
    repodir=/etc/yum.repos.d
    cachedir=/var/cache/tdnf

On Photon OS, you can view the key with which VMware signs packages by running the following command:  

    rpm -qa gpg-pubkey*

The command returns the GPG public key:

    gpg-pubkey-66fd4949-4803fe57

Once you have the name of the key, you can view information about the key with the `rpm -qi` command, as the following abridged output demonstrates: 

    rpm -qi gpg-pubkey-66fd4949-4803fe57
    Name        : gpg-pubkey
    Version     : 66fd4949
    Release     : 4803fe57
    Architecture: (none)
    Install Date: Thu Jun 16 11:51:39 2016
    Group       : Public Keys
    Size        : 0
    License     : pubkey
    Signature   : (none)
    Source RPM  : (none)
    Build Date  : Tue Apr 15 01:01:11 2008
    Build Host  : localhost
    Relocations : (not relocatable)
    Packager    : VMware, Inc. -- Linux Packaging Key -- <linux-packages@vmware.com>
    Summary     : gpg(VMware, Inc. -- Linux Packaging Key -- <linux-packages@vmware.                        com>)
    Description :
    -----BEGIN PGP PUBLIC KEY BLOCK-----
    Version: rpm-4.11.2 (NSS-3)
    mI0ESAP+VwEEAMZylR8dOijUPNn3He3GdgM/kOXEhn3uQl+sRMNJUDm1qebi2D5b ...

If you have one of the RPMs from Photon OS on another Linux system, such as Ubuntu, you can use SHA and the RSA Data Security, Inc. MD5 Message Digest Algorithm for the package to verify that it has not been tampered with:

    rpm -K /home/steve/workspace/photon/stage/SRPMS/kubernetes-1.1.8-4.ph1.src.rpm
    /home/steve/workspace/photon/stage/SRPMS/kubernetes-1.1.8-4.ph1.src.rpm: sha1 md5 OK

You can view the SHA1 digest and the RSA Data Security, Inc. MD5 Message Digest Algorithm by running the following command: 

    rpm -Kv /home/steve/workspace/photon/stage/SRPMS/kubernetes-1.1.8-4.ph1.src.rpm
    /home/steve/workspace/photon/stage/SRPMS/kubernetes-1.1.8-4.ph1.src.rpm:
    Header SHA1 digest: OK (89b55443d4c9f67a61ae0c1ec9bf4ece2d6aa32b)
            MD5 digest: OK (51eee659a8730e25fd2a52aff9a6c2c2)

The above examples show that the Kubernetes package has not been tampered with.