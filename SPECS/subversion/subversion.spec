Summary:        The Apache Subversion control system
Name:           subversion
Version:        1.9.4
Release:        7%{?dist}
License:        Apache License 2.0
URL:            http://subversion.apache.org/
Group:          Utilities/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://archive.apache.org/dist/%{name}/%{name}-%{version}.tar.bz2
%define sha1    subversion=bc7d51fdda43bea01e1272dfe9d23d0a9d6cd11c
Patch0:         subversion-CVE-2017-9800.patch
Patch1:         subversion-CVE-2016-8734.patch
Requires:       apr
Requires:       apr-util
Requires:       serf
BuildRequires:  apr-devel
BuildRequires:  apr-util
BuildRequires:  apr-util-devel
BuildRequires:  sqlite-autoconf
BuildRequires:  libtool
BuildRequires:  expat
BuildRequires:  serf-devel

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
%patch1 -p0
%build
./configure --prefix=%{_prefix}         \
            --disable-static            \
            --with-apache-libexecdir    \
            --with-serf=%{_prefix}

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
*   Wed Mar 20 2019 Tapas Kundu <tkundu@vmware.com> 1.9.4-7
-   Bumped up to use latest openssl
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
