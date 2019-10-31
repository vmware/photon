Summary:        Contains a utility for determining file types
Name:           file
Version:        5.30
Release:        5%{?dist}
License:        BSD
URL:            http://www.darwinsys.com/file
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        ftp://ftp.astron.com/pub/file/%{name}-%{version}.tar.gz
%define sha1    file=276051cd2c438d4e7a321c4422a5b3bc850fd747
Patch0:         file-5.30-keep-not-stripped-last.patch
Patch1:         0001-Avoid-reading-past-the-end-of-buffer-Rui-Reis.patch
Patch2:		CVE-2019-18218.patch
Requires:       %{name}-libs = %{version}-%{release}
Conflicts:      toybox
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
%patch0 -p1
%patch1 -p1
%patch2 -p1
%build
./configure \
    --prefix=%{_prefix} \
    --disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
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
*   Thu Oct 31 2019 Siju Maliakkal <smaliakkal@vmware.com> 5.30-5
-   Patch for CVE-2019-18218
*   Wed Aug 01 2018 Ankit Jain <ankitja@vmware.com> 5.30-4
-   Fix for CVE-2018-10360.
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
