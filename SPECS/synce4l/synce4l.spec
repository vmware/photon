Summary:        Linux SyncE implementation
Name:           synce4l
Version:        0.8.0
Release:        1%{?dist}
License:        GPL v2
Group:          Productivity/Networking/Other
URL:            https://github.com/intel/synce4l
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/intel/synce4l/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=62be68c7c4b0476b8e7eb217fe90f5688db7415d4983abcb934c7ea1733918551228041816ce3525a8d59b294a15b8c60d0eca81ff425ff48fce7839bcde8dff

Source1: %{name}.service
Source2: %{name}.conf.default

Patch0: version.patch
Patch1: gcc-flags.patch
Patch2: warning-fix.patch

BuildRequires:  ethtool
BuildRequires:  systemd-devel

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
install -Dm 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/%{name}.conf

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
* Mon Mar 06 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 0.8.0-1
- Add patch to show version
- Initial version.
