%global sssd_user root

# Set child attrs assuming root user
%global child_attrs 0750

# we don't want to provide private python extension libs
%define __provides_exclude_from %{python3_sitearch}/.*\.so$

# Determine the location of the LDB modules directory
%global ldb_modulesdir %{_libdir}/ldb/modules/ldb

# directory variables
%global servicename sssd
%global sssdstatedir %{_localstatedir}/lib/sss
%global dbpath %{sssdstatedir}/db
%global keytabdir %{sssdstatedir}/keytabs
%global pipepath %{sssdstatedir}/pipes
%global mcpath %{sssdstatedir}/mc
%global pubconfpath %{sssdstatedir}/pubconf
%global gpocachepath %{sssdstatedir}/gpo_cache
%global secdbpath %{sssdstatedir}/secrets
%global deskprofilepath %{sssdstatedir}/deskprofile

Name:           sssd
Summary:        System Security Services Daemon
Version:        2.8.2
Release:        10%{?dist}
URL:            http://github.com/SSSD/sssd
License:        GPLv3+
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/SSSD/sssd/releases/download/%{version}/%{name}-%{version}.tar.gz
%define sha512 sssd=10b7a641823aefb43e30bff9e5f309a1f48446ffff421a06f86496db24ba1fbd384733b5690864507ef9b2f04c91e563fe9820536031f83f1bd6e93edfedee55

Source1: sssd.conf

Patch0: 0001-replace-python-with-python3-in-sss_obfuscate.patch

Requires: sssd-ad = %{version}-%{release}
Requires: sssd-common = %{version}-%{release}
Requires: sssd-ipa = %{version}-%{release}
Requires: sssd-krb5 = %{version}-%{release}
Requires: sssd-ldap = %{version}-%{release}
Requires: sssd-proxy = %{version}-%{release}
Requires: sssd-kcm = %{version}-%{release}
Requires: sssd-ipa = %{version}-%{release}
Requires: libldb
Requires: libtdb
Requires: ding-libs
Requires: libtalloc
Requires: libtevent
Requires: libwbclient
Requires: samba-client
Requires: bindutils
Requires: libselinux
Requires: krb5
Requires: openssl
Requires: glibc
Requires: dbus
Requires: util-linux-libs
Requires: libgcrypt
Requires: libgpg-error
Requires: xz-libs
Requires: openssl
Requires: libsemanage

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: bindutils
BuildRequires: libuv-devel
BuildRequires: c-ares-devel
BuildRequires: check
BuildRequires: cifs-utils-devel
BuildRequires: dbus-devel
BuildRequires: docbook-xsl
BuildRequires: findutils
BuildRequires: gcc
BuildRequires: openldap-devel
BuildRequires: libtirpc
BuildRequires: libtalloc-devel
BuildRequires: samba-client-devel
BuildRequires: samba-client-libs
BuildRequires: libtdb-devel
BuildRequires: libldb-devel
BuildRequires: libtevent-devel
BuildRequires: docbook-xml
BuildRequires: libselinux-devel
BuildRequires: libdhash-devel
BuildRequires: libini-config-devel
BuildRequires: e2fsprogs-devel
BuildRequires: Linux-PAM-devel
BuildRequires: gettext
BuildRequires: libwbclient
BuildRequires: jansson-devel
BuildRequires: keyutils-devel
BuildRequires: krb5-devel
BuildRequires: cmocka-devel >= 1.0.0
BuildRequires: device-mapper-devel
BuildRequires: device-mapper-libs
BuildRequires: libevent-devel
BuildRequires: systemd-devel
BuildRequires: libunistring-devel
BuildRequires: python3-devel
BuildRequires: systemtap-sdt-devel
BuildRequires: python3-xml
BuildRequires: python3-pip
BuildRequires: libnl-devel
BuildRequires: pcre2-devel
BuildRequires: p11-kit-devel
BuildRequires: util-linux-devel
BuildRequires: libsemanage-devel
BuildRequires: nghttp2-devel
BuildRequires: libnfsidmap-devel

%description
Provides a set of daemons to manage access to remote directories and
authentication mechanisms. It provides an NSS and PAM interface toward
the system and a pluggable back end system to connect to multiple different
account sources. It is also the basis to provide client auditing and policy
services for projects like FreeIPA.

The sssd subpackage is a meta-package that contains the daemon as well as all
the existing back ends.

%package common
Summary: Common files for the SSSD
License: GPLv3+
# Requires
Requires: samba-client
Requires: sssd-client = %{version}-%{release}
Requires: libsss_sudo = %{version}-%{release}
Requires: libsss_autofs = %{version}-%{release}
Requires: sssd-nfs_idmap = %{version}-%{release}
Requires: libsss_idmap = %{version}-%{release}
Requires: libsss_certmap = %{version}-%{release}
Requires(pre): shadow
%{?systemd_requires}

