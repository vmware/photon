Summary:       Netfilter conntrack userspace library
Name:          libnetfilter_conntrack
Version:       1.0.9
Release:       1%{?dist}
License:       GPLv2+
URL:           http://www.netfilter.org/projects/libnetfilter_conntrack/index.html
Group:         System Environment/Libraries
Vendor:        VMware, Inc.
Distribution:  Photon
Source0:       http://www.netfilter.org/projects/%{name}/files/%{name}-%{version}.tar.bz2
%define sha512 libnetfilter_conntrack=e8b03425aaba3b72e6034c215656c34176d0550c08e0455aaeb1365d9141505d0c4feaa8978c8ccf2b7af9db6c9e874ceb866347e533b41cb03a189884f4004c

BuildRequires: libmnl-devel
BuildRequires: libnfnetlink-devel
BuildRequires: linux-api-headers

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
%autosetup

%build
%configure --disable-static
make %{?_smp_mflags}

%install
%make_install

%ldconfig_scriptlets

%files
%doc COPYING README
%{_libdir}/*.so.*

%files devel
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.la

%changelog
*   Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.0.9-1
-   Automatic Version Bump
*   Wed Aug 04 2021 Susant Sahani <ssahani@vmware.com> 1.0.8-2
-   Modernize spec file. Use ldconfig scriptlets and autosetup
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.0.8-1
-   Automatic Version Bump
*   Mon Sep 17 2018 Bo Gan <ganb@vmware.com> 1.0.7-1
-   Update to 1.0.7
*   Wed Apr 05 2017 Anish Swaminathan <anishs@vmware.com> 1.0.6-1
-   Initial packaging.
