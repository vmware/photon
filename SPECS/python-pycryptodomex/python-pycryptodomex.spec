Summary:        Cryptographic library for Python
Name:           python3-pycryptodomex
Version:        3.9.9
Release:        3%{?dist}
License:        BSD and Public Domain
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://pypi.org/project/pycryptodomex

Source0: pycryptodomex-%{version}.tar.gz
%define sha512 pycryptodomex=68a59cd537c1745db0082979716f0ba0508bb9d82d7129d42931056b5927f27ada1b92f88cc7c4d3954a02cd724a88c0e60fa38a5d8d7c73baa6541d332ff8a9

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
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot} --skip-build

%files
%defattr(-,root,root,-)
%{python3_sitelib}/Cryptodome
%{python3_sitelib}/pycryptodomex-3.9.9-py%{python3_version}.egg-info

%changelog
* Mon Jan 08 2024 Nitesh Kumar <kunitesh@vmware.com> 3.9.9-3
- Version bump up as a part of python3-sphinx upgrade v5.1.1
* Mon Nov 15 2021 Prashant S Chauhan <psinghchauha@vmware.com> 3.9.9-2
- Update release to compile with python 3.10
* Wed Feb 03 2021 Tapas Kundu <tkundu@vmware.com> 3.9.9-1
- Initial packaging for Photon
