Summary:       Intel LLDP Agent
Name:          lldpad
Version:       1.1
Release:       4%{?dist}
URL:           http://open-lldp.org/
Source0:        %{name}-%{version}.tar.gz
Group:         System Environment/Daemons
Vendor:        VMware, Inc.
Distribution:  Photon

Source1: license.txt
%include %{SOURCE1}

BuildRequires: libconfig
BuildRequires: libnl-devel
BuildRequires: readline-devel
BuildRequires: systemd-rpm-macros

Requires:      systemd
Requires:      libconfig
Requires:      libnl

%description
The lldpad package comes with utilities to manage an LLDP interface with
support for reading and configuring TLVs. TLVs and interfaces are individual
controlled allowing flexible configuration for TX only, RX only, or TX/RX
modes per TLV.

%package       devel
Summary:       Development files for %{name}
Requires:      %{name} = %{version}-%{release}
Provides:      dcbd-devel = %{version}-%{release}

%description devel
The lldpad-devel package contains header files for developing applications
that use lldpad.

%prep
%autosetup -p1 -n openlldp-%{version}

%build
./bootstrap.sh
%configure --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}

%post
%systemd_post %{name}.service %{name}.socket

%preun
%systemd_preun %{name}.service %{name}.socket

%postun
%systemd_postun_with_restart %{name}.service %{name}.socket

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%{_sbindir}/*
%{_libdir}/liblldp_clif.so.*
%{_sysconfdir}/bash_completion.d/*
%dir %{_sharedstatedir}/%{name}
%{_mandir}/man3/*
%{_mandir}/man8/*
%{_unitdir}/lldpad.service
%{_unitdir}/lldpad.socket

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/liblldp_clif.so

%changelog
* Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 1.1-4
- Release bump for SRP compliance
* Tue Dec 20 2022 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.1-3
- Bump release as a part of readline upgrade
* Wed Aug 25 2021 Susant Sahani <ssahani@vmware.com> 1.1-2
- Spec cleaup, split package into devel.
* Fri Jan 15 2021 Alexey Makhalov <amakhalov@vmware.com> 1.1-1
- Version update.
* Wed Oct 21 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 1.0.1-8
- Fix redefinition of ETH_P_LLDP macro
* Fri Apr 03 2020 Alexey Makhalov <amakhalov@vmware.com> 1.0.1-7
- Fix compilation issue with gcc-8.4.0
* Mon Aug 13 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.0.1-6
- Suppress build warnings with gcc 7.3
* Wed May 25 2016 Anish Swaminathan <anishs@vmware.com> 1.0.1-5
- Add required folder for service to start
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.1-4
- GA - Bump release of all rpms
* Thu May 05 2016 Kumar Kaushik <kaushikk@vmware.com>  1.0.1-3
- Adding support in pre/post/un scripts for upgrade.
* Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com>  1.0.1-2
- Add systemd to Requires and BuildRequires.
- The source is based on git://open-lldp.org/open-lldp commit 036e314
- Use systemctl to enable/disable service.
* Tue Nov 24 2015 Xiaolin Li <xiaolinl@vmware.com> 1.0.1-1
- Initial build. First version
