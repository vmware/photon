Summary:        ECDSA cryptographic signature library (pure python)
Name:           python3-ecdsa
Version:        0.18.0
Release:        2%{?dist}
License:        MIT
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://pypi.python.org/pypi/ecdsa
Source0:        https://pypi.python.org/packages/source/e/ecdsa/ecdsa-%{version}.tar.gz
%define         sha512 ecdsa=f26dbeccd8e6ec832405d419b7244ca97b43a2811513493913a4f2f2fd1d2f453068fe0ba7b90b972f42a0d7b9834212fbd4d4559475cffeb1d80075fa954d78
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3

%if 0%{?with_check}
BuildRequires: python3-pip
BuildRequires: python3-pytest
BuildRequires: openssl
%endif

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
python3 setup.py install -O1 --skip-build \
    --root "%{buildroot}" \
    --single-version-externally-managed

%if 0%{?with_check}
%check
pip3 install --ignore-installed tox hypothesis
tox -e coverage
%endif

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root,-)
%{python3_sitelib}/*

%changelog
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.18.0-2
- Bump version as a part of openssl upgrade
* Tue Dec 13 2022 Gerrit Photon <photon-checkins@vmware.com> 0.18.0-1
- Automatic Version Bump.
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