### Provides ###
Provides: libsss_sudo-devel = %{version}-%{release}

%description common
Common files for the SSSD. The common package includes all the files needed
to run a particular back end, however, the back ends are packaged in separate
subpackages such as sssd-ldap.

%package client
Summary: SSSD Client libraries for NSS and PAM
License: LGPLv3+
Requires: libsss_nss_idmap = %{version}-%{release}
Requires: libsss_idmap = %{version}-%{release}
Requires: e2fsprogs-libs
Requires: Linux-PAM
Requires(post):  chkconfig
Requires(preun): chkconfig

%description client
Provides the libraries needed by the PAM and NSS stacks to connect to the SSSD
service.

%package -n libsss_sudo
Summary: A library to allow communication between SUDO and SSSD
License: LGPLv3+
Conflicts: sssd-common < %{version}-%{release}

%description -n libsss_sudo
A utility library to allow communication between SUDO and SSSD

%package -n libsss_autofs
Summary: A library to allow communication between Autofs and SSSD
License: LGPLv3+
Conflicts: sssd-common < %{version}-%{release}

%description -n libsss_autofs
A utility library to allow communication between Autofs and SSSD

%package tools
Summary: Userspace tools for use with the SSSD
License: GPLv3+
Requires: sssd-common = %{version}-%{release}
# required by sss_obfuscate
Requires: python3-sss = %{version}-%{release}
Requires: python3-sssdconfig = %{version}-%{release}
Requires: libsss_certmap = %{version}-%{release}
# for logger=journald support with sss_analyze
# python3-systemd module can be imported with pip3 install systemd-python
Requires: systemd-devel
Requires: sssd-dbus

%description tools
Provides several administrative tools:
* sss_debuglevel to change the debug level on the fly
* sss_seed which pre-creates a user entry for use in kickstarts
* sss_obfuscate for generating an obfuscated LDAP password
* sssctl -- an sssd status and control utility

%package -n python3-sssdconfig
Summary: SSSD and IPA configuration file manipulation classes and functions
License: GPLv3+
BuildArch: noarch
Requires: python3

%description -n python3-sssdconfig
Provides python3 files for manipulation SSSD and IPA configuration files.

%package -n python3-sss
Summary: Python3 bindings for sssd
License: LGPLv3+
Requires: sssd-common = %{version}-%{release}
Requires: python3
Requires: libunistring
Requires: systemd
Requires: popt
Requires: libcap

%description -n python3-sss
Provides python3 bindings:
    * function for retrieving list of groups user belongs to
    * class for obfuscation of passwords

%package -n python3-sss-murmur
Summary: Python3 bindings for murmur hash function
License: LGPLv3+
Requires: python3

%description -n python3-sss-murmur
Provides python3 module for calculating the murmur hash version 3

%package ldap
Summary: The LDAP back end of the SSSD
License: GPLv3+
Requires: sssd-common = %{version}-%{release}
Requires: sssd-krb5-common = %{version}-%{release}
Requires: libsss_idmap = %{version}-%{release}
Requires: libsss_certmap = %{version}-%{release}

%description ldap
Provides the LDAP back end that the SSSD can utilize to fetch identity data
from and authenticate against an LDAP server.

%package krb5-common
Summary: SSSD helpers needed for Kerberos and GSSAPI authentication
License: GPLv3+
# cyrus-sasl should contain gssapi
Requires: cyrus-sasl
Requires: sssd-common = %{version}-%{release}

%description krb5-common
Provides helper processes that the LDAP and Kerberos back ends can use for
Kerberos user or host authentication.

%package krb5
Summary: The Kerberos authentication back end for the SSSD
License: GPLv3+
Requires: sssd-common = %{version}-%{release}
Requires: sssd-krb5-common = %{version}-%{release}

%description krb5
Provides the Kerberos back end that the SSSD can utilize authenticate
against a Kerberos server.

%package common-pac
Summary: Common files needed for supporting PAC processing
License: GPLv3+
Requires: sssd-common = %{version}-%{release}
Requires: libsss_idmap = %{version}-%{release}

%description common-pac
Provides common files needed by SSSD providers such as IPA and Active Directory
for handling Kerberos PACs.

%package ipa
Summary: The IPA back end of the SSSD
License: GPLv3+
Requires: samba-client-libs
Requires: sssd-common = %{version}-%{release}
Requires: sssd-krb5-common = %{version}-%{release}
Requires: libipa_hbac = %{version}-%{release}
Requires: libsss_certmap = %{version}-%{release}
Requires: libsss_idmap = %{version}-%{release}
Requires: sssd-common-pac = %{version}-%{release}

%description ipa
Provides the IPA back end that the SSSD can utilize to fetch identity data
from and authenticate against an IPA server.

