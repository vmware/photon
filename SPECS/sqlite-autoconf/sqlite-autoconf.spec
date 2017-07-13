%define sourcever 3180000
Summary:	A portable, high level programming interface to various calling conventions
Name:		sqlite-autoconf
Version:	3.18.0
Release:	2%{?dist}
License:	Public Domain
URL:		http://www.sqlite.org
Group:		System Environment/GeneralLibraries
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	http://sqlite.org/2017/%{name}-3180000.tar.gz
%define sha1 sqlite=74559194e1dd9b9d577cac001c0e9d370856671b
#https://sqlite.org/src/vpatch?from=0db20efe201736b3&to=66de6f4a9504ec26
Patch0:		CVE-2017-10989.patch
Obsoletes:	libsqlite
Provides:	sqlite3
%description
This package contains most of the static files that comprise the
www.sqlite.org website including all of the SQL Syntax and the 
C/C++ interface specs and other miscellaneous documentation.
%prep
%setup -q -n %{name}-%{sourcever}
%patch0 -p1

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
make -j1
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
install -D -m644 sqlite3.1 %{buildroot}/%{_mandir}/man1/sqlite3.1
find %{buildroot}/%{_libdir} -name '*.la' -delete
rm -rf %{buildroot}/%{_infodir}
%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%{_libdir}/*.so*
%{_bindir}/*
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_mandir}/man1/*
%changelog
*   Thu Jul 13 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.18.0-2
-   Adding patch for CVE-2017-10989
*   Mon May 8 2017 Divya Thaluru <dthaluru@vmware.com> 3.18.0-1
-   Updated to version 3.18.0
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.11.0-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 3.11.0-1
-   Updated to version 3.11.0
*   Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com> - 3.8.3.1-2
-   Fix versioning
*   Mon Oct 7 2014 Divya Thaluru <dthaluru@vmware.com> 3080301-1
-   Initial build.	First version
