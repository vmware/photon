%global pamdir %{_libdir}/security

Name:           nss-pam-ldapd
Version:        0.9.12
Release:        3%{?dist}
Summary:        nsswitch module which uses directory servers
License:        LGPLv2+
URL:            https://github.com/arthurdejong/nss-pam-ldapd
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://arthurdejong.org/nss-pam-ldapd/nss-pam-ldapd-%{version}.tar.gz
%define sha512 %{name}=da154303ba2f86b8653d978acfbba4633d0190afd353b6a57386391078c531bf7b11195fbabbe53cf6f36545c6f1c71b9567fd042892a73251bf0016c5f018ee

Source1:        nslcd.tmpfiles
Source2:        nslcd.service

BuildRequires:  openldap-devel
BuildRequires:  krb5-devel
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  Linux-PAM-devel
%{?systemd_requires}

Requires:       systemd
Requires:       openldap
Requires:       krb5
Requires:       Linux-PAM

%description
The nss-pam-ldapd daemon, nslcd, uses a directory server to look up name
service information (users, groups, etc.) on behalf of a lightweight
nsswitch module.

%prep
%autosetup -p1

%build
autoreconf -f -i
%configure --libdir=%{_libdir} \
           --disable-utils \
           --with-pam-seclib-dir=%{pamdir}

%make_build

%install
%make_install %{?_smp_mflags}
mkdir -p %{buildroot}{%{_libdir},%{_unitdir}} \
         %{buildroot}/run/nslcd \
         %{buildroot}%{_tmpfilesdir}

install -p -m644 %{SOURCE2} %{buildroot}%{_unitdir}/

ln -sfrv %{buildroot}%{_libdir}/libnss_ldap.so.2 %{buildroot}%{_libdir}/libnss_ldap.so

sed -i -e 's,^uid.*,uid nslcd,g' -e 's,^gid.*,gid ldap,g' \
        %{buildroot}%{_sysconfdir}/nslcd.conf

install -p -m 0644 %{SOURCE1} %{buildroot}%{_tmpfilesdir}/%{name}.conf

%if 0%{?with_check}
%check
make check %{?_smp_mflags}
%endif

%pre
getent group ldap >/dev/null || groupadd -r ldap
getent passwd nslcd >/dev/null || \
  useradd -r -g ldap -d / -s %{_sbindir}/nologin -c "nslcd ldap user" nslcd

%post
/sbin/ldconfig
%systemd_post nslcd.service

%preun
%systemd_preun nslcd.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart nslcd.service

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_sbindir}/*
%{_libdir}/*.so*
%{pamdir}/pam_ldap.so
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/nslcd.conf
%attr(0644,root,root) %config(noreplace) %{_tmpfilesdir}/%{name}.conf
%{_unitdir}/nslcd.service
%attr(0775,nslcd,root) /run/nslcd

%changelog
* Wed Feb 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.9.12-3
- Bump version as a part of openldap upgrade
* Thu Jan 26 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 0.9.12-2
- Bump version as a part of krb5 upgrade
* Mon May 30 2022 Gerrit Photon <photon-checkins@vmware.com> 0.9.12-1
- Automatic Version Bump
* Wed Dec 09 2020 Shreenidhi Shedi <sshedi@vmware.com> 0.9.11-1
- Initial version
