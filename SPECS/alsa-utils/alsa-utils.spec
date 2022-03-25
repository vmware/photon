Summary:    ALSA Utilities.
Name:       alsa-utils
Version:    1.1.7
Release:    2%{?dist}
License:    LGPLv2+
URL:        http://alsa-project.org
Group:      Applications/Internet
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    ftp://ftp.alsa-project.org/pub/utils/alsa-utils-%{version}.tar.bz2
%define sha1 %{name}=5c9d6bee351c06baa645d89153d492199a60e66b

Patch0: ens1371.patch

BuildRequires: alsa-lib-devel
BuildRequires: ncurses-devel
BuildRequires: systemd-devel

Requires: linux-drivers-sound
Requires: alsa-lib
Requires: ncurses

%description
The ALSA Utilities package contains various utilities which are useful
for controlling your sound card.

%prep
%autosetup -p1

%build
%configure --disable-alsaconf \
           --disable-xmlto \
           --with-udev-rules-dir=%{_udevrulesdir} \
           --with-systemdsystemunitdir=%{_unitdir}

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
install -d -m 755 %{buildroot}%{_sharedstatedir}/alsa

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
%exclude %dir %{_libdir}/debug

%changelog
* Fri Mar 25 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.1.7-2
- Exclude debug symbols properly
* Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.1.7-1
- initial version, moved from Vivace
