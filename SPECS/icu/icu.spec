Summary:	International Components for Unicode
Name:		icu
Version:	67.1
Release:	1%{?dist}
License:	MIT and UCD and Public Domain
URL:		http://www.icu-project.org
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://download.icu-project.org/files/%{name}4c/%{version}/%{name}4c-67_1-src.tgz
%define sha1    icu=6822a4a94324d1ba591b3e8ef084e4491af253c1

%description
The International Components for Unicode (ICU) package is a mature,
widely used set of C/C++ libraries providing Unicode and Globalization support for software applications.

%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}
%description	devel
It contains the libraries and header files to create applications.

%prep
%setup -q -n %{name}/source

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

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
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 67.1-1
-   Automatic Version Bump
*   Thu Sep 13 2018 Siju Maliakkal <smaliakkal@vmware.com> 61.1-1
-   Update to latest version
*   Wed Jan 31 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 55.1-1
-   Initial build for photon
