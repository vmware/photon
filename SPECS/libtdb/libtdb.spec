Name:           libtdb
Summary:        Trivial database library
Version:        1.4.7
Release:        1%{?dist}
URL:            https://tdb.samba.org
License:        LGPLv3+
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://samba.org/ftp/tdb/tdb-%{version}.tar.gz
%define sha512 tdb=2b5b20c299b60545943f106d854b6e0d4a559e16f08a7ed62fe57ee962bebc888c2e663bd5fef907aace05b316826fe8fbbf3f323b6d3427531e59ffe47d48e4

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
* Thu Jul 21 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 1.4.7-1
- Initial addition to Photon. Needed for SSSD.
