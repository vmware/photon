Summary:        Preload library to back text, data, malloc() or shared memory with hugepages
Name:           libhugetlbfs
Version:        2.23
Release:        3%{?dist}
License:        LGPL-2.1
URL:            https://github.com/libhugetlbfs/libhugetlbfs
Source0:        https://github.com/libhugetlbfs/libhugetlbfs/releases/download/%{version}/libhugetlbfs-%{version}.tar.gz
%define sha512  libhuge=b509ff60179e3dc52532bc16b1a414b4993bb79019733a30a7bfa69311f627606b196aced4457bdb88edccdbe7070df755aaab37c6599f4cecdfcb0015aee212
Patch0:         Disable-hugepage-backend-malloc.patch
Group:          System/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  which
%if %{with_check}
BuildRequires:  python3
%endif

%description
Preload library to back text, data, malloc() or shared memory with hugepages.

%package        devel
Summary:        libhugetlbfs devel
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}
%description    devel
This contains development tools and libraries for libhugetlbfs.

%prep
%autosetup -p1
%build
%make_build PREFIX=/usr BUILDTYPE=NATIVEONLY LIB32=lib32 LIB64=lib

%install
%make_install %{?_smp_mflags} PREFIX=/usr BUILDTYPE=NATIVEONLY LIB32=lib32 LIB64=lib

%check
# make doesn't support _smp_mflags
make PREFIX=/usr BUILDTYPE=NATIVEONLY LIB32=lib32 LIB64=lib check

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/libhugetlbfs.so
%{_libdir}/libhugetlbfs_privutils.so
%{_mandir}/man1/pagesize.1.gz
%{_mandir}/man7/*
%{_mandir}/man8/*

%files devel
%{_includedir}/hugetlbfs.h
%{_libdir}/libhugetlbfs.a
%{_datadir}/%{name}/*
%{_mandir}/man1/ld.hugetlbfs.1.gz
%{_mandir}/man3/*

%changelog
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.23-3
- Update release to compile with python 3.11
* Mon Sep 19 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 2.23-2
- Fix build with latest toolchain
* Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 2.23-1
- Automatic Version Bump
* Tue Dec 17 2019 Alexey Makhalov <amakhalov@vmware.com> 2.22-1
- Initial version.
