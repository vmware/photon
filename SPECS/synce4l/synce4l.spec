Summary:        Linux SyncE implementation
Name:           synce4l
Version:        1.0.0
Release:        1%{?dist}
License:        GPL v2
Group:          Productivity/Networking/Other
URL:            https://github.com/intel/synce4l
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/intel/synce4l/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=b97656a50ee4cabdaddde166c2b74b16ebca339defb69e265c5222198c6d469af4e30328c3af47dcbe916f8474f04369e49f5fe98feb509cf7bb41e69e5d429b

Source1: %{name}.service

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
* Wed Jan 24 2024 Roye Eshed <roye.eshed@broadcom.com> 1.0.0-1
- Update to 1.0.0
* Mon Feb 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.8.0-2
- Spec fixes
- Add patch to show version
* Tue Jan 24 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 0.8.0-1
- Initial version.
