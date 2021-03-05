---
title:  Photon Code
weight: 1
---

Photon is an RPM based Linux distribution similar to variants like CentOS and Fedora. With RPM based distributions granular updates as opposed to updating the whole OS image is possible.

##SPEC File
The "Recipe" for creating an RPM package is a spec file. The Photon code base's **SPECS** folder hast the following directory structure:
```
SourceRoot

       SPECS
            linux
                patch1
                patch2
                linux.spec
```

##To Check if a Package is Signed
Run the following commands to check if the package is signed:
```
#check if a package is signed
rpm -q linux --qf '%{NAME}-%{VERSION}-%{RELEASE} %{SIGPGP:pgpsig} %{SIGGPG:pgpsig}\n'
linux-4.19.79-2.ph3 RSA/SHA1, Thu 31 Oct 2019 10:05:05 AM UTC, Key ID c0b5e0ab66fd4949 (none)
 
#or
rpm -qi linux | grep "Signature"
Signature   : RSA/SHA1, Thu 31 Oct 2019 10:05:05 AM UTC, Key ID c0b5e0ab66fd4949
 
#Last 8 chars of Key ID: 66fd4949
#See if it matches the version of any of the gpg keys installed.
rpm -qa | grep gpg-pubkey | xargs -n1 rpm -q --queryformat "%{NAME} %{VERSION} %{PACKAGER}\n"
gpg-pubkey 66fd4949 VMware, Inc. -- Linux Packaging Key -- linux-packages@vmware.com
gpg-pubkey 3e1ba8d5 Google Cloud Packages RPM Signing Key gc-team@google.com
```

##To Check if Your Image Has Vulnerabilities
Use the security scanners to find security issues. Alternatively The `tdnf updateinfo info` command displays all the applicable security updates the host needs.

##To Check if a CVE is Fixed
The Photon team fix the vulnerabilities and then publish the advisories to (https://github.com/vmware/photon/wiki/Security-Advisories).

##To Check if Security Updates are Available
Use the `tdnf updateinfo info`, `tdnf update --security` or `tdnf update ---sec-severity <level>` commands to check if security updates are available. For example:
```
#check if there are any security updates
root@photon-9a8c05dd97e9 [ ~ ]# tdnf updateinfo
70 Security notice(s)
 
#check if there are security updates for libssh2. note this is relative to what is installed in local
root@photon-9a8c05dd97e9 [ ~ ]# tdnf updateinfo list libssh2
patch:PHSA-2020-3.0-0047 Security libssh2-1.9.0-2.ph3.x86_64.rpm
patch:PHSA-2019-3.0-0025 Security libssh2-1.9.0-1.ph3.x86_64.rpm
patch:PHSA-2019-3.0-0009 Security libssh2-1.8.2-1.ph3.x86_64.rpm
patch:PHSA-2019-3.0-0008 Security libssh2-1.8.0-2.ph3.x86_64.rpm
 
#show details of all the libssh2 updates
root@photon-9a8c05dd97e9 [ ~ ]# tdnf updateinfo info libssh2
       Name : libssh2-1.9.0-2.ph3.x86_64.rpm
  Update ID : patch:PHSA-2020-3.0-0047
       Type : Security
    Updated : Wed Jan 15 10:48:25 2020
Needs Reboot: 0
Description : Security fixes for {'CVE-2019-17498'}
       Name : libssh2-1.9.0-1.ph3.x86_64.rpm
  Update ID : patch:PHSA-2019-3.0-0025
       Type : Security
    Updated : Sat Aug 17 16:14:35 2019
Needs Reboot: 0
Description : Security fixes for {'CVE-2019-13115'}
       Name : libssh2-1.8.2-1.ph3.x86_64.rpm
  Update ID : patch:PHSA-2019-3.0-0009
       Type : Security
    Updated : Sat Apr 13 03:34:22 2019
Needs Reboot: 0
Description : Security fixes for {'CVE-2019-3859', 'CVE-2019-3862', 'CVE-2019-3861', 'CVE-2019-3857', 'CVE-2019-3858', 'CVE-2019-3863', 'CVE-2019-3860', 'CVE-2019-3856'}
       Name : libssh2-1.8.0-2.ph3.x86_64.rpm
  Update ID : patch:PHSA-2019-3.0-0008
       Type : Security
    Updated : Fri Mar 29 16:04:18 2019
Needs Reboot: 0
Description : Security fixes for {'CVE-2019-3855'}
 
 
 
#install all security updates >= score 9.0 (CVSS_v3.0_Severity)
root@photon-9a8c05dd97e9 [ ~ ]# tdnf update --sec-severity 9.0
Upgrading:
apache-tomcat                  noarch          8.5.50-1.ph3         photon-updates    9.00M 9440211
bash                           x86_64          4.4.18-2.ph3         photon-updates    3.16M 3315720
bzip2                          x86_64          1.0.8-1.ph3          photon-updates  124.99k 127990
bzip2-libs                     x86_64          1.0.8-1.ph3          photon-updates   74.31k 76096
file                           x86_64          5.34-2.ph3           photon-updates   43.02k 44056
file-libs                      x86_64          5.34-2.ph3           photon-updates    5.21M 5458536
git                            x86_64          2.23.1-2.ph3         photon-updates   24.34M 25519969
glib                           x86_64          2.58.0-4.ph3         photon-updates    3.11M 3265152
libseccomp                     x86_64          2.4.0-2.ph3          photon-updates  315.79k 323368
libssh2                        x86_64          1.9.0-2.ph3          photon-updates  238.41k 244136
linux-esx                      x86_64          4.19.97-2.ph3        photon-updates   12.68M 13299655
 
Total installed size:  58.28M 61114889
```
