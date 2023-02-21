%define VER 6.1.0
Summary:        A Python-based command-line client for running simple CQL commands on a Cassandra cluster.
Name:           python3-cqlsh
Version:        6.1.0
Release:        1%{?dist}
License:        Apache License Version 2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/cqlsh
Source0:        https://files.pythonhosted.org/packages/source/c/cqlsh/cqlsh-%{VER}.tar.gz
%define sha512  cqlsh=4e045e9cf2ea8bc4d720eeabf23d0a215893bb0407d9c6f6c386798f74f7cc465fc38be39ee5abeb35578c7d23b685257f1499be47e88d116dac1acc374c81f4

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3
Requires:       python3-libs
Requires:       python3-cassandra-driver
Requires:       python3-cql
Requires:       python3-six
Requires:       cassandra

BuildArch:      noarch

Patch0: 0001-cqlshlib-Added-support-for-python-3.11.patch

%description
cqlsh is a Python-based command-line tool, and the most direct way to run simple CQL commonds on a Cassandra cluster.
This is a simple re-bundling of the open source tool that comes bundled with Cassandra to allow for cqlsh to be installed and run inside of virtual environments..

%prep
%autosetup -p1 -n cqlsh-%{VER}

%build
%py3_build

%install
%py3_install

%check
python3 setup.py check

%files
%defattr(-,root,root)
%{_bindir}/cqlsh
%{python3_sitelib}/*

%changelog
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
