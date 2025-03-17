Summary:        Linux SyncE implementation
Name:           synce4l
Version:        1.0.0
Release:        2%{?dist}
Group:          Productivity/Networking/Other
URL:            https://github.com/intel/synce4l
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/intel/synce4l/archive/refs/tags/%{name}-%{version}.tar.gz

Source1: %{name}.service

Source2: license.txt
%include %{SOURCE2}

BuildRequires:  ethtool
BuildRequires:  systemd-devel
BuildRequires:  libnl-devel

Requires: systemd
Requires: ethtool
Requires: glibc

%description
This software is an implementation of  Synchronous Ethernet (SyncE)
according to ITU-T Recommendation G.8264(PTP). The design goal is
to provide logic to supported hardware by processing Ethernet
Synchronization Messaging Channel (ESMC) and control Ethernet Equipment
Clock (EEC) on Network Card Interface (NIC).

%prep
%autosetup -p1

%build
%make_build VERSION="%{version}-%{release}"

%install
%make_install %{?_smp_mflags} \
        prefix=%{_prefix} mandir=%{_mandir} \
        VERSION="%{version}-%{release}"

mkdir -p %{buildroot}%{_unitdir} \
         %{buildroot}%{_presetdir} \
         %{buildroot}%{_sysconfdir}

install -Dm 0644 %{SOURCE1} %{buildroot}%{_unitdir}
install -Dm 0644 configs/%{name}_dpll.cfg %{buildroot}%{_sysconfdir}/%{name}.conf

echo "disable %{name}.service" > %{buildroot}%{_presetdir}/50-%{name}.preset

%clean
rm -rf %{buildroot}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_unitdir}/%{name}.service
%{_presetdir}/50-%{name}.preset
%{_sbindir}/%{name}
%{_mandir}/man8/%{name}.8.gz

%changelog
* Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 1.0.0-2
- Release bump for SRP compliance
* Wed Jan 24 2024 Ankit Jain <ankit-aj.jain@broadcom.com> 1.0.0-1
- Update to 1.0.0
* Mon Mar 06 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 0.8.0-1
- Add patch to show version
- Initial version.
