Summary:	Libxml2-2.9.3
Name:		libxml2
Version:	2.9.3
Release:	1%{?dist}
License:	MIT
URL:		http://xmlsoft.org/
Group:		System Environment/General Libraries
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	ftp://xmlsoft.org/libxml2/%{name}-%{version}.tar.gz
%define sha1 libxml2=0301ce933637e0ceda049047dbefd18714f59b6e
Requires:	python2
BuildRequires:	python2-devel
BuildRequires:	python2-libs
Provides:	pkgconfig(libxml-2.0)

%description
The libxml2 package contains libraries and utilities used for parsing XML files. 

%package python
Summary:    The libxml2 python module
Group:      Development/Languages/Python
Requires:   %{name} = %{version}
Requires:   python2
Requires:   python2-libs

%description python
The libxml2 python module


%package devel
Summary:    Libraries and header files for libxml
Requires:	%{name} = %{version}

%description devel
Static libraries and header files for the support library for libxml

%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--disable-static \
	--with-history
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
find %{buildroot}/%{_libdir} -name '*.la' -delete
%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%{_docdir}/*
%{_libdir}/libxml*
%{_libdir}/xml2Conf.sh
%{_bindir}/*
%{_datadir}/aclocal/*
%{_datadir}/gtk-doc/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%files python
%defattr(-,root,root)
%{_libdir}/python*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/libxml-2.0.pc
%{_libdir}/cmake/libxml2/libxml2-config.cmake


%changelog
*   Wed Dec 2 2015 Xiaolin Li <xiaolinl@vmware.com> 2.9.3-1
-   Update to version 2.9.3
*   Thu Jul 2 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 2.9.1-3
-   Seperate the python module from the main library
*	Thu Jun 11 2015 Alexey Makhalov <amakhalov@vmware.com> 2.9.1-2
-	Moved 'Provides: pkgconfig(...)' into base package
*	Mon Oct 13 2014 Divya Thaluru <dthaluru@vmware.com> 2.9.1-1
-	Initial build.	First version