%package ad
Summary: The AD back end of the SSSD
License: GPLv3+
Requires: samba-client-libs
Requires: sssd-common = %{version}-%{release}
Requires: sssd-krb5-common = %{version}-%{release}
Requires: libsss_idmap = %{version}-%{release}
Requires: libsss_certmap = %{version}-%{release}
Requires: sssd-common-pac = %{version}-%{release}
Requires: openldap-devel
Requires: keyutils
Requires: pcre2-libs
Requires: gnutls
Requires: libcap
Requires: libtasn1
Requires: nettle
Requires: gmp
Requires: jansson
Requires: zlib
Requires: e2fsprogs-libs

%description ad
Provides the Active Directory back end that the SSSD can utilize to fetch
identity data from and authenticate against an Active Directory server.

%package proxy
Summary: The proxy back end of the SSSD
License: GPLv3+
Requires: sssd-common = %{version}-%{release}

%description proxy
Provides the proxy back end which can be used to wrap an existing NSS and/or
PAM modules to leverage SSSD caching.

%package -n libsss_idmap
Summary: FreeIPA Idmap library
License: LGPLv3+

%description -n libsss_idmap
Utility library to convert SIDs to Unix uids and gids

%package -n libsss_idmap-devel
Summary: FreeIPA Idmap library
License: LGPLv3+
Requires: libsss_idmap = %{version}-%{release}

%description -n libsss_idmap-devel
Utility library to SIDs to Unix uids and gids

%package -n libipa_hbac
Summary: FreeIPA HBAC Evaluator library
License: LGPLv3+

%description -n libipa_hbac
Utility library to validate FreeIPA HBAC rules for authorization requests

%package -n libipa_hbac-devel
Summary: FreeIPA HBAC Evaluator library
License: LGPLv3+
Requires: libipa_hbac = %{version}-%{release}

%description -n libipa_hbac-devel
Utility library to validate FreeIPA HBAC rules for authorization requests

%package -n python3-libipa_hbac
Summary: Python3 bindings for the FreeIPA HBAC Evaluator library
License: LGPLv3+
Requires: libipa_hbac = %{version}-%{release}
Requires: python3

%description -n python3-libipa_hbac
The python3-libipa_hbac contains the bindings so that libipa_hbac can be
used by Python applications.

%package -n libsss_nss_idmap
Summary: Library for SID and certificate based lookups
License: LGPLv3+

%description -n libsss_nss_idmap
Utility library for SID and certificate based lookups

%package -n libsss_nss_idmap-devel
Summary: Library for SID and certificate based lookups
License: LGPLv3+
Requires: libsss_nss_idmap = %{version}-%{release}

%description -n libsss_nss_idmap-devel
Utility library for SID and certificate based lookups

%package -n python3-libsss_nss_idmap
Summary: Python3 bindings for libsss_nss_idmap
License: LGPLv3+
Requires: libsss_nss_idmap = %{version}-%{release}
Requires: python3

%description -n python3-libsss_nss_idmap
The python3-libsss_nss_idmap contains the bindings so that libsss_nss_idmap can
be used by Python applications.

%package dbus
Summary: The D-Bus responder of the SSSD
License: GPLv3+
Requires: sssd-common = %{version}-%{release}
%{?systemd_requires}

%description dbus
Provides the D-Bus responder of the SSSD, called the InfoPipe, that allows
the information from the SSSD to be transmitted over the system bus.

%package polkit-rules
Summary: Rules for polkit integration for SSSD
Group: Applications/System
License: GPLv3+
Requires: polkit >= 0.106
Requires: sssd-common = %{version}-%{release}

%description polkit-rules
Provides rules for polkit integration with SSSD. This is required
for smartcard support.

%package -n libsss_simpleifp
Summary: The SSSD D-Bus responder helper library
License: GPLv3+
Requires: sssd-dbus = %{version}-%{release}
Requires: libcap

%description -n libsss_simpleifp
Provides library that simplifies D-Bus API for the SSSD InfoPipe responder.

%package -n libsss_simpleifp-devel
Summary: The SSSD D-Bus responder helper library
License: GPLv3+
Requires: dbus-devel
Requires: libsss_simpleifp = %{version}-%{release}

%description -n libsss_simpleifp-devel
Provides library that simplifies D-Bus API for the SSSD InfoPipe responder.

%package winbind_idmap
Summary: SSSD's idmap_sss Backend for Winbind
License: GPLv3+ and LGPLv3+
Requires: libsss_nss_idmap = %{version}-%{release}
Requires: libsss_idmap = %{version}-%{release}
Conflicts: sssd-common < %{version}-%{release}

%description winbind_idmap
The idmap_sss module provides a way for Winbind to call SSSD to map UIDs/GIDs
and SIDs.

%package nfs_idmap
Summary: SSSD plug-in for NFSv4 rpc.idmapd
License: GPLv3+
Requires: libnfsidmap
Conflicts: sssd-common < %{version}-%{release}

