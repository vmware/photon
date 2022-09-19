Summary:        ECDSA cryptographic signature library (pure python)
Name:           python3-ecdsa
Version:        0.17.0
Release:        2%{?dist}
License:        MIT
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://pypi.python.org/pypi/ecdsa
Source0:        https://pypi.python.org/packages/source/e/ecdsa/ecdsa-%{version}.tar.gz
%define         sha512 ecdsa=23acf993ce4f7f832674a3b70ab870c20172816e27adc836d4c6a876e72a488a830895d63ab6af67cc7cbc83c71f7097d0d530bf67d24c84e69e9fa87031f6fd
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3

%description
This is an easy-to-use implementation of ECDSA cryptography (Elliptic Curve
Digital Signature Algorithm), implemented purely in Python, released under
the MIT license. With this library, you can quickly create keypairs (signing
key and verifying key), sign messages, and verify the signatures. The keys
and signatures are very short, making them easy to handle and incorporate
into other protocols.

%prep
%autosetup -n ecdsa-%{version}

%build
%py3_build

%install
%{__rm} -rf %{buildroot}
python3 setup.py install -O1 --skip-build \
    --root "%{buildroot}" \
    --single-version-externally-managed

%check
python3 setup.py test

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root,-)
%{python3_sitelib}/*

%changelog
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 0.17.0-2
- Update release to compile with python 3.11
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 0.17.0-1
- Automatic Version Bump
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 0.16.1-1
- Automatic Version Bump
* Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 0.16.0-1
- Automatic Version Bump
* Wed Jul 08 2020 Tapas Kundu <tkundu@vmware.com> 0.15-2
- Mass removal python2
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 0.15-1
- Automatic Version Bump
* Mon Jun 19 2017 Xiaolin Li <xiaolinl@vmware.com> 0.13-5
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.13-4
- Use python2 explicitly
* Mon Feb 27 2017 Xiaolin Li <xiaolinl@vmware.com> 0.13-3
- Added python3 site-packages.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.13-2
- GA - Bump release of all rpms
* Tue Jan 5 2016 Xiaolin Li <xiaolinl@vmware.com> 0.13-1
- Initial build.  First version.
