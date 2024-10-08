Name:           stunnel
Version:        5.72
Release:        1%{?dist}
Summary:        A TLS-encrypting socket wrapper
Group:          System Environment/Libraries
License:        GPL v2+
URL:            https://www.stunnel.org
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:  https://www.stunnel.org/downloads/%{name}-%{version}.tar.gz
%define sha512  %{name}=2607bed1159412dc36ed0455ed158ab3141782f05ddaf3605076f1a0e371bc1ada1606cab65a6bc52d69a8c685345617578cb79d521330f2e1d12af3dcbd37ca

BuildRequires: openssl-devel
BuildRequires: tcp_wrappers-devel

%if 0%{?with_check}
Buildrequires: python3-devel
Buildrequires: python3-cryptography
%endif

Requires: openssl-libs
Requires: libnsl
Requires: rpcsvc-proto
Requires: tcp_wrappers
Requires: finger
Requires: perl

%description
Stunnel is a socket wrapper which can provide TLS/SSL
(Transport Layer Security/Secure Sockets Layer) support
to ordinary applications. For example, it can be used in
conjunction with imapd to create a TLS secure IMAP server.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}

%check
%make_build check

%clean
rm -rf %{buildroot}

%files
%{_sysconfdir}/%{name}/%{name}.conf-sample
%{_bindir}/%{name}
%{_bindir}/stunnel3
%{_libdir}/%{name}/libstunnel.so
%{_docdir}/%{name}
%{_mandir}/man8/%{name}*

%changelog
* Tue Oct 08 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 5.72-1
- Initial release
