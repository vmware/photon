Summary:        Linux SyncE implementation
Name:           synce4l
Version:        0.8.0
Release:        1%{?dist}
License:        GPL v2
Group:          Productivity/Networking/Other
Url:            https://github.com/intel/synce4l
Source0:        %{name}-%{version}.tar.gz
%define sha512  synce4l=62be68c7c4b0476b8e7eb217fe90f5688db7415d4983abcb934c7ea1733918551228041816ce3525a8d59b294a15b8c60d0eca81ff425ff48fce7839bcde8dff
Source1:        synce4l.service
Source2:        synce4l
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  ethtool
BuildRequires:  systemd
Requires:       systemd
Requires:       ethtool
Requires:       glibc

%description
This software is an implementation of  Synchronous Ethernet (SyncE)
according to ITU-T Recommendation G.8264(PTP). The design goal is
to provide logic to supported hardware by processing Ethernet
Synchronization Messaging Channel (ESMC) and control Ethernet Equipment
Clock (EEC) on Network Card Interface (NIC).

%prep
%autosetup -n %{name}-%{version}

%build
%make_build

%install
make install %{?_smp_mflags} prefix=%{buildroot}%{_prefix} mandir=%{buildroot}%{_mandir}
mkdir -p %{buildroot}/etc/sysconfig/
mkdir -p %{buildroot}/usr/lib/systemd/system/
install -Dm 0644 configs/synce4l.cfg %{buildroot}/%{_sysconfdir}/synce4l.conf
install -Dm 0644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/
install -Dm 0644 %{SOURCE2}  %{buildroot}/etc/sysconfig/
install -vdm755 %{buildroot}%{_libdir}/systemd/system-preset
echo "disable synce4l.service" > %{buildroot}%{_libdir}/systemd/system-preset/50-synce4l.preset

%clean
rm -rf %{buildroot}

%post
%systemd_post synce4l.service

%preun
%systemd_preun synce4l.service

%postun -p /bin/sh
%systemd_postun_with_restart synce4l.service

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/synce4l.conf
%{_sysconfdir}/sysconfig/synce4l
%{_libdir}/systemd/system/synce4l.service
%{_libdir}/systemd/system-preset/50-synce4l.preset
%{_sbindir}/synce4l
%{_mandir}/man8/synce4l.8.gz

%changelog
*   Tue Jan 24 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 0.8.0-1
-   Initial version.
