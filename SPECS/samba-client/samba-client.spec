%global build_if %{photon_subrelease} >= 91

%global _samba_modules  pdb_tdbsam,pdb_ldap,pdb_smbpasswd,pdb_wbc_sam,pdb_samba4
%define maj_ver         4.0
%global samba_version   4.24.5
%global ldb_version     2.11.0

Summary:        Samba Client Programs
Name:           samba-client
Version:        4.24.5
Release:        3%{?dist}
Group:          Productivity/Networking
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://www.samba.org

Source0: https://www.samba.org/ftp/samba/stable/samba-%{version}.tar.gz
Source1: smb.conf.vendor

Source2: license.txt
%include %{SOURCE2}

BuildRequires: krb5-devel
BuildRequires: libtirpc-devel
BuildRequires: rpcsvc-proto-devel
BuildRequires: python3-devel
BuildRequires: libarchive
BuildRequires: libarchive-devel
BuildRequires: Linux-PAM-devel
BuildRequires: libxslt-devel
BuildRequires: docbook-xsl
BuildRequires: docbook-xml
BuildRequires: gcc
BuildRequires: gnutls-devel
BuildRequires: jansson-devel
BuildRequires: libxml2-devel
BuildRequires: lmdb
BuildRequires: openldap-devel
BuildRequires: libxcrypt-devel
BuildRequires: perl-Parse-Yapp
BuildRequires: dbus-devel
BuildRequires: sudo
BuildRequires: libtdb-devel >= 1.4.15
BuildRequires: libtalloc-devel >= 2.4.1
BuildRequires: libtevent-devel >= 0.15.0
BuildRequires: python3-tdb
BuildRequires: python3-talloc-devel
BuildRequires: python3-tevent
BuildRequires: bison
BuildRequires: perl-JSON
BuildRequires: zlib-devel
BuildRequires: ncurses-devel
BuildRequires: python3-xml

Requires: %{name}-libs = %{version}-%{release}
Requires: libtirpc
Requires: libarchive
Requires: Linux-PAM
Requires: libxslt
Requires: gnutls
Requires: jansson
Requires: libxml2
Requires: lmdb
Requires: openldap
Requires: dbus
Requires: libtalloc
Requires: ncurses-libs
Requires: popt
Requires: bindutils
Requires: libtdb >= 1.4.15
Requires: libtalloc >= 2.4.1
Requires: libtevent >= 0.15.0
Requires: zlib
Requires: ncurses

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

Provides: samba4-client = %{version}-%{release}

%description
Samba is the standard Windows interoperability suite of programs for Linux and Unix.
The samba-client package provides file and print services to SMB/CIFS clients
and Windows networking to Linux clients.
For a more detailed description of Samba, check the Web page https://www.Samba.org/

%package libs
Summary: Samba client libraries
Requires:   libtdb
Requires:   libldb = %{version}-%{release}
Requires:   libtalloc
Requires:   libtevent

%description libs
The samba-client-libs package contains internal libraries needed by the
SMB/CIFS clients.

%package devel
Summary: Developer tools for Samba-Client libraries
Requires: %{name} = %{version}-%{release}

%description devel
The samba-client-devel package contains the header files and libraries needed
to develop programs.

%package -n libwbclient
Summary:        Samba libwbclient Library
Provides:       pkgconfig(wbclient)

%description -n libwbclient
This package includes the wbclient library.

%package -n libwbclient-devel
Summary:        Libraries and Header Files to Develop Programs with wbclient Support
Requires:       libwbclient = %{version}-%{release}

%description -n libwbclient-devel
This package contains the static libraries and header files needed to
develop programs which make use of the wbclient programming interface.

%package -n libldb
Summary:        A schema-less, ldap like, API and database
Requires:       libtalloc >= 2.4.1
Requires:       libtdb >= 1.4.15
Requires:       libtevent >= 0.15.0

%description -n libldb
An extensible library that implements an LDAP like API to access remote LDAP
servers, or use local tdb databases. LDB is now distributed as part of Samba.

