Summary:       Lightning memory-mapped database
Name:          lmdb
Version:       0.9.29
Release:       1%{?dist}
Group:         System/Libraries
Vendor:        VMware, Inc.
License:       OpenLDAP
URL:           https://symas.com/lmdb
Source0:       https://github.com/LMDB/lmdb/archive/LMDB_%{version}.tar.gz
%define sha512 LMDB=a29e40b1a2f2ed542fb59b6dd92cf7f5f9ac603f74b1d2a66d143b65edf0324a03dc4a0a35657ba0992b00a3e9764e33af0dcc5ae8ae91c40c90c3b0581dade3
Source1:       %{name}.pc
Distribution:  Photon
Requires:      lmdb-libs = %{version}-%{release}

%description
An ultra-fast, ultra-compact, crash-proof key-value
embedded data store.

%package       devel
Summary:       Development files for lmdb
Group:         Development/Libraries
Requires:      lmdb = %{version}-%{release}

%description   devel
Development files for lmdb

%package       libs
Summary:       Shared libraries for lmdb
Group:         Development/Libraries

%description   libs
Shared libraries for lmdb

%prep
%autosetup -n lmdb-LMDB_%{version}

%build
cd libraries/liblmdb
make %{?_smp_mflags}

%install
cd libraries/liblmdb
make prefix=%{_prefix} DESTDIR=%{buildroot} %{?_smp_mflags} install
mkdir -p %{buildroot}%{_docdir}/%{name}
mkdir -p %{buildroot}%{_defaultlicensedir}/%{name}
mkdir -p %{buildroot}%{_libdir}/pkgconfig
install -m0644 COPYRIGHT %{buildroot}%{_docdir}/%{name}
install -m0644 LICENSE %{buildroot}%{_defaultlicensedir}/%{name}
install -m0755 %{SOURCE1} %{buildroot}%{_libdir}/pkgconfig
# resolve /usr/bin/mdb_stat conflict with ligthwave-post by renaming the binary
%{__mv} %{buildroot}%{_bindir}/mdb_stat %{buildroot}%{_bindir}/mdb_stat_lmdb
# accordingly rename the man page
%{__mv} %{buildroot}%{_mandir}/man1/mdb_stat.1 %{buildroot}%{_mandir}/man1/mdb_stat_lmdb.1

%post

    /sbin/ldconfig

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

%clean
rm -rf %{buildroot}/*

%files
%{_mandir}/*
%{_bindir}/*

%files devel
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/pkgconfig/%{name}.pc

%files libs
%{_docdir}/%{name}/COPYRIGHT
%{_defaultlicensedir}/%{name}/LICENSE
%{_libdir}/*.so

%changelog
*  Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 0.9.29-1
-  Automatic Version Bump
*  Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 0.9.28-1
-  Automatic Version Bump
*  Fri Jan 22 2021 Dweep Advani <dadvani@vmware.com> 0.9.24-2
-  Resolve /usr/bin/mdb_stat conflict by renaming to mdb_stat_lmdb
*  Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 0.9.24-1
-  Automatic Version Bump
*  Tue Jan 22 2019 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.9.22-2
-  add libs package for library. tools and man in main package.
*  Wed Sep 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 0.9.22-1
-  Update to version 0.9.22
*  Wed Dec 13 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.9.21-1
-  Initial