%description nfs_idmap
The libnfsidmap sssd module provides a way for rpc.idmapd to call SSSD to map
UIDs/GIDs to names and vice versa. It can be also used for mapping principal
(user) name to IDs(UID or GID) or to obtain groups which user are member of.

%package -n libsss_certmap
Summary: SSSD Certificate Mapping Library
License: LGPLv3+
Conflicts: sssd-common < %{version}-%{release}

%description -n libsss_certmap
Library to map certificates to users based on rules

%package -n libsss_certmap-devel
Summary: SSSD Certificate Mapping Library
License: LGPLv3+
Requires: libsss_certmap = %{version}-%{release}

%description -n libsss_certmap-devel
Library to map certificates to users based on rules

%package kcm
Summary: An implementation of a Kerberos KCM server
License: GPLv3+
Requires: sssd-common = %{version}-%{release}
%{?systemd_requires}

%description kcm
An implementation of a Kerberos KCM server. Use this package if you want to
use the KCM: Kerberos credentials cache.

%package idp
Summary: Kerberos plugins and OIDC helper for external identity providers.
License: GPLv3+
Requires: sssd-common = %{version}-%{release}

%description idp
This package provides Kerberos plugins that are required to enable
authentication against external identity providers. Additionally a helper
program to handle the OAuth 2.0 Device Authorization Grant is provided.

%prep
%autosetup -p1

%build

autoreconf -ivf

%configure \
    --disable-rpath \
    --disable-static \
    --enable-gss-spnego-for-zero-maxssf \
    --enable-nsslibdir=%{_libdir} \
    --enable-pammoddir=%{_libdir}/security \
    --enable-sss-default-nss-plugin \
    --enable-systemtap \
    --with-db-path=%{dbpath} \
    --with-gpo-cache-path=%{gpocachepath} \
    --with-init-dir=%{_initrddir} \
    --with-initscript=systemd \
    --with-krb5-rcache-dir=%{_localstatedir}/cache/krb5rcache \
    --with-mcache-path=%{mcpath} \
    --with-pid-path=%{_rundir} \
    --with-pipe-path=%{pipepath} \
    --with-pubconf-path=%{pubconfpath} \
    --with-sssd-user=%{sssd_user} \
    --with-syslog=journald \
    --with-test-dir=/dev/shm \
    --without-oidc-child

%make_build

%install
%make_install %{?_smp_mflags}

# Prepare language files
%find_lang %{name}

# Copy default logrotate file
mkdir -p %{buildroot}/%{_sysconfdir}/logrotate.d
install -m644 src/examples/logrotate %{buildroot}%{_sysconfdir}/logrotate.d/sssd

# Make sure SSSD is able to run on read-only root
mkdir -p %{buildroot}/%{_sysconfdir}/rwtab.d
install -m644 src/examples/rwtab %{buildroot}%{_sysconfdir}/rwtab.d/sssd

# Kerberos KCM credential cache by default
mkdir -p %{buildroot}/%{_sysconfdir}/krb5.conf.d
cp %{buildroot}/%{_datadir}/sssd-kcm/kcm_default_ccache \
   %{buildroot}/%{_sysconfdir}/krb5.conf.d/kcm_default_ccache

# Enable krb5 idp plugins by default (when sssd-idp package is installed)
cp %{buildroot}/%{_datadir}/sssd/krb5-snippets/sssd_enable_idp \
   %{buildroot}/%{_sysconfdir}/krb5.conf.d/sssd_enable_idp

# krb5 configuration snippet
cp %{buildroot}/%{_datadir}/sssd/krb5-snippets/enable_sssd_conf_dir \
   %{buildroot}/%{_sysconfdir}/krb5.conf.d/enable_sssd_conf_dir

# Create directory for cifs-idmap alternative
# Otherwise this directory could not be owned by sssd-client
mkdir -p %{buildroot}/%{_sysconfdir}/cifs-utils

# Suppress developer-only documentation
rm -Rf %{buildroot}%{_docdir}/%{name}

# Older versions of rpmbuild can only handle one -f option
# So we need to append to the sssd*.lang file
for file in $(find %{buildroot}/%{python3_sitelib} -maxdepth 1 -name "*.egg-info" 2> /dev/null)
do
    echo %{python3_sitelib}/$(basename $file) >> python3_sssdconfig.lang
done

touch sssd.lang
for subpackage in sssd_ldap sssd_krb5 sssd_ipa sssd_ad sssd_proxy sssd_tools \
                  sssd_client sssd_dbus sssd_nfs_idmap sssd_winbind_idmap \
                  libsss_certmap sssd_kcm; do
    touch $subpackage.lang
done

