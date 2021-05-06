Summary:        Samba Client Programs
Name:           samba-client
Version:        4.14.4
Release:        1%{?dist}
License:        GPLv3+ and LGPLv3+
Group:          Productivity/Networking
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://www.samba.org
Source0:        https://www.samba.org/ftp/samba/stable/samba-%{version}.tar.gz
%define sha1 samba=123281ce6b0049648be3bd4fe7094057526d6340
%define samba_ver %{version}-%{release}
Source1:        smb.conf.vendor

Patch1:         rename_dcerpc_to_smbdcerpc_%{version}.patch

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildRequires: libtirpc-devel
BuildRequires: rpcsvc-proto-devel
BuildRequires: python3-devel
BuildRequires: libarchive
BuildRequires: libarchive-devel
BuildRequires: Linux-PAM-devel
BuildRequires: xmlto
BuildRequires: python3-defusedxml
BuildRequires: libxslt-devel
BuildRequires: libxslt
BuildRequires: docbook-xsl
BuildRequires: docbook-xml
BuildRequires: gcc
BuildRequires: gnutls-devel >= 3.4.7
BuildRequires: jansson-devel
BuildRequires: libxml2-devel
BuildRequires: lmdb
BuildRequires: openldap
BuildRequires: perl-Parse-Yapp
BuildRequires: dbus-devel

Requires:      samba-client-libs = %{samba_ver}
Requires:      libtirpc
Requires:      python3
Requires:      libarchive
Requires:      Linux-PAM
Requires:      libxslt
Requires:      gnutls
Requires:      jansson
Requires:      libxml2
Requires:      lmdb
Requires:      openldap
Requires:      perl-Parse-Yapp
Requires:      dbus

Provides:      samba4-client = %{samba_ver}

# Samba Client
%description
Samba is the standard Windows interoperability suite of programs for Linux and Unix.
The samba-client package provides file and print services to SMB/CIFS clients
and Windows networking to Linux clients.
For a more detailed description of Samba, check the Web page https://www.Samba.org/

# Samba Client Libaries
%package -n samba-client-libs
Summary: Samba client libraries

%description -n samba-client-libs
The samba-client-libs package contains internal libraries needed by the
SMB/CIFS clients.

# Samba Client Devel
%package -n samba-client-devel
Summary: Developer tools for Samba-Client libraries
Requires: samba-client = %{samba_ver}

%description -n samba-client-devel
The samba-client-devel package contains the header files and libraries needed
to develop programs.

# Winbind Client
%package -n libwbclient
Summary:        Samba libwbclient Library
Group:          System/Libraries

%description -n libwbclient
This package includes the wbclient library.

%package -n libwbclient-devel
Summary:        Libraries and Header Files to Develop Programs with wbclient Support
Group:          Development/Libraries/C and C++
Requires:       libwbclient = %{version}

%description -n libwbclient-devel
This package contains the static libraries and header files needed to
develop programs which make use of the wbclient programming interface.

%prep
%setup -n samba-%{version}
%patch1 -p1

%build
echo "^samba4.rpc.echo.*on.*ncacn_np.*with.*object.*nt4_dc" >> selftest/knownfail

%global _samba_pdb_modules pdb_tdbsam,pdb_ldap,pdb_smbpasswd,pdb_wbc_sam,pdb_samba4
%global _samba_modules %{_samba_pdb_modules}

export CFLAGS="-I/usr/include/tirpc"
export LDFLAGS="-ltirpc"

%configure \
        --enable-fhs \
        --with-piddir=/run \
        --with-sockets-dir=/run/samba \
        --with-modulesdir=%{_libdir}/samba \
        --with-pammodulesdir=%{_libdir}/security \
        --with-lockdir=/var/lib/samba/lock \
        --with-statedir=/var/lib/samba \
        --with-cachedir=/var/lib/samba \
        --without-gettext \
        --without-ldb-lmdb \
        --without-lttng \
        --without-ad-dc \
        --without-systemd  \
        --without-acl-support \
        --with-shared-modules=%{_samba_modules} \
        --disable-python \
        --without-ads \
        --without-ntvfs-fileserver &&
