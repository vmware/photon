Summary:        Cryptographic library for Python
Name:           python3-pycryptodomex
Version:        3.15.0
Release:        1%{?dist}
License:        BSD and Public Domain
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.org/project/pycryptodomex
Source0:        pycryptodomex-%{version}.tar.gz
%define sha512	pycryptodomex=7d76e4997055506f378ef5662f073bcfa561202f4a70792b5fd3a476f0ee7007e2fb0e45631f2963f234c16097544a36f316bbb8ecff3bcded411a8515f34d9d

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-sphinx

Requires:  python3-sphinx
Requires:  python3-libs
Requires:  python3
Requires:  python3-setuptools

%description
Cryptographic library for Python

%prep
%autosetup -n pycryptodomex-%{version}

%build
%py3_build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot} --skip-build

%files
%defattr(-,root,root,-)
%{python3_sitelib}/Cryptodome
%{python3_sitelib}/pycryptodomex-%{version}-py%{python3_version}.egg-info

%changelog
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.15.0-1
- Update to 3.15.0
* Wed Feb 03 2021 Tapas Kundu <tkundu@vmware.com> 3.9.9-1
- Initial packaging for Photon
