Summary:	International Components for Unicode.
Name:		icu
Version:	62.1
Release:	1%{?dist}
License:	MIT and UCD and Public Domain
URL:		http://www.icu-project.org
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://download.icu-project.org/files/%{name}4c/%{version}/%{name}4c-62_1-src.tgz
%define sha1 icu=1884f26568cd773b984580b4fca422a3e2afe35d
%description
The International Components for Unicode (ICU) package is a mature, widely used set of C/C++ libraries providing Unicode and Globalization support for software applications.
%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}
%description	devel
It contains the libraries and header files to create applications 
%prep
%setup -q -n %{name}/source
%build
./configure --prefix=%{_prefix}
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
*   Mon Sep 17 2018 Tapas Kundu <tkundu@vmware.com> 62.1-1
-   Updated to 62.1 release
*   Wed Jan 31 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 55.1-1
-   Initial build for photon
