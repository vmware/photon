Summary:        Contains a utility for determining file types
Name:           file
Version:        5.38
Release:        2%{?dist}
License:        BSD
URL:            http://www.darwinsys.com/file
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        ftp://ftp.astron.com/pub/file/%{name}-%{version}.tar.gz
%define sha1    %{name}=57cad9341c3f74f8681c2ef931786c420105f35e

Requires:       %{name}-libs = %{version}-%{release}

Conflicts:      toybox < 0.7.3-7

%description
The package contains a utility for determining the type of a
given file or files

%package        libs
Summary:        Library files for file
%description    libs
It contains the libraries to run the application.

%package        devel
Summary:        Header and development files for file
Requires:       %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications.

%prep
%setup -q

%build
%configure

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
find %{buildroot}%{_libdir} -name '*.la' -delete

%check
make %{?_smp_mflags} check

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*man1/*
%{_mandir}/*man4/*

%files  libs
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_datarootdir}/misc/magic.mgc

%files  devel
%{_libdir}/*.so
%{_includedir}/*
%{_mandir}/*man3/*

%changelog
* Mon Sep 13 2021 Shreenidhi Shedi <sshedi@vmware.com> 5.38-2
- Conflict only with toybox < 0.7.3-7
* Wed Apr 08 2020 Siju Maliakkal <smaliakkal@vmware.com> 5.38-1
- Upgrade to 5.38
- CVE-2019-8904, CVE-2019-8905, CVE-2019-8906, CVE-2019-8907
* Thu Oct 31 2019 Siju Maliakkal <smaliakkal@vmware.com> 5.30-5
- Patch for CVE-2019-18218
* Wed Aug 01 2018 Ankit Jain <ankitja@vmware.com> 5.30-4
- Fix for CVE-2018-10360.
* Fri Dec 15 2017 Divya Thaluru <dthaluru@vmware.com> 5.30-3
- Added seperate package for libraries
- Added toybox as conflict package
* Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 5.30-2
- Add devel package.
* Tue Apr 04 2017 Chang Lee <changlee@vmware.com> 5.30-1
- Updated to version 5.30
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.24-2
- GA - Bump release of all rpms
* Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 5.24-1
- Updated to version 5.24
* Mon Apr 6 2015 Divya Thaluru <dthaluru@vmware.com> 5.22-1
- Initial build. First version
