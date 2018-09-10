Summary:        Platform-neutral API
Name:           nspr
Version:        4.20
Release:        1%{?dist}
License:        MPLv2.0
URL:            http://ftp.mozilla.org/pub/mozilla.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://ftp.mozilla.org/pub/nspr/releases/v%{version}/src/%{name}-%{version}.tar.gz
%define sha1    nspr=ef1e2ca3205fd1658a69ada2e0436266ca3065b5

%description
Netscape Portable Runtime (NSPR) provides a platform-neutral API
for system level and libc like functions.

%package        devel
Summary:        Header and development files for nspr
Requires:       %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications

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

%post   -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_datarootdir}/aclocal/*

%changelog
*   Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.20-1
-   Upgrade to 4.20.
*   Tue Jun 20 2017 Xiaolin Li <xiaolinl@vmware.com> 4.15-1
-   Upgrade to 4.15.
*   Fri May 05 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.14-2
-   Fix error - binary packed in devel.
*   Sat Apr 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.14-1
-   Update to 4.14
*   Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 4.12-3
-   Added -devel subpackage
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.12-2
-   GA - Bump release of all rpms
*   Thu Feb 25 2016 Kumar Kaushik <kaushikk@vmware.com> 4.12-1
-   Updated to version 4.12
*   Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> 4.11-1
-   Updated to version 4.11
*   Fri May 29 2015 Alexey Makhalov <amakhalov@vmware.com> 4.10.8-1
-   Version update. Firefox requirement.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 4.10.3-1
-   Initial build. First version