make bin/smbclient %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} %{?_smp_mflags}

# Install other stuff
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/samba/smb.conf

# Create /run/samba.
install -d -m 0755 %{buildroot}/%{_tmpfilesdir}
echo "d /run/samba  755 root root" > %{buildroot}%{_tmpfilesdir}/samba.conf

install -d -m 0755 %{buildroot}%{_sysconfdir}/sysconfig
install -m 0644 packaging/systemd/samba.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/samba

# Delete Unpackaged File(s)
for file_dir in \
   %{_libdir}/samba/vfs/* \
   %{_libdir}/samba/libkdc-* \
   %{_libdir}/samba/libldb-* \
   %{_libdir}/samba/libpyldb-* \
   %{_libdir}/samba/libpytalloc-* \
   %{_libdir}/samba/nss_info/* \
   %{_libdir}/samba/idmap/* \
   %{_libdir}/samba/krb5/winbind_krb5_locator.so \
   %{_libdir}/samba/krb5/async_dns_krb5_locator.so \
   %{_libdir}/samba/ldb/asq.so \
   %{_libdir}/samba/ldb/ildap.so \
   %{_libdir}/samba/ldb/ldb.so \
   %{_libdir}/samba/ldb/ldbsamba_extensions.so \
   %{_libdir}/samba/ldb/paged_searches.so \
   %{_libdir}/samba/ldb/rdn_name.so \
   %{_libdir}/samba/ldb/sample.so \
   %{_libdir}/samba/ldb/server_sort.so \
   %{_libdir}/samba/ldb/skel.so \
   %{_libdir}/samba/ldb/tdb.so \
   %{_libdir}/samba/libLIBWBCLIENT-OLD-samba4.so \
   %{_libdir}/samba/libauth-unix-token-samba4.so \
   %{_libdir}/samba/libauth4-samba4.so \
   %{_libdir}/samba/libcmocka-samba4.so \
   %{_libdir}/samba/libdcerpc-samba4.so \
   %{_libdir}/samba/libdsdb-module-samba4.so \
   %{_libdir}/samba/libhdb-* \
   %{_libdir}/samba/libheimntlm-samba4.so.* \
   %{_libdir}/samba/libidmap-samba4.so \
   %{_libdir}/samba/libnss-info-samba4.so \
   %{_libdir}/samba/libsamba-net.cpython-37m-x86-64-linux-gnu-samba4.so \
   %{_libdir}/samba/libsamba-python.cpython-37m-x86-64-linux-gnu-samba4.so \
   %{_libdir}/samba/libshares-samba4.so \
   %{_libdir}/samba/libsmbpasswdparser-samba4.so \
   %{_libdir}/samba/libxattr-tdb-samba4.so \
   %{_libdir}/security/pam_winbind.so \
   %{_libdir}/libdcerpc-samr.* \
   %{_libdir}/libnss_winbind.so* \
   %{_libdir}/libnss_wins.so* \
   %{_libdir}/libsamba-policy.cpython-37m-x86-64-linux-gnu.* \
   %{_libdir}/pkgconfig/dcerpc.pc \
   %{_libdir}/pkgconfig/dcerpc_samr.pc \
   %{_libdir}/pkgconfig/ndr.pc \
   %{_libdir}/pkgconfig/ndr_* \
   %{_libdir}/pkgconfig/netapi.pc \
   %{_libdir}/pkgconfig/samba-credentials.pc \
   %{_libdir}/pkgconfig/samba-hostconfig.pc \
   %{_libdir}/pkgconfig/samba-policy.cpython-37m-*-linux-gnu.pc \
   %{_libdir}/pkgconfig/samba-util.pc \
   %{_libdir}/pkgconfig/samdb.pc \
   %{_libdir}/samba/auth/unix.so \
   %{_sbindir}/eventlogadm \
   %{_sbindir}/nmbd \
   %{_sbindir}/samba-gpupdate \
   %{_sbindir}/smbd \
   %{_sbindir}/winbindd \
   /etc/openldap/schema/samba.schema \
   /etc/pam.d/samba \
   %{_bindir}/async_connect_send_test \
   %{_bindir}/dns_lookuptest \
   %{_bindir}/gentest \
   %{_bindir}/ldb* \
   %{_bindir}/locktest \
   %{_bindir}/locktest2 \
   %{_bindir}/masktest \
   %{_bindir}/ndrdump \
   %{_bindir}/net \
   %{_bindir}/nsstest \
   %{_bindir}/ntlm_auth \
   %{_bindir}/pdbedit \
   %{_bindir}/pdbtest \
   %{_bindir}/profiles \
   %{_bindir}/pthreadpooltest \
   %{_bindir}/pthreadpooltest_cmocka \
   %{_bindir}/resolvconftest \
   %{_bindir}/rpc_open_tcp \
   %{_bindir}/smbconftort \
   %{_bindir}/smbcontrol \
   %{_bindir}/smbpasswd \
   %{_bindir}/smbspool_argv_wrapper \
   %{_bindir}/smbstatus \
   %{_bindir}/smbtorture \
   %{_bindir}/smbtorture3 \
   %{_bindir}/stress-nss-libwbclient \
   %{_bindir}/tdbbackup \
   %{_bindir}/tdbdump \
   %{_bindir}/tdbrestore \
   %{_bindir}/tdbtool \
   %{_bindir}/test_* \
   %{_bindir}/testparm \
   %{_bindir}/tevent_glib_glue_test \
   %{_bindir}/texpect \
   %{_bindir}/timelimit \
   %{_bindir}/vfstest \
   %{_bindir}/vlp \
   %{_bindir}/wbinfo \
   %{_includedir}/samba-4.0/util/* \
   %{_includedir}/samba-4.0/core/* \
   %{_includedir}/samba-4.0/charset.h \
   %{_includedir}/samba-4.0/credentials.h \
   %{_includedir}/samba-4.0/dcerpc.h \
   %{_includedir}/samba-4.0/dcesrv_core.h \
   %{_includedir}/samba-4.0/domain_credentials.h \
   %{_includedir}/samba-4.0/gen_ndr/* \
   %{_includedir}/samba-4.0/ldb_wrap.h \
   %{_includedir}/samba-4.0/lookup_sid.h \
   %{_includedir}/samba-4.0/machine_sid.h \
   %{_includedir}/samba-4.0/ndr.h \
   %{_includedir}/samba-4.0/ndr/* \
   %{_includedir}/samba-4.0/netapi.h \
   %{_includedir}/samba-4.0/param.h \
   %{_includedir}/samba-4.0/passdb.h \
   %{_includedir}/samba-4.0/rpc_common.h \
   %{_includedir}/samba-4.0/samba/session.h \
   %{_includedir}/samba-4.0/samba/version.h \
   %{_includedir}/samba-4.0/share.h \
   %{_includedir}/samba-4.0/smb* \
   %{_includedir}/samba-4.0/tdr.h \
   %{_includedir}/samba-4.0/tsocket.h \
   %{_includedir}/samba-4.0/tsocket_internal.h \
   %{_includedir}/samba-4.0/util_ldb.h \
   %{_mandir}/man1/gentest.1.gz \
   %{_mandir}/man1/ldb* \
   %{_mandir}/man1/locktest.1.gz \
   %{_mandir}/man1/masktest.1.gz \
   %{_mandir}/man1/ndrdump.1.gz \
   %{_mandir}/man1/ntlm_auth.1.gz \
   %{_mandir}/man1/profiles.1.gz \
   %{_mandir}/man1/smbcontrol.1.gz \
   %{_mandir}/man1/smbstatus.1.gz \
   %{_mandir}/man1/smbtorture.1.gz \
   %{_mandir}/man1/testparm.1.gz \
   %{_mandir}/man1/vfstest.1.gz \
   %{_mandir}/man1/wbinfo.1.gz \
   %{_mandir}/man3/ldb.3.gz \
   %{_mandir}/man3/talloc.3.gz \
   %{_mandir}/man5/pam_winbind.conf.5.gz \
   %{_mandir}/man5/lmhosts.5.gz \
   %{_mandir}/man7/libsmbclient.7.gz \
   %{_mandir}/man8/eventlogadm.8.gz \
   %{_mandir}/man8/net.8.gz \
   %{_mandir}/man8/nmbd.8.gz \
   %{_mandir}/man8/pam_winbind.8.gz \
   %{_mandir}/man8/pdbedit.8.gz \
   %{_mandir}/man8/samba-gpupdate.8.gz \
   %{_mandir}/man8/samba-tool.8.gz \
   %{_mandir}/man8/samba.8.gz \
   %{_mandir}/man8/samba_downgrade_db.8.gz \
   %{_mandir}/man8/smbd.8.gz \
   %{_mandir}/man8/smbpasswd.8.gz \
   %{_mandir}/man8/smbspool_krb5_wrapper.8.gz \
   %{_mandir}/man8/tdbbackup.8.gz \
   %{_mandir}/man8/tdbdump.8.gz \
   %{_mandir}/man8/tdbrestore.8.gz \
   %{_mandir}/man8/tdbtool.8.gz \
   %{_mandir}/man8/winbind_krb5_locator.8.gz \
   %{_mandir}/man8/winbindd.8.gz \
   %{_mandir}/man8/idmap* \
   %{_mandir}/man8/tdb* \
   %{_mandir}/man8/vfs* \
   %{_mandir}/man8/winbind* \
   ; do \
   rm -rf %{buildroot}$file_dir
done

# Delete Unpackaged aarch64 File(s)
%ifarch aarch64
for aarch64_file_dir in \
   %{_libdir}/libsamba-policy.cpython-37m-aarch64-linux-gnu.* \
   %{_libdir}/samba/libsamba-net.cpython-37m-aarch64-linux-gnu-samba4.so \
   %{_libdir}/samba/libsamba-python.cpython-37m-aarch64-linux-gnu-samba4.so \
   ; do
   rm -f %{buildroot}$aarch64_file_dir
done
%endif

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%post libs
/sbin/ldconfig

%postun libs
/sbin/ldconfig

# Samba Client
%files
%defattr(-,root,root,-)
%doc source3/client/README.smbspool
%{_bindir}/cifsdd
%{_bindir}/dbwrap_tool
%{_bindir}/dumpmscat
%{_bindir}/findsmb
%{_bindir}/mvxattr
%{_bindir}/mdfind
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
%ghost %{_libexecdir}/samba/cups_backend_smb
%{_tmpfilesdir}/samba.conf
%attr(0700,root,root) %dir /var/log/samba
%ghost %dir /run/samba
%ghost %dir /run/winbindd
%dir /var/lib/samba
%attr(700,root,root) %dir /var/lib/samba/private
%dir /var/lib/samba/lock
%attr(755,root,root) %dir %{_sysconfdir}/samba
%config(noreplace) %{_sysconfdir}/samba/smb.conf
%config(noreplace) %{_sysconfdir}/sysconfig/samba
%{_mandir}/man1/dbwrap_tool.1*
%{_mandir}/man1/nmblookup.1*
%{_mandir}/man1/oLschema2ldif.1*
%{_mandir}/man1/regdiff.1*
%{_mandir}/man1/regpatch.1*
%{_mandir}/man1/regshell.1*
%{_mandir}/man1/regtree.1*
%{_mandir}/man1/findsmb.1*
%{_mandir}/man1/log2pcap.1*
%{_mandir}/man1/mdfind.1*
%{_mandir}/man1/mvxattr.1*
%{_mandir}/man1/rpcclient.1*
%{_mandir}/man1/sharesec.1*
%{_mandir}/man1/smbcacls.1*
%{_mandir}/man1/smbclient.1*
%{_mandir}/man1/smbcquotas.1*
%{_mandir}/man1/smbget.1*
%{_mandir}/man1/smbtar.1*
%{_mandir}/man1/smbtree.1*
%{_mandir}/man5/smbgetrc.5*
%{_mandir}/man7/traffic_learner.7.*
%{_mandir}/man7/traffic_replay.7.*
%{_mandir}/man8/cifsdd.8.*
%{_mandir}/man8/samba-regedit.8*
%{_mandir}/man8/smbspool.8*
%{_mandir}/man5/smb.conf.5*
%{_mandir}/man5/smbpasswd.5*
%{_mandir}/man7/samba.7*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_mandir}/man8/*

# Client libraries
%files -n samba-client-libs
%defattr(-,root,root,-)
%{_libdir}/libdcerpc-binding.so.*
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
%{_libdir}/libsmbdcerpc.so.*
%{_libdir}/libsmbclient.so.*
%dir %{_libdir}/samba
%{_libdir}/samba/libCHARSET3-samba4.so
%{_libdir}/samba/libMESSAGING-SEND-samba4.so
%{_libdir}/samba/libMESSAGING-samba4.so
%{_libdir}/samba/libaddns-samba4.so
%{_libdir}/samba/libads-samba4.so
%{_libdir}/samba/libasn1util-samba4.so
%{_libdir}/samba/libauth-samba4.so
%{_libdir}/samba/libauthkrb5-samba4.so
%{_libdir}/samba/libcli-cldap-samba4.so
%{_libdir}/samba/libcli-ldap-common-samba4.so
%{_libdir}/samba/libcli-ldap-samba4.so
%{_libdir}/samba/libcli-nbt-samba4.so
%{_libdir}/samba/libcli-smb-common-samba4.so
%{_libdir}/samba/libcli-spoolss-samba4.so
%{_libdir}/samba/libcliauth-samba4.so
%{_libdir}/samba/libclidns-samba4.so
%{_libdir}/samba/libcluster-samba4.so
%{_libdir}/samba/libcmdline-contexts-samba4.so
%{_libdir}/samba/libcmdline-credentials-samba4.so
%{_libdir}/samba/libcommon-auth-samba4.so
%{_libdir}/samba/libdbwrap-samba4.so
%{_libdir}/samba/libdcerpc-samba-samba4.so
%{_libdir}/samba/libevents-samba4.so
%{_libdir}/samba/libflag-mapping-samba4.so
%{_libdir}/samba/libgenrand-samba4.so
%{_libdir}/samba/libgensec-samba4.so
%{_libdir}/samba/libgpext-samba4.so
%{_libdir}/samba/libgpo-samba4.so
%{_libdir}/samba/libgse-samba4.so
%{_libdir}/samba/libhttp-samba4.so
%{_libdir}/samba/libinterfaces-samba4.so
%{_libdir}/samba/libiov-buf-samba4.so
%{_libdir}/samba/libkrb5samba-samba4.so
%{_libdir}/samba/libldbsamba-samba4.so
%{_libdir}/samba/liblibcli-lsa3-samba4.so
%{_libdir}/samba/liblibcli-netlogon3-samba4.so
%{_libdir}/samba/liblibsmb-samba4.so
%{_libdir}/samba/libmessages-dgm-samba4.so
%{_libdir}/samba/libmessages-util-samba4.so
%{_libdir}/samba/libmscat-samba4.so
%{_libdir}/samba/libmsghdr-samba4.so
%{_libdir}/samba/libmsrpc3-samba4.so
%{_libdir}/samba/libndr-samba-samba4.so
%{_libdir}/samba/libndr-samba4.so
%{_libdir}/samba/libnet-keytab-samba4.so
%{_libdir}/samba/libnetif-samba4.so
%{_libdir}/samba/libnpa-tstream-samba4.so
%{_libdir}/samba/libposix-eadb-samba4.so
%{_libdir}/samba/libprinter-driver-samba4.so
%{_libdir}/samba/libprinting-migrate-samba4.so
%{_libdir}/samba/libreplace-samba4.so
%{_libdir}/samba/libregistry-samba4.so
%{_libdir}/samba/libsamba-cluster-support-samba4.so
%{_libdir}/samba/libsamba-debug-samba4.so
%{_libdir}/samba/libsamba-modules-samba4.so
%{_libdir}/samba/libsamba-security-samba4.so
%{_libdir}/samba/libsamba-sockets-samba4.so
%{_libdir}/samba/libsamba3-util-samba4.so
%{_libdir}/samba/libsamdb-common-samba4.so
%{_libdir}/samba/libsecrets3-samba4.so
%{_libdir}/samba/libserver-id-db-samba4.so
%{_libdir}/samba/libserver-role-samba4.so
%{_libdir}/samba/libsmb-transport-samba4.so
%{_libdir}/samba/libsmbclient-raw-samba4.so
%{_libdir}/samba/libsmbd-base-samba4.so
%{_libdir}/samba/libsmbd-shim-samba4.so
%{_libdir}/samba/libsmbldaphelper-samba4.so
%{_libdir}/samba/libsys-rw-samba4.so
%{_libdir}/samba/libsocket-blocking-samba4.so
%{_libdir}/samba/libtalloc-report-printf-samba4.so
%{_libdir}/samba/libtalloc-report-samba4.so
%{_libdir}/samba/libtdb-wrap-samba4.so
%{_libdir}/samba/libtime-basic-samba4.so
%{_libdir}/samba/libtorture-samba4.so
%{_libdir}/samba/libtrusts-util-samba4.so
%{_libdir}/samba/libutil-cmdline-samba4.so
%{_libdir}/samba/libutil-reg-samba4.so
%{_libdir}/samba/libutil-setid-samba4.so
%{_libdir}/samba/libutil-tdb-samba4.so
%{_libdir}/samba/libasn1-samba4.so.*
%{_libdir}/samba/libgssapi-samba4.so.*
%{_libdir}/samba/libcom_err-samba4.so.*
%{_libdir}/samba/libkrb5-samba4.so.*
%{_libdir}/samba/libldb.so.*
%{_libdir}/samba/libtdb.so.*
%{_libdir}/samba/libtevent.so.*
%{_libdir}/samba/libtalloc.so.*
%{_libdir}/samba/libhcrypto-samba4.so.*
%{_libdir}/samba/libheimbase-samba4.so.*
%{_libdir}/samba/libhx509-samba4.so.*
%{_libdir}/samba/libroken-samba4.so.*
%{_libdir}/samba/libwinbind-client-samba4.so
%{_libdir}/samba/libwind-samba4.so.*
%{_libdir}/samba/libpopt-samba3-cmdline-samba4.so
%{_libdir}/samba/libpopt-samba3-samba4.so
%dir %{_libdir}/samba/ldb
%dir %{_libdir}/samba/pdb
%{_libdir}/samba/pdb/ldapsam.so
%{_libdir}/samba/pdb/smbpasswd.so
%{_libdir}/samba/pdb/tdbsam.so
%{_libdir}/libdcerpc-server-core.*

# Devel
%files -n samba-client-devel
%{_includedir}/samba-4.0/libsmbclient.h
%{_libdir}/libsmbclient.so
%{_libdir}/libsmbdcerpc.so
%{_libdir}/libdcerpc-binding.so
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
%{_libdir}/pkgconfig/smbclient.pc
%{_mandir}/man7/libsmbclient.7*

# Winbind Client
%files -n libwbclient
%defattr(-,root,root,-)
%{_libdir}/libwbclient.so.*

%files -n libwbclient-devel
%defattr(-,root,root,-)
%dir %_includedir/samba-4.0/
%{_includedir}/samba-4.0/wbclient.h
%{_libdir}/libwbclient.so
%{_libdir}/pkgconfig/wbclient.pc

%changelog
*   Thu May 06 2021 Shreyas B. <shreyasb@vmware.com> 4.14.4-1
-   Split libwclient from samba-client and create separate package.
-   Upgrade to version 4.14.4
*   Fri Feb 19 2021 Shreyas B. <shreyasb@vmware.com> 4.13.4-1
-   Upgrade to version 4.13.4
*   Fri May 29 2020 Shreyas B. <shreyasb@vmware.com> 4.12.0-1
-   Initial version of samba spec.
