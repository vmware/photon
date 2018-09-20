Summary:        Contains a utility for determining file types
Name:           file
Version:        5.34
Release:        1%{?dist}
License:        BSD
URL:            http://www.darwinsys.com/file
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        ftp://ftp.astron.com/pub/file/%{name}-%{version}.tar.gz
%define sha1    file=509e30ad0e0d74fa4040a28ce4667486cfe2170c
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
%build
%configure \
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
