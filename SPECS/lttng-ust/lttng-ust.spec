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

%package devel
Summary:    The libraries and header files needed for LTTng-UST development.
Requires:   %{name} = %{version}-%{release}

%description devel
The libraries and header files needed for LTTng-UST development.

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
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_datadir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/lttng-ust*.pc

%changelog
*	Mon Dec 19 2016 Dheeraj Shetty <dheerajs@vmware.com> 2.9.0-1
-   	Initial build.  First version
