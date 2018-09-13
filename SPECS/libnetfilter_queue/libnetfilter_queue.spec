Summary:    Provides API to packets queued by kernel packet filter
Name:       libnetfilter_queue
Version:    1.0.3
Release:    1%{?dist}
License:    GPLv2
URL:        http://www.netfilter.org/projects/libnetfilter_queue/index.html
Group:      System Environment/Libraries
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    http://www.netfilter.org/projects/%{name}/files/%{name}-%{version}.tar.bz2
%define sha1 libnetfilter_queue=3d182e3211b633d0a0f8a2b12ef80dc2621f53cb

BuildRequires:  libmnl-devel
BuildRequires:  libnfnetlink-devel
BuildRequires:  linux-api-headers

%description
libnetfilter_queue is a userspace library providing an API to packets that have been queued by the kernel packet filter. It is is part of a system that deprecates the old ip_queue / libipq mechanism.
libnetfilter_queue has been previously known as libnfnetlink_queue.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       libnfnetlink-devel
Requires:       linux-api-headers

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
%configure --disable-static 
make %{?_smp_mflags}

%install
%make_install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING 
%{_libdir}/*.so.*

%files devel
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.la

%changelog
*   Mon Sep 17 2018 Bo Gan <ganb@vmware.com> 1.0.3-1
-   Update to 1.0.3
*   Wed Apr 05 2017 Anish Swaminathan <anishs@vmware.com> 1.0.2-1
-   Initial packaging



