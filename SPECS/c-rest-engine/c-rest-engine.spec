Name:          c-rest-engine
Summary:       minimal http(s) server library
Version:       1.2
Release:       6%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache 2.0
URL:           http://www.github.com/vmware/c-rest-engine
BuildArch:     x86_64
Requires:      openssl >= 1.0.1
BuildRequires: coreutils >= 8.22
BuildRequires: openssl-devel >= 1.0.1
Source0:       %{name}-%{version}.tar.gz
Patch1:        c-rest-engine-fix-log-file-len.patch
Patch2:        preprocess-timeout.patch
Patch3:        typo_fixes.patch
Patch4:        ssl_read_error.patch
Patch5:        persistent_connection.patch
Patch6:        fd_leak.patch
Patch7:        http_header_should_be_case_insensitive.patch
%define sha1   c-rest-engine=25aa9d1f2680e26114dee18365c510692552f8e4

%description
c-rest-engine is a minimal embedded http(s) server written in C.
Its primary intent is to enable REST(Representational State Transfer)
API support for C daemons.

%package devel
Summary: c-rest-engine dev files
Requires:  openssl-devel >= 1.0.1
Requires:  %{name} = %{version}-%{release}

%description devel
development libs and header files for c-rest-engine

%prep
%setup -q
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
*  Tue Feb 05 2019 Michelle Wang <michellew@vmware.com> 1.2-6
-  http_header_should_be_case_insensitive.patch.
*  Wed May 09 2018 Kumar Kaushik <kaushikk@vmware.com> 1.2-5
-  Adding patch for file descriptor leak issue.
*  Thu Mar 22 2018 Kumar Kaushik <kaushikk@vmware.com> 1.2-4
-  Adding support for pesistent connection.
*  Wed Mar 07 2018 Kumar Kaushik <kaushikk@vmware.com> 1.2-3
-  Appying patch for some typo in code.
*  Fri Feb 23 2018 Kumar Kaushik <kaushikk@vmware.com> 1.2-2
-  Appying patch for preprocess timeout.
*  Wed Feb 14 2018 Kumar Kaushik <kaushikk@vmware.com> 1.2-1
-  Upgrading to version 1.2. Removing all upstream patches.
*  Thu Nov 23 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.1-1
-  Update to v1.1-1
*  Thu Nov 02 2017 Kumar Kaushik <kaushikk@vmware.com> 1.0.5-1
-  Adding version, 1.0.5, get peer info API.
*  Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 1.0.4-3
-  Remove coreutils runtime dependency.
*  Tue Sep 12 2017 Kumar Kaushik <kaushikk@vmware.com> 1.0.4-2
-  Making default log level as ERROR.
*  Mon Sep 11 2017 Kumar Kaushik <kaushikk@vmware.com> 1.0.4-1
-  Updating to version 1.0.4.
*  Tue Aug 22 2017 Kumar Kaushik <kaushikk@vmware.com> 1.0.3-2
-  Upstream version 1.0.4 patch for 1.0.3.
*  Fri Jul 21 2017 Kumar Kaushik <kaushikk@vmware.com> 1.0.3-1
-  Updating version to 1.0.3, API for setting SSL info.
*  Tue Jun 20 2017 Kumar Kaushik <kaushikk@vmware.com> 1.0.2-1
-  Updating version to 1.0.2
*  Thu May 18 2017 Kumar Kaushik <kaushikk@vmware.com> 1.0.1-1
-  Updating version to 1.0.1
*  Thu May 04 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.0-1
-  Initial build.  First version
