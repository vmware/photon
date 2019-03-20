Name:          c-rest-engine
Summary:       minimal http(s) server library
Version:       1.2
Release:       6%{?dist}
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
Patch0:        log-file-name.patch
Patch1:        preprocess-timeout.patch
Patch2:        typo_fixes.patch
Patch3:        ssl_read_error.patch
Patch4:        persistent_connection.patch
Patch5:        fd_leak.patch
Patch6:        include_time_header.patch
Patch7:        openssl-1.1.1-compatibility.patch 
%define sha1   c-rest-engine=25aa9d1f2680e26114dee18365c510692552f8e4

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
%patch6 -p1
%patch7 -p1

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
*  Wed Mar 06 2019 Tapas Kundu <tkundu@vmware.com> 1.2-6
-  Added patch for compatiable for openssl 1.1.1b
*  Wed May 09 2018 Kumar Kaushik <kaushikk@vmware.com> 1.2-5
-  Adding patch for file decriptor leak issue.
*  Thu Mar 22 2018 Kumar Kaushik <kaushikk@vmware.com> 1.2-4
-  Adding support for persistent connection.
*  Mon Mar 05 2018 Kumar Kaushik <kaushikk@vmware.com> 1.2-3
-  Appying patch for some typo in code.
*  Fri Feb 23 2018 Kumar Kaushik <kaushikk@vmware.com> 1.2-2
-  Appying patch for preprocess timeout.
*  Wed Feb 14 2018 Kumar Kaushik <kaushikk@vmware.com> 1.2-1
-  Upgrading to version 1.2. Removing all upstream patches.
*  Wed Feb 14 2018 Kumar Kaushik <kaushikk@vmware.com> 1.1-10
-  Maintaing instance state for API calls safety.
*  Tue Feb 06 2018 Kumar Kaushik <kaushikk@vmware.com> 1.1-9
-  Fixing bad memory write crash.
*  Mon Jan 29 2018 Kumar Kaushik <kaushikk@vmware.com> 1.1-8
-  Adding fix for timeout cleanup on IO socket.
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
