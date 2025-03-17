Summary:        RNG deamon and tools
Name:           rng-tools
Version:        5
Release:        4%{?dist}
URL:            https://sourceforge.net/projects/gkernel/
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://sourceforge.net/projects/gkernel/files/%{name}/%{name}-%{version}.tar.gz
Source1:        rngd.service

Source2: license.txt
%include %{SOURCE2}
BuildArch:      x86_64
BuildRequires:  systemd
Requires:       systemd
%description
The rng-tools is a set of utilities related to random number generation in kernel.

%prep
%autosetup

%build
%configure
make %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
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
*       Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 5-4
-       Release bump for SRP compliance
*       Wed Dec 22 2021 Keerthana K <keerthanak@vmware.com> 5-3
-       rng-tools is not needed anymore since Kernel 5.6 because /dev/random does not block anymore.
-       Deprecating the package for aarch64
*       Thu May 10 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 5-2
-       Start rngd before cloud-init-local.service to speed up booting.
*       Wed Oct 26 2016 Alexey Makhalov <amakhalov@vmware.com> 5-1
-       Initial version.
