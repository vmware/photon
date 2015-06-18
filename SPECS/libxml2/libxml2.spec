Summary:	Libxml2-2.9.1
Name:		libxml2
Version:	2.9.1
Release:	2%{?dist}
License:	MIT
URL:		http://xmlsoft.org/
Group:		System Environment/General Libraries
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://www.eecis.udel.edu/~ntp/ntp_spool/ntp4/ntp-4.2/%{name}-%{version}.tar.gz
Requires:	python2
BuildRequires:	python2-devel
BuildRequires:	python2-libs
Provides:	pkgconfig(libxml-2.0)

%description
The libxml2 package contains libraries and utilities used for parsing XML files. 

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
%{_libdir}/python*
%{_libdir}/xml2Conf.sh
%{_bindir}/*
%{_datadir}/aclocal/*
%{_datadir}/gtk-doc/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/libxml-2.0.pc

%changelog
*	Thu Jun 11 2015 Alexey Makhalov <amakhalov@vmware.com> 2.9.1-2
-	Moved 'Provides: pkgconfig(...)' into base package
*	Mon Oct 13 2014 Divya Thaluru <dthaluru@vmware.com> 2.9.1-1
-	Initial build.	First version
