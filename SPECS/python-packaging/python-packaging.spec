Summary:        Core utilities for Python packages
Name:           python3-packaging
Version:        21.3
Release:        2%{?dist}
Url:            https://pypi.python.org/pypi/packaging
License:        BSD or ASL 2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: pypi.python.org/packages/source/p/packaging/packaging-%{version}.tar.gz
%define sha512 packaging=2e3aa276a4229ac7dc0654d586799473ced9761a83aa4159660d37ae1a2a8f30e987248dd0e260e2834106b589f259a57ce9936eef0dcc3c430a99ac6b663e05

BuildRequires:  python3-devel
%if 0%{?with_check}
BuildRequires:  python3-setuptools
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-xml
BuildRequires:  python3-pyparsing
BuildRequires:  python3-six
%endif

Requires:       python3
Requires:       python3-pyparsing
Requires:       python3-six

BuildArch:      noarch

Provides: python%{python3_version}dist(packaging)

%description
Cryptography is a Python library which exposes cryptographic recipes and primitives.

%prep
%autosetup -n packaging-%{version}

%build
%py3_build

%install
%py3_install

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 21.3-2
- Bump version as a part of openssl upgrade
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 21.3-1
- Update to 21.3
* Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 20.4-3
- Fix build with new rpm
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 20.4-2
- openssl 1.1.1
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 20.4-1
- Automatic Version Bump
* Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 17.1-3
- Mass removal python2
* Fri Dec 07 2018 Tapas Kundu <tkundu@vmware.com> 17.1-2
- Fix makecheck
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 17.1-1
- Update to version 17.1
* Wed Jul 26 2017 Divya Thaluru <dthaluru@vmware.com> 16.8-4
- Fixed rpm check errors
- Fixed runtime dependencies
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 16.8-3
- Fix arch
* Wed Apr 05 2017 Sarah Choi <sarahc@vmware.com> 16.8-2
- Remove python-setuptools from BuildRequires
* Tue Apr 04 2017 Xiaolin Li <xiaolinl@vmware.com> 16.8-1
- Initial packaging for Photon
