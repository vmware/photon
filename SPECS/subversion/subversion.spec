Summary:        The Apache Subversion control system
Name:           subversion
Version:        1.14.2
Release:        10%{?dist}
License:        Apache License 2.0
URL:            http://subversion.apache.org
Group:          Utilities/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://archive.apache.org/dist/%{name}/%{name}-%{version}.tar.bz2
%define sha512 %{name}=20ada4688ca07d9fb8da4b7d53b5084568652a3b9418c65e688886bae950a16a3ff37710fcfc9c29ef14a89e75b2ceec4e9cf35d5876a7896ebc2b512cfb9ecc

Requires: apr
Requires: apr-util
Requires: serf
Requires: cyrus-sasl
Requires: utf8proc

BuildRequires: cyrus-sasl-devel
BuildRequires: apr-devel
BuildRequires: apr-util-devel
BuildRequires: sqlite-devel
BuildRequires: libtool
BuildRequires: expat-devel
BuildRequires: serf-devel
BuildRequires: lz4
BuildRequires: utf8proc-devel
BuildRequires: swig

%description
The Apache version control system.

%package        devel
Summary:        Header and development files for mesos
Requires:       %{name} = %{version}-%{release}

%description    devel
subversion-devel package contains header files, libraries.

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
   --with-lz4=internal \
   --with-apr=%{_prefix}

%make_build

# For Perl bindings
%make_build swig-pl

%install
# make doesn't support _smp_mflags
%make_install
%find_lang %{name}

# For Perl bindings
# make doesn't support _smp_mflags
%make_install install-swig-pl

%if 0%{?with_check}
%check
# subversion expect nonroot user to run tests
chmod g+w . -R
useradd test -G root -m
sudo -u test make check %{?_smp_mflags}
userdel test -r -f
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/svn*
%{_libdir}/libsvn_*.so.*
%{_mandir}/man[158]/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libsvn_*.so
%{_datadir}/pkgconfig/*.pc
%exclude %dir %{_libdir}/debug

%files perl
%defattr(-,root,root)
%{_libdir}/libsvn_swig_perl*so*
%{_libdir}/perl5/*
%{_mandir}/man3/SVN*
%exclude %{_libdir}/perl5/*/*/perllocal.pod

%changelog
* Tue Sep 10 2024 Kuntal Nayak <kuntal.nayak@broadcom.com> 1.14.2-10
- Bump version as a part of apr upgrade
* Fri Feb 23 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 1.14.2-9
- Bump version as a part of sqlite upgrade to v3.43.2
* Fri Sep 29 2023 Nitesh Kumar <kunitesh@vmware.com> 1.14.2-8
- Bump version as a part of apr-util v1.6.3 upgrade
* Fri May 19 2023 Srish Srinivasan <ssrish@vmware.com> 1.14.2-7
- Bump version as a part of apr version upgrade
* Thu Jan 12 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.14.2-6
- Bump up version no. as part of swig upgrade
* Wed Jan 11 2023 Oliver Kurth <okurth@vmware.com> 1.14.2-5
- bump release as part of sqlite update
* Tue Sep 13 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.14.2-4
- Remove .la files
* Sat Jul 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.14.2-3
- Bump version as a part of sqlite upgrade
* Sun May 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.14.2-2
- Fix binary path
* Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 1.14.2-1
- Automatic Version Bump
* Sun Aug 01 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.14.1-3
- Bump version for openssl 3.0.0
* Fri May 21 2021 Shreenidhi Shedi <sshedi@vmware.com> 1.14.1-2
- Bump version as a part of rpm upgrade
* Fri Mar 26 2021 Ankit Jain <ankitja@vmware.com> 1.14.1-1
- Update to 1.14.1 to fix CVE-2020-17525
* Tue Jan 05 2021 Shreenidhi Shedi <sshedi@vmware.com> 1.14.0-3
- Fix build with new rpm
* Wed Aug 26 2020 Piyush Gupta <gpiyush@vmware.com> 1.14.0-2
- Added Requires cyrus-sasl
* Mon Jul 27 2020 Gerrit Photon <photon-checkins@vmware.com> 1.14.0-1
- Automatic Version Bump
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
