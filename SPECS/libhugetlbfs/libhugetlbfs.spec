Summary:        Preload library to back text, data, malloc() or shared memory with hugepages
Name:           libhugetlbfs
Version:        2.22
Release:        1%{?dist}
License:        LGPL-2.1
URL:            https://github.com/libhugetlbfs/libhugetlbfs
Source0:        https://github.com/libhugetlbfs/libhugetlbfs/releases/download/2.22/libhugetlbfs-2.22.tar.gz
%define sha1    libhuge=d03e9ad795f9434c416895dd2d14054e614c5b0e
Group:          System/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  which
%if %{with_check}
BuildRequires:  python3
%endif

%description
Preload library to back text, data, malloc() or shared memory with hugepages.

%package devel
Summary:        libhugetlbfs devel
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}
%description devel
This contains development tools and libraries for libhugetlbfs.

%prep
%setup -q
%build
make PREFIX=/usr BUILDTYPE=NATIVEONLY LIB32=lib32 LIB64=lib %{?_smp_mflags}

%install
make PREFIX=/usr BUILDTYPE=NATIVEONLY LIB32=lib32 LIB64=lib DESTDIR=%{buildroot} install

%check
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
* Wed Jun 17 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 2.22-1
- Initial version.
