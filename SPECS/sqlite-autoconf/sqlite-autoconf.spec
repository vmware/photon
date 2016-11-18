%define sourcever 3110000
Summary:	A portable, high level programming interface to various calling conventions
Name:		sqlite-autoconf
Version:	3.11.0
Release:	4%{?dist}
License:	Public Domain
URL:		http://www.sqlite.org
Group:		System Environment/GeneralLibraries
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	http://sqlite.org/2016/%{name}-3110000.tar.gz
%define sha1 sqlite-autoconf=e2d300e4b24af5ecd67a1396488893fa44864e36
Obsoletes:	libsqlite
Provides:	sqlite3
Requires:	sqlite-libs = %{version}-%{release}
%description
This package contains most of the static files that comprise the
www.sqlite.org website including all of the SQL Syntax and the 
C/C++ interface specs and other miscellaneous documentation.

%package -n sqlite-devel
Summary:	sqlite3 link library & header files
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%description -n sqlite-devel
The sqlite devel package include the needed library link and
header files for development.

%package -n sqlite-libs
Summary:	sqlite3 library
Group:		Libraries
%description -n sqlite-libs
The sqlite3 library.

%prep
%setup -q -n %{name}-%{sourcever}
%build
./configure \
	CFLAGS="%{optflags}" \
	CXXFLAGS="%{optflags} -DSQLITE_ENABLE_FTS3=1 \
	-DSQLITE_ENABLE_COLUMN_METADATA=1 \
	-DSQLITE_ENABLE_UNLOCK_NOTIFY=1 \
	-DSQLITE_SECURE_DELETE=1" \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--disable-static
make
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
install -D -m644 sqlite3.1 %{buildroot}/%{_mandir}/man1/sqlite3.1
find %{buildroot}/%{_libdir} -name '*.la' -delete
rm -rf %{buildroot}/%{_infodir}
%{_fixperms} %{buildroot}/*

%check
make %{?_smp_mflags} check

%post -n sqlite-libs
/sbin/ldconfig

%postun	-n sqlite-libs
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*

%files -n sqlite-devel
%defattr(-,root,root)
%{_libdir}/libsqlite3.so
%{_libdir}/libsqlite3.so.0
%{_libdir}/pkgconfig/*
%{_includedir}/*

%files -n sqlite-libs
%defattr(-,root,root)
%{_libdir}/libsqlite3.so.0.8.6

%changelog
*   Wed Nov 16 2016 Alexey Makhalov <amakhalov@vmware.com> 3.11.0-4
-   Added -devel and -libs subpackages
*   Mon Oct 04 2016 ChangLee <changlee@vmware.com> 3.11.0-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.11.0-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 3.11.0-1
-   Updated to version 3.11.0
*   Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com> - 3.8.3.1-2
-   Fix versioning
*   Mon Oct 7 2014 Divya Thaluru <dthaluru@vmware.com> 3080301-1
-   Initial build. First version
