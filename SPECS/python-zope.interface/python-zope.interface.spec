%define srcname zope.interface

Name:           python3-zope.interface
Version:        5.4.0
Release:        3%{?dist}
Url:            https://github.com/zopefoundation/zope.interface
Summary:        Interfaces for Python
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://pypi.python.org/packages/source/z/zope.interface/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=ef15d63397e05ad9fc44b2d5d786b0399b6973bb5f4866fab839ff612756f3157f2099d0f5c0469b574a5c8b5920a7c2a5c6eab8e8f84c24d5c43e816669bffe

Source1: license.txt
%include %{SOURCE1}

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
%autosetup -p1 -n %{srcname}-%{version}

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
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 5.4.0-3
- Release bump for SRP compliance
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 5.4.0-2
- Update release to compile with python 3.11
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 5.4.0-1
- Automatic Version Bump
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
