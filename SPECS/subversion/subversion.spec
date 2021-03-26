Summary:        The Apache Subversion control system
Name:           subversion
Version:        1.10.4
Release:        2%{?dist}
License:        Apache License 2.0
URL:            http://subversion.apache.org/
Group:          Utilities/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://archive.apache.org/dist/%{name}/%{name}-%{version}.tar.bz2
%define sha1    subversion=a9052724d94fe5d3ee886473eb7cdc4297af4cdd
Patch0:         subversion-CVE-2018-11782.patch
Patch1:         subversion-CVE-2019-0203.patch
Patch2:         subversion-CVE-2020-17525.patch
Requires:       apr
Requires:       apr-util
Requires:       serf
Requires:       utf8proc
BuildRequires:  apr-devel
BuildRequires:  apr-util
BuildRequires:  apr-util-devel
BuildRequires:  sqlite-autoconf
BuildRequires:  libtool
BuildRequires:  expat
BuildRequires:  serf-devel
BuildRequires:  utf8proc-devel

%description
The Apache version control system.

%package        devel
Summary:        Header and development files for mesos
Requires:       %{name} = %{version}
%description    devel
 subversion-devel package contains header files, libraries.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
./configure --prefix=%{_prefix}         \
            --disable-static            \
            --with-apache-libexecdir    \
            --with-serf=%{_prefix}      \
            --with-lz4=internal

make %{?_smp_mflags}

%install
make -j1 DESTDIR=%{buildroot} install
%find_lang %{name}
find %{buildroot}/%{_libdir} -name '*.la' -delete

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/svn*
%{_libdir}/libsvn_*.so.*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%files devel
%{_includedir}/*
%{_libdir}/libsvn_*.so
%{_datadir}/pkgconfig/*.pc

%changelog
*   Fri Mar 26 2021 Ankit Jain <ankitja@vmware.com> 1.10.4-2
-   Added patches for CVE-2020-17525
*   Mon Nov 11 2019 Prashant S Chauhan <psinghchauha@vmware.com> 1.10.4-1
-   Fix CVE-2018-11803 update to version 1.10.4
*   Fri Oct 11 2019 Ankit Jain <ankitja@vmware.com> 1.9.4-7
-   Fix for CVE-2018-11782 and CVE-2019-0203
*   Thu Feb 01 2018 Xiaolin Li <xiaolinl@vmware.com> 1.9.4-6
-   Move pkgconfig files to devel package.
*   Mon Jan 22 2018 Xiaolin Li <xiaolinl@vmware.com> 1.9.4-5
-   Compile subversion with https repository access module support
*   Thu Dec 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.9.4-4
-   Fix CVE-2016-8734
*   Tue Sep 26 2017 Anish Swaminathan <anishs@vmware.com> 1.9.4-3
-   Release bump for expat version update
*   Mon Aug 28 2017 Xiaolin Li <xiaolinl@vmware.com> 1.9.4-2
-   Apply patch for CVE-2017-9800
*   Wed Nov 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.9.4-1
-   Upgraded to version 1.9.4, fixes CVE-2016-2167  CVE-2016-2168
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.3-6
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 1.9.3-1
-   Updated to version 1.9.3
*   Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 1.8.13-5
-   Handled locale files with macro find_lang
*   Tue Sep 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.8.13-4
-   Updated build-requires after creating devel package for apr.
*   Mon Sep 21 2015 Xiaolin Li <xiaolinl@vmware.com> 1.8.13-3
-   Move .a, and .so files to devel pkg.
*   Tue Sep 08 2015 Vinay Kulkarni <kulkarniv@vmware.com> 1.8.13-2
-   Move headers into devel pkg.
*   Fri Jun 26 2015 Sarah Choi <sarahc@vmware.com> 1.8.13-1
-   Initial build. First version
