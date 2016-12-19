Summary: LTTng-UST is an Userspace Tracer library
Name:    lttng-ust
Version: 2.9.0
Release: 1%{?dist}
License: GPLv2 and LGPLv2
URL: https://lttng.org/download/
Source: https://lttng.org/files/lttng-ust/%{name}-%{version}.tar.bz2
%define sha1 lttng-ust=9937eae64540821b8597cce081e92be76e6b5568
Group:      Development/Libraries
Vendor:     VMware, Inc.
Distribution:  Photon

BuildRequires: userspace-rcu-devel
Requires:      userspace-rcu
%description
This library may be used by user-space applications to generate 
trace-points using LTTng.

%prep
%setup -q

%build
./configure \
	--prefix=%{_prefix} \
	--docdir=%{_docdir}/%{name} \
	--disable-static

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
rm -vf %{buildroot}%{_libdir}/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*.so*
%{_libdir}/pkgconfig/lttng-ust*.pc
%{_datadir}/*

%changelog
*	Mon Dec 19 2016 Dheeraj Shetty <dheerajs@vmware.com> 2.9.0-1
-   	Initial build.  First version