for man in `find %{buildroot}/%{_mandir}/??/man?/ -type f | sed -e "s#%{buildroot}/%{_mandir}/##"`
do
    lang=`echo $man | cut -c 1-2`
    case `basename $man` in
        sss_cache*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd.lang
            ;;
        sss_ssh*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd.lang
            ;;
        sss_rpcidmapd*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_nfs_idmap.lang
            ;;
        sss_*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_tools.lang
            ;;
        sssctl*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_tools.lang
            ;;
        sssd_krb5_*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_client.lang
            ;;
        pam_sss*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_client.lang
            ;;
        sssd-ldap*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_ldap.lang
            ;;
        sssd-krb5*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_krb5.lang
            ;;
        sssd-ipa*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_ipa.lang
            ;;
        sssd-ad*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_ad.lang
            ;;
        sssd-proxy*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_proxy.lang
            ;;
        sssd-ifp*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_dbus.lang
            ;;
        sssd-kcm*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_kcm.lang
            ;;
        idmap_sss*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_winbind_idmap.lang
            ;;
        sss-certmap*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> libsss_certmap.lang
            ;;
        *)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd.lang
            ;;
    esac
done

# Print these to the rpmbuild log
echo "sssd.lang:"
cat sssd.lang

echo "python3_sssdconfig.lang:"
cat python3_sssdconfig.lang

for subpackage in sssd_ldap sssd_krb5 sssd_ipa sssd_ad sssd_proxy sssd_tools \
                  sssd_client sssd_dbus sssd_nfs_idmap sssd_winbind_idmap \
                  libsss_certmap sssd_kcm
do
    echo "$subpackage.lang:"
    cat $subpackage.lang
done

# copy in default sssd.conf
install -D %{SOURCE1} %{buildroot}%{_sysconfdir}/sssd/sssd.conf

libtool --finish %{buildroot}%{_libdir}/sssd

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%define common_service sssd.service sssd-autofs.socket sssd-nss.socket sssd-pam.socket sssd-pam-priv.socket sssd-ssh.socket sssd-sudo.socket
%define other_services sssd-autofs.service sssd-nss.service sssd-pam.service sssd-ssh.service sssd-sudo.service

%post common
%systemd_post %common_service

%preun common
%systemd_preun %common_service

%postun common
%systemd_postun_with_restart %common_service

# Services have RefuseManualStart=true, therefore we can't request restart.
%systemd_postun %other_services

%post dbus
%systemd_post sssd-ifp.service

%preun dbus
%systemd_preun sssd-ifp.service

%postun dbus
%systemd_postun_with_restart sssd-ifp.service

%post kcm
%systemd_post sssd-kcm.socket
systemctl enable sssd-kcm.socket
systemctl start sssd-kcm.socket

%preun kcm
%systemd_preun sssd-kcm.socket

%postun kcm
%systemd_postun_with_restart sssd-kcm.socket
%systemd_postun_with_restart sssd-kcm.service

%post client
/usr/sbin/alternatives --install /etc/cifs-utils/idmap-plugin cifs-idmap-plugin %{_libdir}/cifs-utils/cifs_idmap_sss.so 20

%preun client
if [ $1 -eq 0 ] ; then
        /usr/sbin/alternatives --remove cifs-idmap-plugin %{_libdir}/cifs-utils/cifs_idmap_sss.so
fi

%posttrans common
%systemd_postun_with_restart sssd.service

%files
%defattr(-,root,root)
%license COPYING

%files common -f sssd.lang
%defattr(-,root,root)
%license COPYING
%{_sbindir}/sssd
%{_unitdir}/sssd.service
%{_unitdir}/sssd-autofs.socket
%{_unitdir}/sssd-autofs.service
%{_unitdir}/sssd-nss.socket
%{_unitdir}/sssd-nss.service
%{_unitdir}/sssd-pac.socket
%{_unitdir}/sssd-pac.service
%{_unitdir}/sssd-pam.socket
%{_unitdir}/sssd-pam-priv.socket
%{_unitdir}/sssd-pam.service
%{_unitdir}/sssd-ssh.socket
%{_unitdir}/sssd-ssh.service
%{_unitdir}/sssd-sudo.socket
%{_unitdir}/sssd-sudo.service

%dir %{_libexecdir}/%{servicename}
%{_libexecdir}/%{servicename}/sssd_be
%{_libexecdir}/%{servicename}/sssd_nss
%{_libexecdir}/%{servicename}/sssd_pam
%{_libexecdir}/%{servicename}/sssd_autofs
%{_libexecdir}/%{servicename}/sssd_ssh
%{_libexecdir}/%{servicename}/sssd_sudo
%{_libexecdir}/%{servicename}/p11_child
%{_libexecdir}/%{servicename}/sssd_check_socket_activated_responders

%dir %{_libdir}/%{name}
# The files provider is intentionally packaged in -common
%{_libdir}/%{name}/libsss_files.so
%{_libdir}/%{name}/libsss_simple.so

