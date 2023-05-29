Summary:        Intrusion detection environment
Name:           aide
Version:        0.16.2
Release:        4%{?dist}
URL:            http://sourceforge.net/projects/aide
License:        GPLv2+
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/aide/aide/releases/download/v%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=8b3a74b2f29431c0b5afef8ca2d914a71fabdf10de943622e52601ad3682c02d2d289d876d138422b39dbc6b101002061a6bbf190234b33688767d8fd2954401

Source1: %{name}.conf

Patch0: CVE-2021-45417.patch

BuildRequires:  build-essential
BuildRequires:  pcre-devel
BuildRequires:  libgpg-error-devel
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel
BuildRequires:  curl-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  audit-devel
BuildRequires:  libacl-devel
BuildRequires:  attr-devel

Requires: openssl
Requires: pcre
Requires: libgcrypt
Requires: audit
Requires: libacl
Requires: attr
Requires: libgpg-error
Requires: curl-libs

%description
AIDE (Advanced Intrusion Detection Environment) is a file integrity
checker and intrusion detection program.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%configure  \
  --disable-static \
  --with-config_file=%{_sysconfdir}/%{name}.conf \
  --with-gcrypt \
  --with-zlib \
  --with-curl \
  --with-posix-acl \
  --with-xattr \
  --with-audit

%make_build

%install
%make_install %{?_smp_mflags}

mkdir -p %{buildroot}%{_sysconfdir} \
         %{buildroot}%{_sharedstatedir}/%{name} \
         %{buildroot}%{_var}/log/%{name} \

cp %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}.conf

chmod 600 %{buildroot}%{_sysconfdir}/%{name}.conf

chmod 700 %{buildroot}%{_sharedstatedir}/%{name} \
          %{buildroot}%{_var}/log/%{name}

%check

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_mandir}/*
%config(noreplace) %{_sysconfdir}/%{name}.conf
%dir %{_sharedstatedir}/%{name}
%dir %{_var}/log/%{name}
%{_var}/log/%{name}

%changelog
* Mon May 29 2023 Harinadh D <hdommaraju@vmware.com> 0.16.2-4
- Version bump to use curl 8.1.1
* Tue Sep 13 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.16.2-3
- Enable bunch of essential options during configure
* Wed Jan 19 2022 Tapas Kundu <tkundu@vmware.com> 0.16.2-2
- Fix CVE-2021-45417
* Wed Aug 14 2019 Tapas Kundu <tkundu@vmware.com> 0.16.2-1
- Initial build for Photon
