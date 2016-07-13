Summary:	An Event notification library.
Name:		libevent
Version:	2.0.22
Release:	3%{?dist}
License:	BSD
URL:		http://libevent.org
Source0:        https://github.com/libevent/libevent/releases/download/release-2.0.22-stable/%{name}-%{version}-stable.tar.gz
%define sha1 libevent=a586882bc93a208318c70fc7077ed8fca9862864
Group:		System/Library
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:  pkg-config
BuildRequires:  openssl-devel
Requires:       openssl

%description
The libevent API provides a mechanism to execute a callback function when a specific event 
occurs on a file descriptor or after a timeout has been reached. Furthermore, libevent also 
support callbacks due to signals or regular timeouts.

%package        devel
Summary:        Development files for libevent
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The subpackage includes all development related headers and library.

%prep
%setup -q -n %{name}-%{version}-stable

%build
%configure --disable-static --disable-libevent-regress
make %{?_smp_mflags}

%install
%makeinstall

%post -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_bindir}/event_rpcgen.py
%{_libdir}/*.so
%{_libdir}/pkgconfig/libevent.pc
%{_libdir}/pkgconfig/libevent_pthreads.pc
%{_libdir}/pkgconfig/libevent_openssl.pc

%changelog
*	Wed Jul 13 2016 Alexey Makhalov <amakhalov@vmware.com> 2.0.22-3
-	Added openssl runtime requirement
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.22-2
-	GA - Bump release of all rpms
*       Thu Apr 28 2016 Kumar Kaushik <kaushikk@vmware.com> 2.0.22-1
-       Initial Version.
