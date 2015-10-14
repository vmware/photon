Summary:	Platform-neutral API
Name:		nspr
Version:	4.10.8
Release:	2%{?dist}
License:	MPLv2.0
URL:		http://ftp.mozilla.org/pub/mozilla.org
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: Photon
Source0:		http://ftp.mozilla.org/pub/mozilla.org/%{name}/releases/v%{version}/src/%{name}-%{version}.tar.gz
%define sha1 nspr=c87c6a10e0e36866006b45c194d70cd8c67d0934
%description
Netscape Portable Runtime (NSPR) provides a platform-neutral API
for system level and libc like functions.
%package devel
Summary:	The libraries and header files needed for %{name} development.
Requires: 	%{name} = %{version}-%{release}

%description devel
The libraries and header files needed for%{name} development.

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
%{_libdir}/*.so
%{_datarootdir}/aclocal/*

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*

%changelog
*   Wed Oct 14 2015 Xiaolin Li <xiaolinl@vmware.com> 4.10.8-2
-   Move development libraries and header files to devel package.
*	Fri May 29 2015 Alexey Makhalov <amakhalov@vmware.com> 4.10.8-1
-	Version update. Firefox requirement.
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 4.10.3-1
-	Initial build. First version
