Summary:        Rsync libraries
Name:           librsync
Version:        2.0.2
Release:        1%{?dist}
URL:            http://librsync.sourcefrog.net/
License:        LGPLv2+
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
#https://github.com/librsync/librsync/archive/v2.0.0.tar.gz
Source0:        %{name}-%{version}.tar.gz
%define sha1    librsync=f8e74edf82520e682e6c213f0de644874829da9a

BuildRequires:  cmake

%description
librsync implements the "rsync" algorithm, which allows remote
differencing of binary files.  librsync computes a delta relative to a
file's checksum, so the two files need not both be present to generate
a delta.

This library was previously known as libhsync up to version 0.9.0.

The current version of this package does not implement the rsync
network protocol and uses a delta format slightly more efficient than
and incompatible with rsync 2.4.6.

%package devel
Summary: Headers and development libraries for librsync
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
librsync implements the "rsync" algorithm, which allows remote
differencing of binary files.  librsync computes a delta relative to a
file's checksum, so the two files need not both be present to generate
a delta.

This library was previously known as libhsync up to version 0.9.0.

The current version of this package does not implement the rsync
network protocol and uses a delta format slightly more efficient than
and incompatible with rsync 2.4.6.

This package contains header files necessary for developing programs
based on librsync.

%prep
%setup -q

%build
mkdir -p build
cd build
%{cmake} -DCMAKE_SKIP_RPATH:BOOL=YES \
         -DCMAKE_SKIP_INSTALL_RPATH:BOOL=YES \
         -DENABLE_STATIC:BOOL=NO ..
make %{?_smp_mflags}

%install
cd build
make DESTDIR=%{buildroot} install

%check
cd build
make test

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS COPYING
%{_bindir}/rdiff
%{_libdir}/*.so.*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_mandir}/man3/*
%{_libdir}/*.so

%changelog
*   Sun Sep 30 2018 Bo Gan <ganb@vmware.com> 2.0.2-1
-   Update to 2.0.2
*   Wed Jun 28 2017 Chang Lee <changlee@vmware.com>  2.0.0-2
-   Updated %check
*   Wed Apr 12 2017 Xiaolin Li <xiaolinl@vmware.com>  2.0.0-1
-   Initial build. First version

