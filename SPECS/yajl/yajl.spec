Name:          yajl
Version:       2.1.0
Release:       3%{?dist}
Summary:       Yet Another JSON Library
Group:         Development/Libraries
Vendor:        VMware, Inc.
Distribution:  Photon
URL:           http://lloyd.github.com/yajl/
Source0:       https://github.com/lloyd/yajl/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 yajl=9e786d080803df80ec03a9c2f447501e6e8e433a6baf636824bc1d50ecf4f5f80d7dfb1d47958aeb0a30fe459bd0ef033d41bc6a79e1dc6e6b5eade930b19b02

Source1: license.txt
%include %{SOURCE1}
BuildRequires: gcc
BuildRequires: cmake

Patch0: 0001-CVE-2023-33460.patch
Patch1: 0002-CVE-2023-33460.patch

%package devel
Summary: Include files, Libraries for development with YAJL
Requires: %{name} = %{version}-%{release}

%description
A fast streaming JSON parsing library in C

%description devel
This sub-package  provides the libraries and includes
files which are required for development with YAJL

%prep
%autosetup -p1

%build
%cmake
%cmake_build

%install
%cmake_install

%files
%defattr(-,root,root)
%license COPYING
%doc ChangeLog README TODO
%{_bindir}/json_reformat
%{_bindir}/json_verify
%{_libdir}/libyajl.so.2
%{_libdir}/libyajl.so.2.*

%files devel
%defattr(-,root,root)
%{_includedir}/yajl/yajl_common.h
%{_includedir}/yajl/yajl_gen.h
%{_includedir}/yajl/yajl_parse.h
%{_includedir}/yajl/yajl_tree.h
%{_includedir}/yajl/yajl_version.h
%{_libdir}/libyajl.so
%{_libdir}/libyajl_s.a
%{_datadir}/pkgconfig/yajl.pc

%changelog
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 2.1.0-3
- Release bump for SRP compliance
* Tue Sep 12 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 2.1.0-2
- Apply two patches to fix CVE-2023-33460
* Fri May 27 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.1.0-1
- Initial Build
