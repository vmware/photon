---
title:  Examining Signed Packages
weight: 4
---

Photon OS signs its packages and repositories with GPG signatures to enhance security. The GPG signature uses keyed-hash authentication method codes, typically the SHA1 algorithm and an RSA Data Security, Inc. MD5 Message Digest Algorithm, to simultaneously verify the integrity of a package. A keyed-hash message authentication code combines a cryptographic hash function with a secret cryptographic key.

In Photon OS, GPG signature verification automatically takes place when you install or update a package with the default package manager, `tdnf`. The default setting in the tdnf configuration file for checking the GPG is set to `1` for true:  

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
	gpg-pubkey-8a6a826d-596882ca
	

Once you have the name of the key, you can view information about the key with the `rpm -qi` command, as the following abridged output demonstrates: 

```
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
```   



```
rpm -qi gpg-pubkey-8a6a826d-596882ca
Name        : gpg-pubkey
Version     : 8a6a826d
Release     : 596882ca
Architecture: (none)
Install Date: Tue 18 Apr 2023 10:17:59 AM UTC
Group       : Public Keys
Size        : 0
License     : pubkey
Signature   : (none)
Source RPM  : (none)
Build Date  : Fri 14 Jul 2017 08:37:30 AM UTC
Build Host  : localhost
Packager    : VMware, Inc. (Linux Packaging Key) <linux-packages@vmware.com>
Summary     : VMware, Inc. (Linux Packaging Key) <linux-packages@vmware.com> public key
Description :
-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: rpm-4.18.0

mQINBFlogsoBEACylcZdKvVdq+XZZ5oXyV7+Wk4wYo9ALIy5Y/TlQ7YoJndF3A6d
j3KXLFZ3xLMYuktUwqEiVN24s2loAG3kcS5c8bb7LxiZMFoEfo8bUm8mcfcPKCdy
ZgE0TNwYejn6w9tuEOLtewVtFaP3FrCjzZz2VMXi5c9sNxmIxfrBuuDZP8MLoDKr
fv4Zzif2K6J4nRMBY2t8SSj8Z4zDUCLQ36wYlD2slONdmX8Ufd86rt/ZJ156xsCX
2UgTb62uUVESlWfsuMhv5CBO2JEbbnMBjfZdI5qplwEt54kq34PzP6fRCa8yrLR8
FlZsAQO32A0SDNUWHphDP3d2W64XtttjRJPsWv16IXss1YwyjUd1CBYDpefXvzW2
h8Ca6HDgLRG0eoVZdY8gx1geF64wuGjSA+4gnjTaMeLQSBfeAzm6Pe4eB6bEc/iX
NiZY9KlA1orRcuHxXIzjsHR5f1JCK0Fgl76aNzxnztuU0uRSLZRxUMUpszCOyqy9
ufsbMeklbKtobfVqRulQEJwCXHL99t+Ln14L3PgXKeLqaj/LReIqWlWiFtm6Zgyf
a45z8lf8Z3lRK+orrNJ8fVJr/8T9O/vgpbwwqEZ2bflzqXcUPyWnMl6Cu8SNbtwK
orvZ1bwNkz5T9myW+6pXcr9sB/IiNmyfTS1rXqwUlRN60vwD+a52MpnCGwARAQAB
tD5WTXdhcmUsIEluYy4gKExpbnV4IFBhY2thZ2luZyBLZXkpIDxsaW51eC1wYWNr
YWdlc0B2bXdhcmUuY29tPokCNgQTAQIAIAUCWWiCygIbAwYLCQgHAwIEFQIIAwQW
AgMBAh4BAheAAAoJEHXACeqKaoJtIYIP/3y2+xIZ3ZArdhH6NR3ilMPGSVoe1M2+
10XlL9wydgXPdKrq8IZUNg5/VBEjpOZML82aD9VRkMXI6XdbrdRw+5G2D5ZOtWRp
ha8KPuFxax2YuB8ifRgcrgR0kq4v+p3XHaT88UQxk/gDpJVOMJaLhyn8KNBPVkPq
zJ3IXC/A/rWv6rbDAnyyt20GpCqWuoCJCQDMCbBItyaL42OWY3yk3WlfFOjQU1Sq
zIYCCJGM87rNHpwErHDIanFu0gXCarFB6uRT9ixgyJqg7dtPAyBdydxo0JesH0Fc
t30NYkRiqqeSz6ImWlcvDHZkiDXNvP0D9utyOPQDoIaX+G0gCnf+UpHTgc0eGc6U
+aHIyHMK7Du+cfTXL8W5LAbSw7pTPSPc/sZal1ijDvk1lyMhT6kZ22v2IXYadosp
eA7+9ykSk3Iy9qhjUTQ+qG/KMgUTMVqWUp6IEze80892w3yNFi8tEvdRzORbOHuP
IhyoLek4vQj+ziDm4C1ARrYk8AiW40ioRJuT73DF8RhuzD8hBt1tH6mjeIANz8Lf
1big996JofkxU2eN99MnhUeBxFrOCPef7y9h0rM7UqZHDo1HGxCZxd12COyspWkG
WsFN4VrLxkXhPfa8jc5TBY5e1632JoL+VuWFjKd0CddgtSm2bqfX355BQi6+eJ4A
kJ3L8QRJSNeY
=ogBe
-----END PGP PUBLIC KEY BLOCK-----

#
```   

If you have one of the RPMs from Photon OS on another Linux system, such as Ubuntu, you can use SHA and the RSA Data Security, Inc. MD5 Message Digest Algorithm for the package to verify that it has not been tampered with:

```
rpm -K GConf-3.2.6-1.ph5.src.rpm
GConf-3.2.6-1.ph5.src.rpm: digests signatures OK
```

You can view the SHA1 digest and the RSA Data Security, Inc. MD5 Message Digest Algorithm by running the following command: 

```
rpm -Kv GConf-3.2.6-1.ph5.src.rpm
GConf-3.2.6-1.ph5.src.rpm:
    Header V3 RSA/SHA256 Signature, key ID 66fd4949: OK
    Header SHA256 digest: OK
    Header SHA1 digest: OK
    Payload SHA256 digest: OK
    V3 RSA/SHA256 Signature, key ID 66fd4949: OK
    MD5 digest: OK
#
```   

The above examples show that the Kubernetes package has not been tampered with.