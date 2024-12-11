Name:           python3-mock
Version:        4.0.3
Release:        3%{?dist}
Summary:        Rolling backport of unittest.mock for all Pythons
Group:          Development/Languages/Python
Url:            https://files.pythonhosted.org/packages/e2/be/3ea39a8fd4ed3f9a25aae18a1bff2df7a610bca93c8ede7475e32d8b73a0/mock-4.0.3.tar.gz
Source0:        mock-%{version}.tar.gz
%define sha512  mock=aa4275344a40fd3eea75c1c305f82dd6a561d2a4584b7acd0a85f3a9b34d0cfd1722770d74ae26c04d871d844a3189186d7f087017ddf850d6c378cc98676ea5

Source1: license.txt
%include %{SOURCE1}
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
Requires:       python3
Requires:       python3-libs
Requires:       python3-setuptools
BuildArch:      noarch
Provides:       python%{python3_version}dist(mock)

%description
mock is a library for testing in Python. It allows you to replace parts of your system under test with mock objects and make assertions about how they have been used.
mock is now part of the Python standard library, available as unittest.mock in Python 3.3 onwards.
This package contains a rolling backport of the standard library mock code compatible with Python 3.6 and up.

%prep
%autosetup -n mock-%{version}

%build
%py3_build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot} --skip-build
find %{buildroot}%{_libdir} -name '*.pyc' -delete

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 4.0.3-3
- Release bump for SRP compliance
* Mon Oct 31 2022 Prashant S Chauhan <psinghchauha@vmware.com> 4.0.3-2
- Update release to compile with python 3.11
* Wed Jul 21 2021 Tapas Kundu <tkundu@vmware.com> 4.0.3-1
- Initial packaging for python3-mock
