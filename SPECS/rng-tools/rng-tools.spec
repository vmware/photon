Summary:	RNG deamon and tools
Name:		rng-tools
Version:	5
Release:	1%{?dist}
License:	GPLv2
URL:		https://sourceforge.net/projects/gkernel/
Group:          System Environment/Base
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://sourceforge.net/projects/gkernel/files/%{name}/%{name}-%{version}.tar.gz
%define sha1 rng-tools=3092768ac45315a5dcc0170d05566d1d00dbad96
Source1:        rngd.service
BuildRequires:  systemd
Requires:	systemd
%description
The rng-tools is a set of utilities related to random number generation in kernel.

%prep
%setup -q

%build
./configure \
	--prefix=%{_prefix}
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}%{_libdir}/systemd/system
install -p -m 644 %{SOURCE1} %{buildroot}%{_libdir}/systemd/system/

%check
make  %{?_smp_mflags} check

%post
/sbin/ldconfig
%systemd_post rngd.service

%preun
%systemd_preun rngd.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart rngd.service

%files
%defattr(-,root,root)
%{_libdir}/systemd/*
%{_bindir}/rngtest
%{_sbindir}/rngd
%{_mandir}/*

%changelog
*       Wed Oct 26 2016 Alexey Makhalov <amakhalov@vmware.com> 5-1
-	Initial version.