#Internal shared libraries
%{_libdir}/%{name}/libsss_child.so
%{_libdir}/%{name}/libsss_crypt.so
%{_libdir}/%{name}/libsss_cert.so
%{_libdir}/%{name}/libsss_debug.so
%{_libdir}/%{name}/libsss_krb5_common.so
%{_libdir}/%{name}/libsss_ldap_common.so
%{_libdir}/%{name}/libsss_util.so
%{_libdir}/%{name}/libsss_semanage.so
%{_libdir}/%{name}/libifp_iface.so
%{_libdir}/%{name}/libifp_iface_sync.so
%{_libdir}/%{name}/libsss_iface.so
%{_libdir}/%{name}/libsss_iface_sync.so
%{_libdir}/%{name}/libsss_sbus.so
%{_libdir}/%{name}/libsss_sbus_sync.so

%{ldb_modulesdir}/memberof.so
%{_bindir}/sss_ssh_authorizedkeys
%{_bindir}/sss_ssh_knownhostsproxy
%{_sbindir}/sss_cache
%{_libexecdir}/%{servicename}/sss_signal

%dir %{sssdstatedir}
%dir %{_localstatedir}/cache/krb5rcache
%attr(700,%{sssd_user},%{sssd_user}) %dir %{dbpath}
%attr(775,%{sssd_user},%{sssd_user}) %dir %{mcpath}
%attr(700,root,root) %dir %{secdbpath}
%attr(751,root,root) %dir %{deskprofilepath}
%ghost %attr(0664,%{sssd_user},%{sssd_user}) %verify(not md5 size mtime) %{mcpath}/passwd
%ghost %attr(0664,%{sssd_user},%{sssd_user}) %verify(not md5 size mtime) %{mcpath}/group
%ghost %attr(0664,%{sssd_user},%{sssd_user}) %verify(not md5 size mtime) %{mcpath}/initgroups
%attr(755,%{sssd_user},%{sssd_user}) %dir %{pipepath}
%attr(750,%{sssd_user},root) %dir %{pipepath}/private
%attr(755,%{sssd_user},%{sssd_user}) %dir %{pubconfpath}
%attr(755,%{sssd_user},%{sssd_user}) %dir %{gpocachepath}
%attr(750,%{sssd_user},%{sssd_user}) %dir %{_var}/log/%{name}
%attr(700,%{sssd_user},%{sssd_user}) %dir %{_sysconfdir}/sssd
%attr(0600,%{sssd_user},%{sssd_user}) %config(noreplace) %{_sysconfdir}/sssd/sssd.conf
%attr(711,%{sssd_user},%{sssd_user}) %dir %{_sysconfdir}/sssd/conf.d
%attr(711,root,root) %dir %{_sysconfdir}/sssd/pki
%dir %{_sysconfdir}/logrotate.d
%config(noreplace) %{_sysconfdir}/logrotate.d/sssd
%dir %{_sysconfdir}/rwtab.d
%config(noreplace) %{_sysconfdir}/rwtab.d/sssd
%dir %{_datadir}/sssd
%config(noreplace) %{_sysconfdir}/pam.d/sssd-shadowutils
%exclude %dir %{_libdir}/%{name}/conf
%exclude %{_libdir}/%{name}/conf/sssd.conf

%{_datadir}/sssd/cfg_rules.ini
%{_mandir}/man1/sss_ssh_authorizedkeys.1*
%{_mandir}/man1/sss_ssh_knownhostsproxy.1*
%{_mandir}/man5/sssd.conf.5*
%{_mandir}/man5/sssd-files.5*
%{_mandir}/man5/sssd-simple.5*
%{_mandir}/man5/sssd-sudo.5*
%{_mandir}/man5/sssd-session-recording.5*
%{_mandir}/man8/sssd.8*
%{_mandir}/man8/sss_cache.8*
%dir %{_datadir}/sssd/systemtap
%{_datadir}/sssd/systemtap/id_perf.stp
%{_datadir}/sssd/systemtap/nested_group_perf.stp
%{_datadir}/sssd/systemtap/dp_request.stp
%{_datadir}/sssd/systemtap/ldap_perf.stp
%dir %{_datadir}/systemtap
%dir %{_datadir}/systemtap/tapset
%{_datadir}/systemtap/tapset/sssd.stp
%{_datadir}/systemtap/tapset/sssd_functions.stp
%{_mandir}/man5/sssd-systemtap.5*

