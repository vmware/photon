Summary:	Platform-neutral API
Name:		nspr
Version:	4.13.1
Release:	1%{?dist}
License:	MPLv2.0
URL:		http://ftp.mozilla.org/pub/mozilla.org
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: Photon
Source0:		http://ftp.mozilla.org/pub/mozilla.org/%{name}/releases/v%{version}/src/%{name}-%{version}.tar.gz
%define sha1 nspr=ec6660257d41267a0e6ee25812e9012cb9ddd274

%description
Netscape Portable Runtime (NSPR) provides a platform-neutral API
for system level and libc like functions.

%prep
%setup -q
cd nspr
sed -ri 's#^(RELEASE_BINS =).*#\1#' pr/src/misc/Makefile.in
sed -i 's#$(LIBRARY) ##' config/rules.mk

%build
cd nspr
./configure \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--with-mozilla \
	--with-pthreads \
	$([ $(uname -m) = x86_64 ] && echo --enable-64bit) \
	--disable-silent-rules

make %{?_smp_mflags}

%install
cd nspr
make DESTDIR=%{buildroot} install

%post	-p /sbin/ldconfig

%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datarootdir}/aclocal/*

%changelog
*	Sat Apr 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.13.1-1
-	Update to 4.13.1
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.12-2
-	GA - Bump release of all rpms
*       Thu Feb 25 2016 Kumar Kaushik <kaushikk@vmware.com> 4.12-1
-       Updated to version 4.12
* 	Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> 4.11-1
- 	Updated to version 4.11
*	Fri May 29 2015 Alexey Makhalov <amakhalov@vmware.com> 4.10.8-1
-	Version update. Firefox requirement.
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 4.10.3-1
-	Initial build. First version
