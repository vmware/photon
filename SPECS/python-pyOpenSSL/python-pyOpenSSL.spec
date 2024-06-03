Summary:        Python wrapper module around the OpenSSL library
Name:           python3-pyOpenSSL
Version:        24.1.0
Release:        1%{?dist}
Url:            https://github.com/pyca/pyopenssl
License:        ASL 2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://files.pythonhosted.org/packages/source/p/pyOpenSSL/pyOpenSSL-%{version}.tar.gz
%define sha512 pyOpenSSL=acb07025f085d2fe9338e5ce5f65937001b1a8376c41ac532e9b0548668ce05c844e3e28c58efad812a034becf8e24aa9504165ff6af4c3b085cf463fa4d2fb6

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
%if 0%{?with_check}
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  python3-cryptography
BuildRequires:  python3-six
BuildRequires:  python3-pycparser
BuildRequires:  python3-cffi
BuildRequires:  python3-idna
BuildRequires:  python3-pyasn1
BuildRequires:  python3-six
BuildRequires:  python3-packaging
BuildRequires:  python3-asn1crypto
BuildRequires:  python3-pytest
%endif

Requires:       python3
Requires:       python3-cryptography
Requires:       python3-six

BuildArch:      noarch

%description
High-level wrapper around a subset of the OpenSSL library.

%prep
%autosetup -n pyOpenSSL-%{version}

%build
%{pyproject_wheel}

%install
%{pyproject_install}

%check
pip3 install pretend flaky tomli
%pytest

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Mon Jun 03 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 24.1.0-1
- Upgrade to v24.1.0
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 22.0.0-3
- Bump version as a part of openssl upgrade
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 22.0.0-2
- Update release to compile with python 3.11
* Tue Nov 29 2022 Ankit Jain <ankitja@vmware.com> 22.0.0-1
- Downgraded to version 22.0.0 due to an upstream issue #1154
* Mon Nov 07 2022 Prashant S Chauhan <psinghchauha@vmware.com> 22.1.0-1
- Update to 22.1.0
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 19.1.0-2
- openssl 1.1.1
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 19.1.0-1
- Automatic Version Bump
* Mon Jun 15 2020 Tapas Kundu <tkundu@vmware.com> 18.0.0-4
- Mass removal python2
* Mon Sep 09 2019 Tapas Kundu <tkundu@vmware.com> 18.0.0-3
- Fix make check
* Fri Jan 11 2019 Tapas Kundu <tkundu@vmware.com> 18.0.0-2
- Fix makecheck
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 18.0.0-1
- Update to version 18.0.0
* Thu Jun 14 2018 Tapas Kundu <tkundu@vmware.com> 17.2.0-2
- Added memory fix for X509StoreContext Class.
* Mon Aug 14 2017 Xiaolin Li <xiaolinl@vmware.com> 17.2.0-1
- Updated to version 17.2.0 and fixed make check.
* Fri Jul 21 2017 Divya Thaluru <dthaluru@vmware.com> 16.2.0-5
- Fixed runtime dependencies
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 16.2.0-4
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 16.2.0-3
- Use python2 explicitly
* Tue Feb 21 2017 Xiaolin Li <xiaolinl@vmware.com> 16.2.0-2
- Add Requires for python-enum and python-ipaddress
* Tue Feb 14 2017 Xiaolin Li <xiaolinl@vmware.com> 16.2.0-1
- Initial packaging for Photon
