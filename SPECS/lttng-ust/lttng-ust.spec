Summary: LTTng-UST is an Userspace Tracer library
Name:    lttng-ust
Version: 2.10.2
Release: 2%{?dist}
License: GPLv2, LGPLv2.1 and MIT
URL: https://lttng.org/download/
Source: https://lttng.org/files/lttng-ust/%{name}-%{version}.tar.bz2
%define sha1 lttng-ust=b92d789c7277362715a6a9557f65f7e6066d8130
Group:      Development/Libraries
Vendor:     VMware, Inc.
Distribution:  Photon

BuildRequires: userspace-rcu-devel
%if %{with_check}
BuildRequires: perl
%endif
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

%check
make %{?_smp_mflags} check

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
*       Wed Jan 02 2019 Keerthana K <keerthanak@vmware.com> 2.10.2-2
-       Added make check.
*	Wed Sep 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 2.10.2-1
-	Update to version 2.10.2
*	Mon Dec 19 2016 Dheeraj Shetty <dheerajs@vmware.com> 2.9.0-1
-   	Initial build.  First version
