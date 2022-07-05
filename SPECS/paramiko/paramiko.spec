Summary:        Python SSH module
Name:           python3-paramiko
Version:        2.10.3
Release:        1%{?dist}
License:        LGPL
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://www.paramiko.org

Source0:        https://github.com/paramiko/paramiko/archive/paramiko-%{version}.tar.gz
%define         sha1 paramiko=dd2481e15187cfc56d4ba6848b43fd8fbb4917fa

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-ecdsa > 0.11
BuildRequires:  python3-pycrypto > 2.1
BuildRequires:  python3-cryptography
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

Requires:       python3
Requires:       python3-pycrypto > 2.1
Requires:       python3-ecdsa > 0.11
Requires:       python3-cryptography
Requires:       python3-PyNaCl
Requires:       python3-bcrypt

%description
"Paramiko" is a combination of the esperanto words for "paranoid" and "friend". It's a module for Python 2.6+ that implements the SSH2 protocol for secure (encrypted and authenticated) connections to remote machines. Unlike SSL (aka TLS), SSH2 protocol does not require hierarchical certificates signed by a powerful central authority.

%prep
%autosetup -p1 -n paramiko-%{version}

%build
%{py3_build}

%install
rm -rf %{buildroot}
python3 setup.py install -O1 --skip-build \
    --root "%{buildroot}" \
    --single-version-externally-managed

%check
%if 0%{?with_check}
LANG=en_US.UTF-8 python3 test.py
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%{python3_sitelib}/*

%changelog
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
