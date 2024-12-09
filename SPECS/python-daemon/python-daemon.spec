%define srcname python-daemon

Summary:        Library to implement a well-behaved Unix daemon process.
Name:           python3-daemon
Version:        2.3.2
Release:        2%{?dist}
URL:            https://pypi.org/project/python-daemon
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://files.pythonhosted.org/packages/source/p/python-daemon/python-daemon-%{version}.tar.gz
%define sha512 %{srcname}=d9f6e6c376a496fae96bd9efed0a56d00a137617a3d1d5ef74802ef176bc813bb1d49bbb9164cdbec03213529f944b32b257bcc64283abfa4a3522ff00826bfd

Source1: license.txt
%include %{SOURCE1}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-docutils
BuildRequires: python3-lockfile
BuildRequires: python3-xml
BuildRequires: curl-devel
BuildRequires: libffi-devel

%if 0%{?with_check}
BuildRequires: python3-pip
%endif

Requires: libffi
Requires: python3
Requires: python3-lockfile

BuildArch: noarch

%description
This library implements the well-behaved daemon specification of PEP 3143, “Standard daemon process library”.

A well-behaved Unix daemon process is tricky to get right, but the required steps are much the same for every daemon program. A DaemonContext instance holds the behaviour and configured process environment for the program; use the instance as a context manager to enter a daemon state.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
export PYTHONPATH=%{buildroot}%{python3_sitelib}
%{python3} -m setup test --quiet
%endif

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 2.3.2-2
- Release bump for SRP compliance
* Sat Nov 19 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.3.2-1
- Upgrade to v2.3.2
* Tue May 10 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.2.4-3
- Bump version as a part of libffi upgrade
* Thu Aug 13 2020 Shreenidhi Shedi <sshedi@vmware.com> 2.2.4-2
- Added libffi to BuildRequires
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2.2.4-1
- Automatic Version Bump
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 2.2.0-3
- Mass removal python2
* Wed Dec 19 2018 Tapas Kundu <tkundu@vmware.com> 2.2.0-2
- Fix makecheck
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 2.2.0-1
- Updated to 2.2.0
* Mon Jul 17 2017 Divya Thaluru <dthaluru@vmware.com> 2.1.2-4
- Fixed check command to run unit tests
- Added packages required to run tests
- Added missing runtime dependent packages
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 2.1.2-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.1.2-2
- Corrected an error in command
* Fri Mar 24 2017 Xiaolin Li <xiaolinl@vmware.com> 2.1.2-1
- Initial packaging for Photon
