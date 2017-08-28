Summary:        The Apache Subversion control system
Name:           subversion
Version:        1.9.4
Release:        2%{?dist}
License:        Apache License 2.0
URL:            http://subversion.apache.org/
Group:          Utilities/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://archive.apache.org/dist/%{name}/%{name}-%{version}.tar.bz2
%define sha1 subversion=bc7d51fdda43bea01e1272dfe9d23d0a9d6cd11c
Patch0:         subversion-CVE-2017-9800.patch
Requires:       apr
Requires:       apr-util
BuildRequires:  apr-devel
BuildRequires:  apr-util
BuildRequires:  apr-util-devel
BuildRequires:  sqlite-autoconf
BuildRequires:  libtool
BuildRequires:  expat

%description
The Apache version control system.

%package    devel
Summary:    Header and development files for mesos
Requires:   %{name} = %{version}
%description    devel
 subversion-devel package contains header files, libraries.

%prep
%setup -q
%patch0 -p1
%build
./configure --prefix=%{_prefix}                         \
        --disable-static                \
        --with-apache-libexecdir 

make %{?_smp_mflags}

%install
make -j1 DESTDIR=%{buildroot} install 
%find_lang %{name}
%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/svn*
%{_libdir}/libsvn_*.so.*
%{_datadir}/*

%files devel
%{_includedir}/*
%{_libdir}/libsvn_*.*a
%{_libdir}/libsvn_*.so
%exclude %{_libdir}/debug/

%changelog
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
