Summary:        Caching and forwarding HTTP web proxy
Name:           squid
Version:        5.6
Release:        3%{?dist}
License:        GPL-2.0-or-later
URL:            http://www.squid-cache.org
Group:          Networking/Web/Proxy
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://www.squid-cache.org/Versions/v5/%{name}-%{version}.tar.xz
%define sha512 %{name}=940a4d21ea8e3384642951d80c501a192178d1220f06a59a7bc54ce86d49caea0a86b6e789e28bcb7125ffa2a564ca1aca886a96cccf6356314121a81f38221a

Patch0:         squid-5.6-openssl3.patch

Source1:        %{name}.sysconfig
Source2:        %{name}.pam
Source3:        %{name}.service
Source4:        cache_swap.sh
Source5:        %{name}.logrotate

BuildRequires:  Linux-PAM-devel
BuildRequires:  ed
BuildRequires:  expat-devel
BuildRequires:  build-essential
BuildRequires:  gnupg
BuildRequires:  krb5-devel
BuildRequires:  libcap-devel
BuildRequires:  libecap-devel
BuildRequires:  libgpg-error-devel
BuildRequires:  libxml2-devel
BuildRequires:  nettle-devel
BuildRequires:  openldap
BuildRequires:  openssl-devel
BuildRequires:  systemd-devel
BuildRequires:  systemd-rpm-macros

Requires:       openssl
Requires:       shadow
Requires:       perl-URI
Requires:       systemd
Requires:       libxml2
Requires:       nettle
Requires:       perl
Requires:       Linux-PAM
Requires:       cyrus-sasl
Requires:       openldap

%description
Squid is a high-performance proxy caching server for Web clients,
supporting FTP, gopher, and HTTP data objects. Unlike traditional
caching software, Squid handles all requests in a single,
non-blocking, I/O-driven process. Squid keeps meta data and especially
hot objects cached in RAM, caches DNS lookups, supports non-blocking
DNS lookups, and implements negative caching of failed requests.

Squid consists of a main server program %{name}, a Domain Name System
lookup program (dnsserver), a program for retrieving FTP data
(ftpget), and some management and client tools.

%prep
%autosetup -p1

%define _confdir %{_sysconfdir}
%define _squiddatadir %{_datadir}/%{name}

%build
%define _lto_cflags %{nil}

sh ./configure --host=%{_host} --build=%{_build} \
      --program-prefix= \
      --disable-dependency-tracking \
      --bindir=%{_bindir} \
      --sbindir=%{_sbindir} \
      --includedir=%{_includedir} \
      --libdir=%{_libdir} \
      --localstatedir=%{_localstatedir} \
      --sharedstatedir=%{_sharedstatedir} \
      --mandir=%{_mandir} \
      --infodir=%{_infodir} \
      --prefix=%{_sysconfdir}/%{name} \
      --sysconfdir=%{_confdir}/%{name} \
      --libexecdir=%{_libdir}/%{name} \
      --datadir=%{_squiddatadir} \
      --exec-prefix=%{_prefix} \
      --with-logdir='%{_localstatedir}/log/%{name}' \
      --with-pidfile='/run/%{name}.pid' \
      --disable-dependency-tracking \
      --enable-eui \
      --enable-follow-x-forwarded-for \
      --enable-auth \
      --enable-auth-basic="DB,fake,getpwnam,LDAP,NCSA,PAM,POP3,RADIUS,SASL,SMB,SMB_LM" \
      --enable-auth-ntlm="SMB_LM,fake" \
      --enable-auth-digest="file,LDAP" \
      --enable-external-acl-helpers="LDAP_group,unix_group,wbinfo_group" \
      --enable-cache-digests \
      --enable-cachemgr-hostname=localhost \
      --enable-delay-pools \
      --enable-epoll \
      --enable-ecap \
      --enable-icap-client \
      --enable-ident-lookups \
      --enable-linux-netfilter \
      --enable-removal-policies="heap,lru" \
      --enable-ssl \
      --enable-ssl-crtd \
      --enable-diskio \
      --enable-wccpv2 \
      --enable-esi \
      --with-aio \
      --with-default-user="%{name}" \
      --with-dl \
      --with-openssl \
      --with-pthreads \
      --without-mit-krb5 \
      --without-heimdal-krb5 \
      --disable-arch-native \
      --disable-security-cert-validators \
      --disable-strict-error-checking \
      --with-swapdir=%{_localstatedir}/spool/%{name}

mkdir -p src/icmp/tests \
         tools/squidclient/tests \
         tools/tests

%make_build DEFAULT_SWAP_DIR=%{_localstatedir}/spool/%{name}

