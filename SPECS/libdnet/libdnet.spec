Summary:        A simplified, portable interface to several low-level networking routines
Name:           libdnet
Version:        1.11
Release:        7%{?dist}
License:        BSD
URL:            http://prdownloads.sourceforge.net/libdnet/libdnet-1.11.tar.gz
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://prdownloads.sourceforge.net/libdnet/%{name}-%{version}.tar.gz
Patch0:         DisableMakeCheckCases.patch
%define sha1    libdnet=e2ae8c7f0ca95655ae9f77fd4a0e2235dc4716bf
%description
libdnet provides a simplified, portable interface to several low-level networking routines.

%package        devel
Summary:        Header and development files for libdnet
Requires:       %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications.

%prep
%setup -q
%patch0 -p1
%build
%configure "CFLAGS=-fPIC"
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
find %{buildroot}/usr/lib/ -name '*.la' -delete

%check
make  %{?_smp_mflags} check
%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files 
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/libdnet
%{_libdir}/libdnet.1
%{_libdir}/libdnet.1.0.1
%{_sbindir}/*
%{_mandir}/man8/*

%files  devel
%{_includedir}/*
%{_mandir}/man3/*
%{_libdir}/libdnet.a

%changelog
*   Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 1.11-7
-   Cross compilation support
*   Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 1.11-6
-   Aarch64 support
*   Thu Aug 03 2017 Kumar Kaushik <kaushikk@vmware.com> 1.11-5
-   Applying patch for makecheck bug #1633615.
*   Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 1.11-4
-   Move man files to /usr/share, add devel package
*   Thu Oct 06 2016 ChangLee <changlee@vmware.com> 1.11-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.11-2
-   GA - Bump release of all rpms
*   Thu Nov 06 2014 Sharath George <sharathg@vmware.com> 1.11-1
    Initial version
