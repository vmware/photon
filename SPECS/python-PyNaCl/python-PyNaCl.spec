Name:           python3-PyNaCl
Version:        1.5.0
Release:        3%{?dist}
Summary:        PyNaCl is a Python binding to libsodium
Group:          Development/Languages/Python
Url:            https://pypi.org/project/PyNaCl
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://pypi.python.org/packages/source/e/PyNaCl/PyNaCl-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-cffi
BuildRequires:  python3-xml
BuildRequires:  curl-devel
Requires:       python3
Requires:       python3-libs

%description
Good password hashing for your software and your servers.

%prep
%autosetup -n PyNaCl-%{version}

%build
%py3_build

%install
%py3_install

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.5.0-3
- Release bump for SRP compliance
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.5.0-2
- Update release to compile with python 3.11
* Fri Oct 21 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.5.0-1
- Upgrade to latest version
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 1.4.0-1
- Automatic Version Bump
* Fri Jun 19 2020 Tapas Kundu <tkundu@vmware.com> 1.3.0-2
- Mass removal python2
* Wed Mar 06 2019 Tapas Kundu <tkundu@vmware.com> 1.3.0-1
- Initial packaging for Photon