%install
%make_install %{?_smp_mflags}

mkdir -p %{buildroot}%{_sysconfdir}/%{name} \
         %{buildroot}%{_sysconfdir}/logrotate.d \
         %{buildroot}%{_sysconfdir}/sysconfig \
         %{buildroot}%{_sysconfdir}/pam.d/ \
         %{buildroot}%{_libexecdir}/%{name} \
         %{buildroot}%{_unitdir} \
         %{buildroot}%{_datadir}/%{name} \
         %{buildroot}/run/%{name}

rm -rf %{buildroot}%{_datadir}/man/

install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/pam.d/
install -m 644 %{SOURCE3} %{buildroot}%{_unitdir}
install -m 755 %{SOURCE4} %{buildroot}%{_libexecdir}/%{name}
install -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/logrotate.d/

mkdir -p %{buildroot}%{_localstatedir}/log/%{name} \
         %{buildroot}%{_localstatedir}/spool/%{name} \
         %{buildroot}/run/%{name}

chmod 644 contrib/url-normalizer.pl contrib/user-agents.pl

# install /usr/lib/tmpfiles.d/squid.conf
mkdir -p %{buildroot}%{_tmpfilesdir}
cat > %{buildroot}%{_tmpfilesdir}/%{name}.conf <<EOF
# See tmpfiles.d(5) for details
d /run/%{name} 0755 %{name} %{name} - -
EOF

%pre
if ! getent group %{name} >/dev/null 2>&1; then
  /usr/sbin/groupadd -g 53 %{name}
fi

if ! getent passwd %{name} >/dev/null 2>&1 ; then
  /usr/sbin/useradd -g 53 -u 53 -d /var/spool/%{name} -r -s /sbin/nologin %{name} >/dev/null 2>&1 || exit 1
fi

for i in /var/log/%{name} /var/spool/%{name}; do
  if [ -d $i ]; then
    for adir in $(find $i -maxdepth 0 \! -user %{name}); do
      chown -R %{name}:%{name} $adir
    done
  fi
done

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%license COPYING
%doc CONTRIBUTORS README ChangeLog QUICKSTART src/%{name}.conf.documented
%doc contrib/url-normalizer.pl contrib/user-agents.pl

%{_unitdir}/%{name}.service
%attr(755,root,root) %dir %{_libexecdir}/%{name}
%attr(755,root,root) %{_libexecdir}/%{name}/cache_swap.sh
%attr(755,root,root) %dir %{_sysconfdir}/%{name}
%attr(755,root,root) %dir %{_libdir}/%{name}
%attr(770,%{name},root) %dir %{_localstatedir}/log/%{name}
%attr(750,%{name},%{name}) %dir %{_localstatedir}/spool/%{name}
%attr(755,%{name},%{name}) %dir /run/%{name}
%{_tmpfilesdir}/squid.conf

%config(noreplace) %{_sysconfdir}/pam.d/%{name}.pam
%config(noreplace) %{_sysconfdir}/%{name}/cachemgr.conf.default
%config(noreplace) %{_sysconfdir}/%{name}/errorpage.css.default
%config(noreplace) %{_sysconfdir}/%{name}/mime.conf.default
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf.documented
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf.default
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}.logrotate

%{_sysconfdir}/%{name}/cachemgr.conf
%{_sysconfdir}/%{name}/errorpage.css
%{_sysconfdir}/%{name}/mime.conf
%{_sysconfdir}/%{name}/%{name}.conf
%{_sysconfdir}/sysconfig/%{name}
%{_datadir}/%{name}/mib.txt

%dir %{_datadir}/%{name}
%attr(-,root,root) %{_datadir}/%{name}/errors
%{_datadir}/%{name}/icons
%{_sbindir}/%{name}
%{_bindir}/%{name}client
%{_bindir}/purge
%{_libdir}/%{name}/*

%changelog
* Mon Sep 19 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.6-3
- Add squid.conf to create runtime directories at boot
* Wed Aug 24 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.6-2
- Bump version as a part of nettle upgrade
* Mon Jul 25 2022 Susant Sahani <ssahani@vmware.com> 5.6-1
- Version bump.
* Wed Nov 10 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 5.0.5-4
- Openssl 3.0.0 compatibility
* Fri Aug 20 2021 Shreenidhi Shedi <sshedi@vmware.com> 5.0.5-3
- Bump version as a part of rpm upgrade
* Tue Aug 17 2021 Shreenidhi Shedi <sshedi@vmware.com> 5.0.5-2
- Bump version as a part of nettle upgrade
* Fri Apr 30 2021 Susant Sahani <ssahani@vmware.com> 5.0.5-1
- Initial rpm release.
