Summary:       Netfilter conntrack userspace library
Name:          libnetfilter_conntrack
Version:       1.0.9
Release:       3%{?dist}
URL:           http://www.netfilter.org/projects/libnetfilter_conntrack/index.html
Group:         System Environment/Libraries
Vendor:        VMware, Inc.
Distribution:  Photon

Source0:       http://www.netfilter.org/projects/%{name}/files/%{name}-%{version}.tar.bz2
%define sha512 %{name}=e8b03425aaba3b72e6034c215656c34176d0550c08e0455aaeb1365d9141505d0c4feaa8978c8ccf2b7af9db6c9e874ceb866347e533b41cb03a189884f4004c

Source1: license.txt
%include %{SOURCE1}

BuildRequires: libmnl-devel
BuildRequires: libnfnetlink-devel
BuildRequires: linux-api-headers

Requires: libmnl
Requires: libnfnetlink

%description
libnetfilter_conntrack is a userspace library providing a programming
interface (API) to the in-kernel connection tracking state table.
The library libnetfilter_conntrack has been previously known as
libnfnetlink_conntrack and libctnetlink.

%package       devel
Summary:       Development files for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}
Requires:      libnfnetlink-devel
Requires:      linux-api-headers

%description   devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build

%install
%make_install %{?_smp_mflags}

%ldconfig_scriptlets

%files
%doc COPYING README
%{_libdir}/*.so.*

%files devel
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_libdir}/*.so

%changelog
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.0.9-3
- Release bump for SRP compliance
* Sun Aug 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.0.9-2
- Remove .la files
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.0.9-1
- Automatic Version Bump
* Wed Aug 04 2021 Susant Sahani <ssahani@vmware.com> 1.0.8-2
- Modernize spec file. Use ldconfig scriptlets and autosetup
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.0.8-1
- Automatic Version Bump
* Mon Sep 17 2018 Bo Gan <ganb@vmware.com> 1.0.7-1
- Update to 1.0.7
* Wed Apr 05 2017 Anish Swaminathan <anishs@vmware.com> 1.0.6-1
- Initial packaging.
