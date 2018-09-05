Summary:       Lightning memory-mapped database manager
Name:          lmdb
Version:       0.9.22
Release:       1%{?dist}
Group:         System/Libraries
Vendor:        VMware, Inc.
License:       OpenLDAP
URL:           https://github.com/LMDB/lmdb
Source0:       https://github.com/LMDB/lmdb/archive/LMDB_%{version}.tar.gz
%define sha1 LMDB=5d62d4c7527f3474f60a0d87db2bfd539e6493eb
Source1:       %{name}.pc
Distribution:  Photon

%description
Lightning memory-mapped database manager

%package devel
Summary:    Development files for lmdb
Group:      Development/Libraries
Requires:   lmdb = %{version}-%{release}

%description devel
Development files for lmdb

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
%{_docdir}/*
%{_libdir}/*.so
%{_bindir}/*

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/%{name}.pc

%changelog
*  Wed Sep 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 0.9.22-1
-  Update to version 0.9.22
*  Wed Dec 13 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.9.21-1
-  Initial
