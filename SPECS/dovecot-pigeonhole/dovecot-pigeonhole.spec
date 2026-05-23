%global build_if %{photon_subrelease} >= 91

Summary:        Sieve and ManageSieve support for Dovecot
Name:           dovecot-pigeonhole
Version:        0.5.21.1
Release:        1%{?dist}
URL:            https://pigeonhole.dovecot.org/
Group:          System Environment/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://pigeonhole.dovecot.org/releases/2.3/dovecot-2.3-pigeonhole-%{version}.tar.gz
Source1:        license.txt
%include %{SOURCE1}

BuildRequires:  dovecot-devel

Requires:       %{name}-libs = %{version}-%{release}
Requires:       dovecot
Requires:       dovecot-libs
Requires:       dovecot-lmtpd

%description
Pigeonhole is the name of the project that adds support for the Sieve
language (RFC 5228) and the ManageSieve protocol (RFC 5804) to the
Dovecot Secure IMAP Server. The Sieve language can be used to specify
how e-mail is delivered and in what way the user is notified about new
messages.

%package        libs
Summary:        Libraries for %{name}
Group:          System Environment/Libraries

%description    libs
Shared libraries and helper executables for the Dovecot Pigeonhole plugin.

%prep
%autosetup -p1 -n dovecot-2.3-pigeonhole-%{version}

%build
%configure \
    --disable-static \
    --with-dovecot=%{_libdir}/dovecot \
    --without-unfinished-features

%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print
find %{buildroot} -type f -name "*.a" -delete -print
rm -rf %{buildroot}%{_includedir}/dovecot/sieve
rm -rf %{buildroot}%{_docdir}
rm -rf %{buildroot}%{_mandir}
rm -f %{buildroot}%{_datadir}/aclocal/dovecot-pigeonhole.m4

%files
%defattr(-,root,root)
%{_bindir}/sievec
%{_bindir}/sieve-dump
%{_bindir}/sieve-filter
%{_bindir}/sieve-test

%ldconfig_scriptlets libs

%files libs
%defattr(-,root,root)
%{_libdir}/dovecot/libdovecot-sieve.so*
%{_libdir}/dovecot/lib90_sieve_plugin.so
%{_libdir}/dovecot/lib95_imap_filter_sieve_plugin.so
%{_libdir}/dovecot/lib95_imap_sieve_plugin.so
%{_libdir}/dovecot/doveadm/lib10_doveadm_sieve_plugin.so
%{_libdir}/dovecot/settings/
%{_libdir}/dovecot/sieve/
%{_libexecdir}/dovecot/managesieve
%{_libexecdir}/dovecot/managesieve-login

%changelog
* Mon May 25 2026 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 0.5.21.1-1
- Initial build
