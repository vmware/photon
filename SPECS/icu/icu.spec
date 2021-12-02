Summary:	International Components for Unicode
Name:		icu
Version:	70.1
Release:	1%{?dist}
License:	MIT and UCD and Public Domain
URL:		http://www.icu-project.org
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://download.icu-project.org/files/%{name}4c/%{version}/%{name}4c-70_1-src.tgz
%define sha1    icu=f7c1363edee6be7de8b624ffbb801892b3417d4e

%description
The International Components for Unicode (ICU) package is a mature,
widely used set of C/C++ libraries providing Unicode and Globalization support for software applications.

%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}
%description	devel
It contains the libraries and header files to create applications.

%prep
%autosetup -n %{name}/source

%build
%configure
make %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install

%files
%defattr(-,root,root)
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/*.so.*
%exclude %{_libdir}/debug/
%exclude %{_libdir}/icu/

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_datadir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
*   Wed Nov 24 2021 Alexey Makhalov <amakhalov@vmware.com> 70.1-1
-   Version update
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 69.1-1
-   Automatic Version Bump
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 67.1-1
-   Automatic Version Bump
*   Thu Sep 13 2018 Siju Maliakkal <smaliakkal@vmware.com> 61.1-1
-   Update to latest version
*   Wed Jan 31 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 55.1-1
-   Initial build for photon
