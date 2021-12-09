Summary:        Preload library to back text, data, malloc() or shared memory with hugepages
Name:           libhugetlbfs
Version:        2.23
Release:        2%{?dist}
License:        LGPL-2.1
URL:            https://github.com/libhugetlbfs/libhugetlbfs
Source0:        https://github.com/libhugetlbfs/libhugetlbfs/releases/download/%{version}/libhugetlbfs-%{version}.tar.gz
%define sha1    libhuge=d84cfd845c2aab84053daec3c2337f5e9d73115b
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
%autosetup
%build
make PREFIX=/usr BUILDTYPE=NATIVEONLY LIB32=lib32 LIB64=lib %{?_smp_mflags}

%install
make %{?_smp_mflags} PREFIX=/usr BUILDTYPE=NATIVEONLY LIB32=lib32 LIB64=lib DESTDIR=%{buildroot} install

%check
make %{?_smp_mflags} PREFIX=/usr BUILDTYPE=NATIVEONLY LIB32=lib32 LIB64=lib check

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
*   Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 2.23-2
-   Bump up to compile with python 3.10
*   Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 2.23-1
-   Automatic Version Bump
*   Tue Dec 17 2019 Alexey Makhalov <amakhalov@vmware.com> 2.22-1
-   Initial version.