%package -n libldb-devel
Summary:        Developer tools for the LDB library
Requires:       libldb = %{version}-%{release}
Requires:       libtevent-devel

%description -n libldb-devel
Header files needed to develop programs that link against the LDB library.

%package -n ldb-tools
Summary:        Tools to manage LDB files
Requires:       libldb = %{version}-%{release}

%description -n ldb-tools
Tools to manage LDB files.

%package -n ldb-docs
Summary:        Documentation for the LDB library and tools
BuildArch:      noarch

%description -n ldb-docs
Man pages for the LDB library API and command-line tools.

%package -n python3-ldb
Summary:        Python bindings for the LDB library
Requires:       libldb = %{version}-%{release}
Requires:       python3-tdb
Provides:       python3-ldb-devel = %{version}-%{release}
Obsoletes:      python3-ldb-devel < 4.24.5

%description -n python3-ldb
Python bindings for the LDB library.

%prep
%autosetup -n samba-%{samba_version} -p1
rm -r third_party/heimdal

%build
export CFLAGS="-I%{_includedir}/tirpc"
export LDFLAGS="-ltirpc"
export LDBMODULESDIR=%{_libdir}/ldb/modules/ldb

%configure \
        --enable-fhs \
        --with-piddir=/run \
        --with-sockets-dir=/run/samba \
        --with-modulesdir=%{_libdir}/samba \
        --with-pammodulesdir=%{_libdir}/security \
        --with-lockdir=%{_sharedstatedir}/samba/lock \
        --with-statedir=%{_sharedstatedir}/samba \
        --with-cachedir=%{_sharedstatedir}/samba \
        --without-gettext \
        --without-ldb-lmdb \
        --without-lttng \
        --without-ad-dc \
        --without-systemd  \
        --without-acl-support \
        --with-shared-modules=%{_samba_modules} \
        --bundled-libraries=cmocka,!talloc,!pytalloc,!pytalloc-util,!tevent,!pytevent,!tdb,!pytdb \
        --private-libraries=!ldb \
        --enable-debug \
        --with-system-mitkrb5

%make_build bin/smbclient bin/ldbadd bin/ldbdel bin/ldbedit bin/ldbmodify bin/ldbrename bin/ldbsearch

%install
# smb.conf.5.xml exceeds xsltproc's default recursion limit (5000) in 4.24.x;
# waf hardcodes the absolute path to xsltproc, so replace it at /usr/bin/xsltproc directly
mv /usr/bin/xsltproc /usr/bin/xsltproc.real
printf '#!/bin/sh\nexec /usr/bin/xsltproc.real --maxdepth 200000 "$@"\n' > /usr/bin/xsltproc
chmod +x /usr/bin/xsltproc
%make_install %{?_smp_mflags}
mv /usr/bin/xsltproc.real /usr/bin/xsltproc

install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/samba/smb.conf

install -d -m 0755 %{buildroot}%{_tmpfilesdir}
echo "d /run/samba 755 root root" > %{buildroot}%{_tmpfilesdir}/samba.conf

install -d -m 0755 %{buildroot}%{_sysconfdir}/sysconfig
install -m 0644 packaging/systemd/samba.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/samba

