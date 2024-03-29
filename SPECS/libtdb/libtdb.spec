Name:           libtdb
Summary:        Trivial database library
Version:        1.4.8
Release:        1%{?dist}
URL:            https://tdb.samba.org
License:        LGPLv3+
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://samba.org/ftp/tdb/tdb-%{version}.tar.gz
%define sha512 tdb=763beebe923aa04303cbb91ce5970e6bbd13546888cff75ea9ab025afff3ef88fee539ae173fc2fb7ec661b6c337b0c2da361ce3d318f51ef6627bdb3fe6ca63

BuildRequires: make
BuildRequires: gcc
BuildRequires: libxslt
BuildRequires: docbook-xsl
BuildRequires: docbook-xml
BuildRequires: which
BuildRequires: gnupg
BuildRequires: python3-devel

Requires: glibc

Provides: bundled(libreplace)

%description
A library that implements a trivial database.

%package devel
Summary: Header files need to link the Tdb library
Requires: libtdb = %{version}-%{release}

%description devel
Header files needed to develop programs that link against the Tdb library.

%package -n tdb-tools
Summary: Developer tools for the Tdb library
Requires: libtdb = %{version}-%{release}

%description -n tdb-tools
Tools to manage Tdb files

%package -n python3-tdb
Summary: Python3 bindings for the Tdb library
Requires: %{name} = %{version}-%{release}
Requires: python3

%description -n python3-tdb
Python3 bindings for libtdb

%prep
%autosetup -n tdb-%{version} -p1

%build
%configure --disable-rpath \
           --bundled-libraries=NONE \
           --builtin-libraries=replace \
           --enable-debug
%make_build

%install
%make_install %{?_smp_mflags}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/libtdb.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/tdb.h
%{_libdir}/libtdb.so
%{_libdir}/pkgconfig/tdb.pc

%files -n tdb-tools
%defattr(-,root,root)
%{_bindir}/tdbbackup
%{_bindir}/tdbdump
%{_bindir}/tdbtool
%{_bindir}/tdbrestore
%{_mandir}/man8/tdbbackup.8*
%{_mandir}/man8/tdbdump.8*
%{_mandir}/man8/tdbtool.8*
%{_mandir}/man8/tdbrestore.8.gz

%files -n python3-tdb
%defattr(-,root,root)
%{python3_sitearch}/*

%changelog
* Tue Feb 14 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 1.4.8-1
- Initial addition to Photon. Needed for SSSD.
