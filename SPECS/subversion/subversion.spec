Summary:        The Apache Subversion control system
Name:           subversion
Version:        1.10.8
Release:        4%{?dist}
License:        Apache License 2.0
URL:            http://subversion.apache.org
Group:          Utilities/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://archive.apache.org/dist/%{name}/%{name}-%{version}.tar.bz2
%define sha512  %{name}=94464202b4a4ac7a6055c50eaa19ea55127f70f0efe5e0e655ef0a0866c8148bde56417b1dfd3204260300488ab668228faadec5015fe3e4b17e06c76e1d86b4

Requires:       apr
Requires:       apr-util
Requires:       serf
Requires:       utf8proc

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

%description
The Apache version control system.

%package        devel
Summary:        Header and development files for mesos
Requires:       %{name} = %{version}-%{release}

%description    devel
The subversion-devel package contains header files, libraries.

%package        perl
Summary:        Allows Perl scripts to directly use Subversion repositories.
Requires:       perl
Requires:       %{name} = %{version}-%{release}

%description    perl
Provides Perl (SWIG) support for Subversion version control system.

%prep
%autosetup -p1

%build
%configure \
        --disable-static \
        --with-apache-libexecdir \
        --with-serf=%{_prefix} \
        --with-lz4=internal

%make_build

# For Perl bindings
%make_build swig-pl

%install
# make doesn't support _smp_mflags
%make_install
%find_lang %{name}

# make doesn't support _smp_mflags
%make_install install-swig-pl

%if 0%{?with_check}
%check
# subversion expect nonroot user to run tests
chmod g+w . -R
useradd test -G root -m
# make doesn't support _smp_mflags
sudo -u test make check && userdel test -r -f
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/svn*
%exclude %{_libdir}/libsvn_swig_perl*so*
%{_libdir}/libsvn_*.so.*
%{_mandir}/man[158]/*

%files devel
%{_includedir}/*
%{_libdir}/libsvn_*.so
%{_datadir}/pkgconfig/*.pc
%exclude %dir %{_libdir}/debug

%files perl
%defattr(-,root,root)
%{perl_sitearch}/SVN
%{perl_sitearch}/auto/SVN
%{_libdir}/libsvn_swig_perl*.so.*
%{_mandir}/man3/SVN*
%exclude %{_libdir}/perl5/*/*/perllocal.pod

%changelog
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.10.8-4
- Remove .la files
* Mon Jul 04 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.10.8-3
- Remove redundant locale directory packaging
* Fri Apr 29 2022 Michelle Wang <michellew@vmware.com> 1.10.8-2
- Update sha1 to sha512
* Tue Apr 26 2022 Ankit Jain <ankitja@vmware.com> 1.10.8-1
- Update to 1.10.8 to fix CVE-2022-24070, CVE-2021-28544
* Sat Mar 26 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.10.2-7
- Exclude debug symbols properly
* Fri Mar 26 2021 Ankit Jain <ankitja@vmware.com> 1.10.2-6
- Added patches for CVE-2020-17525
* Fri Oct 11 2019 Ankit Jain <ankitja@vmware.com> 1.10.2-5
- Added patches for CVE-2019-0203 and CVE-2018-11782
* Tue Mar 05 2019 Siju Maliakkal <smaliakkal@vmware.com> 1.10.2-4
- Excluding conflicting perllocal.pod
* Tue Oct 02 2018 Siju Maliakkal <smaliakkal@vmware.com> 1.10.2-3
- Added Perl bindings
* Fri Sep 21 2018 Ankit Jain <ankitja@vmware.com> 1.10.2-2
- Added utf8proc as Requires.
* Wed Sep 19 2018 Ankit Jain <ankitja@vmware.com> 1.10.2-1
- Updated to version 1.10.2
* Mon Jan 22 2018 Xiaolin Li <xiaolinl@vmware.com> 1.9.7-2
- Compile subversion with https repository access module support
* Mon Aug 28 2017 Xiaolin Li <xiaolinl@vmware.com> 1.9.7-1
- Update to version 1.9.7.
* Thu Jun 15 2017 Xiaolin Li <xiaolinl@vmware.com> 1.9.5-2
- Fix make check issues.
* Wed Apr 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.9.5-1
- Update to version 1.9.5
* Tue Dec 27 2016 Xiaolin Li <xiaolinl@vmware.com> 1.9.4-2
- Moved pkgconfig/*.pc to devel subpackage.
* Wed Nov 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.9.4-1
- Upgraded to version 1.9.4, fixes CVE-2016-2167  CVE-2016-2168
* Wed Nov 16 2016 Alexey Makhalov <ppadmavilasom@vmware.com> 1.9.3-8
- Use sqlite-{devel,libs}
* Mon Oct 10 2016 ChangLee <changlee@vmware.com> 1.9.3-7
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.3-6
- GA - Bump release of all rpms
* Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 1.9.3-1
- Updated to version 1.9.3
* Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 1.8.13-5
- Handled locale files with macro find_lang
* Tue Sep 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.8.13-4
- Updated build-requires after creating devel package for apr.
* Mon Sep 21 2015 Xiaolin Li <xiaolinl@vmware.com> 1.8.13-3
- Move .a, and .so files to devel pkg.
* Tue Sep 08 2015 Vinay Kulkarni <kulkarniv@vmware.com> 1.8.13-2
- Move headers into devel pkg.
* Fri Jun 26 2015 Sarah Choi <sarahc@vmware.com> 1.8.13-1
- Initial build. First version
