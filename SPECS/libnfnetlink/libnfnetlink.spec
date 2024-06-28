Summary:       Library for netfilter related kernel/userspace communication
Name:          libnfnetlink
Version:       1.0.2
Release:       1%{?dist}
License:       GPLv2+
URL:           http://www.netfilter.org/projects/libnfnetlink/index.html
Group:         System Environment/Libraries
Vendor:        VMware, Inc.
Distribution:  Photon
Source0:       http://www.netfilter.org/projects/%{name}/files/%{name}-%{version}.tar.bz2
%define sha512 libnfnetlink=a5e9ae22831f1d17703f83953f3b0ef898e8b3fa7f0f771b038db51816ddae3158574380ac4d45c09fb8fbb8677e2ccdcc5c4736e3b09de06eac99f899130854

BuildRequires: linux-api-headers

%description
libnfnetlink is the low-level library for netfilter related kernel/userspace
communication. It provides a generic messaging infrastructure for in-kernel
netfilter subsystems (such as nfnetlink_log, nfnetlink_queue, nfnetlink_conntrack)
and their respective users and/or management tools in userspace.

%package       devel
Summary:       Development files for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}
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
find %{buildroot} -type f -name '*.la' -exec rm -f {} ';'

%ldconfig_scriptlets

%files
%doc COPYING README
%{_libdir}/*.so.*

%files devel
%{_libdir}/pkgconfig/*.pc
%dir %{_includedir}/libnfnetlink
%{_includedir}/libnfnetlink/*.h
%{_libdir}/*.so

%changelog
*   Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.0.2-1
-   Automatic Version Bump
*   Wed Aug 04 2021 Susant Sahani <ssahani@vmware.com> 1.0.1-2
-   Moderize spec files. Use ldconfig scriptlets and autosetup
*   Wed Apr 05 2017 Anish Swaminathan <anishs@vmware.com> 1.0.1-1
-   Initial packaging.
