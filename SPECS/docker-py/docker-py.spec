Name:           docker-py3
Version:        6.0.0
Release:        3%{?dist}
Summary:        Python API for docker
License:        ASL2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/docker/docker-py

Source0: https://github.com/docker/docker-py/releases/download/%{version}/docker-%{version}.tar.gz
%define sha512 docker=09edf7b058d38d34d0fe0432b336d6fc494648c0e41cf4ae7f7bbf3db158143ca8fbea87e51d3b354c5f40bd7f1481e003e4b55f879ef562e91f19b62143c271

BuildRequires: python3-devel
BuildRequires: python3-ipaddress
BuildRequires: python3-pip
BuildRequires: python3-requests
BuildRequires: python3-setuptools
BuildRequires: python3-setuptools_scm
BuildRequires: python3-six
BuildRequires: python3-typing-extensions
BuildRequires: python3-xml
BuildRequires: python3-macros

%if 0%{?with_check}
BuildRequires: python3-pytest
BuildRequires: python3-websocket-client
BuildRequires: python3-paramiko
%endif

Requires: python3
Requires: docker-pycreds3
Requires: python3-backports.ssl_match_hostname
Requires: python3-ipaddress
Requires: python3-requests
Requires: python3-six
Requires: python3-websocket-client

BuildArch: noarch

%description
Python API for docker

%prep
%autosetup -p1 -n docker-%{version}

%build
%{py3_build}

%install
%{py3_install}

%if 0%{?with_check}
%check
%{pytest} tests/unit
%endif

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Tue Jun 04 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 6.0.0-3
- Add setuptools_scm and typing-extensions in BuildRequires
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 6.0.0-2
- Update release to compile with python 3.11
* Mon Oct 24 2022 Shreenidhi Shedi <sshedi@vmware.com> 6.0.0-1
- Upgrade to v6.0.0
* Thu Oct 15 2020 Ashwin H <ashwinh@vmware.com> 4.3.1-1
- Upgrade to 4.3.1 release.
* Mon Jun 15 2020 Tapas Kundu <tkundu@vmware.com> 3.5.0-2
- Mass removal python2
* Tue Sep 04 2018 Tapas Kundu <tkundu@vmware.com> 3.5.0-1
- Upgraded to 3.5.0 release.
* Fri Dec 01 2017 Xiaolin Li <xiaolinl@vmware.com> 2.3.0-3
- Added docker-pycreds3, python3-requests, python3-six,
- python3-websocket-client to requires of docker-py3
* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 2.3.0-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Sun Jun 04 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.3.0-1
- Initial version of docker-py for PhotonOS.