for fn in \
   %{_bindir}/gentest \
   %{_bindir}/locktest \
   %{_bindir}/masktest \
   %{_bindir}/ndrdump \
   %{_bindir}/ntlm_auth \
   %{_bindir}/pdbedit \
   %{_bindir}/profiles \
   %{_bindir}/samba-tool \
   %{_bindir}/smbcontrol \
   %{_bindir}/smbpasswd \
   %{_bindir}/smbstatus \
   %{_bindir}/smbtorture \
   %{_bindir}/testparm \
   %{_bindir}/wbinfo \
   %{_includedir}/samba-%{maj_ver}/credentials.h \
   %{_includedir}/samba-%{maj_ver}/dcerpc.h \
   %{_includedir}/samba-%{maj_ver}/dcesrv_core.h \
   %{_includedir}/samba-%{maj_ver}/domain_credentials.h \
   %{_includedir}/samba-%{maj_ver}/lookup_sid.h \
   %{_includedir}/samba-%{maj_ver}/machine_sid.h \
   %{_includedir}/samba-%{maj_ver}/netapi.h \
   %{_includedir}/samba-%{maj_ver}/param.h \
   %{_includedir}/samba-%{maj_ver}/passdb.h \
   %{_includedir}/samba-%{maj_ver}/policy.h \
   %{_includedir}/samba-%{maj_ver}/rpc_common.h \
   %{_includedir}/samba-%{maj_ver}/samba/session.h \
   %{_includedir}/samba-%{maj_ver}/share.h \
   %{_includedir}/samba-%{maj_ver}/smb2_lease_struct.h \
   %{_includedir}/samba-%{maj_ver}/smb_ldap.h \
   %{_includedir}/samba-%{maj_ver}/smbconf.h \
   %{_includedir}/samba-%{maj_ver}/smbldap.h \
   %{_includedir}/samba-%{maj_ver}/tdr.h \
   %{_includedir}/samba-%{maj_ver}/tsocket.h \
   %{_includedir}/samba-%{maj_ver}/tsocket_internal.h \
   %{_includedir}/samba-%{maj_ver}/util/attr.h \
   %{_includedir}/samba-%{maj_ver}/util/blocking.h \
   %{_includedir}/samba-%{maj_ver}/util/debug.h \
   %{_includedir}/samba-%{maj_ver}/util/fault.h \
   %{_includedir}/samba-%{maj_ver}/util/genrand.h \
   %{_includedir}/samba-%{maj_ver}/util/idtree.h \
   %{_includedir}/samba-%{maj_ver}/util/idtree_random.h \
   %{_includedir}/samba-%{maj_ver}/util/signal.h \
   %{_includedir}/samba-%{maj_ver}/util/substitute.h \
   %{_includedir}/samba-%{maj_ver}/util/tevent_ntstatus.h \
   %{_includedir}/samba-%{maj_ver}/util/tevent_unix.h \
   %{_includedir}/samba-%{maj_ver}/util/tevent_werror.h \
   %{_includedir}/samba-%{maj_ver}/util/tfork.h \
   %{_includedir}/samba-%{maj_ver}/util_ldb.h \
   %{_libdir}/libdcerpc-samr.* \
   %{_libdir}/libsamba-policy.so* \
   %{_libdir}/libnss_winbind.so.2 \
   %{_libdir}/libnss_wins.so.2 \
   %{_libdir}/pkgconfig/dcerpc.pc \
   %{_libdir}/pkgconfig/dcerpc_samr.pc \
   %{_libdir}/pkgconfig/netapi.pc \
   %{_libdir}/pkgconfig/samba-credentials.pc \
   %{_libdir}/pkgconfig/samba-hostconfig.pc \
   %{_libdir}/pkgconfig/samba-policy.pc \
   %{_libdir}/pkgconfig/samdb.pc \
   %{_libdir}/samba/idmap/*.so \
   %{_libdir}/samba/krb5/async_dns_krb5_locator.so \
   %{_libdir}/samba/krb5/winbind_krb5_localauth.so \
   %{_libdir}/samba/krb5/winbind_krb5_locator.so \
   %{_libdir}/samba/libLIBWBCLIENT-OLD-private-samba.so \
   %{_libdir}/samba/libREG-FULL-private-samba.so \
   %{_libdir}/samba/libauth-unix-token-private-samba.so \
   %{_libdir}/samba/libauth4-private-samba.so \
   %{_libdir}/samba/libcmocka-private-samba.so \
   %{_libdir}/samba/libdsdb-module-private-samba.so \
   %{_libdir}/samba/libnss-info-private-samba.so \
   %{_libdir}/samba/libsamba-net-join.cpython-*-private-samba.so \
   %{_libdir}/samba/libsamba-python.cpython-*-private-samba.so \
   %{_libdir}/samba/libshares-private-samba.so \
   %{_libdir}/samba/libsmbpasswdparser-private-samba.so \
   %{_libdir}/samba/libxattr-tdb-private-samba.so \
   %{_libdir}/security/pam_winbind.so \
   %{_libdir}/samba/nss_info/*.so \
   %{_libdir}/samba/vfs/*.so \
   %{_libexecdir}/samba/rpcd_* \
   %{_libexecdir}/samba/samba-* \
   %{_sbindir}/eventlogadm \
   %{_sbindir}/nmbd \
   %{_sbindir}/samba-gpupdate \
   %{_sbindir}/smbd \
   %{_sbindir}/winbindd
do
  rm %{buildroot}${fn}
done

# Remove samba Python package; keep only ldb Python bindings
rm -rf %{buildroot}%{python3_sitearch}/samba/
%{py_byte_compile_and_ghost}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%post libs
/sbin/ldconfig

%postun libs
/sbin/ldconfig

%post -n libldb
/sbin/ldconfig

%postun -n libldb
/sbin/ldconfig

%post -n python3-ldb
/sbin/ldconfig

%postun -n python3-ldb
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,-)
%{_bindir}/mdsearch
%{_bindir}/cifsdd
%{_bindir}/dbwrap_tool
%{_bindir}/dumpmscat
%{_bindir}/mvxattr
%{_bindir}/nmblookup
%{_bindir}/oLschema2ldif
%{_bindir}/regdiff
%{_bindir}/regpatch
%{_bindir}/regshell
%{_bindir}/regtree
%{_bindir}/rpcclient
%{_bindir}/samba-regedit
%{_bindir}/sharesec
%{_bindir}/smbcacls
%{_bindir}/smbclient
%{_bindir}/smbcquotas
%{_bindir}/smbget
%{_bindir}/smbspool
%{_bindir}/smbtar
%{_bindir}/smbtree
%{_bindir}/net
%{_bindir}/samba-log-parser
%{_bindir}/wspsearch
%ghost %{_libexecdir}/samba/cups_backend_smb
%{_tmpfilesdir}/samba.conf
%attr(0700,root,root) %dir /var/log/samba
%ghost %dir /run/samba
%ghost %dir /run/winbindd
%dir %{_sharedstatedir}/samba
%attr(700,root,root) %dir %{_sharedstatedir}/samba/private
%dir %{_sharedstatedir}/samba/lock
%attr(755,root,root) %dir %{_sysconfdir}/samba
%config(noreplace) %{_sysconfdir}/samba/smb.conf
%config(noreplace) %{_sysconfdir}/sysconfig/samba
%{_mandir}/man1/*
%exclude %{_mandir}/man1/ldbadd.1*
%exclude %{_mandir}/man1/ldbdel.1*
%exclude %{_mandir}/man1/ldbedit.1*
%exclude %{_mandir}/man1/ldbmodify.1*
%exclude %{_mandir}/man1/ldbrename.1*
%exclude %{_mandir}/man1/ldbsearch.1*
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_mandir}/man8/*

%files libs
%defattr(-,root,root,-)
%{_libdir}/libdcerpc-binding.so.*
%{_libdir}/libdcerpc.so.*
%{_libdir}/libdcerpc-server-core.so.*
%{_libdir}/libndr.so.*
%{_libdir}/libndr-krb5pac.so.*
%{_libdir}/libndr-nbt.so.*
%{_libdir}/libndr-standard.so.*
%{_libdir}/libnetapi.so.*
%{_libdir}/libsamba-credentials.so.*
%{_libdir}/libsamba-errors.so.*
%{_libdir}/libsamba-passdb.so.*
%{_libdir}/libsamba-util.so.*
%{_libdir}/libsamba-hostconfig.so.*
%{_libdir}/libsamdb.so.*
%{_libdir}/libsmbconf.so.*
%{_libdir}/libsmbldap.so.*
%{_libdir}/libtevent-util.so.*
%{_libdir}/libsmbclient.so.*
%dir %{_libdir}/samba
%{_libdir}/samba/libaddns-private-samba.so
%{_libdir}/samba/libads-private-samba.so
%{_libdir}/samba/libasn1util-private-samba.so
%{_libdir}/samba/libauth-private-samba.so
%{_libdir}/samba/libauthkrb5-private-samba.so
%{_libdir}/samba/libCHARSET3-private-samba.so
%{_libdir}/samba/libcliauth-private-samba.so
%{_libdir}/samba/libcli-cldap-private-samba.so
%{_libdir}/samba/libclidns-private-samba.so
%{_libdir}/samba/libcli-ldap-common-private-samba.so
%{_libdir}/samba/libcli-ldap-private-samba.so
%{_libdir}/samba/libcli-nbt-private-samba.so
%{_libdir}/samba/libcli-smb-common-private-samba.so
%{_libdir}/samba/libcli-spoolss-private-samba.so
%{_libdir}/samba/libcluster-private-samba.so
%{_libdir}/samba/libcmdline-contexts-private-samba.so
%{_libdir}/samba/libcmdline-private-samba.so
%{_libdir}/samba/libcommon-auth-private-samba.so
%{_libdir}/samba/libdbwrap-private-samba.so
%{_libdir}/samba/libdcerpc-pkt-auth-private-samba.so
%{_libdir}/samba/libdcerpc-samba4-private-samba.so
%{_libdir}/samba/libdcerpc-samba-private-samba.so
%{_libdir}/samba/libdnsserver-common-private-samba.so
%{_libdir}/samba/libevents-private-samba.so
%{_libdir}/samba/libflag-mapping-private-samba.so
%{_libdir}/samba/libgenrand-private-samba.so
%{_libdir}/samba/libgensec-private-samba.so
%{_libdir}/samba/libgpext-private-samba.so
%{_libdir}/samba/libgpo-private-samba.so
%{_libdir}/samba/libgse-private-samba.so
%{_libdir}/samba/libhttp-private-samba.so
%{_libdir}/samba/libinterfaces-private-samba.so
%{_libdir}/samba/libiov-buf-private-samba.so
%{_libdir}/samba/libkrb5samba-private-samba.so
%{_libdir}/samba/liblibcli-lsa3-private-samba.so
%{_libdir}/samba/liblibcli-netlogon3-private-samba.so
%{_libdir}/samba/liblibsmb-private-samba.so
%{_libdir}/samba/libmessages-dgm-private-samba.so
%{_libdir}/samba/libmessages-util-private-samba.so
%{_libdir}/samba/libMESSAGING-private-samba.so
%{_libdir}/samba/libMESSAGING-SEND-private-samba.so
%{_libdir}/samba/libmscat-private-samba.so
%{_libdir}/samba/libmsghdr-private-samba.so
%{_libdir}/samba/libmsrpc3-private-samba.so
%{_libdir}/samba/libndr-samba4-private-samba.so
%{_libdir}/samba/libndr-samba-private-samba.so
%{_libdir}/samba/libnetif-private-samba.so
%{_libdir}/samba/libnet-keytab-private-samba.so
%{_libdir}/samba/libngtcp2-crypto-gnutls-private-samba.so
%{_libdir}/samba/libngtcp2-private-samba.so
%{_libdir}/samba/libnpa-tstream-private-samba.so
%{_libdir}/samba/libposix-eadb-private-samba.so
%{_libdir}/samba/libprinter-driver-private-samba.so
%{_libdir}/samba/libprinting-migrate-private-samba.so
%{_libdir}/samba/libquic-private-samba.so
%{_libdir}/samba/libregistry-private-samba.so
%{_libdir}/samba/libreplace-private-samba.so
%{_libdir}/samba/libRPC-SERVER-LOOP-private-samba.so
%{_libdir}/samba/libRPC-WORKER-private-samba.so
%{_libdir}/samba/libsamba3-util-private-samba.so
%{_libdir}/samba/libsamba-cluster-support-private-samba.so
%{_libdir}/samba/libsamba-debug-private-samba.so
%{_libdir}/samba/libsamba-modules-private-samba.so
%{_libdir}/samba/libsamba-net-private-samba.so
%{_libdir}/samba/libsamba-security-private-samba.so
%{_libdir}/samba/libsamba-security-trusts-private-samba.so
%{_libdir}/samba/libsamba-sockets-private-samba.so
%{_libdir}/samba/libsamdb-common-private-samba.so
%{_libdir}/samba/libsecrets3-private-samba.so
%{_libdir}/samba/libserver-id-db-private-samba.so
%{_libdir}/samba/libserver-role-private-samba.so
%{_libdir}/samba/libsmbclient-raw-private-samba.so
%{_libdir}/samba/libsmbd-base-private-samba.so
%{_libdir}/samba/libsmbd-shim-private-samba.so
%{_libdir}/samba/libsmbldaphelper-private-samba.so
%{_libdir}/samba/libsocket-blocking-private-samba.so
%{_libdir}/samba/libstable-sort-private-samba.so
%{_libdir}/samba/libsys-rw-private-samba.so
%{_libdir}/samba/libtalloc-report-printf-private-samba.so
%{_libdir}/samba/libtalloc-report-private-samba.so
%{_libdir}/samba/libtdb-wrap-private-samba.so
%{_libdir}/samba/libtime-basic-private-samba.so
%{_libdir}/samba/libtorture-private-samba.so
%{_libdir}/samba/libutil-crypt-private-samba.so
%{_libdir}/samba/libutil-reg-private-samba.so
%{_libdir}/samba/libutil-setid-private-samba.so
%{_libdir}/samba/libutil-tdb-private-samba.so
%dir %{_libdir}/samba/pdb
%{_libdir}/samba/pdb/ldapsam.so
%{_libdir}/samba/pdb/smbpasswd.so
%{_libdir}/samba/pdb/tdbsam.so

%files devel
%defattr(-,root,root,-)
%{_includedir}/samba-%{maj_ver}/libsmbclient.h
%{_includedir}/samba-%{maj_ver}/core/*.h
%{_includedir}/samba-%{maj_ver}/samba/version.h
%{_includedir}/samba-%{maj_ver}/ndr.h
%{_includedir}/samba-%{maj_ver}/smb3posix.h
%{_includedir}/samba-%{maj_ver}/util/discard.h
%{_includedir}/samba-%{maj_ver}/util/data_blob.h
%{_includedir}/samba-%{maj_ver}/util/talloc_keep_secret.h
%{_includedir}/samba-%{maj_ver}/util/time.h
%{_includedir}/samba-%{maj_ver}/charset.h
%{_includedir}/samba-%{maj_ver}/gen_ndr/*
%{_includedir}/samba-%{maj_ver}/ndr/*
%{_libdir}/libdcerpc.so
%{_libdir}/libdcerpc-binding.so
%{_libdir}/libdcerpc-server-core.so
%{_libdir}/libsmbclient.so
%{_libdir}/libndr-krb5pac.so
%{_libdir}/libndr-nbt.so
%{_libdir}/libndr-standard.so
%{_libdir}/libndr.so
%{_libdir}/libnetapi.so
%{_libdir}/libsamba-credentials.so
%{_libdir}/libsamba-errors.so
%{_libdir}/libsamba-hostconfig.so
%{_libdir}/libsamba-passdb.so
%{_libdir}/libsamba-util.so
%{_libdir}/libsamdb.so
%{_libdir}/libsmbconf.so
%{_libdir}/libsmbldap.so
%{_libdir}/libtevent-util.so
%{_libdir}/samba/libidmap-private-samba.so
%{_libdir}/pkgconfig/ndr*.pc
%{_libdir}/pkgconfig/samba-util.pc
%{_libdir}/pkgconfig/smbclient.pc

%files -n libwbclient
%defattr(-,root,root,-)
%{_libdir}/libwbclient.so.*

%files -n libwbclient-devel
%defattr(-,root,root,-)
%dir %_includedir/samba-%{maj_ver}/
%{_includedir}/samba-%{maj_ver}/wbclient.h
%{_libdir}/libwbclient.so
%{_libdir}/pkgconfig/wbclient.pc

%files -n libldb
%defattr(-,root,root,-)
%{_libdir}/libldb.so.*
%dir %{_libdir}/samba
%{_libdir}/samba/libldb-cmdline-private-samba.so
%{_libdir}/samba/libldb-key-value-private-samba.so
%{_libdir}/samba/libldb-tdb-err-map-private-samba.so
%{_libdir}/samba/libldb-tdb-int-private-samba.so
%{_libdir}/samba/libldbsamba-private-samba.so
%dir %{_libdir}/samba/ldb
%{_libdir}/samba/ldb/*.so

%files -n libldb-devel
%defattr(-,root,root,-)
%{_includedir}/samba-%{maj_ver}/ldb.h
%{_includedir}/samba-%{maj_ver}/ldb_module.h
%{_includedir}/samba-%{maj_ver}/ldb_handlers.h
%{_includedir}/samba-%{maj_ver}/ldb_errors.h
%{_includedir}/samba-%{maj_ver}/ldb_version.h
%{_includedir}/samba-%{maj_ver}/ldb_wrap.h
%{_libdir}/libldb.so
%{_libdir}/pkgconfig/ldb.pc

%files -n ldb-tools
%defattr(-,root,root,-)
%{_bindir}/ldbadd
%{_bindir}/ldbdel
%{_bindir}/ldbedit
%{_bindir}/ldbmodify
%{_bindir}/ldbrename
%{_bindir}/ldbsearch

%files -n ldb-docs
%defattr(-,root,root,-)
%{_mandir}/man1/ldbadd.1.*
%{_mandir}/man1/ldbdel.1.*
%{_mandir}/man1/ldbedit.1.*
%{_mandir}/man1/ldbmodify.1.*
%{_mandir}/man1/ldbrename.1.*
%{_mandir}/man1/ldbsearch.1.*
%{_mandir}/man3/ldb*.gz

%files -n python3-ldb -f %{py_ghost_filelist}
%defattr(-,root,root,-)
%{python3_sitearch}/ldb.cpython-*.so
%{python3_sitearch}/_ldb_text.py
%{_libdir}/samba/libpyldb-util.cpython-*-private-samba.so

%changelog
* Sat Aug 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 4.24.5-3
- Extend to build for 91 and above
* Sat Aug 08 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.24.5-2
- Minor fixes qith requires and add Obsoletes for python3-;db-devel
* Thu Jul 30 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 4.24.5-1
- Upgrade to 4.24.5; fix CVE-2026-4408 and CVE-2026-4480
* Tue Jun 16 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 4.19.3-20
- Fix CVE-2026-4480
- Fix CVE-2026-4408
* Mon Jun 8 2026 Michelle Wang <michelle.wang@broadcom.com> 4.19.3-19
- Bump release due to bindutils upgrade
* Wed Jun 03 2026 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 4.19.3-18
- Release version bump as part of libxml2/libxslt
* Fri May 29 2026 Dweep Advani <dweep.advani@broadcom.com> 4.19.3-17
- bump for perl 5.42.2
* Thu May 28 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 4.19.3-16
- Bump release due to bindutils upgrade
* Wed May 27 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 4.19.3-15
- Remove deprecated python3-defusedxml from BuildRequires
* Tue May 26 2026 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 4.19.3-14
- Remove runtime depedency of perl-Parse-Yapp
* Sat May 16 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.19.3-13
- Extended to build for subrelease 91 and above
* Tue May 05 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> - 4.19.3-12
- Version bump due to gnutls update
* Fri Apr 24 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 4.19.3-11
- Fix build with latest glibc
* Mon Apr 13 2026 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 4.19.3-10
- Bump version as a part of libarchive upgrade
* Tue Mar 31 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 4.19.3-9
- Remove BuildRequires: xmlto; confirmed xmlto not used in samba 4.19.3 build system
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 4.19.3-8
- Bump version as a part of python3.14 upgrade
* Mon Jan 05 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.19.3-7
- Build with system provided mit krb5
- Fix CVE-2025-9640
* Tue Nov 04 2025 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 4.19.3-6
- Bump version as a part of libarchive upgrade
* Mon Oct 27 2025 Ankit Jain <ankit-aj.jain@broadcom.com> 4.19.3-5
- Bump up to build with latest jansson
* Tue Oct 21 2025 Michelle Wang <michelle.wang@broadcom.com> 4.19.3-4
- Fix CVE-2025-10230
* Tue Aug 26 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 4.19.3-3
- Bump version as a part of ncurses upgrade
* Thu Aug 07 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 4.19.3-2
- config.yaml changes
* Fri Apr 11 2025 Michelle Wang <michelle.wang@broadcom.com> 4.19.3-1
- Bump up version to 4.19.3 for CVE-2023-5568 and CVE-2018-14628
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.18.8-4
- Release bump for SRP compliance
* Fri Jan 05 2024 Mukul Sikka <msikka@vmwrae.com> 4.18.8-3
- Bump version as a part of sudo upgrade
* Wed Nov 29 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.18.8-2
- Bump version as a part of gnutls upgrade
* Mon Nov 27 2023 Harinadh D <hdommaraju@vmwrae.com> 4.18.8-1
- fix CVE-2023-3961
* Tue Sep 19 2023 Nitesh Kumar <kunitesh@vmware.com> 4.18.5-3
- Bump version as a part of openldap v2.6.4 upgrade
* Mon Jul 31 2023 Mukul Sikka <msikka@vmware.com> 4.18.5-2
- Bump version as a part of sudo upgrade
* Thu Jul 27 2023 Oliver Kurth <okurth@vmware.com> 4.18.5-1
- update to 4.18.5 including various CVE fixes
* Thu Jun 29 2023 Anmol Jain <anmolja@vmware.com> 4.18.3-2
- Version bump up to use sudo
* Tue Jun 13 2023 Oliver Kurth <okurth@vmware.com> 4.18.3-1
- update to 4.18.3 including various CVE fixes
* Thu Jun 01 2023 Nitesh Kumar <kunitesh@vmware.com> 4.17.5-3
- Bump version as a part of ncurses upgrade to v6.4
* Thu May 25 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.17.5-2
- Bump version as a part of libxml2 upgrade
* Tue Feb 14 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 4.17.5-1
- Upgrade version for SSSD addition. Include some additional needed libraries.
* Wed Feb 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.14.4-9
- Bump version as a part of openldap upgrade
* Thu Dec 08 2022 Dweep Advani <dadvani@vmware.com> 4.14.4-8
- Rebuild for perl version upgrade to 5.36.0
* Tue Dec 06 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.14.4-7
- Bump version as a part of libtalloc upgrade
* Sun Nov 13 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.14.4-6
- Bump version as a part of libtirpc upgrade
* Fri Oct 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.14.4-5
- Bump version as a part of libxslt upgrade
* Tue Aug 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.14.4-4
- Bump version as a part of gnutls upgrade
* Thu Jun 16 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 4.14.4-3
- Bump version as a part of libxslt upgrade
* Wed Nov 17 2021 Nitesh Kumar <kunitesh@vmware.com> 4.14.4-2
- Release bump up to use libxml2 2.9.12-1.
* Thu May 06 2021 Shreyas B. <shreyasb@vmware.com> 4.14.4-1
- Split libwclient from samba-client and create separate package.
- Upgrade to version 4.14.4
* Fri Feb 19 2021 Shreyas B. <shreyasb@vmware.com> 4.13.4-1
- Upgrade to version 4.13.4
* Fri May 29 2020 Shreyas B. <shreyasb@vmware.com> 4.12.0-1
- Initial version of samba spec.
