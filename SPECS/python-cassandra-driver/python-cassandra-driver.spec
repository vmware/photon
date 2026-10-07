%global build_if %{photon_subrelease} >= 92

%define srcname cassandra-driver

Summary:        A modern, feature-rich and highly-tunable Python client library for Apache Cassandra (2.1+)
Name:           python3-cassandra-driver
Version:        3.29.3
Release:        1%{?dist}
Url:            https://github.com/apache/cassandra-python-driver
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/apache/cassandra-python-driver/archive/refs/tags/%{version}.tar.gz#/%{srcname}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-build
BuildRequires: python3-installer
BuildRequires: python3-packaging
BuildRequires: libev-devel

Requires: libev
Requires: python3
Requires: python3-geomet >= 1.1.0

%description
A modern, feature-rich and highly-tunable Python client library for Apache Cassandra (2.1+)
using exclusively Cassandra's binary protocol and Cassandra Query Language v3. The driver
supports Python 3.3, 3.4, 3.5, and 3.6.

%prep
%autosetup -p1 -n cassandra-python-driver-%{version}

%build
export CASS_DRIVER_NO_CYTHON=1
%py3_build_wheel

%install
%py3_install_wheel
%{py_byte_compile_and_ghost}

%files -f %{py_ghost_filelist}
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Wed Oct 07 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.29.3-1
- Upgrade to 3.29.3
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 3.25.0-4
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.25.0-3
- Bump version as a part of python3.14 upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.25.0-2
- Release bump for SRP compliance
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 3.25.0-1
- Automatic Version Bump
* Fri Jun 11 2021 Ankit Jain <ankitja@vmware.com> 3.24.0-4
- Fixed install time dependency
* Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 3.24.0-3
- Fix build with new rpm
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.24.0-2
- openssl 1.1.1
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 3.24.0-1
- Automatic Version Bump
* Tue Jun 16 2020 Tapas Kundu <tkundu@vmware.com> 3.15.1-3
- Mass removal python2
* Wed Dec 12 2018 Tapas Kundu <tkundu@vmware.com> 3.15.1-2
- Fix make check
* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 3.15.1-1
- Update to version 3.15.1
* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 3.10.0-5
- Remove BuildArch
* Tue Sep 12 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.10.0-4
- Do make check for python3 subpackage
* Wed Aug 16 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.10.0-3
- Fix make check.
* Tue Jun 20 2017 Xiaolin Li <xiaolinl@vmware.com> 3.10.0-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
* Thu Jun 15 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.10.0-1
- Initial packaging for Photon
