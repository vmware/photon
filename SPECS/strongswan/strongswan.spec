Summary:          The OpenSource IPsec-based VPN Solution
Name:             strongswan
Version:          5.5.1
Release:          2%{?dist}
License:          GPLv2+
URL:              https://www.strongswan.org/
Group:            System Environment/Security
Vendor:           VMware, Inc.
Distribution:     Photon
Source0:          https://download.strongswan.org/strongswan-5.5.1.tar.bz2
%define sha1      strongswan=7d400eb501ac9e41eb889199891457003baa284c

BuildRequires:    autoconf

%description
strongSwan is a complete IPsec implementation for Linux 2.6, 3.x, and 4.x kernels.

%prep
%setup -q

%build
./configure --prefix=%{_prefix} --sysconfdir=%{_sysconfdir}/%{name} --with-fips-mode=2 --enable-openssl

make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete
find %{buildroot} -name '*.a' -delete

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/%{name}
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/ipsec/*
%{_libexecdir}/*
%{_mandir}/man[158]/*
%{_datadir}/strongswan/*


%changelog
*   Thu Jul 27 2017 Anish Swaminathan <anishs@vmware.com> 5.5.1-2
-   Configure FIPS mode
*   Wed Dec 21 2016 Xiaolin Li <xiaolinl@vmware.com>  5.5.1-1
-   Initial build.
