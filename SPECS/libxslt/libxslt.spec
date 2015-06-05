Summary:	Libxslt-1.1.28
Name:		libxslt
Version:	1.1.28
Release:	1%{?dist}
License:	MIT
URL:		http:/http://xmlsoft.org/libxslt/
Group:		System Environment/General Libraries
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://xmlsoft.org/sources/%{name}-%{version}.tar.gz
Requires:	libxml2-devel
BuildRequires:	libxml2-devel
BuildRequires:	python2
%description
The libxslt package contains XSLT libraries used for extending libxml2 libraries to support XSLT files. 
%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--disable-static
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete
%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.sh
%{_libdir}/libxslt-plugins
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_docdir}/*
%{_datadir}/aclocal/*
%changelog
*	Mon Oct 13 2014 Divya Thaluru <dthaluru@vmware.com> 1.1.28-1
-	Initial build.	First version
