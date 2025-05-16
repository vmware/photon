Name:           libtdb
Summary:        Trivial database library
Version:        1.4.13
Release:        1%{?dist}
URL:            https://tdb.samba.org
License:        LGPLv3+
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://samba.org/ftp/tdb/tdb-%{version}.tar.gz
%define sha512 tdb=23cbabaf272947d65ab6ba22481ecbf2b86889f860b223ae650101fbf3c6a19acd179d8da15013502076172876acbf3ee3695e9cdeeaa721ed30920b1bd4937d

BuildRequires: make
BuildRequires: gcc
BuildRequires: libxslt-devel
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

%clean
rm -rf %{buildroot}/*

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
* Fri May 16 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.4.13-1
- Upgrade to v1.4.13, needed by samba-4.19.3
* Tue Feb 14 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 1.4.8-1
- Initial addition to Photon. Needed for SSSD.