%files polkit-rules
%defattr(-,root,root)
%{_datadir}/polkit-1/rules.d/*

%files ldap -f sssd_ldap.lang
%defattr(-,root,root)
%license COPYING
%{_libdir}/%{name}/libsss_ldap.so
%{_mandir}/man5/sssd-ldap.5*
%{_mandir}/man5/sssd-ldap-attributes.5*

%files krb5-common
%defattr(-,root,root)
%license COPYING
%attr(755,%{sssd_user},%{sssd_user}) %dir %{pubconfpath}/krb5.include.d
%attr(%{child_attrs},root,%{sssd_user}) %{_libexecdir}/%{servicename}/ldap_child
%attr(%{child_attrs},root,%{sssd_user}) %{_libexecdir}/%{servicename}/krb5_child

%files krb5 -f sssd_krb5.lang
%defattr(-,root,root)
%license COPYING
%{_libdir}/%{name}/libsss_krb5.so
%{_mandir}/man5/sssd-krb5.5*
%config(noreplace) %{_sysconfdir}/krb5.conf.d/enable_sssd_conf_dir
%dir %{_datadir}/sssd/krb5-snippets
%{_datadir}/sssd/krb5-snippets/enable_sssd_conf_dir

%files common-pac
%defattr(-,root,root)
%license COPYING
%{_libexecdir}/%{servicename}/sssd_pac

%files ipa -f sssd_ipa.lang
%defattr(-,root,root)
%license COPYING
%attr(%{child_attrs},root,%{sssd_user}) %{_libexecdir}/%{servicename}/selinux_child
%attr(700,%{sssd_user},%{sssd_user}) %dir %{keytabdir}
%{_libdir}/%{name}/libsss_ipa.so
%{_mandir}/man5/sssd-ipa.5*

%files ad -f sssd_ad.lang
%defattr(-,root,root)
%license COPYING
%{_libdir}/%{name}/libsss_ad.so
%{_libexecdir}/%{servicename}/gpo_child
%{_mandir}/man5/sssd-ad.5*

%files proxy
%defattr(-,root,root)
%license COPYING
%attr(%{child_attrs},root,%{sssd_user}) %{_libexecdir}/%{servicename}/proxy_child
%{_libdir}/%{name}/libsss_proxy.so

%files dbus -f sssd_dbus.lang
%defattr(-,root,root)
%license COPYING
%{_libexecdir}/%{servicename}/sssd_ifp
%{_mandir}/man5/sssd-ifp.5*
%{_unitdir}/sssd-ifp.service
# InfoPipe DBus plumbing
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.sssd.infopipe.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.sssd.infopipe.service

%files -n libsss_simpleifp
%defattr(-,root,root)
%{_libdir}/libsss_simpleifp.so.*

%files -n libsss_simpleifp-devel
%defattr(-,root,root)
%{_includedir}/sss_sifp.h
%{_includedir}/sss_sifp_dbus.h
%{_libdir}/libsss_simpleifp.so
%{_libdir}/pkgconfig/sss_simpleifp.pc

%files client -f sssd_client.lang
%defattr(-,root,root)
%license src/sss_client/COPYING src/sss_client/COPYING.LESSER
%{_libdir}/libnss_sss.so.2
%{_libdir}/security/pam_sss.so
%{_libdir}/security/pam_sss_gss.so
%{_libdir}/krb5/plugins/libkrb5/sssd_krb5_locator_plugin.so
%{_libdir}/krb5/plugins/authdata/sssd_pac_plugin.so
%dir %{_libdir}/cifs-utils
%{_libdir}/cifs-utils/cifs_idmap_sss.so
%dir %{_sysconfdir}/cifs-utils
%ghost %{_sysconfdir}/cifs-utils/idmap-plugin
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/modules
%{_libdir}/%{name}/modules/sssd_krb5_localauth_plugin.so
%{_mandir}/man8/pam_sss.8*
%{_mandir}/man8/pam_sss_gss.8*
%{_mandir}/man8/sssd_krb5_locator_plugin.8*
%{_mandir}/man8/sssd_krb5_localauth_plugin.8*

%files -n libsss_sudo
%defattr(-,root,root)
%license src/sss_client/COPYING
%{_libdir}/libsss_sudo.so*

%files -n libsss_autofs
%defattr(-,root,root)
%license src/sss_client/COPYING src/sss_client/COPYING.LESSER
%dir %{_libdir}/%{name}/modules
%{_libdir}/%{name}/modules/libsss_autofs.so

%files tools -f sssd_tools.lang
%defattr(-,root,root)
%license COPYING
%{_sbindir}/sss_obfuscate
%{_sbindir}/sss_override
%{_sbindir}/sss_debuglevel
%{_sbindir}/sss_seed
%{_sbindir}/sssctl
%{_libexecdir}/%{servicename}/sss_analyze
%{python3_sitelib}/sssd/
%{_mandir}/man8/sss_obfuscate.8*
%{_mandir}/man8/sss_override.8*
%{_mandir}/man8/sss_debuglevel.8*
%{_mandir}/man8/sss_seed.8*
%{_mandir}/man8/sssctl.8*

%files -n python3-sssdconfig
%defattr(-,root,root)
%{python3_sitearch}/SSSDConfig-%{version}-py3.11.egg-info
%dir %{python3_sitelib}/SSSDConfig
%{python3_sitelib}/SSSDConfig/*.py*
%dir %{python3_sitelib}/SSSDConfig/__pycache__
%{python3_sitelib}/SSSDConfig/__pycache__/*.py*
%dir %{_datadir}/sssd
%{_datadir}/sssd/sssd.api.conf
%{_datadir}/sssd/sssd.api.d

%files -n python3-sss
%defattr(-,root,root)
%{python3_sitearch}/pysss.so

%files -n python3-sss-murmur
%defattr(-,root,root)
%{python3_sitearch}/pysss_murmur.so

%files -n libsss_idmap
%defattr(-,root,root)
%license src/sss_client/COPYING src/sss_client/COPYING.LESSER
%{_libdir}/libsss_idmap.so.*

%files -n libsss_idmap-devel
%defattr(-,root,root)
%{_includedir}/sss_idmap.h
%{_libdir}/libsss_idmap.so
%{_libdir}/pkgconfig/sss_idmap.pc

%files -n libipa_hbac
%defattr(-,root,root)
%license src/sss_client/COPYING src/sss_client/COPYING.LESSER
%{_libdir}/libipa_hbac.so.*

%files -n libipa_hbac-devel
%defattr(-,root,root)
%{_includedir}/ipa_hbac.h
%{_libdir}/libipa_hbac.so
%{_libdir}/pkgconfig/ipa_hbac.pc

%files -n libsss_nss_idmap
%defattr(-,root,root)
%license src/sss_client/COPYING src/sss_client/COPYING.LESSER
%{_libdir}/libsss_nss_idmap.so.*

%files -n libsss_nss_idmap-devel
%defattr(-,root,root)
%{_includedir}/sss_nss_idmap.h
%{_libdir}/libsss_nss_idmap.so
%{_libdir}/pkgconfig/sss_nss_idmap.pc

%files -n python3-libsss_nss_idmap
%defattr(-,root,root)
%{python3_sitearch}/pysss_nss_idmap.so

%files -n python3-libipa_hbac
%defattr(-,root,root)
%{python3_sitearch}/pyhbac.so

%files winbind_idmap -f sssd_winbind_idmap.lang
%defattr(-,root,root)
%dir %{_libdir}/samba/idmap
%{_libdir}/samba/idmap/sss.so
%{_mandir}/man8/idmap_sss.8*

%files nfs_idmap -f sssd_nfs_idmap.lang
%defattr(-,root,root)
%{_mandir}/man5/sss_rpcidmapd.5*
%{_libdir}/libnfsidmap/sss.so

%files -n libsss_certmap
%defattr(-,root,root)
%license src/sss_client/COPYING src/sss_client/COPYING.LESSER
%{_libdir}/libsss_certmap.so.*
%{_mandir}/man5/sss-certmap.5*
%{_mandir}/*/man5/sss-certmap.5*

