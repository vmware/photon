Summary:        Rsync libraries
Name:           librsync
Version:        2.3.1
Release:        2%{?dist}
URL:            http://librsync.sourcefrog.net
License:        LGPLv2+
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/librsync/librsync/archive/%{name}-%{version}.tar.gz
%define sha512 %{name}=89e5b5ad960b8036acce41df09f5e50601d7eb57d48a2bd21c4ee54a3a375f62ee514036b9a562277b5656735b84cadf6f54cbf48c364bbf0c04f2d95ae3b5a6

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
Requires: %{name} = %{version}-%{release}

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
%autosetup -p1

%build
%cmake \
    -DCMAKE_BUILD_TYPE=Debug \
    -DCMAKE_SKIP_RPATH:BOOL=YES \
    -DCMAKE_SKIP_INSTALL_RPATH:BOOL=YES \
    -DENABLE_STATIC:BOOL=NO \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir}

%cmake_build

%install
%cmake_install

%if 0%{?with_check}
%check
export LD_LIBRARY_PATH="%{buildroot}%{_libdir}"
make %{?_smp_mflags} test
%endif

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
* Wed Sep 21 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.3.1-2
- Use cmake macros
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 2.3.1-1
- Automatic Version Bump
* Sun Sep 30 2018 Bo Gan <ganb@vmware.com> 2.0.2-1
- Update to 2.0.2
* Wed Jun 28 2017 Chang Lee <changlee@vmware.com>  2.0.0-2
- Updated %check
* Wed Apr 12 2017 Xiaolin Li <xiaolinl@vmware.com>  2.0.0-1
- Initial build. First version
