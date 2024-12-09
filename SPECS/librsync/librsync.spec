Summary:        Rsync libraries
Name:           librsync
Version:        2.3.2
Release:        3%{?dist}
URL:            http://librsync.sourcefrog.net/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

#https://github.com/librsync/librsync/archive/v2.0.0.tar.gz
Source0:        %{name}-%{version}.tar.gz
%define sha512  %{name}=77d826dbaf02061b759d876a6b537238bad40379a08e4494ebfd3e380b2eb921b7b060bc570330aeac9424ef1a9d521f449d559c9ffa3be24acdef4ad530fe90

Source1: license.txt
%include %{SOURCE1}

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
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 2.3.2-3
- Release bump for SRP compliance
* Fri Jun 17 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.3.2-2
- Fix build with latest cmake
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 2.3.2-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 2.3.1-1
- Automatic Version Bump
* Sun Sep 30 2018 Bo Gan <ganb@vmware.com> 2.0.2-1
- Update to 2.0.2
* Wed Jun 28 2017 Chang Lee <changlee@vmware.com>  2.0.0-2
- Updated %check
* Wed Apr 12 2017 Xiaolin Li <xiaolinl@vmware.com>  2.0.0-1
- Initial build. First version
