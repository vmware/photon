Summary:        Contains a utility for determining file types
Name:           file
Version:        5.39
Release:        3%{?dist}
License:        BSD
URL:            http://www.darwinsys.com/file
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        ftp://ftp.astron.com/pub/file/%{name}-%{version}.tar.gz
%define sha512  file=9cf1a7b769c56eb6f5b25c66ce85fa1300128396e445b2e53dbbd8951e5da973a7a07c4ef9f7ebd1fe945d47bdaf2cd9ef09bd2be6c217a0bcb907d9449835e6
Patch0:         file-5.39-CLOEXEC.patch
Patch1:         CVE-2022-48554.patch
Requires:       %{name}-libs = %{version}-%{release}
Conflicts:      toybox < 0.8.2-2
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
%autosetup -p1

%build
autoreconf -fi
%configure --disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} %{?_smp_mflags} install
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
%{_libdir}/pkgconfig/libmagic.pc

%changelog
*   Thu Sep 14 2023 Siju Maliakkal <smaliakkal@vmware.com> 5.39-3
-   Apply patch for CVE-2022-48554
*   Thu Feb 18 2021 Shreenidhi Shedi <sshedi@vmware.com> 5.39-2
-   Fix close_on_exec multithreaded decompression issue
*   Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 5.39-1
-   Automatic Version Bump
*   Tue Jul 07 2020 Gerrit Photon <photon-checkins@vmware.com> 5.38-1
-   Automatic Version Bump
*   Thu Apr 16 2020 Alexey Makhalov <amakhalov@vmware.com> 5.34-3
-   Do not conflict with toybox >= 0.8.2-2
*   Tue Oct 29 2019 Siju Maliakkal <smaliakkal@vmware.com> 5.34-2
-   Apply patch for CVE-2019-18218
*   Thu Sep 20 2018 Sujay G <gsujay@vmware.com> 5.34-1
-   Bump file version to 5.34
*   Fri Dec 15 2017 Divya Thaluru <dthaluru@vmware.com> 5.30-3
-   Added seperate package for libraries
-   Added toybox as conflict package
*   Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 5.30-2
-   Add devel package.
*   Tue Apr 04 2017 Chang Lee <changlee@vmware.com> 5.30-1
-   Updated to version 5.30
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.24-2
-   GA - Bump release of all rpms
*   Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 5.24-1
-   Updated to version 5.24
*   Mon Apr 6 2015 Divya Thaluru <dthaluru@vmware.com> 5.22-1
-   Initial build. First version