%files -n libsss_certmap-devel
%defattr(-,root,root)
%{_includedir}/sss_certmap.h
%{_libdir}/libsss_certmap.so
%{_libdir}/pkgconfig/sss_certmap.pc

%files kcm -f sssd_kcm.lang
%defattr(-,root,root)
%{_libexecdir}/%{servicename}/sssd_kcm
%config(noreplace) %{_sysconfdir}/krb5.conf.d/kcm_default_ccache
%dir %{_datadir}/sssd-kcm
%{_datadir}/sssd-kcm/kcm_default_ccache
%{_unitdir}/sssd-kcm.socket
%{_unitdir}/sssd-kcm.service
%{_mandir}/man8/sssd-kcm.8*

%files idp
%defattr(-,root,root)
%{_libdir}/%{name}/modules/sssd_krb5_idp_plugin.so
%{_datadir}/sssd/krb5-snippets/sssd_enable_idp
%config(noreplace) %{_sysconfdir}/krb5.conf.d/sssd_enable_idp

%changelog
* Mon Nov 27 2023 Harinadh D <hdommaraju@vmware.com> 2.8.2-10
- Bump version as part of samba upgrade
* Thu Nov 9 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 2.8.2-9
- Remove autoconfiguration scripts
* Mon Oct 23 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.8.2-8
- Version bump as part of nghtttp2 upgrade
* Tue Sep 19 2023 Nitesh Kumar <kunitesh@vmware.com> 2.8.2-7
- Bump version as a part of openldap v2.6.4 upgrade
* Mon Jul 31 2023 Oliver Kurth <okurth@vmware.com> 2.8.2-6
- bump version as part of samba update
* Fri Jul 28 2023 Srish Srinivasan <ssrish@vmware.com> 2.8.2-5
- Bump version as a part of krb5 upgrade
* Fri Jun 30 2023 Piyush Gupta <gpiyush@vmware.com> 2.8.2-4
- Replace Requires and BuildRequires from nfs-utils to libnfsidmap.
* Thu Jun 22 2023 Oliver Kurth <okurth@vmware.com> 2.8.2-3
- bump version as part of samba and libldb update
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.8.2-2
- Bump version as a part of zlib upgrade
* Tue Feb 14 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 2.8.2-1
- Initial addition to Photon. Reorganized, edited and updated
- for Photon OS from provided spec file in the sssd github repo.
