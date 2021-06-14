Summary:        Intrusion detection environment
Name:           aide
Version:        0.16.2
Release:        2%{?dist}
URL:            https://github.com/aide/aide
License:        GPLv2+
Source0:        https://github.com/%{name}/%{name}/releases/download/%{version}/%{name}-%{version}.tar.gz
%define sha1    %{name}=1dbb954bd545addd5c3934ea9b58a785974c8664
Source1:        aide.conf
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:	Photon

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  bison flex
BuildRequires:  pcre-devel
BuildRequires:  libgpg-error-devel openssl-devel
BuildRequires:  zlib-devel
BuildRequires:  curl-devel

Requires:       openssl
Requires:       curl-libs

%description
AIDE (Advanced Intrusion Detection Environment) is a file integrity
checker and intrusion detection program.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%configure  \
  --disable-static \
  with_mhash=no \
  --with-gcrypt=no
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} %{?_smp_mflags}
mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}/var/lib/aide
mkdir -p %{buildroot}/var/log/aide
mkdir -p %{buildroot}/var/opt/%{name}/log
touch %{buildroot}/var/opt/%{name}/log/%{name}.log
ln -sfv /var/opt/%{name}/log/%{name}.log %{buildroot}/var/log/%{name}/%{name}.log

cp %{SOURCE1} %{buildroot}%{_sysconfdir}/aide.conf
chmod 0600 %{buildroot}%{_sysconfdir}/aide.conf
chmod 0700 %{buildroot}/var/lib/aide
chmod 0700 %{buildroot}/var/log/aide

%check

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/aide
%{_mandir}/*
%config(noreplace) %{_sysconfdir}/aide.conf
%dir %{_var}/lib/aide
%dir %{_var}/log/aide
%{_var}/log/aide/*
%{_var}/opt/%{name}/log/%{name}.log

%changelog
*    Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 0.16.2-2
-    openssl 1.1.1
*    Wed Aug 14 2019 Tapas Kundu <tkundu@vmware.com> 0.16.2-1
-    Initial build for Photon
