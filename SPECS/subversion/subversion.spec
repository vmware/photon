Summary:        The Apache Subversion control system
Name:           subversion
Version:        1.9.5
Release:        1%{?dist}
License:        Apache License 2.0
URL:            http://subversion.apache.org/
Group:          Utilities/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://archive.apache.org/dist/%{name}/%{name}-%{version}.tar.bz2
%define sha1    subversion=8bd6a44a1aed30c4c6b6b068488dafb44eaa6adf
Requires:       apr
Requires:       apr-util
BuildRequires:  apr-devel
BuildRequires:  apr-util
BuildRequires:  apr-util-devel
BuildRequires:  sqlite-devel
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

%build
./configure --prefix=%{_prefix}         \
        --disable-static                \
        --with-apache-libexecdir

make %{?_smp_mflags}

%install
make -j1 DESTDIR=%{buildroot} install 
%find_lang %{name}

%check
make  %{?_smp_mflags} check

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/svn*
%{_libdir}/libsvn_*.so.*
%{_mandir}/man[158]/*
%{_datadir}/locale/*

%files devel
%{_includedir}/*
%{_libdir}/libsvn_*.*a
%{_libdir}/libsvn_*.so
%{_datadir}/pkgconfig/*.pc
%exclude %{_libdir}/debug/

%changelog
*   Wed Apr 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.9.5-1
-   Update to version 1.9.5
*   Tue Dec 27 2016 Xiaolin Li <xiaolinl@vmware.com> 1.9.4-2
-   Moved pkgconfig/*.pc to devel subpackage.
*   Wed Nov 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.9.4-1
-   Upgraded to version 1.9.4, fixes CVE-2016-2167  CVE-2016-2168
*   Wed Nov 16 2016 Alexey Makhalov <ppadmavilasom@vmware.com> 1.9.3-8
-   Use sqlite-{devel,libs}
*   Mon Oct 10 2016 ChangLee <changlee@vmware.com> 1.9.3-7
-   Modified %check
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
