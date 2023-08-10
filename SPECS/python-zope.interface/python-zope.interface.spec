%define srcname zope.interface

Name:           python3-zope.interface
Version:        5.2.0
Release:        2%{?dist}
Url:            https://github.com/zopefoundation/zope.interface
Summary:        Interfaces for Python
License:        ZPL 2.1
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://pypi.python.org/packages/source/z/zope.interface/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=64688b8a823d63fc78720ee15d59cc54c07a700dc45e46336cb23cd1a0a3eb998284a4d954d3fa08c7f26b35583c0284fb2fcd18f84f3133ce93f7c3ade0a988

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

%if 0%{?with_check}
BuildRequires: python3-pip
%endif

Requires:       python3
Requires:       python3-setuptools

%description
This package is intended to be independently reusable in any Python project.
It is maintained by the Zope Toolkit project.

This package provides an implementation of “object interfaces” for Python.
Interfaces are a mechanism for labeling objects as conforming to a given
API or contract. So, this package can be considered as implementation of
the Design By Contract methodology support in Python.

For detailed documentation, please visit http://docs.zope.org/zope.interface

%prep
%autosetup -n %{srcname}-%{version}

%build
%{py3_build}

%install
%{py3_install}

%if 0%{?with_check}
%check
pip3 install zope.testing
pushd %{buildroot}%{python3_sitelib}
PURE_PYTHON=1 %{python3} -m unittest discover -s zope/interface -t .
popd
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 5.2.0-2
- Bump up to compile with python 3.10
* Fri Nov 06 2020 Gerrit Photon <photon-checkins@vmware.com> 5.2.0-1
- Automatic Version Bump
* Wed Sep 30 2020 Gerrit Photon <photon-checkins@vmware.com> 5.1.2-1
- Automatic Version Bump
* Thu Sep 03 2020 Tapas Kundu <tkundu@vmware.com> 5.1.0-2
- Requires python3-setuptools for installation
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 5.1.0-1
- Automatic Version Bump
* Thu Jun 11 2020 Tapas Kundu <tkundu@vmware.com> 4.5.0-2
- Mass removal python2
* Fri Sep 14 2018 Tapas Kundu <tkundu@vmware.com> 4.5.0-1
- Updated to release 4.5.0
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 4.3.3-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Mon Mar 13 2017 Xiaolin Li <xiaolinl@vmware.com> 4.3.3-1
- Updated to version 4.3.3.
* Tue Oct 04 2016 ChangLee <changlee@vmware.com> 4.1.3-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.1.3-2
- GA - Bump release of all rpms
* Tue Oct 27 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging for Photon
