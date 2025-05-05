Name:           dbus-broker
Version:        32
Release:        4%{?dist}
Summary:        Linux D-Bus Message Broker
License:        ASL 2.0
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          System Environment/Security

URL:            https://github.com/bus1/dbus-broker
Source0:        https://github.com/bus1/dbus-broker/releases/download/v%{version}/dbus-broker-%{version}.tar.xz
%define sha512  dbus-broker=aa23d058771f56e6378df0a17ac413813b6350b77e61128c0887f35a546f10534b1a6d598868e9f5c642244c3632a8ce5e315e6794305a56f5abbebd36bf822c

Provides:       bundled(c-dvar) = 1
Provides:       bundled(c-ini) = 1
Provides:       bundled(c-list) = 3
Provides:       bundled(c-rbtree) = 3
Provides:       bundled(c-shquote) = 1

BuildRequires:  expat-devel
BuildRequires:  libcap-ng
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  glibc-devel
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  python3-docutils
BuildRequires:  systemd
BuildRequires:  systemd-devel

%description
dbus-broker is an implementation of a message bus as defined by the D-Bus
specification. Its aim is to provide high performance and reliability, while
keeping compatibility to the D-Bus reference implementation. It is exclusively
written for Linux systems, and makes use of many modern features provided by
recent Linux kernel releases.

%prep
%autosetup -p1 %{name}-%{version}

%build
CONFIGURE_OPTS=(
   --prefix=/usr
)
%meson "${CONFIGURE_OPTS[@]}"
%meson_build

%install
%meson_install

%check
%meson_test

%post

if [ $1 -eq 1 ] ; then
        systemctl --no-reload          disable dbus-daemon.service &>/dev/null || :
        systemctl --no-reload --global disable dbus-daemon.service &>/dev/null || :
        systemctl --no-reload          enable dbus-broker.service &>/dev/null || :
        systemctl --no-reload --global enable dbus-broker.service &>/dev/null || :
fi

%journal_catalog_update

%preun
%systemd_preun dbus-broker.service
%systemd_user_preun dbus-broker.service

%postun
%systemd_postun dbus-broker.service
%systemd_user_postun dbus-broker.service

%files
%license AUTHORS
%license LICENSE
%{_bindir}/dbus-broker
%{_bindir}/dbus-broker-launch
%{_journalcatalogdir}/dbus-broker.catalog
%{_journalcatalogdir}/dbus-broker-launch.catalog
%{_unitdir}/dbus-broker.service
%{_userunitdir}/dbus-broker.service

%changelog
* Mon May 05 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 32-4
- Version bump for expat upgrade
* Wed Jan 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 32-3
- Bump version as a part of meson upgrade
* Thu Feb 29 2024 Anmol Jain <anmol.jain@broadcom.com> 32-2
- Bump version as a part of expat upgrade
* Wed Oct 26 2022 Shivani Agarwal <shivania2@vmware.com> 32-1
- Update version for CVE-2022-31212
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 29-2
- Bump up to compile with python 3.10
* Fri Jul 23 2021 Susant Sahani <ssahani@vmware.com> 29-1
- Update version and switch to meson
* Sat Jan 23 2021 Susant Sahani <ssahani@vmware.com> 26-1
- Update version
* Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 24-1
- Automatic Version Bump
* Fri Aug 14 2020 Susant Sahani <ssahani@vmware.com> 23-1
- Update to v23
* Tue May 05 2020 Susant Sahani <ssahani@vmware.com> 22-1
- Initial RPM release
