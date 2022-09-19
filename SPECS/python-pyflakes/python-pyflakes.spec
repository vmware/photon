Name:           python3-pyflakes
Version:        2.5.0
Release:        2%{?dist}
Summary:        A simple program which checks Python source files for errors
License:        MIT
Group:          Development/Languages/Python
Url:            https://github.com/PyCQA/pyflakes/archive/refs/tags/%{version}.tar.gz
Source0:        pyflakes-%{version}.tar.gz
%define sha512  pyflakes=e47303c4b445e0c010dfc96244b6fa991bd1870072c61cc7acd309947af3d81581276b012b56b7db0d8df3f91a4216a5ec502720c149f5707d5d1d28654aeeb4
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python3
Requires:       python3-libs
Requires:       python3-setuptools
BuildArch:      noarch

%description
Pyflakes is similar to PyChecker in scope, but differs in that it does
not execute the modules to check them. This is both safer and faster,
although it does not perform as many checks. Unlike PyLint, Pyflakes
checks only for logical errors in programs; it does not perform any
check on style.

%prep
%autosetup -n pyflakes-%{version}

%build
%py3_build

%install
%py3_install
find %{buildroot}%{_libdir} -name '*.pyc' -delete

%check
python3 setup.py test

%files
%defattr(-,root,root,-)
%{_bindir}/pyflakes
%{python3_sitelib}/*

%changelog
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.5.0-2
- Update release to compile with python 3.11
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 2.5.0-1
- Automatic Version Bump
* Fri Jul 09 2021 Tapas Kundu <tkundu@vmware.com> 2.3.1-1
- Initial packaging for python3-pyflakes
