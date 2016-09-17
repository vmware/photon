Summary:	Library for manipulating pipelines
Name:		libpipeline
Version:	1.4.1
Release:	2%{?dist}
License:	GPLv3+
URL:		http://libpipeline.nongnu.org
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://download.savannah.gnu.org/releases/libpipeline/%{name}-%{version}.tar.gz
%define sha1 libpipeline=b31cc955f22b1aa4545dc8d00ddbde831936594f
%description
Contains a library for manipulating pipelines of sub processes
in a flexible and convenient way.
%prep
%setup -q
sed -i -e '/gets is a/d' gnulib/lib/stdio.in.h
%build
PKG_CONFIG_PATH=/tools/lib/pkgconfig \
	./configure \
	--prefix=%{_prefix} \
	--disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
find %{buildroot}/%{_libdir} -name '*.la' -delete

%check
make -C tests check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/libpipeline.pc
%{_mandir}/*/*
%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.4.1-2
-	GA - Bump release of all rpms
*       Wed Feb 24 2016 Kumar Kaushik <kaushikk@vmware.com> 1.4.1-1
-       Initial build. First version
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.2.6-1
-	Initial build. First version
