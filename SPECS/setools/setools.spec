%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Policy analysis tools for SELinux
Name:           setools
Version:        4.3.0
Release:        1%{?dist}
License:        GPLv2, LGPLv2.1
Group:          System Environment/Libraries
Source0:        https://github.com/SELinuxProject/setools/releases/download/%{version}/%{name}-%{version}.tar.bz2
%define sha1    setools=75ffc1724707b8bc4eb90b118cd29161c43fe568
Url:            https://github.com/SELinuxProject/selinux/wiki
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  cython3
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  libselinux-devel
Requires:       python3
Requires:       libselinux
Requires:       libsepol
# setools use networkx library, which we do not have.
# It can be installed by: pip3 install networkx
#Requires:       networkx

%description
Policy analysis tools for SELinux

%prep
%setup -qn %{name}
sed -i "s/, 'networkx>=2.0'//" setup.py

%build
python3 setup.py build_ext
python3 setup.py build

%install
python3 setup.py install --root %{buildroot}
# do not package ru man pages
rm -rf %{buildroot}%{_mandir}/ru

%files
%defattr(-,root,root,-)
%{_bindir}/sesearch
%{_bindir}/apol
%{_bindir}/seinfoflow
%{_bindir}/sedta
%{_bindir}/seinfo
%{_bindir}/sediff
%{python3_sitelib}/*
%{_mandir}/man1/*

%changelog
* Fri May 01 2020 Alexey Makhalov <amakhalov@vmware.com> 4.3.0-1
- Initial build.
