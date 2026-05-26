%global build_if %{photon_subrelease} >= 91

%global _samba_modules  pdb_tdbsam,pdb_ldap,pdb_smbpasswd,pdb_wbc_sam,pdb_samba4
%define maj_ver         4.0

Summary:        Samba Client Programs
Name:           samba-client
Version:        4.19.3
Release:        14%{?dist}
Group:          Productivity/Networking
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://www.samba.org

Source0: https://www.samba.org/ftp/samba/stable/samba-%{version}.tar.gz
Source1: smb.conf.vendor

Source2: license.txt
%include %{SOURCE2}

Patch0: CVE-2025-9640.patch
Patch1: CVE-2025-10230.patch
Patch2: 0001-fix-memset_explicit-usage-for-newer-glibc.patch

BuildRequires: krb5-devel
BuildRequires: libtirpc-devel
BuildRequires: rpcsvc-proto-devel
BuildRequires: python3-devel
BuildRequires: libarchive
BuildRequires: libarchive-devel
BuildRequires: Linux-PAM-devel
BuildRequires: python3-defusedxml
BuildRequires: libxslt-devel
BuildRequires: docbook-xsl
BuildRequires: docbook-xml
BuildRequires: gcc
BuildRequires: gnutls-devel
BuildRequires: jansson-devel
BuildRequires: libxml2-devel
BuildRequires: lmdb
BuildRequires: openldap-devel
BuildRequires: perl-Parse-Yapp
BuildRequires: dbus-devel
BuildRequires: sudo
BuildRequires: libtdb-devel >= 1.4.8
BuildRequires: libtalloc-devel >= 2.4.1
BuildRequires: libldb-devel >= 2.7.2
BuildRequires: libtevent-devel >= 0.15.0
BuildRequires: python3-tdb
BuildRequires: bison
BuildRequires: perl-JSON
BuildRequires: zlib-devel
BuildRequires: ncurses-devel

Requires: %{name}-libs = %{version}-%{release}
Requires: libtirpc
Requires: python3
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
Requires: libtdb >= 1.4.8
Requires: libldb >= 2.7.2
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
Requires:   libldb
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
Group:          System/Libraries
Provides:       pkgconfig(wbclient)

%description -n libwbclient
This package includes the wbclient library.

%package -n libwbclient-devel
Summary:        Libraries and Header Files to Develop Programs with wbclient Support
Group:          Development/Libraries/C and C++
Requires:       libwbclient = %{version}-%{release}

%description -n libwbclient-devel
This package contains the static libraries and header files needed to
develop programs which make use of the wbclient programming interface.

%prep
%autosetup -n samba-%{version} -p1
rm -r third_party/heimdal

%build
export CFLAGS="-I%{_includedir}/tirpc"
export LDFLAGS="-ltirpc"

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
        --disable-python \
        --bundled-libraries=cmocka,!talloc,!pytalloc,!pytalloc-util,!tevent,!pytevent,!tdb,!pytdb,!ldb,!pyldb,!pldb-util \
        --enable-debug \
        --with-system-mitkrb5

%make_build bin/smbclient

