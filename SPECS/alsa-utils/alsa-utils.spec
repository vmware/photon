Summary:        ALSA Utilities
Name:           alsa-utils
Version:        1.2.4
Release:        1%{?dist}
License:        LGPLv2+
URL:            http://alsa-project.org
Group:          Applications/Internet
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://www.alsa-project.org/files/pub/utils/%{name}-%{version}.tar.bz2
%define sha1    %{name}=84b2c5e8f0c345844e03e8e4ae73b761c3ae8829

Patch0:         ens1371.patch

BuildRequires:  alsa-lib-devel
BuildRequires:  ncurses-devel
Requires:       linux-drivers-sound
Requires:       alsa-lib
Requires:       ncurses

%description
The ALSA Utilities package contains various utilities which are useful for controlling your sound card.

%prep
%autosetup -p1

%build
%configure --disable-alsaconf --disable-xmlto
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
install -d -m 755 %{buildroot}/var/lib/alsa

%post
alsactl init
alsactl -L store

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*
%exclude %{_libdir}/debug/
/lib/*
%{_sbindir}/*
%{_datadir}/*
%{_localstatedir}/*

%changelog
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 1.2.4-1
- Automatic Version Bump
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.2.3-1
- Automatic Version Bump
* Mon Dec 10 2018 Alexey Makhalov <amakhalov@vmware.com> 1.1.7-1
- initial version, moved from Vivace
