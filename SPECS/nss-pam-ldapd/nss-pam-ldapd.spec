%global nssdir %{_lib}
%global pamdir %{_lib}/security

Name:           nss-pam-ldapd
Version:        0.9.11
Release:        1%{?dist}
Summary:        nsswitch module which uses directory servers
License:        LGPLv2+
URL:            https://github.com/arthurdejong/nss-pam-ldapd
Group:          System Environment/Security
Vendor:         VMware, Inc
Distribution:   Photon

Source0:        http://arthurdejong.org/nss-pam-ldapd/nss-pam-ldapd-%{version}.tar.gz
%define sha1 %{name}=fea1e4a536b5078df8133276d4db7b429418fe42
Source1:        nslcd.tmpfiles
Source2:        nslcd.service

BuildRequires:  openldap, krb5-devel
BuildRequires:  autoconf, automake
BuildRequires:  Linux-PAM-devel
%{?systemd_requires}

Requires: openldap
Requires: krb5
Requires: Linux-PAM

%description
The nss-pam-ldapd daemon, nslcd, uses a directory server to look up name
service information (users, groups, etc.) on behalf of a lightweight
nsswitch module.

%prep
%autosetup -p1
autoreconf -f -i

%build
%configure --libdir=%{nssdir} \
           --disable-utils \
           --with-pam-seclib-dir=%{pamdir}
%make_build

%check
make check

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}/{%{_libdir},%{_unitdir}}
install -p -m644 %{SOURCE2} %{buildroot}/%{_unitdir}/

ln -s libnss_ldap.so.2 %{buildroot}/%{nssdir}/libnss_ldap.so

sed -i -e 's,^uid.*,uid nslcd,g' -e 's,^gid.*,gid ldap,g' \
        %{buildroot}/%{_sysconfdir}/nslcd.conf

mkdir -p -m 0755 %{buildroot}/var/run/nslcd
mkdir -p -m 0755 %{buildroot}/%{_tmpfilesdir}
install -p -m 0644 %{SOURCE1} %{buildroot}/%{_tmpfilesdir}/%{name}.conf

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING HACKING NEWS README TODO
%{_sbindir}/*
%{nssdir}/*.so*
%{pamdir}/pam_ldap.so
%{_mandir}/*/*
%attr(0600,root,root) %config(noreplace) /etc/nslcd.conf
%attr(0644,root,root) %config(noreplace) %{_tmpfilesdir}/%{name}.conf
%{_unitdir}/nslcd.service
%attr(0775,nslcd,root) /var/run/nslcd

%pre
%{_bindir}/getent group ldap >/dev/null || %{_sbindir}/groupadd -r ldap
%{_bindir}/getent passwd nslcd >/dev/null || \
  %{_sbindir}/useradd -r -g ldap -d / -s %{_sbindir}/nologin -c "nslcd ldap user" nslcd

%post
/sbin/ldconfig
%systemd_post nslcd.service

%preun
%systemd_preun nslcd.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart nslcd.service
if [ $1 -eq 0 ]; then
  %{_bindir}/getent passwd nslcd > /dev/null && %{_sbindir}/userdel -f nslcd
  %{_bindir}/getent group ldap > /dev/null && %{_sbindir}/groupdel -f ldap
fi

%clean
rm -rf %{buildroot}/*

%changelog
* Wed Dec 09 2020 Shreenidhi Shedi <sshedi@vmware.com> 0.9.11-1
- Initial version