%install
%make_install %{?_smp_mflags}

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
   %{_bindir}/testparm \
   %{_bindir}/wbinfo \
   %{_includedir}/samba-%{maj_ver}/credentials.h \
   %{_includedir}/samba-%{maj_ver}/dcerpc.h \
   %{_includedir}/samba-%{maj_ver}/dcesrv_core.h \
   %{_includedir}/samba-%{maj_ver}/domain_credentials.h \
   %{_includedir}/samba-%{maj_ver}/ldb_wrap.h \
   %{_includedir}/samba-%{maj_ver}/lookup_sid.h \
   %{_includedir}/samba-%{maj_ver}/machine_sid.h \
   %{_includedir}/samba-%{maj_ver}/netapi.h \
   %{_includedir}/samba-%{maj_ver}/param.h \
   %{_includedir}/samba-%{maj_ver}/passdb.h \
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
   %{_libdir}/libnss_winbind.so.2 \
   %{_libdir}/libnss_wins.so.2 \
   %{_libdir}/pkgconfig/dcerpc.pc \
   %{_libdir}/pkgconfig/dcerpc_samr.pc \
   %{_libdir}/pkgconfig/netapi.pc \
   %{_libdir}/pkgconfig/samba-credentials.pc \
   %{_libdir}/pkgconfig/samba-hostconfig.pc \
   %{_libdir}/pkgconfig/samdb.pc \
   %{_libdir}/samba/idmap/*.so \
   %{_libdir}/samba/krb5/async_dns_krb5_locator.so \
   %{_libdir}/samba/krb5/winbind_krb5_localauth.so \
   %{_libdir}/samba/krb5/winbind_krb5_locator.so \
   %{_libdir}/samba/libLIBWBCLIENT-OLD-samba4.so \
   %{_libdir}/samba/libREG-FULL-samba4.so \
   %{_libdir}/samba/libauth-unix-token-samba4.so \
   %{_libdir}/samba/libauth4-samba4.so \
   %{_libdir}/samba/libcmocka-samba4.so \
   %{_libdir}/samba/libdsdb-module-samba4.so \
   %{_libdir}/samba/libnss-info-samba4.so \
   %{_libdir}/samba/libshares-samba4.so \
   %{_libdir}/samba/libsmbpasswdparser-samba4.so \
   %{_libdir}/samba/libxattr-tdb-samba4.so \
   %{_libdir}/security/pam_winbind.so \
   %{_libdir}/samba/nss_info/*.so \
   %{_libdir}/samba/vfs/*.so \
   %{_libexecdir}/samba/rpcd_* \
   %{_libexecdir}/samba/samba-* \
   %{_sbindir}/eventlogadm \
   %{_sbindir}/nmbd \
   %{_sbindir}/smbd \
   %{_sbindir}/winbindd
do
  rm %{buildroot}${fn}
done

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%post libs
/sbin/ldconfig

%postun libs
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
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_mandir}/man8/*

%files libs
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
%{_libdir}/libsmbclient.so.*
%{_libdir}/libdcerpc.so.*
%dir %{_libdir}/samba
%{_libdir}/samba/libdnsserver-common-samba4.so
%{_libdir}/samba/ldb/ildap.so
%{_libdir}/samba/libRPC-WORKER-samba4.so
%{_libdir}/samba/libcmdline-samba4.so
%{_libdir}/samba/libRPC-SERVER-LOOP-samba4.so
%{_libdir}/samba/ldb/ldbsamba_extensions.so
%{_libdir}/samba/libdcerpc-samba4.so
%{_libdir}/samba/libdcerpc-pkt-auth-samba4.so
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
%{_libdir}/samba/libstable-sort-samba4.so
%{_libdir}/samba/libsys-rw-samba4.so
%{_libdir}/samba/libsocket-blocking-samba4.so
%{_libdir}/samba/libtalloc-report-printf-samba4.so
%{_libdir}/samba/libtalloc-report-samba4.so
%{_libdir}/samba/libtdb-wrap-samba4.so
%{_libdir}/samba/libtime-basic-samba4.so
%{_libdir}/samba/libtorture-samba4.so
%{_libdir}/samba/libtrusts-util-samba4.so
%{_libdir}/samba/libutil-reg-samba4.so
%{_libdir}/samba/libutil-setid-samba4.so
%{_libdir}/samba/libutil-tdb-samba4.so
%dir %{_libdir}/samba/ldb
%dir %{_libdir}/samba/pdb
%{_libdir}/samba/pdb/ldapsam.so
%{_libdir}/samba/pdb/smbpasswd.so
%{_libdir}/samba/pdb/tdbsam.so
%{_libdir}/libdcerpc-server-core.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/samba-%{maj_ver}/libsmbclient.h
%{_includedir}/samba-%{maj_ver}/core/*.h
%{_includedir}/samba-%{maj_ver}/samba/version.h
%{_includedir}/samba-%{maj_ver}/ndr.h
%{_includedir}/samba-%{maj_ver}/util/discard.h
%{_includedir}/samba-%{maj_ver}/util/data_blob.h
%{_includedir}/samba-%{maj_ver}/util/time.h
%{_includedir}/samba-%{maj_ver}/charset.h
%{_includedir}/samba-%{maj_ver}/gen_ndr/*
%{_includedir}/samba-%{maj_ver}/ndr/*
%{_libdir}/libdcerpc.so
%{_libdir}/libsmbclient.so
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
%{_libdir}/samba/libidmap-samba4.so
%{_libdir}/pkgconfig/ndr*.pc
%{_libdir}/pkgconfig/samba-util.pc
%{_libdir}/pkgconfig/smbclient.pc
%{_mandir}/man7/libsmbclient.7*

%files -n libwbclient
%defattr(-,root,root,-)
%{_libdir}/libwbclient.so.*

%files -n libwbclient-devel
%defattr(-,root,root,-)
%dir %_includedir/samba-%{maj_ver}/
%{_includedir}/samba-%{maj_ver}/wbclient.h
%{_libdir}/libwbclient.so
%{_libdir}/pkgconfig/wbclient.pc

%changelog
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
