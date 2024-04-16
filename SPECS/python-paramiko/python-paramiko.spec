Summary:        Python SSH module
Name:           python3-paramiko
Version:        2.12.0
Release:        6%{?dist}
License:        LGPL
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://www.paramiko.org

Source0: https://github.com/paramiko/paramiko/archive/paramiko-%{version}.tar.gz
%define sha512 paramiko=1bf325ffd393447cb90009d01dc1104d0d43a6acdd08cc6d28310063a649a333323748800dab119ab5e10833975e68f5f5702044fc247a2e8058122a5327f2c7

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-ecdsa
BuildRequires:  python3-pycryptodome
BuildRequires:  python3-cryptography
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if 0%{?with_check}
BuildRequires:  python3-pytest
BuildRequires:  python3-pip
%endif

Requires:       python3
Requires:       python3-ecdsa > 0.11
Requires:       python3-cryptography
Requires:       python3-PyNaCl
Requires:       python3-bcrypt

Patch0:         CVE-2023-48795.patch

%description
"Paramiko" is a combination of the esperanto words for "paranoid" and "friend". It's a module for Python 2.6+ that implements the SSH2 protocol for secure (encrypted and authenticated) connections to remote machines. Unlike SSL (aka TLS), SSH2 protocol does not require hierarchical certificates signed by a powerful central authority.

%prep
%autosetup -p1 -n paramiko-%{version}

%build
%{py3_build}

%install
%py3_install -- --single-version-externally-managed

%check
pip3 install mock pytest_relaxed PyNaCl bcrypt
%{pytest}

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%{python3_sitelib}/*

%changelog
* Mon Apr 15 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.12.0-6
- Bump to compile with python3-pycryptodome v3.20.0
* Tue Dec 26 2023 Prashant S Chauhan <psingchauha@vmware.com> 2.12.0-5
- Bump up to compile with latest python3-cryptography, Fix makecheck
* Fri Dec 22 2023 Mukul Sikka <msikka@vmware.com> 2.12.0-4
- Fix for CVE-2023-48795
* Fri Dec 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.12.0-3
- Remove cryptodome dependency
* Fri Jan 06 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 2.12.0-2
- Version bump for python3-ecdsa upgrade.
* Tue Dec 13 2022 Gerrit Photon <photon-checkins@vmware.com> 2.12.0-1
- Automatic Version Bump
* Mon Oct 10 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.11.0-2
- Replace deprecated pycrypto with pycryptodome
* Wed Jun 01 2022 Gerrit Photon <photon-checkins@vmware.com> 2.11.0-1
- Automatic Version Bump
* Tue Apr 05 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.10.3-1
- Upgrade to v2.10.3
* Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 2.7.2-1
- Automatic Version Bump
* Wed Jul 08 2020 Tapas Kundu <tkundu@vmware.com> 2.7.1-2
- Mass removal python2
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 2.7.1-1
- Automatic Version Bump
* Wed Mar 06 2019 Tapas Kundu <tkundu@vmware.com> 2.4.2-2
- Added bcrypt and PyNaCl to requires.
* Thu Jan 10 2019 Siju Maliakkal <smaliakkal@vmware.com> 2.4.2-1
- Upgraded to 2.4.2 to mitigate CVE-2018-1000805
* Tue Sep 11 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.4.1-1
- Update version to 2.4.1
* Mon Apr 16 2018 Xiaolin Li <xiaolinl@vmware.com> 2.1.5-1
- Update version to 2.1.5 for CVE-2018-1000132
* Tue Jul 25 2017 Divya Thaluru <dthaluru@vmware.com> 2.1.2-5
- Fixed test command
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 2.1.2-4
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.1.2-3
- Use python2 explicitly while building
* Fri May 05 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.2-2
- Added missing requires python-cryptography
* Sat Apr 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.2-1
- Update to 2.1.2
* Mon Feb 27 2017 Xiaolin Li <xiaolinl@vmware.com> 1.16.0-4
- Added python3 site-packages.
* Fri Oct 07 2016 ChangLee <changlee@vmware.com> 1.16.0-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.16.0-2
- GA - Bump release of all rpms
* Tue Jan 5 2016 Xiaolin Li <xiaolinl@vmware.com> 1.16.0-1
- Initial build.  First version
