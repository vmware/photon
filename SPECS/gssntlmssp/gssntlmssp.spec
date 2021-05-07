Summary:        GSSAPI NTLMSSP Mechanism
Name:           gssntlmssp
Version:        1.0.0
Release:        1%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        LGPLv3+
URL:            https://github.com/gssapi/gss-ntlmssp
Group:          Applications/System
Source0:        https://github.com/gssapi/gss-ntlmssp/releases/download/v%{version}/%{name}-%{version}.tar.gz
%define sha1 gssntlmssp=b029ab920383002c966335c65d07d72ab11bc842

Requires:      krb5
Requires:      libtasn1

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: m4
BuildRequires: libxslt
BuildRequires: libxml2
BuildRequires: docbook-xsl
BuildRequires: gettext
BuildRequires: pkg-config
BuildRequires: krb5-devel >= 1.11.2
BuildRequires: libunistring-devel
BuildRequires: openssl-devel
BuildRequires: gnutls-devel >= 3.4.7
BuildRequires: libtasn1-devel
BuildRequires: libtirpc-devel
BuildRequires: openldap
BuildRequires: Linux-PAM-devel
BuildRequires: jansson-devel
BuildRequires: gnutls-devel >= 3.4.7
BuildRequires: samba-client-libs
BuildRequires: libwbclient
BuildRequires: libwbclient-devel
BuildRequires: zlib-devel
BuildRequires: make

%description
A GSSAPI Mechanism that implements NTLMSSP

%package devel
Summary: Development header for GSSAPI NTLMSSP
License: LGPLv3+

%description devel
Adds a header file with definition for custom GSSAPI extensions for NTLMSSP

%prep
%setup -q

%build
autoreconf -fiv
%configure \
    --with-wbclient \
    --disable-static \
    --disable-rpath \
    --with-manpages=no

make %{?_smp_mflags} all

%install
%make_install
rm -f %{buildroot}%{_libdir}/gssntlmssp/gssntlmssp.la
mkdir -p %{buildroot}%{_sysconfdir}/gss/mech.d
install -pm644 examples/mech.ntlmssp %{buildroot}%{_sysconfdir}/gss/mech.d/ntlmssp.conf
%{find_lang} %{name}

%check
make test_gssntlmssp

%files -f %{name}.lang
%config(noreplace) %{_sysconfdir}/gss/mech.d/ntlmssp.conf
%{_libdir}/gssntlmssp/
%doc COPYING

%files devel
%{_includedir}/gssapi/gssapi_ntlmssp.h

%changelog
*   Thu May 06 2021 Shreyas B. <shreyasb@vmware.com> 1.0.0-1
-   Initial version of gssntlmssp spec.
