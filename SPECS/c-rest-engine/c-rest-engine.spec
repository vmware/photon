Name:          c-rest-engine
Summary:       minimal http(s) server library
Version:       1.1
Release:       7%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache 2.0
URL:           http://www.github.com/vmware/c-rest-engine
BuildArch:     x86_64
Requires:      coreutils >= 8.22
Requires:      openssl >= 1.0.1
BuildRequires: coreutils >= 8.22
BuildRequires: openssl-devel >= 1.0.1
Source0:       %{name}-%{version}.tar.gz
Patch0:        socket_RW.patch
Patch1:        syslog_noInit.patch
Patch2:        socket_logging.patch
Patch3:        errno_init.patch
Patch4:        ssl_shutdown.patch
Patch5:        minimal_request_logging.patch
%define sha1   c-rest-engine=a25927fd98ec92df5e210cc4941fa626604636f6

%description
c-rest-engine is a minimal embedded http(s) server written in C.
Its primary intent is to enable REST(Representational State Transfer)
API support for C daemons.

%package devel
Summary: c-rest-engine dev files
Requires:  coreutils >= 8.22
Requires:  openssl-devel >= 1.0.1
Requires:  %{name} = %{version}-%{release}

%description devel
development libs and header files for c-rest-engine

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
cd build
autoreconf -mif ..
../configure \
    --prefix=%{_prefix} \
    --with-ssl=/usr \
    --enable-debug=%{_enable_debug} \
    --disable-static

make

%install

[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
cd build && make install DESTDIR=$RPM_BUILD_ROOT
find %{buildroot} -name '*.la' -delete

%post -p  /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%exclude %{_sbindir}/vmrestd

%files devel
%{_includedir}/vmrest.h
%{_libdir}/*.so

# %doc ChangeLog README COPYING

%changelog
*  Fri Dec 15 2017 Kumar Kaushik <kaushikk@vmware.com> 1.1-7
-  Adding patch for minimal packet level logging.
*  Wed Nov 29 2017 Kumar Kaushik <kaushikk@vmware.com> 1.1-6
-  Adding patch for ssl_shutdown order.
*  Wed Nov 29 2017 Kumar Kaushik <kaushikk@vmware.com> 1.1-5
-  Adding patch for right use of errno.
*  Mon Nov 20 2017 Kumar Kaushik <kaushikk@vmware.com> 1.1-4
-  Socket poller/read logging patch.
*  Fri Nov 17 2017 Kumar Kaushik <kaushikk@vmware.com> 1.1-3
-  Removing syslog open/close from library.
*  Fri Nov 10 2017 Kumar Kaushik <kaushikk@vmware.com> 1.1-2
-  Fix 0 bytes error codition on socket read and write.
*  Tue Oct 31 2017 Kumar Kaushik <kaushikk@vmware.com> 1.1-1
-  Async support.
*  Thu Oct 20 2017 Kumar Kaushik <kaushikk@vmware.com> 1.0.5-1
-  New API for peer info.
*  Tue Sep 12 2017 Kumar Kaushik <kaushikk@vmware.com> 1.0.4-2
-  Making default log level as ERROR.
*  Mon Sep 11 2017 Kumar Kaushik <kaushikk@vmware.com> 1.0.4-1
-  Updating to version 1.0.4.
*  Fri Jul 21 2017 Kumar Kaushik <kaushikk@vmware.com> 1.0.3-1
-  Updating version to 1.0.3, API for setting SSL info.
*  Tue Jun 20 2017 Kumar Kaushik <kaushikk@vmware.com> 1.0.2-1
-  Updating version to 1.0.2
*  Thu May 18 2017 Kumar Kaushik <kaushikk@vmware.com> 1.0.1-1
-  Updating version to 1.0.1
*  Thu May 04 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.0-1
-  Initial build.  First version
