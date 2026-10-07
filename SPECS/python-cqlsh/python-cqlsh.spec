%global build_if %{photon_subrelease} >= 92

%define srcname cqlsh

Summary:        A Python-based command-line client for running simple CQL commands on a Cassandra cluster.
Name:           python3-cqlsh
Version:        6.2.1
Release:        1%{?dist}
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/cqlsh

Source0: https://github.com/jeffwidman/cqlsh/archive/refs/tags/%{version}.tar.gz#/%{srcname}-%{version}.tar.gz
Patch0: 0001-pyproject-Drop-the-pure-sasl-dependency.patch

Source1: license.txt
%include %{SOURCE1}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-build
BuildRequires: python3-installer
BuildRequires: python3-packaging
BuildRequires: python3-wheel

Requires: python3
Requires: cassandra
Requires: python3-cassandra-driver
Requires: python3-wcwidth

BuildArch: noarch

%description
cqlsh is a Python-based command-line tool, and the most direct way to run simple CQL commonds on a Cassandra cluster.
This is a simple re-bundling of the open source tool that comes bundled with Cassandra to allow for cqlsh to be installed and run inside of virtual environments..

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%py3_build_wheel

%install
%py3_install_wheel
%{py_byte_compile_and_ghost}

%files -f %{py_ghost_filelist}
%defattr(-,root,root)
%{_bindir}/%{srcname}
%{python3_sitelib}/*

%changelog
* Tue Oct 13 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 6.2.1-1
- Upgrade to 6.2.1
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 6.1.2-4
- Extended to build for subrelease 91 and above
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 6.1.2-3
- Bump version as a part of python3.14 upgrade
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 6.1.2-2
- Release bump for SRP compliance
* Sat Aug 05 2023 Shreenidhi Shedi <sshedi@vmware.com> 6.1.2-1
- Upgrade to v6.1.2
- Remove python3-cql dependency
* Tue Feb 21 2023 Ankit Jain <ankitja@vmware.com> 6.1.0-1
- Update to 6.1.0
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 6.0.0-1
- Automatic Version Bump
* Thu Nov 11 2021 Shreenidhi Shedi <sshedi@vmware.com> 6.0.0ga-1
- Update to 6.0.0
* Wed Jun 09 2021 Ankit Jain <ankitja@vmware.com> 6.0.0b4-1
- Update to 6.0.0b4 to support python3
* Mon Jul 10 2017 Xiaolin Li <xiaolinl@vmware.com> 5.0.4-1
- Initial packaging for Photon
