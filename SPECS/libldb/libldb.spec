%global cmocka_version  1.1.5
%global talloc_version  2.4.1
%global tdb_version     1.4.8
%global tevent_version  0.15.0

Name:           libldb
Version:        2.8.2
Release:        1%{?dist}
Summary:        A schema-less, ldap like, API and database
License:        LGPLv3+
Distribution:   Photon
Vendor:         VMware, Inc.
Group:          Development/Libraries
URL:            http://ldb.samba.org

Source0: https://www.samba.org/ftp/ldb/ldb-%{version}.tar.gz
%define sha512 ldb=df1c228307ede75920a927ae3124cd0d507dfcf00f93b6f5c14b79f4e1a23dbe00249bc92b3ee3ed1e5ce06fe363f0be1eb3dab491fbe79e83b1a1b35a6e50e1

BuildRequires: cmocka-devel
BuildRequires: gcc
BuildRequires: libtalloc-devel
BuildRequires: libtdb-devel
BuildRequires: libtevent-devel
BuildRequires: popt-devel
BuildRequires: libxslt-devel
BuildRequires: docbook-xsl
BuildRequires: openldap
BuildRequires: make
BuildRequires: gnupg
BuildRequires: which
BuildRequires: python3-devel
BuildRequires: python3-tdb
BuildRequires: python3-talloc-devel
BuildRequires: python3-tevent

Requires: cmocka >= %{cmocka_version}
Requires: libtalloc >= %{talloc_version}
Requires: libtdb >= %{tdb_version}
Requires: libtevent >= %{tevent_version}

Provides: bundled(libreplace)

%description
An extensible library that implements an LDAP like API to access remote LDAP
servers, or use local tdb databases.

%package -n ldb-tools
Summary: Tools to manage LDB files
Requires: %{name} = %{version}-%{release}

%description -n ldb-tools
Tools to manage LDB files

%package devel
Summary: Developer tools for the LDB library
Requires: libldb = %{version}-%{release}
Requires: libtdb-devel >= %{tdb_version}
Requires: libtalloc-devel >= %{talloc_version}
Requires: libtevent-devel >= %{tevent_version}

%description devel
Header files needed to develop programs that link against the LDB library.

%package -n python3-ldb
Summary: Python bindings for the LDB library
Requires: libldb = %{version}-%{release}
Requires: python3-tdb >= %{tdb_version}
Provides: python3-ldb

%description -n python3-ldb
Python bindings for the LDB library

%package -n python3-ldb-devel
Summary: Development files for the Python bindings for the LDB library
Requires: python3-ldb = %{version}-%{release}
Provides: python3-ldb-devel

%description -n python3-ldb-devel
Development files for the Python bindings for the LDB library

%prep
%autosetup -n ldb-%{version} -p1

%build
%configure \
   --disable-rpath \
   --disable-rpath-install \
   --builtin-libraries=replace \
   --with-modulesdir=%{_libdir}/ldb/modules \
   --with-privatelibdir=%{_libdir}/ldb \
   --without-ldb-lmdb \
   --enable-debug

%make_build

%install
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
%make_build check
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%dir %{_libdir}/ldb
%{_libdir}/libldb.so.*
%{_libdir}/ldb/libldb-key-value.so
%{_libdir}/ldb/libldb-tdb-err-map.so
%{_libdir}/ldb/libldb-tdb-int.so
%dir %{_libdir}/ldb/modules
%dir %{_libdir}/ldb/modules/ldb
%{_libdir}/ldb/modules/ldb/*.so

%files -n ldb-tools
%defattr(-,root,root)
%{_bindir}/ldbadd
%{_bindir}/ldbdel
%{_bindir}/ldbedit
%{_bindir}/ldbmodify
%{_bindir}/ldbrename
%{_bindir}/ldbsearch
%{_libdir}/ldb/libldb-cmdline.so
%{_mandir}/man1/ldbadd.1.*
%{_mandir}/man1/ldbdel.1.*
%{_mandir}/man1/ldbedit.1.*
%{_mandir}/man1/ldbmodify.1.*
%{_mandir}/man1/ldbrename.1.*
%{_mandir}/man1/ldbsearch.1.*

%files devel
%defattr(-,root,root)
%{_includedir}/ldb_module.h
%{_includedir}/ldb_handlers.h
%{_includedir}/ldb_errors.h
%{_includedir}/ldb_version.h
%{_includedir}/ldb.h
%{_libdir}/libldb.so
%{_libdir}/pkgconfig/ldb.pc
%{_mandir}/man3/ldb*.gz

%files -n python3-ldb
%defattr(-,root,root)
%{python3_sitearch}/*.cpython-*.so
%{_libdir}/libpyldb-util.cpython-*.so.2*
%{python3_sitearch}/_ldb_text.py

%files -n python3-ldb-devel
%defattr(-,root,root)
%{_includedir}/pyldb.h
%{_libdir}/libpyldb-util.cpython-*.so
%{_libdir}/pkgconfig/pyldb-util.cpython-*.pc

%changelog
* Fri May 16 2025 Michelle Wang <michelle.wang@broadcom.com> 2.8.2-1
- Upgrade to v1.4.13, needed by samba-4.19.3
* Mon Jul 03 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.7.2-2
- Remove _isa entry
* Tue Jun 13 2023 Oliver Kurth <okurth@vmware.com> 2.7.2-1
- update to 2.7.2 - required by samba 4.18.3
* Tue Feb 14 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 2.6.1-1
- Initial addition to Photon. Needed for SSSD.
