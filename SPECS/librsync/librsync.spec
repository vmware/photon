Summary:        Rsync libraries
Name:           librsync
Version:        2.0.0
Release:        1%{?dist}
URL:            http://librsync.sourcefrog.net/
License:        LGPLv2+
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
#https://github.com/librsync/librsync/archive/v2.0.0.tar.gz
Source0:        %{name}-%{version}.tar.gz
%define sha1    librsync=c24a623bba5f9eae48bd3b6cb99ee43d2a40b8c6

BuildRequires:  cmake
BuildRequires:  popt-devel

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
cmake -DCMAKE_INSTALL_PREFIX=/usr   \
      -DCMAKE_BUILD_TYPE=Release    \
      -Wno-dev ..

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
cd build
make DESTDIR=%{buildroot} install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS COPYING
%{_bindir}/rdiff
%{_libdir}/librsync.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/librsync.so


%changelog
*   Wed Apr 12 2017 Xiaolin Li <xiaolinl@vmware.com>  2.0.0-1
-   Initial build. First version

