%global build_if %{photon_subrelease} >= 91

Summary:        Secure IMAP and POP3 server
Name:           dovecot
Version:        2.3.21.1
Release:        4%{?dist}
URL:            https://dovecot.org/
Group:          System Environment/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://dovecot.org/releases/2.3/%{name}-%{version}.tar.gz
Source1:        license.txt
%include %{SOURCE1}
Source2:        dovecot.conf
Source3:        dovecot.sysusers

Patch1:         0001-use-openssl-hmac-instead-of-custom-implementation.patch
Patch2:         0002-Remove-OTP-authentication-support.patch
Patch3:         0003-lib-dcrypt-add-OpenSSL-3.x-compatibility-for-EVP_PKE.patch
Patch4:         0004-support-OpenSSL-3-providers-and-drop-ENGINE-API.patch
Patch5:         0005-m4-crypt_xpg6-define-_DEFAULT_SOURCE-for-current-gli.patch

BuildRequires:  openssl-devel
BuildRequires:  Linux-PAM-devel
BuildRequires:  systemd-devel
BuildRequires:  zstd-devel
BuildRequires:  libcap-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gettext

Requires:       %{name}-libs = %{version}-%{release}
Requires(pre):  systemd-rpm-macros
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd
# /var/mail must be 1775 root:mail (sticky) so dovecot-lda can deliver
Requires:       filesystem >= 1.1-11

Obsoletes: procmail

%description
Dovecot is an open source IMAP and POP3 server for Linux/UNIX-like
systems, written primarily with security in mind. It is fast, simple
to set up, does not require special administration and uses little
memory.

%package        libs
Summary:        Libraries for %{name}
Group:          System Environment/Libraries
Requires:       openssl
Requires:       Linux-PAM
Requires:       systemd

%description    libs
Shared libraries and helper executables for the Dovecot server.

%package        lmtpd
Summary:        LMTP server for Dovecot
Group:          System Environment/Daemons
Requires:       %{name} = %{version}-%{release}

%description    lmtpd
The LMTP (Local Mail Transfer Protocol, RFC 2033) server for Dovecot.
LMTP is used for final mail delivery from an MTA into a user mailbox.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
Header files, pkg-config files and import libraries required to build
plugins and external tools against the Dovecot server.

%prep
%autosetup -p1

%build
autoreconf -fi

%configure \
    --disable-static \
    --with-lmtpd \
    --with-pam \
    --with-shadow \
    --with-zstd \
    --with-libcap \
    --with-ssl=openssl \
    --without-lucene

%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/dovecot/dovecot.conf
install -p -D -m 0644 %{SOURCE3} %{buildroot}%{_sysusersdir}/%{name}.conf
rm -rf %{buildroot}%{_docdir}/%{name}
rm -rf %{buildroot}%{_mandir}

%pre
%sysusers_create_compat %{SOURCE3}

%files
%defattr(-,root,root)
%{_bindir}/doveadm
%{_bindir}/doveconf
%{_bindir}/dovecot-sysreport
%{_bindir}/dsync
%{_sbindir}/dovecot
%config(noreplace) %{_sysconfdir}/dovecot
%{_datadir}/dovecot
%{_unitdir}/dovecot.service
%{_unitdir}/dovecot.socket
%{_sysusersdir}/%{name}.conf

%ldconfig_scriptlets libs

%files libs
%defattr(-,root,root)
%{_libdir}/dovecot/*.so*
%{_libdir}/dovecot/auth/
%{_libdir}/dovecot/doveadm/
%{_libdir}/dovecot/old-stats/
%{_libexecdir}/dovecot/
%exclude %{_libexecdir}/dovecot/lmtp

%files lmtpd
%defattr(-,root,root)
%{_libexecdir}/dovecot/lmtp

%files devel
%defattr(-,root,root)
%{_includedir}/dovecot
%{_datadir}/aclocal/*
%{_libdir}/dovecot/dovecot-config

%changelog
* Sun Jun 14 2026 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 2.3.21.1-4
- Enable dovecot-lda local delivery: set protocols to imap pop3, mail_location
  to system mbox (/var/mail/%%u), add postmaster_address and passwd userdb /
  pam passdb
- Require filesystem >= 1.1-11 for correct /var/mail permissions (1775 root:mail)
* Mon Jun 08 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.3.21.1-3
- Add obsoletes procmail
* Tue Jun 02 2026 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 2.3.21.1-2
- Use OpenSSL HMAC for FIPS compliance
- Remove OTP authentication support
- Add OpenSSL 3.x compatibility and drop deprecated ENGINE API
- Fix configure crypt check for current glibc
* Tue May 26 2026 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 2.3.21.1-1
- Initial build
