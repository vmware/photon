Summary:        A library that performs asynchronous DNS operations
Name:           c-ares
Version:        1.16.1
Release:        2%{?dist}
License:        MIT
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            http://c-ares.haxx.se/
Source0:        http://c-ares.haxx.se/download/%{name}-%{version}.tar.gz
%define sha1    c-ares=1111250ae1bf9adea1afc278ada1136091531d72
Patch0:         CVE-2020-8277.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool

%description
c-ares is a C library that performs DNS requests and name resolves
asynchronously. c-ares is a fork of the library named 'ares', written
by Greg Hudson at MIT.

%package devel
Summary: Development files for c-ares
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkg-config

%description devel
This package contains the header files and libraries needed to
compile applications or shared objects that use c-ares.

%prep
%setup -q
f=CHANGES ; iconv -f iso-8859-1 -t utf-8 $f -o $f.utf8 ; mv $f.utf8 $f
%patch0 -p1

%build
autoreconf -if
%configure --enable-shared --disable-static \
           --disable-dependency-tracking
%{__make} %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT/%{_libdir}/libcares.la

%check
make %{?_smp_mflags} check

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc README.md README.msvc README.cares CHANGES NEWS
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/ares.h
%{_includedir}/ares_build.h
%{_includedir}/ares_dns.h
%{_includedir}/ares_rules.h
%{_includedir}/ares_version.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/libcares.pc
%{_mandir}/man3/ares_*

%changelog
*   Sun Mar 14 2021 Prashant S Chauhan <psinghchauha@vmware.com> 1.16.1-2
-   Fix CVE-2020-8277
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.16.1-1
-   Automatic Version Bump
*   Fri Sep 21 2018 Sujay G <gsujay@vmware.com> 1.14.0-1
-   Bump c-ares version to 1.14.0
*   Fri Sep 29 2017 Dheeraj Shetty <dheerajs@vmware.com>  1.12.0-2
-   Fix for CVE-2017-1000381
*   Fri Apr 07 2017 Anish Swaminathan <anishs@vmware.com>  1.12.0-1
-   Upgrade to 1.12.0
*   Wed Oct 05 2016 Xiaolin Li <xiaolinl@vmware.com> 1.10.0-3
-   Apply patch for CVE-2016-5180.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.10.0-2
-   GA - Bump release of all rpms
*   Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com> - 1.10.0-1
-   Initial version