Summary:        LDAP authentication with nss-pam-ldapd
Name:           nss-pam-ldapd
Version:        0.9.10
Release:        1%{?dist}
License:        LGPL v2.1
URL:            https://github.com/arthurdejong/nss-pam-ldapd
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source:         https://github.com/arthurdejong/nss-pam-ldapd/archive/%{name}-%{version}.tar.gz
%define sha1    %{name}-%{version}.tar.gz=c8ba356e1ea2e0fb696376c1f33371835a3dcac5
Source1:        nslcd.service
BuildRequires:  automake
BuildRequires:  krb5-devel
BuildRequires:  openldap
BuildRequires:  Linux-PAM-devel
BuildRequires:  systemd
Requires:       systemd
Requires:       shadow

%description
NSS and PAM libraries for name lookups and authentication using LDAP

%prep
%setup -q

%build
autoreconf -f -i
%configure --libdir=/%{_libdir} \
        --with-pam-seclib-dir=/%{_libdir}/security \
        --disable-utils
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}/%{_unitdir}/
install -p -m644 %{S:1} %{buildroot}/%{_unitdir}/

%pre
%{_bindir}/getent group nslcd >/dev/null || \
%{_sbindir}/groupadd -r nslcd
%{_bindir}/getent passwd nslcd >/dev/null || \
%{_sbindir}/useradd -r -g nslcd -d / -s /sbin/nologin -c "LDAP user" nslcd

%post
/sbin/ldconfig
%systemd_post nslcd.service

%preun
%systemd_preun nslcd.service

%postun
/sbin/ldconfig
%systemd_postun nslcd.service

%files
%defattr(-,root,root)
/%{_libdir}/libnss_ldap*.so*
/%{_libdir}/security/pam_ldap*.so
%config(noreplace) %attr(640,root,root) %{_sysconfdir}/nslcd.conf
/%{_unitdir}/nslcd.service
%{_sbindir}/nslcd

%changelog
*   Mon Jul 01 2019 Ashwin H <ashwinh@vmware.com> 0.9.10-1
-   Initial version
