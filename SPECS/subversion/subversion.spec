Summary:        The Apache Subversion control system
Name:           subversion
Version:        1.10.2
Release:        3%{?dist}
License:        Apache License 2.0
URL:            http://subversion.apache.org/
Group:          Utilities/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://archive.apache.org/dist/%{name}/%{name}-%{version}.tar.bz2
%define sha1    %{name}=bc52ef2e671f821998ac9a5f7ebecbbcaaef83b8
Requires:       apr
Requires:       apr-util
Requires:       serf
BuildRequires:  apr-devel
BuildRequires:  apr-util
BuildRequires:  apr-util-devel
BuildRequires:  sqlite-devel
BuildRequires:  libtool
BuildRequires:  expat-devel
BuildRequires:  serf-devel
BuildRequires:  lz4
BuildRequires:  utf8proc-devel
BuildRequires:  swig
Requires:       utf8proc

%description
The Apache version control system.

%package    devel
Summary:    Header and development files for mesos
Requires:   %{name} = %{version}
%description    devel
 subversion-devel package contains header files, libraries.

%package    perl
Summary:    Allows Perl scripts to directly use Subversion repositories.
Requires:   perl
Requires:   %{name} = %{version}
%description    perl
Provides Perl (SWIG) support for Subversion version control system.


%prep
%setup -q

%build
./configure --prefix=%{_prefix}         \
        --disable-static                \
        --with-apache-libexecdir        \
        --with-serf=%{_prefix}		\
        --with-lz4=internal

make %{?_smp_mflags}

# For Perl bindings
make  %{?_smp_mflags} swig-pl

%install
make -j1 DESTDIR=%{buildroot} install
%find_lang %{name}

# For Perl bindings
make -j1 DESTDIR=%{buildroot} install-swig-pl

%check
# subversion expect nonroot user to run tests
chmod g+w . -R
useradd test -G root -m
sudo -u test make check && userdel test -r -f

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

%files perl
%defattr(-,root,root)
%{perl_sitearch}/SVN
%{perl_sitearch}/auto/SVN
%{_libdir}/libsvn_swig_perl*so*
%{_libdir}/perl5/*
%{_mandir}/man3/SVN*


%changelog
*   Tue Oct 02 2018 Siju Maliakkal <smaliakkal@vmware.com> 1.10.2-3
-   Added Perl bindings
*   Fri Sep 21 2018 Ankit Jain <ankitja@vmware.com> 1.10.2-2
-   Added utf8proc as Requires.
*   Wed Sep 19 2018 Ankit Jain <ankitja@vmware.com> 1.10.2-1
-   Updated to version 1.10.2
*   Mon Jan 22 2018 Xiaolin Li <xiaolinl@vmware.com> 1.9.7-2
-   Compile subversion with https repository access module support
*   Mon Aug 28 2017 Xiaolin Li <xiaolinl@vmware.com> 1.9.7-1
-   Update to version 1.9.7.
*   Thu Jun 15 2017 Xiaolin Li <xiaolinl@vmware.com> 1.9.5-2
-   Fix make check issues.
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
