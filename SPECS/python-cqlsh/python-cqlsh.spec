%define VER 6.0.0
Summary:        A Python-based command-line client for running simple CQL commands on a Cassandra cluster.
Name:           python3-cqlsh
# Note: "ga" is added to version because previous version was
# 6.0.0b4 so tdnf update/install considers 6.0.0b4 as latest version
# Thus, to overcome this appended "ga" at the end 6.0.0 to make it latest one
# Once next version > 6.0.0 is available then we can remove "ga"
Version:        6.0.0
Release:        1%{?dist}
License:        Apache License Version 2.0
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/cqlsh
Source0:        https://files.pythonhosted.org/packages/source/c/cqlsh/cqlsh-%{VER}.tar.gz
%define sha512  cqlsh=762f9fb17d2a0123ae01df7898d9fa912a211a9283649035ba1e21b8ce0fc348a4520c89a9073821127e86261f457edb127a436cc2594308f082e7c25eae8f9b

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
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 6.0.0-1
- Automatic Version Bump
* Thu Nov 11 2021 Shreenidhi Shedi <sshedi@vmware.com> 6.0.0ga-1
- Update to 6.0.0
* Wed Jun 09 2021 Ankit Jain <ankitja@vmware.com> 6.0.0b4-1
- Update to 6.0.0b4 to support python3
* Mon Jul 10 2017 Xiaolin Li <xiaolinl@vmware.com> 5.0.4-1
- Initial packaging for Photon
