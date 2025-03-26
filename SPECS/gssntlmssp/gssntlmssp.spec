Summary:        GSSAPI NTLMSSP Mechanism
Name:           gssntlmssp
Version:        1.1.0
Release:        16%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/gssapi/gss-ntlmssp
Group:          Applications/System

Source0: https://github.com/gssapi/gss-ntlmssp/releases/download/v%{version}/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Requires: krb5
Requires: libtasn1
Requires: openssl
Requires: e2fsprogs-libs
Requires: libunistring
Requires: libwbclient
Requires: zlib
Requires: gnutls

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: m4
BuildRequires: libxslt-devel
BuildRequires: libxml2
BuildRequires: docbook-xsl
BuildRequires: doxygen
BuildRequires: gettext
BuildRequires: pkg-config
BuildRequires: krb5-devel
BuildRequires: libunistring-devel
BuildRequires: openssl-devel
BuildRequires: gnutls-devel
BuildRequires: libtasn1-devel
BuildRequires: libtirpc-devel
BuildRequires: openldap-devel
BuildRequires: Linux-PAM-devel
BuildRequires: jansson-devel
BuildRequires: gnutls-devel
BuildRequires: samba-client-libs
BuildRequires: libwbclient
BuildRequires: libwbclient-devel
BuildRequires: zlib-devel
BuildRequires: make

%description
A GSSAPI Mechanism that implements NTLMSSP

%package devel
Summary: Development header for GSSAPI NTLMSSP
Requires: %{name} = %{version}-%{release}

%description devel
Adds a header file with definition for custom GSSAPI extensions for NTLMSSP

%prep
%autosetup -n gss-ntlmssp-%{version} -p1

%build
autoreconf -fiv
%configure \
    --with-wbclient \
    --disable-static \
    --disable-rpath \
    --with-manpages=no

%make_build

%install
%make_install %{?_smp_mflags}
mkdir -p %{buildroot}%{_sysconfdir}/gss/mech.d
install -pm644 examples/mech.ntlmssp %{buildroot}%{_sysconfdir}/gss/mech.d/ntlmssp.conf
%{find_lang} %{name}

%if 0%{?with_check}
%check
make %{?_smp_mflags} test_gssntlmssp
%endif

%clean
rm -rf %{buildroot}/*

%files -f %{name}.lang
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/gss/mech.d/ntlmssp.conf
%{_libdir}/%{name}/%{name}.so

%files devel
%defattr(-,root,root)
%{_includedir}/gssapi/gssapi_ntlmssp.h

%changelog
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 1.1.0-16
- Release bump for SRP compliance
* Wed Nov 29 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.1.0-15
- Bump version as a part of gnutls upgrade
* Mon Nov 27 2023 Harinadh D <hdommaraju@vmware.com> 1.1.0-14
- Bump version as part of samba-client upgrade
* Tue Sep 19 2023 Nitesh Kumar <kunitesh@vmware.com> 1.1.0-13
- Bump version as a part of openldap v2.6.4 upgrade
* Mon Jul 31 2023 Oliver Kurth <okurth@vmware.com> 1.1.0-12
- Bump version as part of samba-client upgrade
* Fri Jul 28 2023 Srish Srinivasan <ssrish@vmware.com> 1.1.0-11
- Bump version as a part of krb5 upgrade
* Thu Jun 22 2023 Oliver Kurth <okurth@vmware.com> 1.1.0-10
- Bump version as part of samba-client upgrade
* Thu May 25 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.1.0-9
- Bump version as a part of libxml2 upgrade
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.1.0-8
- Bump version as a part of zlib upgrade
* Wed Feb 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.1.0-7
- Bump version as a part of openldap upgrade
* Thu Jan 26 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.1.0-6
- Bump version as a part of krb5 upgrade
* Sat Jan 14 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.1.0-5
- Bump version as a part of gettext upgrade
* Sun Nov 13 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.1.0-4
- Bump version as a part of libtirpc upgrade
* Fri Oct 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.1.0-3
- Bump version as a part of libxslt upgrade
* Tue Aug 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.1.0-2
- Bump version as a part of gnutls upgrade
* Mon Jul 11 2022 Gerrit Photon <photon-checkins@vmware.com> 1.1.0-1
- Automatic Version Bump
* Thu Jun 16 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.0.0-2
- Bump version as a part of libxslt upgrade
* Thu May 06 2021 Shreyas B. <shreyasb@vmware.com> 1.0.0-1
- Initial version of gssntlmssp spec.
