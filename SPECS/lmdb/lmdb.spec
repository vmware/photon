Summary:       Lightning memory-mapped database
Name:          lmdb
Version:       0.9.22
Release:       2%{?dist}
Group:         System/Libraries
Vendor:        VMware, Inc.
License:       OpenLDAP
URL:           https://symas.com/lmdb
Source0:       https://github.com/LMDB/lmdb/archive/LMDB_%{version}.tar.gz
%define sha1 LMDB=5d62d4c7527f3474f60a0d87db2bfd539e6493eb
Source1:       %{name}.pc
Distribution:  Photon
Requires:      lmdb-libs = %{version}-%{release}

%description
An ultra-fast, ultra-compact, crash-proof key-value
embedded data store.

%package devel
Summary:    Development files for lmdb
Group:      Development/Libraries
Requires:   lmdb = %{version}-%{release}

%description devel
Development files for lmdb

%package libs
Summary:    Shared libraries for lmdb
Group:      Development/Libraries

%description libs
Shared libraries for lmdb

%prep
%setup -qn lmdb-LMDB_%{version}

%build
cd libraries/liblmdb
make %{?_smp_mflags}

%install
%define relpath       %{_builddir}/%{buildsubdir}/libraries/liblmdb
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_libdir}/pkgconfig
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}

install -m0755 %{relpath}/liblmdb.so %{buildroot}%{_libdir}
install -m0755 %{SOURCE1} %{buildroot}%{_libdir}/pkgconfig
install -m0755 %{relpath}/mdb_copy %{buildroot}%{_bindir}
install -m0755 %{relpath}/mdb_dump %{buildroot}%{_bindir}
install -m0755 %{relpath}/mdb_load %{buildroot}%{_bindir}
install -m0755 %{relpath}/mdb_stat %{buildroot}%{_bindir}
install -m0644 %{relpath}/lmdb.h %{buildroot}%{_includedir}
install -m0644 %{relpath}/{CHANGES,LICENSE,intro.doc} %{buildroot}%{_docdir}/%{name}-%{version}

%post

    /sbin/ldconfig

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

%clean
rm -rf %{buildroot}/*

%files
%{_bindir}/*

%files devel
%{_docdir}/%{name}-%{version}/{CHANGES,intro.doc}
%{_includedir}/*
%{_libdir}/pkgconfig/%{name}.pc

%files libs
%{_docdir}/%{name}-%{version}/LICENSE
%{_libdir}/*.so

%changelog
*  Tue Jan 22 2019 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.9.22-2
-  add libs package for library. tools in main package.
*  Wed Sep 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 0.9.22-1
-  Update to version 0.9.22
*  Wed Dec 13 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.9.21-1
-  Initial
