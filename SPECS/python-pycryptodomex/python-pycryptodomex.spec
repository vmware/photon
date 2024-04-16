Summary:        Cryptographic library for Python
Name:           python3-pycryptodomex
Version:        3.20.0
Release:        1%{?dist}
License:        BSD and Public Domain
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.org/project/pycryptodomex
Source0: https://files.pythonhosted.org/packages/31/a4/b03a16637574312c1b54c55aedeed8a4cb7d101d44058d46a0e5706c63e1/pycryptodomex-%{version}.tar.gz
%define sha512 pycryptodomex=dd0f05338a209de26d93321d0709bdc9240c74768683c7decc572ee3a9a075bda95f527ae0d433e02a1674b6e12c4e7d35cc0ef721fb5e98fdb12878e047ebcd

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
%py3_install

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/Cryptodome
%{python3_sitelib}/pycryptodomex-%{version}-py%{python3_version}.egg-info
%exclude %{python3_sitearch}/Cryptodome/SelfTest

%changelog
* Mon Apr 15 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.20.0-1
- Update to 3.20.0, fixes CVE-2023-52323. Exclude SelfTest
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 3.15.0-1
- Update to 3.15.0
* Wed Feb 03 2021 Tapas Kundu <tkundu@vmware.com> 3.9.9-1
- Initial packaging for Photon
