%define debug_package %{nil}

Name:           python3-subprocess32
Version:        3.5.4
Release:        2%{?dist}
Summary:        A backport of the subprocess module from Python 3.2/3.3 for use on 2.x
License:        PSF
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/subprocess32
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: subprocess32-%{version}.tar.gz
%define sha512 subprocess32=c811bdb5842d9f5ed9e51df4d13ba39045fbe98ca6e90a2c8138e68e44c2a55a2f0f3eb3e77e26caa3f88c360584912b001a0ca37ba68ac6c946c68c7a37d29a

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%if 0%{?with_check}
BuildRequires:  python3-test
BuildRequires:  python3-pytest
%endif

Requires:       python3
Requires:       python3-setuptools

%description
A backport of the subprocess module from Python 3.2/3.3 for use on 2.x

%prep
%autosetup -p1 -n subprocess32-%{version}

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
PYTHONPATH=build/lib.linux-%{_arch}-%{python3_version} python3 test_subprocess32.py
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 3.5.4-2
- Fix build with new rpm
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 3.5.4-1
- Automatic Version Bump
* Wed Jun 17 2020 Tapas Kundu <tkundu@vmware.com> 3.5.2-3
- Mass removal python2
* Tue Jan 08 2019 Alexey Makhalov <amakhalov@vmware.com> 3.5.2-2
- Added BuildRequires python2-devel
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 3.5.2-1
- Update to version 3.5.2
* Mon Sep 25 2017 Rui Gu <ruig@vmware.com> 3.2.7-2
- Fix make check failure.
* Fri Aug 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.2.7-1
- Initial version of python-subprocess32 package for Photon.
