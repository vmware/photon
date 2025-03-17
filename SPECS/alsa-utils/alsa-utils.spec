Summary:        ALSA Utilities
Name:           alsa-utils
Version:        1.2.8
Release:        3%{?dist}
URL:            http://alsa-project.org
Group:          Applications/Internet
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://www.alsa-project.org/files/pub/utils/%{name}-%{version}.tar.bz2

Source1: license.txt
%include %{SOURCE1}

Patch0: ens1371.patch

BuildRequires: alsa-lib-devel
BuildRequires: ncurses-devel
BuildRequires: systemd-devel

Requires: linux-drivers-sound
Requires: alsa-lib
Requires: ncurses

%description
The ALSA Utilities package contains various utilities which are useful for controlling your sound card.

%prep
%autosetup -p1

%build
%configure --disable-alsaconf \
           --disable-xmlto \
           --with-udev-rules-dir=%{_udevrulesdir} \
           --with-systemdsystemunitdir=%{_unitdir}

%make_build

%install
%make_install %{?_smp_mflags}
install -dm 755 %{buildroot}%{_sharedstatedir}/alsa
find %{buildroot} -name \*.la -delete

%post
alsactl init
alsactl -L store

%files
%defattr(-,root,root)
%{_bindir}/*
%{_sbindir}/*
%{_datadir}/*
%{_localstatedir}/*
%{_unitdir}/*
%{_udevrulesdir}/*
%{_libdir}/alsa-topology/libalsatplg_module_nhlt.so
%exclude %dir %{_libdir}/debug

%changelog
* Wed Dec 11 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 1.2.8-3
- Release bump for SRP compliance
* Thu Jun 01 2023 Nitesh Kumar <kunitesh@vmware.com> 1.2.8-2
- Bump version as a part of ncurses upgrade to v6.4
* Fri Oct 28 2022 Gerrit Photon <photon-checkins@vmware.com> 1.2.8-1
- Automatic Version Bump
* Mon Jul 11 2022 Gerrit Photon <photon-checkins@vmware.com> 1.2.7-1
- Automatic Version Bump
* Mon Feb 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.2.4-2
- Fix binary path
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 1.2.4-1
- Automatic Version Bump
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.2.3-1
- Automatic Version Bump
* Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.1.7-1
- initial version, moved from Vivace
